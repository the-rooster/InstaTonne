from django.http import HttpRequest, HttpResponse
import json
from ..models import Post, Comment, Author, Like, LikeSerializer, LikesResponseSerializer, LikeResponseSerializer
from .utils import get_one_url, make_author_url, send_to_single_inbox, check_auth_header, get_auth_headers, isaURL
import requests
import re
from InstaTonne.settings import HOSTNAME
from adapters.adapters import adapter_get_remote_single_post, adapter_get_remote_posts, adapter_inbox_like
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions, serializers
from rest_framework.response import Response
from rest_framework.views import APIView


class SingleAuthorPostLikesAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        operation_description="Get the list of likes of the post whose id is post_id.",
        operation_id="single_post_likes_get",
        responses={200: LikesResponseSerializer()},
        manual_parameters=[
            openapi.Parameter(
                'author_id',
                in_=openapi.IN_PATH,
                description='ID of an author stored on this server',
                type=openapi.TYPE_STRING,
                default='1',
            ),
            openapi.Parameter(
                'post_id',
                in_=openapi.IN_PATH,
                description='- ID of a post stored on this server\n\nOR\n\n- URL to a post [FOR LOCAL USE]',
                type=openapi.TYPE_STRING,
                default='1',
            ),
        ],
    )
    def get(self, request: HttpRequest, author_id: str, post_id: str):
        if isaURL(post_id):
            return single_post_likes_get_remote(request, author_id, post_id)
        else:
            return single_post_likes_get(request, author_id, post_id)
        
    @swagger_auto_schema(
        operation_description="Add a like to the post whose id is post_id.",
        operation_id="single_post_likes_post",
        responses={204: 'success'},
        manual_parameters=[
            openapi.Parameter(
                'author_id',
                in_=openapi.IN_PATH,
                description='ID of an author stored on this server',
                type=openapi.TYPE_STRING,
                default='1',
            ),
            openapi.Parameter(
                'post_id',
                in_=openapi.IN_PATH,
                description='- ID of a post stored on this server\n\nOR\n\n- URL to a post [FOR LOCAL USE]',
                type=openapi.TYPE_STRING,
                default='1',
            ),
        ],
    )
    def post(self, request: HttpRequest, author_id : str, post_id: str):
        if isaURL(post_id):
            return single_post_likes_post_remote(request,author_id,post_id)
        return single_post_likes_post(request,author_id,post_id)


class SingleAuthorPostCommentLikesAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        operation_description="Get the list of likes of the comment whose id is comment_id.",
        operation_id="single_comment_likes_get",
        responses={200: LikesResponseSerializer()},
        manual_parameters=[
            openapi.Parameter(
                'author_id',
                in_=openapi.IN_PATH,
                description='ID of an author stored on this server',
                type=openapi.TYPE_STRING,
                default='1',
            ),
            openapi.Parameter(
                'post_id',
                in_=openapi.IN_PATH,
                description='ID of a post stored on this server',
                type=openapi.TYPE_STRING,
                default='1',
            ),
            openapi.Parameter(
                'comment_id',
                in_=openapi.IN_PATH,
                description='- ID of a comment stored on this server\n\nOR\n\n- URL to a comment [FOR LOCAL USE]',
                type=openapi.TYPE_STRING,
                default='1',
            ),
        ],
    )
    def get(self, request: HttpRequest, author_id: str, post_id: str, comment_id: str):
        if isaURL(comment_id):
            return single_comment_likes_get_remote(request, author_id, post_id, comment_id)
        else:
            return single_comment_likes_get(request, author_id, post_id, comment_id)
        
    @swagger_auto_schema(
        operation_description="Add a like to the comment whose id is comment_id.",
        operation_id="single_comment_likes_post",
        responses={204: 'success'},
        manual_parameters=[
            openapi.Parameter(
                'author_id',
                in_=openapi.IN_PATH,
                description='ID of an author stored on this server',
                type=openapi.TYPE_STRING,
                default='1',
            ),
            openapi.Parameter(
                'post_id',
                in_=openapi.IN_PATH,
                description='ID of a post stored on this server',
                type=openapi.TYPE_STRING,
                default='1',
            ),
            openapi.Parameter(
                'comment_id',
                in_=openapi.IN_PATH,
                description='- ID of a comment stored on this server\n\nOR\n\n- URL to a comment [FOR LOCAL USE]',
                type=openapi.TYPE_STRING,
                default='1',
            ),
        ],
    )
    def post(self,request: HttpRequest,author_id : str,post_id : str, comment_id: str):
        if isaURL(comment_id):
            return single_comment_likes_post_remote(request,author_id,post_id,comment_id)
        
        return single_comment_likes_post(request,author_id,post_id,comment_id)
        

class SingleAuthorLikesAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        operation_description="Get the list of likes of the author whose id is author_id.",
        operation_id="single_author_likes",
        responses={200: LikesResponseSerializer()},
        manual_parameters=[
            openapi.Parameter(
                'author_id',
                in_=openapi.IN_PATH,
                description='- ID of an author stored on this server\n\nOR\n\n- URL to an author [FOR LOCAL USE]',
                type=openapi.TYPE_STRING,
                default='1',
            ),
        ],
    )
    def get(self, request: HttpRequest, author_id: str):
        if isaURL(author_id):
            return single_author_likes_get_remote(request, author_id)
        else:
            return single_author_likes_get(request, author_id)
        

class SingleAuthorPostLikeAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        operation_description="Get the like whose id is like_id of the post whose id is post_id.",
        operation_id="single_post_like_get",
        responses={200: LikeResponseSerializer()},
        manual_parameters=[
            openapi.Parameter(
                'author_id',
                in_=openapi.IN_PATH,
                description='ID of an author stored on this server',
                type=openapi.TYPE_STRING,
                default='1',
            ),
            openapi.Parameter(
                'post_id',
                in_=openapi.IN_PATH,
                description='ID of a post stored on this server',
                type=openapi.TYPE_STRING,
                default='1',
            ),
            openapi.Parameter(
                'like_id',
                in_=openapi.IN_PATH,
                description='ID of a like stored on this server',
                type=openapi.TYPE_STRING,
                default='1',
            ),
        ],
    )
    def get(self, request: HttpRequest, author_id: str, post_id: str, like_id: str):
        return get_single_like_post_local(request, author_id, post_id, like_id)
    

class SingleAuthorPostCommentLikeAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        operation_description="Get the like whose id is like_id of the comment whose id is comment_id.",
        operation_id="single_comment_like_get",
        responses={200: LikeResponseSerializer()},
        manual_parameters=[
            openapi.Parameter(
                'author_id',
                in_=openapi.IN_PATH,
                description='ID of an author stored on this server',
                type=openapi.TYPE_STRING,
                default='1',
            ),
            openapi.Parameter(
                'post_id',
                in_=openapi.IN_PATH,
                description='ID of a post stored on this server',
                type=openapi.TYPE_STRING,
                default='1',
            ),
            openapi.Parameter(
                'comment_id',
                in_=openapi.IN_PATH,
                description='ID of a comment stored on this server',
                type=openapi.TYPE_STRING,
                default='1',
            ),
            openapi.Parameter(
                'like_id',
                in_=openapi.IN_PATH,
                description='ID of a like stored on this server',
                type=openapi.TYPE_STRING,
                default='1',
            ),
        ],
    )
    def get(self, request: HttpRequest, author_id: str, post_id: str, comment_id: str, like_id: str):
        return get_single_like_comment_local(request, author_id, post_id, comment_id, like_id)
        


# add a like to a remote post
def single_post_likes_post_remote(request : HttpRequest,author_id : str,post_id : str):
    author: Author | None = Author.objects.all().filter(userID=request.user.pk).first()
    
    if not author:
        return HttpResponse(status=401)
    
    try:
        like: dict = {
            "type" : "like",
            "author" : author.id_url,
            "object" : post_id,
            "summary" : "An author liked your post!"
        }

        like = adapter_inbox_like(like,post_id)

        status_code = send_to_single_inbox(post_id.split('/posts')[0], like)

        return HttpResponse(status=status_code)
    except Exception as e:
        print(e)
        print("ERROR IN SINGLE POST LIKES POST REMOTE")
        return HttpResponse(status=400)


