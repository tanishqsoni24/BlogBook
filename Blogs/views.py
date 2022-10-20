from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from .models import Blogpost, Blogcomment, Emails, Contact
from Blogs.templatetags import extras
from django.core.files.storage import FileSystemStorage

# Create your views here.

# Redirections

def index(request):
    posts = Blogpost.objects.all()
    l_of_comment = []
    blog = {}
    for i in posts:
        comments = Blogcomment.objects.filter(post=i)
        l_of_comment.append(len(comments))
        blog.update({i.id:len(comments)})
    l_of_comment.sort(reverse=True)
    def get_key(val):
        for key, value in blog.items():
            if val == value:
                return key
    allblog = []
    for item in range(3):
        allpost = Blogpost.objects.filter(id = get_key(l_of_comment[item]))
        for i in allpost:
            blog.pop(i.id)
        allblog.append(allpost)
    context = {'allblogs': allblog}
    
    return render(request , 'home.html' , context)


def blogs(request):

    # Sending Blog Data to HTML

    all_blogs = Blogpost.objects.all()
    params = {'all_blogs':all_blogs}
    return render(request, 'blogs.html',params)

def signup(request):
    return render(request, 'signup.html')

def login(request):
    return render(request, 'login.html')

def handleblogs(request):
    messages.success(request, "Register or LogIn first!")
    return redirect('/Sign_Up/')

# API Keys

def handlesignup(request):
    if request.method == 'POST':

        #Getting User Info

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repass = request.POST['repass']
        
        #Throwing the errors

        if len(password)<8:
            messages.success(request,"Password must be greater than or equals to 8 characters")
            return redirect('/Sign_Up/')

        if password!=repass:
            messages.success(request,"Passwords Do not match")
            return redirect('/Sign_Up/')

        #Creating the user

        myuser = User.objects.create_user(username, email, password)
        myuser.save()
        user = authenticate(username = username, password = password)
        if user is not None:
            auth_login(request, user)
            messages.success(request,"Your id has been successfully registered")
            # messages.success(request, "Successfully Logged In")
            return redirect('/myblogs')
        
        
    else:
        return HttpResponse("404 Not found")

def handlelogin(request) :
    if request.method == 'POST':

        #Getting User Info

        username = request.POST['loginusername']
        password = request.POST['loginpassword']

        user = authenticate(username = username, password = password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('/myblogs')

        else:
            messages.success(request, "Account Do Not Exist!")
            return redirect('/login/')

    else:
        return HttpResponse("404 Not found")

def handlelogout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('/')

def search(request):
    # all_blogs = Blogpost.objects.all()
    query = request.GET['query']
    if len(query)>78:
        all_blogs = []
    
    else:
        all_blogs_title = Blogpost.objects.filter(Title__icontains=query)
        all_blogs_content = Blogpost.objects.filter(content__icontains=query)
        all_blogs = all_blogs_title.union(all_blogs_content)

    if len(all_blogs) == 0:  # To check the length of Query set
        messages.error(request, "No search Results Found")
    params = {'all_blogs':all_blogs,'query':query}
    return render(request, 'search.html',params)
        
def addblogs(request):
    addblog = Blogpost.objects.all()
    params = {'addblog':addblog}
    return render(request, 'addblogs.html',params)

def readmore(request,slug):
    post = Blogpost.objects.filter(slug=slug).first()
    comments = Blogcomment.objects.filter(post=post,parent=None)
    replies = Blogcomment.objects.filter(post=post).exclude(parent=None)
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]  = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    print(replyDict)
    params = {'post':post,'comments':comments, 'replyDict':replyDict}
    return render(request, 'readmore.html', params)

def postComment(request):
    if request.method == "POST":
        comment = request.POST.get("comment")
        user = request.user
        postSno = request.POST.get("postSno")
        post = Blogpost.objects.get(id=postSno)
        parentSno = request.POST.get("parentSno")
        if parentSno == "":
            comment = Blogcomment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request,"Comment Sent")

        else:
            parent = Blogcomment.objects.get(sno=parentSno)
            comment = Blogcomment(comment=comment, user=user, post=post, parent = parent)          
            comment.save()
            messages.success(request,"Reply Sent")

        return redirect(f"/{post.slug}")

def myblogs(request):
    all_blogs = Blogpost.objects.filter(username=request.user)
    params = {'all_blogs':all_blogs} 
    return render(request, 'myblogs.html',params)

def userid(request):
    return render(request, 'userid.html')

def handleaddblogs(request):
    if request.method == 'POST' and request.FILES['image']:
        title = request.POST['title']
        content = request.POST['content']
        upload = request.FILES['image']
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        slug= str(request.user) + str(len(Blogpost.objects.filter(username = request.user)) + 1)
        blogfields = Blogpost(username=request.user, Title= title, content=content, image=file, slug=slug)
        blogfields.save()
        return redirect("/"+slug)

def emails(request):
    if request.method == 'POST':
        email = request.POST['email']
        Email = Emails(email=email)
        Email.save()
        messages.success(request,"Reply Sent")
        return redirect("/")

def contactus(request):
    return render(request,"contactus.html")

def handlecontact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        contact_details = Contact(name=name, email=email, message= message)
        contact_details.save()
        messages.success(request,"Query Sent")
        return redirect("/contactus")