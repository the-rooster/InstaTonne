from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from ..models import Author
from django.contrib.auth.models import User
from InstaTonne.forms import LoginForm
from django.contrib.auth import authenticate, login as auth_login



def login(request : HttpRequest):

    if request.method != "POST":
        return HttpResponse(status=405)

    form = LoginForm(request.POST)


    if not form.is_valid():
        form.add_error("username","Form is invalid.")
        return render(request,"registration/login.html",context= {"form" : form})


    user = authenticate(request,username=form.data["username"],password=form.data["password"])

    if not user:
        form.add_error("username","Form is invalid.")
        return render(request,"registration/login.html",context= {"form" : form})
        
    authors = Author.objects.filter(userID=user.pk)

    if not authors:
        form.add_error("username","something has gone terribly wrong")
        return render(request,"registration/login.html",context= {"form" : form})

    author = authors[0]

    if not author.active:
        form.add_error("username","Admin has not approved of your account yet.")
        return render(request,"registration/login.html",context= {"form" : form})
    
    auth_login(request,user)

    return redirect("/")