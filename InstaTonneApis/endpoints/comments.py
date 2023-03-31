from django.http import HttpRequest, HttpResponse
import json
from ..models import Post, PostSerializer, Comment, Author, CommentSerializer, CommentsResponseSerializer, CommentResponseSerializer
from django.core.paginator import Paginator
from .utils import make_comment_url, make_comments_url, get_one_url, make_author_url, send_to_single_inbox, check_authenticated, check_auth_header, isaURL, get_auth_headers
import requests
import re
from InstaTonne.settings import HOSTNAME

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions, serializers
from rest_framework.response import Response
from rest_framework.views import APIView


class SingleAuthorPostCommentsAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        operation_description="Get the list of comments of the post whose id is post_id (paginated).",
        operation_id="single_post_comments_get",
        responses={200: CommentsResponseSerializer()},
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
            openapi.Parameter(
                'page',
                in_=openapi.IN_QUERY,
                description='page number',
                type=openapi.TYPE_INTEGER,
                default=1,
            ),
            openapi.Parameter(
                'size',
                in_=openapi.IN_QUERY,
                description='number of items per page',
                type=openapi.TYPE_INTEGER,
                default=1,
            ),
        ],
    )
    def get(self, request: HttpRequest, author_id: str, post_id: str):
        if isaURL(post_id):
            return single_post_comments_get_remote(request, author_id, post_id)
        else:
            return single_post_comments_get(request, author_id, post_id)
        
    @swagger_auto_schema(
        operation_description="Add a comment to the post whose id is post_id.",
        operation_id="single_post_comments_post",
        responses={204: 'success',},
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "comment": openapi.Schema(type=openapi.TYPE_STRING),
                "contentType": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
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
    def post(self, request: HttpRequest, author_id: str, post_id: str):
        if isaURL(post_id):
            return single_post_comments_post_remote(request,author_id,post_id)
        
        return single_post_comments_post(request, author_id, post_id)


class SingleAuthorPostCommentAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        operation_description="Get the comment whose id is comment_id.",
        operation_id="single_post_comment_get",
        responses={200: CommentResponseSerializer()},
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
        return get_single_comment_local(request, author_id, post_id, comment_id)


# get the comments from a post
def single_post_comments_get(request: HttpRequest, author_id: str, post_id: str):
    post: Post | None = Post.objects.all().filter(pk=post_id).first()

    if post is None:
        print("HERE3")
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
        url = comment.author

        try:
            response: requests.Response = requests.get(url, headers=get_auth_headers(url))
            serialized_comment["author"] = json.loads(response.content.decode('utf-8'))
            serialized_data.append(serialized_comment)
        except Exception as e:
            serialized_comment["author"] = {"error url": url}
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
        print("HERE?")
        return HttpResponse(status=401)
    
    try:
        print(request.data)
        body: dict = request.data
        print(body)
        comment: dict = {
            "type" : "comment",
            "contentType" : body["contentType"],
            "comment" : body["comment"],
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
        print("HERE",request.user.pk)
        return HttpResponse(status=401)
    
    post: Post | None = Post.objects.all().filter(pk=post_id).first()

    if post is None:
        print("HERE2",post_id)
        return HttpResponse(status=404)
    
    try:
        print(request.data)
        body: dict = request.data
        comment: dict = {
            "type" : "comment",
            "contentType" : body["contentType"],
            "comment" : body["comment"],
            "author" : author.id_url,
            "post" : post.id_url
        }

        author_inbox_url = make_author_url(HOSTNAME, author_id)

        status_code = send_to_single_inbox(author_inbox_url, comment)

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

    url = comment.author

    try:
        response: requests.Response = requests.get(url, headers=get_auth_headers(url))
        serialized_comment["author"] = json.loads(response.content.decode('utf-8'))
    except Exception as e:
        serialized_comment["author"] = {"error url": url}

    res = json.dumps(serialized_comment)

    return HttpResponse(content=res, content_type="application/json", status=200)