# add a like to a post
def single_post_likes_post(request : HttpRequest,author_id : str,post_id : str):
    author: Author | None = Author.objects.all().filter(userID=request.user.pk).first()

    if not author:
        return HttpResponse(status=401)
    
    post: Post | None = Post.objects.all().filter(pk=post_id).first()

    if post is None:
        return HttpResponse(status=404)

    try:
        like: dict = {
            "type" : "like",
            "author" : author.id_url,
            "object" : post.id_url,
            "summary" : "An author liked your post!"
        }

        author_inbox_url = make_author_url(HOSTNAME, author_id)

        status_code = send_to_single_inbox(author_inbox_url, like)

        return HttpResponse(status=status_code)
    except Exception as e:
        print(e)
        return HttpResponse(status=400)


# add a like to a remote comment
def single_comment_likes_post_remote(request: HttpRequest, author_id: str, post_id: str, comment_id: str):
    author: Author | None = Author.objects.all().filter(userID=request.user.pk).first()
    
    if not author:
        return HttpResponse(status=401)
    
    try:
        like: dict = {
            "type" : "like",
            "author" : author.id_url,
            "object" : comment_id,
            "summary" : "An author liked your post!"
        }

        send_to_single_inbox(comment_id.split('/posts')[0], like)

        return HttpResponse(status=204)
    except Exception as e:
        print(e)
        return HttpResponse(status=400)


# add a like to a comment
def single_comment_likes_post(request: HttpRequest, author_id: str, post_id: str, comment_id: str):
    author: Author | None = Author.objects.all().filter(userID=request.user.pk).first()

    if not author:
        return HttpResponse(status=401)
    
    comment: Comment | None = Comment.objects.all().filter(pk=comment_id).first()

    if comment is None:
        return HttpResponse(status=404)
    
    try:
        like: dict = {
            "type" : "like",
            "author" : author.id_url,
            "object" : comment.id_url,
            "summary" : "An author liked your comment!"
        }

        author_inbox_url = make_author_url(HOSTNAME, author_id)

        status_code = send_to_single_inbox(author_inbox_url,like)

        return HttpResponse(status=status_code)
    except Exception as e:
        print(e)
        return HttpResponse(status=400)


# get the likes from a post
def single_post_likes_get(request: HttpRequest, author_id: str, post_id: str):
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


# get the likes from a remote post
def single_post_likes_get_remote(request: HttpRequest, author_id: str, post_id: str):
    url = post_id + '/likes'
    response: requests.Response = requests.get(url, headers=get_auth_headers(url))
    return HttpResponse(
        status=response.status_code,
        content_type=response.headers['Content-Type'],
        content=response.content.decode('utf-8')
    )


# get the likes from a comment
def single_comment_likes_get(request: HttpRequest, author_id: str, post_id: str, comment_id: str):
    comment = Comment.objects.all().filter(pk=comment_id).first()

    if comment is None:
        return HttpResponse(status=404)

    likes = Like.objects.all().filter(comment=comment_id).order_by("published")

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


# get the likes from a remote comment
def single_comment_likes_get_remote(request: HttpRequest, author_id: str, post_id: str, comment_id: str):
    url = comment_id + '/likes'
    response: requests.Response = requests.get(url, headers=get_auth_headers(url))
    return HttpResponse(
        status=response.status_code,
        content_type=response.headers['Content-Type'],
        content=response.content.decode('utf-8')
    )


# get the likes of an author on this server
def single_author_likes_get(request: HttpRequest, author_id: str):
    author: Author | None = Author.objects.all().filter(pk=author_id).first()

    if author is None:
        return HttpResponse(status=404)

    likes = Like.objects.all().filter(author=author.id_url).order_by("published")

    serialized_data = []
    for like in likes:
        serialized_like = LikeSerializer(like).data

        if like.post is not None:
            serialized_like["object"] = like.post.id_url
        if like.comment is not None:
            serialized_like["object"] = like.comment.id_url
        del serialized_like["post"]
        del serialized_like["comment"]

        serialized_data.append(serialized_like)

    res = json.dumps({
        "type": "likes",
        "items": serialized_data
    })

    return HttpResponse(content=res, content_type="application/json", status=200)


# get the likes of an author on a remote server
def single_author_likes_get_remote(request: HttpRequest, author_id: str):
    url = author_id + '/liked'
    response: requests.Response = requests.get(url, headers=get_auth_headers(url))
    return HttpResponse(
        status=response.status_code,
        content_type=response.headers['Content-Type'],
        content=response.content.decode('utf-8')
    )


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
