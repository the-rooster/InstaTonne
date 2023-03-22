from django.http import HttpRequest, HttpResponse
from ..models import Author, Follow, Inbox, Comment, Like, Post, LikeSerializer
import json
import requests
from InstaTonne.settings import HOSTNAME
from django.views.decorators.csrf import csrf_exempt
from .utils import check_authenticated, get_author, get_all_urls, check_auth_header, get_auth_headers, valid_requesting_user
import time
from threading import Thread, Lock
from InstaTonne.settings import HOSTNAME
from urllib.parse import quote
import re


# handle requests to the inbox
def inbox_endpoint(request: HttpRequest, author_id: str):
    if not check_auth_header(request):
        return HttpResponse(status=401)
    
    if request.method == "GET":
        return get_inbox(request, author_id)
    
    if request.method == "POST":
        return post_inbox(request, author_id)
    
    if request.method == "DELETE":
        return delete_inbox(request, author_id)
    
    return HttpResponse(status=405)


# get the items in an authors inbox
def get_inbox(request: HttpRequest, author_id: str):
    author: Author | None = Author.objects.all().filter(pk=author_id).first()

    if author is None:
        return HttpResponse(status=404)

    inboxes = Inbox.objects.all().filter(author=author.id).order_by('published')

    serialized_data = []
    for inbox in inboxes:
        try:
            response: requests.Response = requests.get(inbox.url, headers=get_auth_headers(inbox.url))
            if response.status_code == 204:
                serialized_data.append({"found url": inbox.url})
            else:
                serialized_data.append(response.json())
        except Exception as e:
            serialized_data.append({"error url": inbox.url})

    res = json.dumps({
        "type" : "inbox",
        "author" : author.id_url,
        "items" : serialized_data
    })
        
    return HttpResponse(content=res, status=200, content_type="application/json")


def parse_inbox(data : dict, user : Author):
    if "type" not in data:
        print("NO TYPE ON INBOX POST!")
        return None
    
    data_type = str(data["type"].lower())

    if data_type == "follow":
        return parse_inbox_follow_request(data, user)
    elif data_type == "post":
        return parse_inbox_post(data)
    elif data_type == "comment":
        return parse_inbox_comment(data)
    elif data_type == "like":
        return parse_inbox_like(data)


def parse_inbox_comment(data):
    if "post" not in data:
        print('ERROR: no post field in body')
        return None
    
    try:
        post_url = data["post"].rstrip('/')
    except:
        print('ERROR: bad post field')
        return None
    
    post: Post | None = Post.objects.all().filter(id_url=post_url).first()

    if post is not None:
        comment = Comment.objects.create(type="comment", post=post)
    else:
        print('ERROR: object does not exist')
        return None
    
    if "contentType" in data:
        comment.contentType = data["contentType"]
    if "comment" in data:
        comment.comment = data["comment"]
    if "author" in data:
        comment.author = data["author"]
    comment.id_url = post_url + '/comments/' + comment.id

    comment.save()

    return comment.id_url


def parse_inbox_like(data):
    if "object" not in data:
        print('ERROR: no object field in body')
        return None
    
    try:
        object_url = data["object"].rstrip('/')
    except:
        print('ERROR: bad object field')
        return None

    comment: Comment | None = Comment.objects.all().filter(id_url=object_url).first()
    post: Post | None = Post.objects.all().filter(id_url=object_url).first()

    if comment is not None:
        like = Like.objects.create(type="like", comment=comment, post=None)
    elif post is not None:
        like = Like.objects.create(type="like", post=post, comment=None)
    else:
        print('ERROR: object does not exist')
        return None
    
    if "summary" in data:
        like.summary = data["summary"]
    if "author" in data:
        like.author = data["author"]

    like.save()

    like_url = object_url + '/likes/' + like.id
    return like_url


def parse_inbox_post(data):
    if "id" not in data:
        print('ERROR: no id field in body')
        return None
    
    return data["id"]


def parse_inbox_follow_request(data : dict, user: Author):
    try:
        #parse expected fields in follow request here
        actor_id = data["actor"]["id"]
        summary = data["summary"]
    except Exception as e:
        print("INBOX FOLLOW REQUEST BROKEN!")
        print(e)
        return None

    obj = Follow.objects.create(object=user,follower_url=actor_id,accepted=False,summary=summary)

    obj.save()

    return HOSTNAME + "/authors/" + user.id + "/followers/" + quote(actor_id, safe='').replace('.', '%2E') + "/request"


# add a post to an inbox
@csrf_exempt
def post_inbox(request: HttpRequest, author_id: str):
    #parse request body
    data = request.body
    try:
        data = json.loads(data)
    except Exception as e:
        return HttpResponse(content="expected json!",status=400)
    
    #receiver author object
    author: Author | None = Author.objects.all().filter(pk=author_id).first()

    if author is None:
        #author doesn't exist. cannot post to them.
        return HttpResponse(status=404)

    #parse inbox request
    url = parse_inbox(data, author)

    if not url:
        return HttpResponse(status=400)
    
    print("TEST: ",author,url)
    
    obj = Inbox.objects.create(author=author,url=url)

    obj.save()

    return HttpResponse(status=204)


# clear the inbox of author_id
def delete_inbox(request: HttpRequest, author_id: str):

    if not valid_requesting_user(request, author_id):
        return HttpResponse(status=401)

    author: Author | None = Author.objects.all().filter(pk=author_id).first()

    if author is None:
        return HttpResponse(status=404)

    Inbox.objects.filter(author=author).delete()

    return HttpResponse(status=204)

