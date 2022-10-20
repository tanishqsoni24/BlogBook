from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # URL's

    path("", views.index,name="BlogPage"),
    path("Blogs/", views.blogs ,name="BlogPage"),
    path("Sign_Up/", views.signup ,name="SignupPage"),
    path("login/", views.login ,name="LoginPage"),
    path("userid", views.userid ,name="userid"),
    path("handleblogs", views.handleblogs ,name="handleblogs"),

    # API Keys

    path("handleaddblogs", views.handleaddblogs ,name="handleaddblogs"),
    path("submitregister", views.handlesignup ,name="handlesignup"),
    path("submitlogin", views.handlelogin ,name="handlelogin"),
    path("logout", views.handlelogout ,name="handlelogin"),
    path("search", views.search ,name="search"),
    path("addblogs", views.addblogs ,name="addblogs"),
    path("postComment", views.postComment ,name="postComment"),
    path("emails", views.emails ,name="emails"),
    path("contactus/", views.contactus ,name="contactus"),
    path("handlecontact", views.handlecontact ,name="handlecontact"),
    path("myblogs", views.myblogs ,name="myblogs"),
    path("<str:slug>/", views.readmore ,name="readmore")
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)