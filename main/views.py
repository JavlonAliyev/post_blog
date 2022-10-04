from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.http import Http404

from main.forms import PostCommentForm
from main.models import Post, Category, PostComment
from django.core.paginator import Paginator


class MainIndex(View):
    def get (self, request, id=None):
        query = Post.objects.order_by('-id')
        if id is not None:
            query = query.filter(category_id=id)
        paginator = Paginator(query.all(), 2)
        page = paginator.get_page(request.GET.get('page'))

        return render(request, 'main/index.html', {
            'object_list': page.object_list,
            'page_obj': page,
        })


class UploadPost(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['category', 'comment', 'file']
    template_name = 'layouts/form.html'
    success_url = reverse_lazy('main:upload')

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        request.title = _("Yuklanish")

    def form_valid(self, form):
        form.instance.user = self.request.user

        messages.success(self.request, _("Muvafaqiyatli yuklandi."))
        return super().form_valid(form)

class Postlike(View):
    def get(self, request, post_id, action):
        if action not in ['like', 'dislike']:
            raise Http404
        def _redirect():
            return redirect(request.GET.get('return', 'main:index'))

        with transaction.atomic():
            try:
                post = Post.objects.select_for_update().get(id=post_id)
            except:
                return _redirect()

            if action == 'like':
                post.like += 1
            else:
                post.dislike += 1
            post.save()

        return _redirect()

class PostCommentView(ListView):
    model = PostComment
    paginate_by = 10
    ordering = '-id'

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(post_id=self.kwargs['post_id'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['post'] = Post.objects.get(id=self.kwargs['post_id'])
        context['form'] = PostCommentForm()
        return context

    def post(self, request, post_id):
        form = PostCommentForm(data=request.Post, files=request.FILES)
        if form.is_valid():
            comment:PostComment = form.save(commit=False)
            comment.post_id = self.kwargs['post_id']
            comment.user = self.request.user
            comment.save()
            return redirect('main:comment', post_id=post_id)

        return self.get(request)
