from django.http import HttpRequest, HttpResponse
import json
from InstaTonneApis.models import Author, AuthorSerializer
from InstaTonneApis.endpoints.utils import valid_requesting_user, check_auth_header, isaURL, get_auth_headers
from django.core.paginator import Paginator
import requests


# handle requests for remote authors
def remote_authors(request: HttpRequest, remote_authors: str):
    if not check_auth_header(request):
        print("HERE???")
        return HttpResponse(status=401)

    if request.method == "GET":
        return authors_get_remote(request, remote_authors)
    
    return HttpResponse(status=405)


# handle requests for authors
def authors(request: HttpRequest):
    if not check_auth_header(request):
        return HttpResponse(status=401)

    if request.method == "GET":
        return authors_get(request)
    
    return HttpResponse(status=405)


# handle requests for a single author
def single_author(request: HttpRequest, author_id: str):
    if not check_auth_header(request):
        return HttpResponse(status=401)

    if isaURL(author_id) and request.method == "GET":
        return single_author_get_remote(request, author_id)
    
    if isaURL(author_id):
        return HttpResponse(status=405)
    
    if request.method == "GET":
        return single_author_get(request, author_id)
    
    if request.method == "POST":
        return single_author_post(request, author_id)
    
    return HttpResponse(status=405)


# get all authors
def authors_get(request : HttpRequest):
    authors = Author.objects.all().filter(active=True).order_by("id")
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


# get all remote authors
def authors_get_remote(request: HttpRequest, remote_authors: str):
    url = remote_authors
    response: requests.Response = requests.get(url, headers=get_auth_headers(url))

    print(response.content)
    return HttpResponse(
        status=response.status_code,
        content_type=response.headers['Content-Type'],
        content=response.content.decode('utf-8')
    )


# get a single author
def single_author_get(request: HttpRequest, author_id: str):
    author: Author | None = Author.objects.all().filter(pk=author_id).first()

    if author is None:
        return HttpResponse(status=404)

    serialized_author = AuthorSerializer(author).data
    
    res = json.dumps(serialized_author)
    return HttpResponse(content=res, content_type="application/json", status=200)


# get a single remote author
def single_author_get_remote(request: HttpRequest, author_id: str):
    url = author_id
    response: requests.Response = requests.get(url, headers=get_auth_headers(url))
    return HttpResponse(
        status=response.status_code,
        content_type=response.headers['Content-Type'],
        content=response.content.decode('utf-8')
    )


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


def get_author_id(request : HttpRequest):
    if request.method != "POST":
        return HttpResponse(status=405)
    
    author = Author.objects.filter(userID=request.user.id) #type: ignore

    if not author:
        return HttpResponse(status=404)
    
    author = author[0]

    res = {"id" : author.id}

    return HttpResponse(content=json.dumps(res),status=200)
