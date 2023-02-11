from django.http import HttpRequest, HttpResponse
import json
from .auth_wrapper import checkAuthorization
from django.db import models
from ..models import Author, AuthorSerializer
from rest_framework.renderers import JSONRenderer
from django.core.paginator import Paginator

# @checkAuthorization
def page_all_authors(request : HttpRequest):

    if request.method != "GET":
        return HttpResponse(status=405)

    if "page" not in request.GET.keys() or "size" not in request.GET.keys():
        return HttpResponse(status=400)
    
    page_num = request.GET.get("page")
    page_size = request.GET.get("size")

    authors = Author.objects.all()

    paginator = Paginator(authors,page_size)
    
    result = paginator.get_page(page_num)

    serializer = AuthorSerializer(result,many=True)

    return HttpResponse(content=JSONRenderer().render(serializer.data),status=200)


def get_single_author(request : HttpRequest,id : str):

    if request.method != "GET":
        return HttpResponse(status=405)

    author = Author.objects.get(pk=id)

    serializer = AuthorSerializer(author)

    return HttpResponse(content=JSONRenderer().render(serializer.data),status=200)

