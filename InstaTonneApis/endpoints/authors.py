from django.http import HttpRequest, HttpResponse
import json
from ..models import Author, AuthorSerializer
from django.core.paginator import Paginator
from .utils import valid_requesting_user, get_one_url, check_auth_header
import re


def get_author_id(request : HttpRequest):
    if request.method != "POST":
        return HttpResponse(status=405)
    
    author = Author.objects.filter(userID=request.user.id) #type: ignore

    if not author:
        return HttpResponse(status=404)
    
    author = author[0]

    res = {"id" : author.id}

    return HttpResponse(content=json.dumps(res),status=200)


def authors(request: HttpRequest):
    if request.method == "GET":
        return authors_get(request)
    return HttpResponse(status=405)


def single_author(request: HttpRequest):
    matched = re.search(r"^\/authors\/(.*?)\/?$", request.path)
    if matched:
        author_id: str = matched.group(1)
    else:
        return HttpResponse(status=405)

    if "/" in author_id and request.method == "GET":
        return single_author_get_remote(request, author_id)
    elif "/" in author_id:
        return HttpResponse(status=405)
    if request.method == "GET":
        return single_author_get(request, author_id)
    if request.method == "POST":
        print("Getting into single_author_post")
        print(request)
        print(author_id)
        return single_author_post(request, author_id)
    return HttpResponse(status=405)


# get all authors
def authors_get(request : HttpRequest):

    if not check_auth_header(request):
        return HttpResponse(status=401)
    
    authors = Author.objects.all().order_by("id")
    page_num = request.GET.get("page")
    page_size = request.GET.get("size")

    if page_num is not None and page_size is not None:
        paginator = Paginator(authors, page_size)
        authors = paginator.get_page(page_num)

    serialized_data = []
    for author in authors:
        serialized_author = AuthorSerializer(author).data
        serialized_data.append(serialized_author)

    res = json.dumps({
        "type": "authors",
        "items": serialized_data
    })

    return HttpResponse(content=res, content_type="application/json", status=200)


# get a single author
def single_author_get(request: HttpRequest, author_id: str):

    if not check_auth_header(request):
        return HttpResponse(status=401)
    
    author = Author.objects.get(pk=author_id)
    serialized_author = AuthorSerializer(author).data
    # serialized_author["id"] = serialized_author["id_url"]
    # del serialized_author["id_url"]
    res = json.dumps(serialized_author)
    return HttpResponse(content=res, content_type="application/json", status=200)


# get a single remote author
def single_author_get_remote(request: HttpRequest, author_id: str):
    status_code, text = get_one_url(author_id)
    return HttpResponse(content=text, content_type="application/json", status=status_code)


# update a single author
def single_author_post(request: HttpRequest, author_id: str):
    
    if not valid_requesting_user(request, author_id):
        return HttpResponse(status=401)

    try:
        author: Author | None = Author.objects.all().filter(pk=author_id).first()

        if author is None:
            return HttpResponse(status=404)
    
        body: dict = json.loads(request.body)

        if "displayName" in body:
            author.displayName = body["displayName"]
        if "github" in body:
            author.github = body["github"]
        if "profileImage" in body:
            author.profileImage = body["profileImage"]
        author.save()

        return HttpResponse(status=204)
    except Exception as e:
        print(e)
        return HttpResponse(status=400)
