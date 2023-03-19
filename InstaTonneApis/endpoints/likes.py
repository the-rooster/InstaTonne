from django.http import HttpRequest, HttpResponse
import json
from ..models import Post, PostSerializer, Comment, Author, CommentSerializer, Like, LikeSerializer
from .utils import get_one_url, make_author_url, send_to_single_inbox, check_auth_header
from django.core.paginator import Paginator
import re


def single_post_likes(request: HttpRequest):
    matched = re.search(r"^\/authors\/(.*?)\/posts\/(.*?)\/likes\/?$", request.path)
    if matched:
        author_id: str = matched.group(1)
        post_id: str = matched.group(2)
    else:
        return HttpResponse(status=400)
    print("POST ID: " + post_id)
    print("request.method: " + request.method)
    if "/" in post_id and request.method == "GET":
        return single_post_likes_get_remote(request, author_id, post_id)
    elif "/" in post_id and request.method == "POST":
        print("POSTING TO REMOTE")
        return single_post_likes_post_remote(request,author_id,post_id)
    elif "/" in post_id or "/" in author_id:
        return HttpResponse(status=405)
    elif request.method == "GET":
        return single_post_likes_get(request, author_id, post_id)
    elif request.method == "POST":
        print("POSTING TO LOCAL")
        return single_post_likes_post(request,author_id,post_id)
    return HttpResponse(status=405)


def single_comment_like(request: HttpRequest):
    matched = re.search(r"^\/authors\/(.*?)\/posts\/(.*?)\/comments\/(.*?)\/likes\/(.*?)\/?$", request.path)
    if matched:
        author_id: str = matched.group(1)
        post_id: str = matched.group(2)
        comment_id: str = matched.group(3)
        like_id: str = matched.group(4)
    else:
        return HttpResponse(status=400)

    if request.method == "GET":
        return get_single_like_comment_local(request, author_id, post_id, comment_id, like_id)
    return HttpResponse(status=405)


def single_post_like(request: HttpRequest):
    matched = re.search(r"^\/authors\/(.*?)\/posts\/(.*?)\/likes\/(.*?)\/?$", request.path)
    if matched:
        author_id: str = matched.group(1)
        post_id: str = matched.group(2)
        like_id: str = matched.group(3)
    else:
        return HttpResponse(status=400)
    print("posting to local in single_post_like")
    if request.method == "GET":
        return get_single_like_post_local(request, author_id, post_id, like_id)
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
    if "/" in comment_id and request.method == "POST":
        return single_comment_likes_post_remote(request, author_id, post_id, comment_id)
    elif "/" in comment_id:
        return HttpResponse(status=405)
    if request.method == "GET":
        return single_comment_likes_get(request, author_id, post_id, comment_id)
    if request.method == "POST":
        return single_comment_likes_post(request, author_id, post_id, comment_id)
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


