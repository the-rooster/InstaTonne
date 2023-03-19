from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from ..models import Author
from django.contrib.auth.models import User
from InstaTonne.forms import LoginForm
from django.contrib.auth import authenticate, login as auth_login
import json

@csrf_exempt
def login(request : HttpRequest):

    
    if request.method != "POST":
        return HttpResponse(status=405)

    form = LoginForm(request.POST)


    if not form.is_valid():
        form.add_error("username","Form is invalid.")
        return HttpResponse(status=400)
        # return render(request,"registration/login.html",context= {"form" : form})


    user = authenticate(request,username=form.data["username"],password=form.data["password"])

    if not user:
        form.add_error("username","Form is invalid.")
        return HttpResponse(status=404)
        #return render(request,"registration/login.html",context= {"form" : form})
        
    authors = Author.objects.filter(userID=user.pk)

    if not authors:
        form.add_error("username","something has gone terribly wrong")
        return render(request,"registration/login.html",context= {"form" : form})

    author = authors[0]

    if not author.active:
        form.add_error("username","Admin has not approved of your account yet.")
        return HttpResponse(content="Admin has not approved of your account yet",status=403)
    
    auth_login(request,user)

    res = json.dumps({
        "authorId": author.id
    })

    return HttpResponse(status=200, content=res)