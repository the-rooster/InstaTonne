from django.http import HttpRequest, HttpResponse
import json
from ..models import Post, PostSerializer, Comment, Author, CommentSerializer, Like, LikeSerializer
from .utils import get_one_url, make_author_url
from django.core.paginator import Paginator
import re


def single_post_likes(request: HttpRequest):
    matched = re.search(r"^\/authors\/(.*?)\/posts\/(.*?)\/likes\/?$", request.path)
    if matched:
        author_id: str = matched.group(1)
        post_id: str = matched.group(2)
    else:
        return HttpResponse(status=405)

    if "/" in post_id and request.method == "GET":
        return single_post_likes_get_remote(request, author_id, post_id)
    elif "/" in post_id:
        return HttpResponse(status=405)
    if request.method == "GET":
        return single_post_likes_get(request, author_id, post_id)
    return HttpResponse(status=405)


def single_comment_likes(request: HttpRequest):
    matched = re.search(r"^\/authors\/(.*?)\/posts\/(.*?)\/comments\/(.*?)\/likes\/?$", request.path)
    if matched:
        author_id: str = matched.group(1)
        post_id: str = matched.group(2)
        comment_id: str = matched.group(3)
    else:
        return HttpResponse(status=405)

    if "/" in comment_id and request.method == "GET":
        return single_comment_likes_get_remote(request, author_id, post_id, comment_id)
    elif "/" in comment_id:
        return HttpResponse(status=405)
    if request.method == "GET":
        return single_comment_likes_get(request, author_id, post_id, comment_id)
    return HttpResponse(status=405)


def single_author_likes(request: HttpRequest):
    matched = re.search(r"^\/authors\/(.*?)\/liked\/?$", request.path)
    if matched:
        author_id: str = matched.group(1)
    else:
        return HttpResponse(status=405)

    if "/" in author_id and request.method == "GET":
        return single_author_likes_get_remote(request, author_id,)
    elif "/" in author_id:
        return HttpResponse(status=405)
    if request.method == "GET":
        return single_author_likes_get(request, author_id)
    return HttpResponse(status=405)


# get the likes from a post
def single_post_likes_get(request: HttpRequest, author_id: str, post_id: str):
    post_url = Post.objects.all().filter(pk=post_id).first().id_url #type: ignore
    likes = Like.objects.all().filter(post=post_id).order_by("published")

    serialized_data = []
    for like in likes:
        serialized_like = LikeSerializer(like).data

        serialized_like["object"] = post_url
        del serialized_like["post"]
        del serialized_like["comment"]

        serialized_data.append(serialized_like)

    res = json.dumps({
        "type": "likes",
        "items": serialized_data
    })

    return HttpResponse(content=res, status=200)


def single_post_likes_get_remote(request: HttpRequest, author_id: str, post_id: str):
    remote_url = post_id + '/likes'
    status_code, text = get_one_url(remote_url)
    return HttpResponse(status=status_code, content=text)


# get the likes from a comment
def single_comment_likes_get(request: HttpRequest, author_id: str, post_id: str, comment_id: str):
    comment_url = Comment.objects.all().filter(pk=comment_id).first().id_url #type: ignore
    likes = Like.objects.all().filter(post=post_id).order_by("published")

    serialized_data = []
    for like in likes:
        serialized_like = LikeSerializer(like).data

        serialized_like["object"] = comment_url
        del serialized_like["post"]
        del serialized_like["comment"]

        serialized_data.append(serialized_like)

    res = json.dumps({
        "type": "likes",
        "items": serialized_data
    })

    return HttpResponse(content=res, status=200)


def single_comment_likes_get_remote(request: HttpRequest, author_id: str, post_id: str, comment_id: str):
    remote_url = comment_id + '/likes'
    status_code, text = get_one_url(remote_url)
    return HttpResponse(status=status_code, content=text)


# get the likes from an author
def single_author_likes_get(request: HttpRequest, author_id: str):
    likes = Like.objects.all().filter(author=make_author_url(request.get_host(), author_id)).order_by("published")

    serialized_data = []
    for like in likes:
        serialized_like = LikeSerializer(like).data

        if serialized_like["post"]:
            serialized_like["object"] = Post.objects.all().filter(pk=serialized_like["post"]).first().id_url #type: ignore
        elif serialized_like["comment"]:
            serialized_like["object"] = Comment.objects.all().filter(pk=serialized_like["comment"]).first().id_url #type: ignore

        del serialized_like["post"]
        del serialized_like["comment"]

        serialized_data.append(serialized_like)

    res = json.dumps({
        "type": "likes",
        "items": serialized_data
    })

    return HttpResponse(content=res, status=200)


def single_author_likes_get_remote(request: HttpRequest, author_id: str):
    remote_url = author_id + '/liked'
    status_code, text = get_one_url(remote_url)
    return HttpResponse(status=status_code, content=text)
