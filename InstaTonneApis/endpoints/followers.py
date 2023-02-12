from django.http import HttpRequest, HttpResponse
import json
from .auth_wrapper import checkAuthorization
from django.db import models
from ..models import Author, AuthorSerializer
from rest_framework.renderers import JSONRenderer
from django.core.paginator import Paginator


def single_author_followers(request : HttpRequest,id : str):
    print("here")

    if request.method == "GET":

        author = Author.objects.get(pk=id)

        serializer = AuthorSerializer(author)

        data = serializer.data
        data["type"] = "author"

        print("helooooo")
        return HttpResponse(content=JSONRenderer().render(data),status=200)

    elif request.method == "POST":

        print("AAA")
        try:
            print(request.body)
            body : dict = json.loads(request.body)
        except Exception as e:
            print(e)
            return HttpResponse(status=400)
        
        author = Author.objects.get(pk=id)

        
        if not author:
            return HttpResponse(status=400)

        if "url" in body:
            author.url = body["url"]
        if "id" in body:
            author.id = body["id"]
        if "host" in body:
            author.host = body["host"]
        if "displayName" in body:
            author.displayName = body["displayName"]
        if "github" in body:
            author.github = body["github"]
        if "profileImage" in body:
            author.profileImage = body["profileImage"]
        
        author.save()

        return HttpResponse(status=204)

    return HttpResponse(status=405)