from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Just for woopra
class Version(models.Model):
    user = models.ForeignKey(User)
    version = models.BooleanField(default=False)

# Create your models here.

class Share(models.Model):
    user = models.ForeignKey(User)
    publish = models.BooleanField(default=False)
    title = models.CharField(max_length=100)
    paragraph = models.CharField(max_length=1000)
    id = models.AutoField('#', primary_key=True)
    date = models.DateTimeField(default = datetime.now())

class Image(models.Model):
    story = models.ForeignKey(Share)
    user = models.ForeignKey(User)
    paths = models.ImageField(upload_to='%Y/%m/%d')

class Highlight(models.Model):
    story = models.ForeignKey(Share)
    user = models.ForeignKey(User)
    highlights = models.CharField(max_length=1000)
    id = models.AutoField('#', primary_key=True)

class Link(models.Model):
    story = models.ForeignKey(Share)
    path = models.ManyToManyField(Image, blank = True)
    links = models.CharField(max_length=20)
    id = models.AutoField('#', primary_key=True)

class Follow(models.Model):
    following = models.BooleanField(default=False)
    user1 = models.ForeignKey(User, related_name='user1')
    user2 = models.ForeignKey(User, related_name='user2')

class Like(models.Model):
    liking = models.BooleanField(default=False)
    user = models.ForeignKey(User)
    story = models.ForeignKey(Share)
