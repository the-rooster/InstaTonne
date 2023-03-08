from django.http import HttpRequest, HttpResponse
import json
from ..models import Post, PostSerializer, Comment, Author, CommentSerializer, Like, LikeSerializer
from .utils import get_one_url, make_author_url, send_to_single_inbox
from django.core.paginator import Paginator
import re


def single_post_likes(request: HttpRequest):
    matched = re.search(r"^\/authors\/(.*?)\/posts\/(.*?)\/likes\/?$", request.path)
    if matched:
        author_id: str = matched.group(1)
        post_id: str = matched.group(2)
    else:
        return HttpResponse(status=400)

    if "/" in post_id and request.method == "GET":
        return single_post_likes_get_remote(request, author_id, post_id)
    elif request.method == "GET":
        return single_post_likes_get(request, author_id, post_id)
    
    if "/" in post_id and request.method == "POST":
        return single_post_likes_post_remote(request,author_id,post_id)
    elif request.method == "POST":
        return single_post_likes_post(request,author_id,post_id)
    
    return HttpResponse(status=400)

def single_post_likes_post_remote(request : HttpRequest,author_id : str,post_id : str):
    author: Author | None = Author.objects.all().filter(userID=request.user.id).first()
    
    if not author:
        return HttpResponse(status=403)
    
    try:
        like: dict = {
            "type" : "like",
            "author" : make_author_url(request.get_host(), author.id),
            "object" : post_id
        }

        # comment_id = comment.id #type: ignore
        # comment.id_url = make_comment_url(request.get_host(), author_id, post_id, comment_id)
        # comment.save()

        #get post information to recover author url
        res = get_one_url(post_id)

        if not res:
            print("POST NOT FOUND WHEN TRYING TO MAKE COMMENT!")
            return HttpResponse(status=400)
        
        #assume author.id field. might need adapter for this boy
        res_content = json.loads(res[1])
        print("CONTENT: ",res_content)
        author_inbox_url = res_content["author"]["id"]

        send_to_single_inbox(author_inbox_url,like)

        return HttpResponse(status=204)
    except Exception as e:
        print(e)
        return HttpResponse(status=400)

def single_post_likes_post(request : HttpRequest,author_id : str,post_id : str):
    author: Author | None = Author.objects.all().filter(userID=request.user.id).first()

    if not author:
        print('yahoooo',request.user.id)
        return HttpResponse(status=403)
    try:
        post: Post | None = Post.objects.all().filter(pk=post_id).first()

        if post is None:
            return HttpResponse(status=404)
        
        like: dict = {
            "type" : "like",
            "author" : make_author_url(request.get_host(), author.id),
            "object" : post_id,
            "summary" : "An author liked your post!"
        }

        # comment_id = comment.id #type: ignore
        # comment.id_url = make_comment_url(request.get_host(), author_id, post_id, comment_id)
        # comment.save()

        author_inbox_url = make_author_url(request.get_host(),author_id)

        send_to_single_inbox(author_inbox_url,like)

        return HttpResponse(status=204)
    except Exception as e:
        print(e)
        return HttpResponse(status=400)

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

def get_single_like_post_local(request: HttpRequest,author_id : str,post_id : str, like_id : str):
    post = Post.objects.filter(id=post_id).first()

    if not post:
        return HttpResponse(status=404)
    
    
    
    like = Like.objects.filter(id=like_id).first()

    res = json.dumps({
        "type": "like",
        "post": like.post.id_url,
        "author" : like.post.author.id,
        "summary" : like.summary
    })

    return HttpResponse(content=res,status=200)

def get_single_like_comment_local(request: HttpRequest,author_id : str,post_id : str, comment_id : str, like_id : str):
    comment = Comment.objects.filter(id=comment_id).first()

    if not comment:
        return HttpResponse(status=404)
    
    
    
    like = Like.objects.filter(id=like_id).first()

    res = json.dumps({
        "type": "like",
        "post": like.comment.id_url,
        "author" : like.comment.author,
        "summary" : like.summary
    })

    return HttpResponse(content=res,status=200)
