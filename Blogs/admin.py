from django.contrib import admin
from .models import Blogpost,Blogcomment,Emails,Contact

# Register your models here.

admin.site.register((Blogpost,Blogcomment,Emails,Contact))