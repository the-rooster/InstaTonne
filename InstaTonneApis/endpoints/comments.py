from django.http import HttpRequest, HttpResponse
import json
from ..models import Post, PostSerializer, Comment, Author, CommentSerializer
from django.core.paginator import Paginator
from .utils import make_comment_url, make_comments_url, get_one_url, make_author_url, send_to_single_inbox, check_authenticated, check_auth_header, isaURL, get_auth_headers
import requests
import re
from InstaTonne.settings import HOSTNAME


# handle requests for the comments of a post
def single_post_comments(request: HttpRequest, author_id: str, post_id: str):
    if not check_auth_header(request):
        return HttpResponse(status=401)

    if isaURL(post_id) and request.method == "GET":
        return single_post_comments_get_remote(request, author_id, post_id)
    
    if isaURL(post_id) and request.method == "POST":
        return single_post_comments_post_remote(request,author_id,post_id)
    
    if isaURL(post_id):
        return HttpResponse(status=405)
    
    if request.method == "GET":
        return single_post_comments_get(request, author_id, post_id)
    
    if request.method == "POST":
        return single_post_comments_post(request, author_id, post_id)
    
    return HttpResponse(status=405)


# handle requests for a single comment of a post
def single_post_comment(request: HttpRequest, author_id: str, post_id: str, comment_id: str):
    if not check_auth_header(request):
        return HttpResponse(status=401)

    if request.method == "GET":
        return get_single_comment_local(request, author_id, post_id, comment_id)
    
    return HttpResponse(status=405)


# get the comments from a post
def single_post_comments_get(request: HttpRequest, author_id: str, post_id: str):
    post: Post | None = Post.objects.all().filter(pk=post_id).first()

    if post is None:
        return HttpResponse(status=404)
    
    comments = Comment.objects.all().filter(post=post_id).order_by("published")
    page_num = request.GET.get("page")
    page_size = request.GET.get("size")

    if page_num is not None and page_size is not None:
        paginator = Paginator(comments, page_size)
        comments = paginator.get_page(page_num)

    serialized_data = []
    for comment in comments:
        serialized_comment = CommentSerializer(comment).data

        serialized_data.append(serialized_comment)

    res = json.dumps({
        "type": "comments",
        "page": page_num,
        "size": page_size,
        "post": post.id_url,
        "id": make_comments_url(HOSTNAME, author_id, post_id),
        "comments": serialized_data
    })

    return HttpResponse(content=res, content_type="application/json", status=200)


# get the comments from a remote post
def single_post_comments_get_remote(request: HttpRequest, author_id: str, post_id: str):
    query = request.META.get('QUERY_STRING', '')
    if query: query = '?' + query
    url = post_id + '/comments' + query
    response: requests.Response = requests.get(url, headers=get_auth_headers(url))
    return HttpResponse(
        status=response.status_code,
        content_type=response.headers['Content-Type'],
        content=response.content.decode('utf-8')
    )


# add a comment to a remote post
def single_post_comments_post_remote(request: HttpRequest, author_id : str, post_id : str):
    author: Author | None = Author.objects.all().filter(userID=request.user.pk).first()
    
    if not author:
        return HttpResponse(status=401)
    
    try:
        body: dict = json.loads(request.body)
        comment: dict = {
            "type" : "comment",
            "contentType" : body["contentType"],
            "content" : body["comment"],
            "author" : author.id_url,
            "post" : post_id
        }

        status_code = send_to_single_inbox(post_id.split('/posts')[0], comment)

        return HttpResponse(status=status_code)
    except Exception as e:
        print(e)
        return HttpResponse(status=400)
    

# add a comment to a post
def single_post_comments_post(request: HttpRequest, author_id: str, post_id: str):
    author: Author | None = Author.objects.all().filter(userID=request.user.pk).first()

    if not author:
        return HttpResponse(status=401)
    
    post: Post | None = Post.objects.all().filter(pk=post_id).first()

    if post is None:
        return HttpResponse(status=404)
    
    try:
        body: dict = json.loads(request.body)
        comment: dict = {
            "type" : "comment",
            "contentType" : body["contentType"],
            "content" : body["comment"],
            "author" : author.id_url,
            "post" : post.id_url
        }

        status_code = send_to_single_inbox(author.id_url, comment)

        return HttpResponse(status=status_code)
    except Exception as e:
        print(e)
        return HttpResponse(status=400)


# get a single comment from a post
def get_single_comment_local(request: HttpRequest, author_id: str, post_id: str, comment_id: str):
    comment = Comment.objects.filter(id=comment_id).first()

    if comment is None:
        return HttpResponse(status=404)
    
    serialized_comment = CommentSerializer(comment).data

    res = json.dumps(serialized_comment)

    return HttpResponse(content=res, content_type="application/json", status=200)