def single_post_likes_post_remote(request : HttpRequest,author_id : str,post_id : str):
    author: Author | None = Author.objects.all().filter(userID=request.user.pk).first()
    
    if not author:
        return HttpResponse(status=401)
    
    try:
        like: dict = {
            "type" : "like",
            "author" : make_author_url(request.get_host(), author.id),
            "object" : post_id,
            "summary" : "I like this post!"
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
        print("CONTENT for single_post_likes_post_remote: ",res_content)
        print("res_content: ",res_content)
        author_inbox_url = res_content["author"]["id"]
        print("author_inbox_url: ",author_inbox_url)
        send_to_single_inbox(author_inbox_url,like)

        return HttpResponse(status=204)
    except Exception as e:
        print(e)
        print("ERROR IN SINGLE POST LIKES POST REMOTE")
        return HttpResponse(status=400)


def single_post_likes_post(request : HttpRequest,author_id : str,post_id : str):
    author: Author | None = Author.objects.all().filter(userID=request.user.pk).first()

    if not author:
        return HttpResponse(status=401)
    
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
    

def single_comment_likes_post_remote(request: HttpRequest, author_id: str, post_id: str, comment_id: str):
    author: Author | None = Author.objects.all().filter(userID=request.user.pk).first()
    
    if not author:
        return HttpResponse(status=401)
    
    try:
        like: dict = {
            "type" : "like",
            "author" : make_author_url(request.get_host(), author.id),
            "object" : comment_id,
            "summary" : "I like this comment!"
        }

        # comment_id = comment.id #type: ignore
        # comment.id_url = make_comment_url(request.get_host(), author_id, post_id, comment_id)
        # comment.save()

        #get post information to recover author url
        status, res = get_one_url(comment_id)

        print("RESPONSE: ",res)
        if not res:
            print("POST NOT FOUND WHEN TRYING TO MAKE COMMENT!")
            return HttpResponse(status=400)
        
        #assume author.id field. might need adapter for this boy
        res_content = json.loads(res[1])
        print("CONTENT for single_comment_likes_post_remote: ",res_content)
        author_inbox_url = res_content["author"]

        send_to_single_inbox(author_inbox_url,like)

        return HttpResponse(status=204)
    except Exception as e:
        print(e)
        return HttpResponse(status=400)


def single_comment_likes_post(request: HttpRequest, author_id: str, post_id: str, comment_id: str):
    author: Author | None = Author.objects.all().filter(userID=request.user.pk).first()

    if not author:
        return HttpResponse(status=401)
    
    try:
        comment: Comment | None = Comment.objects.all().filter(pk=comment_id).first()

        if comment is None:
            return HttpResponse(status=404)
        
        like: dict = {
            "type" : "like",
            "author" : make_author_url(request.get_host(), author.id),
            "object" : comment_id,
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


# get the likes from a post
def single_post_likes_get(request: HttpRequest, author_id: str, post_id: str):

    #check that request is authenticated. remote or local
    if not check_auth_header(request):
        return HttpResponse(status=401)
    
    post: Post | None = Post.objects.all().filter(pk=post_id).first()

    if post is None:
        return HttpResponse(status=404)

    likes = Like.objects.all().filter(post=post_id).order_by("published")

    serialized_data = []
    for like in likes:
        serialized_like = LikeSerializer(like).data

        serialized_like["object"] = post.id_url
        del serialized_like["post"]
        del serialized_like["comment"]

        serialized_data.append(serialized_like)

    res = json.dumps({
        "type": "likes",
        "items": serialized_data
    })

    return HttpResponse(content=res, content_type="application/json", status=200)


def single_post_likes_get_remote(request: HttpRequest, author_id: str, post_id: str):
    remote_url = post_id + '/likes'
    status_code, text = get_one_url(remote_url)
    return HttpResponse(status=status_code, content_type="application/json", content=text)


# get the likes from a comment
def single_comment_likes_get(request: HttpRequest, author_id: str, post_id: str, comment_id: str):

    #check that request is authenticated. remote or local
    if not check_auth_header(request):
        return HttpResponse(status=401)
    
    comment = Comment.objects.all().filter(pk=comment_id).first()

    if comment is None:
        return HttpResponse(status=404)

    likes = Like.objects.all().filter(post=post_id).order_by("published")

    serialized_data = []
    for like in likes:
        serialized_like = LikeSerializer(like).data

        serialized_like["object"] = comment.id_url
        del serialized_like["post"]
        del serialized_like["comment"]

        serialized_data.append(serialized_like)

    res = json.dumps({
        "type": "likes",
        "items": serialized_data
    })

    return HttpResponse(content=res, content_type="application/json", status=200)


def single_comment_likes_get_remote(request: HttpRequest, author_id: str, post_id: str, comment_id: str):
    remote_url = comment_id + '/likes'
    status_code, text = get_one_url(remote_url)
    return HttpResponse(status=status_code, content_type="application/json", content=text)


# get the likes from an author
def single_author_likes_get(request: HttpRequest, author_id: str):
    
    #check that request is authenticated. remote or local
    if not check_auth_header(request):
        return HttpResponse(status=401)
    
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

    return HttpResponse(content=res, content_type="application/json", status=200)


def single_author_likes_get_remote(request: HttpRequest, author_id: str):
    remote_url = author_id + '/liked'
    status_code, text = get_one_url(remote_url)
    return HttpResponse(status=status_code, content_type="application/json", content=text)


def get_single_like_post_local(request: HttpRequest,author_id : str,post_id : str, like_id : str):
    post = Post.objects.filter(id=post_id).first()

    if not post:
        return HttpResponse(status=404)
    
    like = Like.objects.filter(id=like_id, post=post_id).first()

    if not like:
        return HttpResponse(status=404)

    serialized_like = LikeSerializer(like).data
    serialized_like["object"] = post.id_url
    del serialized_like["post"]
    del serialized_like["comment"]

    res = json.dumps(serialized_like)

    return HttpResponse(content=res, content_type="application/json", status=200)


def get_single_like_comment_local(request: HttpRequest,author_id : str,post_id : str, comment_id : str, like_id : str):
    comment = Comment.objects.filter(id=comment_id).first()

    if not comment:
        return HttpResponse(status=404)
    
    like = Like.objects.filter(id=like_id, comment=comment_id).first()

    if not like:
        return HttpResponse(status=404)

    serialized_like = LikeSerializer(like).data
    serialized_like["object"] = comment.id_url
    del serialized_like["post"]
    del serialized_like["comment"]

    res = json.dumps(serialized_like)

    return HttpResponse(content=res, content_type="application/json", status=200)
