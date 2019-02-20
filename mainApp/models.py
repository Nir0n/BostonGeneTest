from django.db import models

# Create your models here.
class Task(models.Model):
    url=models.URLField(max_length=200,blank=True)
    state = models.CharField(max_length=30,default="task failed")
    email = models.EmailField(blank=True)
    data = models.FileField(upload_to='fileStorage', blank=True)
    md5 = models.UUIDField(blank=True,null=True)