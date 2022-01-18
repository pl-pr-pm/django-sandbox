from django.conf import settings
from django.db import models

# Create your models here.
class Snippet(models.Model):
  title=models.CharField('タイトル', max_length=128)
  code=models.TextField('コード', blank=True)
  desciption=models.TextField('説明', blank=True)
  created_by=models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='投稿者', on_delete=models.CASCADE)
  created_at=models.DateTimeField(auto_now_add=True)
  updated_at=models.DateTimeField(auto_now=True)
