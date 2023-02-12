from django.http import HttpRequest, HttpResponse
import json
from .auth_wrapper import checkAuthorization
from django.db import models
from ..models import Author, AuthorSerializer
from rest_framework.renderers import JSONRenderer
from django.views.decorators.csrf import csrf_exempt
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
    
    data = {"type" : "authors","items" : serializer.data}
    

    return HttpResponse(content=JSONRenderer().render(data),status=200)

@csrf_exempt
def single_author(request : HttpRequest,id : str):

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
        
        author = Author.objects.filter(pk=id)

        print('foeey')
        if not author.exists():
            return HttpResponse(status=400)

        for k,v in body.items():
            author.update()
        author.save()

    return HttpResponse(status=405)