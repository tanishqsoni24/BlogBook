from django.db import models
from ckeditor.fields import RichTextField
from datetime import datetime
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.

class Blogpost(models.Model):
    sno = models.AutoField
    username = models.CharField(max_length=20)
    Title = models.CharField(max_length=100,default="")
    content = RichTextField(blank=True,null=True)
    pub_date = models.DateTimeField(default=datetime.now(),blank=True)
    image = models.ImageField(default="")
    slug = models.CharField(max_length=130)

    def __str__(self):
        return self.Title + " by " + self.username

class Blogcomment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Blogpost, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:13] + "..." + " by " + self.user.username

class Emails(models.Model):
    email = models.EmailField(max_length=254)
    def __str__(self):
        return self.email

class Contact(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=254)
    message = models.TextField()

    def __str__(self):
        return self.name