from django.http import HttpRequest, HttpResponse
import json
from ..models import Post, PostSerializer, Comment, Author, CommentSerializer, Like, LikeSerializer
from django.core.paginator import Paginator


def single_post_likes(request: HttpRequest, author_id: int, post_id: int):
    if request.method == "GET":
        return single_post_likes_get(request, author_id, post_id)
    return HttpResponse(status=405)


def single_comment_likes(request: HttpRequest, author_id: int, post_id: int, comment_id: int):
    if request.method == "GET":
        return single_comment_likes_get(request, author_id, post_id, comment_id)
    return HttpResponse(status=405)


def single_author_likes(request: HttpRequest, author_id: int):
    if request.method == "GET":
        return single_author_likes_get(request, author_id)
    return HttpResponse(status=405)


# get the likes from a post
def single_post_likes_get(request: HttpRequest, author_id: int, post_id: int):
    post_url = Post.objects.all().filter(pk=post_id).first().url #type: ignore
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


# get the likes from a comment
def single_comment_likes_get(request: HttpRequest, author_id: int, post_id: int, comment_id: int):
    comment_url = Comment.objects.all().filter(pk=comment_id).first().url #type: ignore
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


# get the likes from an author
def single_author_likes_get(request: HttpRequest, author_id: int):
    likes = Like.objects.all().filter(author=author_id).order_by("published")

    serialized_data = []
    for like in likes:
        serialized_like = LikeSerializer(like).data

        if serialized_like["post"]:
            serialized_like["object"] = Post.objects.all().filter(pk=serialized_like["post"]).first().url #type: ignore
        elif serialized_like["comment"]:
            serialized_like["object"] = Comment.objects.all().filter(pk=serialized_like["comment"]).first().url #type: ignore

        del serialized_like["post"]
        del serialized_like["comment"]

        serialized_data.append(serialized_like)

    res = json.dumps({
        "type": "likes",
        "items": serialized_data
    })

    return HttpResponse(content=res, status=200)

