from django.http import HttpRequest, HttpResponse
from ..models import Author, Follow, Inbox, Comment, Like, Post, LikeSerializer, InboxSerializer, InboxResponseSerializer, GInboxSerializer, GInboxResponseSerializer
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

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

class InboxAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        operation_description="get the inbox of author_id",
        operation_id="inbox_get",
        responses={200: InboxResponseSerializer(),},
        manual_parameters=[
            openapi.Parameter(
                'author_id',
                in_=openapi.IN_PATH,
                description='author id',
                type=openapi.TYPE_STRING,
                default='1',
            ),
        ],
    )
    def get(self, request: HttpRequest, author_id: str):
        return get_inbox(request, author_id)

    @swagger_auto_schema(
        operation_description='''
        add item to inbox of author_id\n
        When adding a post, the body should contain at least:\n
            - type: 'post'\n
            - id: <url to the post>\n
        When adding a like, the body should contain at least:\n
            - summary: <summary of the like>\n
            - type: 'like'\n
            - author: <url to the author making the like>\n
            - object: <url to the comment or post being liked>\n
        When adding a comment, the body should contain at least:\n
            - type: 'comment'\n
            - contentType: <contentType of the comment>\n
            - content: <content of the comment>\n
            - author: <url to the author making the comment>\n
            - post: <url to the post being commented on>\n
        When adding a follow, the body should contain at least:\n
            - type: 'follow'\n
            - summary: <summary of the follow>\n
            - actor: { id: <url to the author making the follow request> }\n
        ''',
        operation_id="inbox_post",
        responses={204: 'success',},             
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "type": openapi.Schema(type=openapi.TYPE_STRING, example="post"),
                "id": openapi.Schema(type=openapi.TYPE_STRING, example="http://127.0.0.1:8000/authors/1/posts/1"),
            },
        ),
        manual_parameters=[
            openapi.Parameter(
                'author_id',
                in_=openapi.IN_PATH,
                description='author id',
                type=openapi.TYPE_STRING,
                default='1',
            ),
        ],
    )
    def post(self, request: HttpRequest, author_id: str):
        return post_inbox(request, author_id)

    @swagger_auto_schema(
        operation_description="clear the inbox of author_id",
        operation_id="inbox_delete",
        responses={204: 'success',},
        manual_parameters=[
            openapi.Parameter(
                'author_id',
                in_=openapi.IN_PATH,
                description='author id',
                type=openapi.TYPE_STRING,
                default='1',
            ),
        ],
    )
    def delete(self, request: HttpRequest, author_id: str):
        return delete_inbox(request, author_id)
    

class GInboxAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        operation_description="get the inbox of author_id with github data",
        operation_id="ginbox_get",
        responses={200: GInboxResponseSerializer(),},
        manual_parameters=[
            openapi.Parameter(
                'author_id',
                in_=openapi.IN_PATH,
                description='author id',
                type=openapi.TYPE_STRING,
                default='1',
            ),
        ],
    )
    def get(self, request: HttpRequest, author_id: str):
        return get_ginbox(request, author_id)


# get the items in an authors inbox
def get_ginbox(request: HttpRequest, author_id: str):
    author: Author | None = Author.objects.all().filter(pk=author_id).first()

    if author is None:
        return HttpResponse(status=404)

    inboxes = Inbox.objects.all().filter(author=author.id).order_by('published')

    github_url = author.id_url + '/github'
    github_response: requests.Response = requests.get(github_url, headers=get_auth_headers(github_url))
    if github_response.status_code != 200:
        github_data = []
        print('ERROR:', github_response.status_code)
    else:
        github_data = github_response.json()
        #print('SUCCESS:', github_data)

    serialized_data = []
    for inbox in inboxes:
        try:
            response: requests.Response = requests.get(inbox.url, headers=get_auth_headers(inbox.url))

            if response.status_code == 204:
                response_data = {"found url": inbox.url}
            elif response.status_code != 200:
                response_data = {"error url": inbox.url}
            else:
                response_data = response.json()

            response_data['created_at'] = inbox.published.strftime("%Y-%m-%dT%H:%M:%SZ")
            serialized_data.append(response_data)
        except Exception as e:
            print('ERROR:', e)

    #print('SERIAL', serialized_data)
    all_data = serialized_data + github_data
    all_data.sort(key=lambda x: x['created_at'], reverse=True)

    res = json.dumps({
        "type" : "ginbox",
        "author" : author.id_url,
        "items" : all_data
    })
        
    return HttpResponse(content=res, status=200, content_type="application/json")


# get the items in an authors inbox
def get_inbox(request: HttpRequest, author_id: str):
    author: Author | None = Author.objects.all().filter(pk=author_id).first()

    if author is None:
        return HttpResponse(status=404)

    inboxes = Inbox.objects.all().filter(author=author.id).order_by('published')

    urls = set()
    result = []
    #get only results with a unique url
    for inbox in inboxes:
        if inbox.url in urls:
            continue
        urls.add(inbox.url)
        result.append(inbox)

    serialized_data = []
    for inbox in result:
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
    
    #check that all fields are present
    if "summary" not in data:
        print('ERROR: no summary field in body')
        return None
    if "author" not in data:
        print('ERROR: no author field in body')
        return None
    

    comment: Comment | None = Comment.objects.all().filter(id_url=object_url).first()
    post: Post | None = Post.objects.all().filter(id_url=object_url).first()

    if comment is not None:

        if Like.objects.all().filter(comment=comment,author=data["author"]).count() > 0:
            print('ERROR: already liked')
            return None
        like = Like.objects.create(type="like", comment=comment, post=None)
    elif post is not None:

        if Like.objects.all().filter(post=post,author=data["author"]).count() > 0:
            print('ERROR: already liked')
            return None

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
    
    if Follow.objects.all().filter(follower_url=actor_id, object=user).exists():
        print("FOLLOW REQUEST ALREADY EXISTS!")
        return None

    obj = Follow.objects.create(object=user,follower_url=actor_id,accepted=False,summary=summary)

    obj.save()

    return HOSTNAME + "/authors/" + user.id + "/followers/" + quote(actor_id, safe='').replace('.', '%2E') + "/request"


# add a post to an inbox
@csrf_exempt
def post_inbox(request: HttpRequest, author_id: str):
    #parse request body
    try:
        data = request.data
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

