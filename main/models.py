import os.path
from django.db import models
from uy.mixins import TranslateMixin
from uy.helpers import UploadTo
from django.utils.translation import gettext_lazy as _
import os


class Category(TranslateMixin, models.Model):
    translate_fields = ['name']

    name_uz = models.CharField(max_length=50)
    name_ru = models.CharField(max_length=50)
    image = models.ImageField(upload_to=UploadTo("category"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'kategoriyalar'


class Post(models.Model):
    user = models.ForeignKey('client.User', on_delete=models.RESTRICT, default=1)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, verbose_name=_("kategoriya"))
    comment = models.TextField(verbose_name="izoh")
    file = models.FileField(verbose_name="Rasm/Video", upload_to=UploadTo("post"))
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def ext(self):
        return ((os.path.splitext(self.file.name)[1])[1:]).lower()

    @property
    def is_image(self):
        return self.ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp']

    @property
    def is_video(self):
        return self.ext in ['mp4', 'mpeg']

    @property
    def is_audio(self):
        return self.ext in ['mp3', 'wav']


class PostComment(models.Model):
      parent = models.ForeignKey('PostComment', on_delete=models.RESTRICT, null=True, default=None)
      post = models.ForeignKey(Post, on_delete=models.RESTRICT)
      user = models.ForeignKey('client.User', on_delete=models.RESTRICT)
      comment = models.TextField()
      image = models.ImageField(upload_to=UploadTo("comment"), null=True, blank=True, default=None)
      like = models.IntegerField(default=0)
      dislike = models.IntegerField(default=0)
      added_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)









