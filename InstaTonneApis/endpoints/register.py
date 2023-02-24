from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from InstaTonneApis.models import Author
from InstaTonne.forms import RegisterForm


def register_author(request : HttpRequest):

    if request.method != "POST":
        return HttpResponse(status=405)

    form = RegisterForm(request.POST)

    if not form.is_valid():
        form.add_error("username","Form is invalid.")
        return HttpResponse(status=400)

    if len(User.objects.filter(username=form.data["username"])) != 0:
        form.add_error("username","User already exists!")
        return HttpResponse(status=400)

    user = User.objects.create_user(username=form.data["username"],password=form.data["password"])
    Author.objects.create(displayName=form.data["username"],type="author",url="none",host="none",github="none",profileImage="none",userID=user.pk,active=False,id_url="none")


    return HttpResponse(status=200)