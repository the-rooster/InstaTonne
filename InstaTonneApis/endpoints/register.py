from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from InstaTonneApis.models import Author
from InstaTonne.forms import RegisterForm
from InstaTonne.settings import HOSTNAME
import json

def register_author(request : HttpRequest):

    if request.method != "POST":
        return HttpResponse(status=405)

    data = json.loads(request.body)
    form = RegisterForm(data)

    if not form.is_valid():
        form.add_error("username","Form is invalid.")
        return HttpResponse(status=400)

    if len(User.objects.filter(username=form.data["username"])) != 0:
        form.add_error("username","User already exists!")
        return HttpResponse(status=400)

    user = User.objects.create_user(username=form.data["username"],password=form.data["password"])
    obj = Author.objects.create(displayName=form.data["username"],type="author",url="none",host=HOSTNAME,github="none",profileImage="https://www.gravatar.com/avatar/205e460b479e2e5b48aec07710c08d50",userID=user.pk,active=False,id_url="none")

    obj.id_url = HOSTNAME + "/authors/" + obj.id
    obj.url = HOSTNAME + "/authors/" + obj.id
    obj.save()
    
    return HttpResponse(status=200)