from django.http import HttpRequest, HttpResponse
import json
from InstaTonneApis.models import Post, PostSerializer, Comment, Author, Follow, PostsResponseSerializer
from django.core.paginator import Paginator
from InstaTonneApis.endpoints.utils import make_comments_url, make_post_url, valid_requesting_user, send_to_inboxes, check_auth_header, isaURL, get_auth_headers, send_to_single_inbox, get_author, check_if_friends_local, check_if_friends_remote
import requests
import base64
from InstaTonne.settings import HOSTNAME
from InstaTonneApis.endpoints.permissions import CustomPermission

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions, serializers
from rest_framework.response import Response
from rest_framework.views import APIView


PNG_CONTENT_TYPE = "image/png;base64"
JPEG_CONTENT_TYPE = "image/jpeg;base64"


class SingleAuthorPostAPIView(APIView):
    #permission_classes = (permissions.AllowAny,CustomPermission,)
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        operation_description="get a post of author_id",
        operation_id="single_author_post_get",
        responses={200: PostSerializer(),},
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
            return single_author_post_get_remote(request, author_id, post_id)
        else:
            return single_author_post_get(request, author_id, post_id)

    @swagger_auto_schema(
        operation_description="update a post of author_id",
        operation_id="single_author_post_post",
        responses={204: 'success',},
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "title" : openapi.Schema(type=openapi.TYPE_STRING),
                "description" : openapi.Schema(type=openapi.TYPE_STRING),
                "contentType" : openapi.Schema(type=openapi.TYPE_STRING),
                "content" : openapi.Schema(type=openapi.TYPE_STRING),
                "visibility" : openapi.Schema(type=openapi.TYPE_STRING, example="PUBLIC"),
                "categories" : openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
                "unlisted" : openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
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
                description='ID of a post stored on this server',
                type=openapi.TYPE_STRING,
                default='1',
            ),
        ],
    )
    def post(self, request: HttpRequest, author_id: str, post_id: str):
        return single_author_post_post(request, author_id, post_id)

    @swagger_auto_schema(
        operation_description="remote a post of author_id",
        operation_id="single_author_post_delete",
        responses={204: 'success',},
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
        ],
    )
    def delete(self, request: HttpRequest, author_id: str, post_id: str):
        return single_author_post_delete(request, author_id, post_id)

    @swagger_auto_schema(
        operation_description="create a post of author_id",
        operation_id="single_author_post_put",
        responses={204: 'success',},
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "title" : openapi.Schema(type=openapi.TYPE_STRING),
                "source" : openapi.Schema(type=openapi.TYPE_STRING),
                "origin" : openapi.Schema(type=openapi.TYPE_STRING),
                "description" : openapi.Schema(type=openapi.TYPE_STRING),
                "contentType" : openapi.Schema(type=openapi.TYPE_STRING),
                "content" : openapi.Schema(type=openapi.TYPE_STRING),
                "visibility" : openapi.Schema(type=openapi.TYPE_STRING, example="PUBLIC"),
                "categories" : openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
                "unlisted" : openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
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
                description='ID of a post stored on this server',
                type=openapi.TYPE_STRING,
                default='1',
            ),
        ],
    )
    def put(self, request: HttpRequest, author_id: str, post_id: str):
        return single_author_post_put(request, author_id, post_id)


class SingleAuthorPostsAPIView(APIView):
    #permission_classes = (permissions.AllowAny,CustomPermission,)
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        operation_description="get the posts of author_id",
        responses={200: PostsResponseSerializer(),},
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
            return single_author_posts_get_remote(request, author_id)
        else:
            return single_author_posts_get(request, author_id)

    @swagger_auto_schema(
        operation_description="create a post as author_id",
        responses={204: 'success',},
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "title" : openapi.Schema(type=openapi.TYPE_STRING),
                "source" : openapi.Schema(type=openapi.TYPE_STRING),
                "origin" : openapi.Schema(type=openapi.TYPE_STRING),
                "description" : openapi.Schema(type=openapi.TYPE_STRING),
                "contentType" : openapi.Schema(type=openapi.TYPE_STRING),
                "content" : openapi.Schema(type=openapi.TYPE_STRING),
                "visibility" : openapi.Schema(type=openapi.TYPE_STRING, example="PUBLIC"),
                "categories" : openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
                "unlisted" : openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
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
        ],
    )
    def post(self, request: HttpRequest, author_id: str):
        return single_author_posts_post(request, author_id)


class SingleAuthorPostImageAPIView(APIView):
    #permission_classes = (permissions.AllowAny,CustomPermission,)
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        operation_description="get the image in a post of author_id",
        operation_id="single_author_post_image_get",
        responses={200: PostSerializer(),},
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
                default='3',
            ),
        ],
    )
    def get(self, request: HttpRequest, author_id: str, post_id: str):
        return single_author_post_image_get(request, author_id, post_id)


# get a the encoded image from a single post
def single_author_post_image_get(request: HttpRequest, author_id: str, post_id: str):
    post: Post | None = Post.objects.all().filter(pk=post_id).first()

    if post is None:
        return HttpResponse(status=404)

    serialized_post = PostSerializer(post).data

    if serialized_post["contentType"] != PNG_CONTENT_TYPE and serialized_post["contentType"] != JPEG_CONTENT_TYPE:
        return HttpResponse(status=404)

    res : str = serialized_post["content"]
    res = res.split(",")[-1]

    res_bytes = base64.decodebytes(res.encode("UTF-8"))

    return HttpResponse(content=res_bytes, content_type=serialized_post["contentType"], status=200)


# get a single post
def single_author_post_get(request: HttpRequest, author_id: str, post_id: str):
    post: Post | None = Post.objects.all().filter(author=author_id, pk=post_id).first()

    if post is None:
        return HttpResponse(status=404)
    
    requesting_author : Author | None = Author.objects.all().filter(userID=request.user.pk).first()

    if requesting_author and post.visibility == "FRIENDS" and not check_if_friends_local(post.author,requesting_author):
        print("HERE")
        print('DO NOT SHOW')
        return HttpResponse(status=401)

    serialized_post = PostSerializer(post).data
    comments_url = make_comments_url(HOSTNAME, author_id, post_id)
    comment_count = Comment.objects.all().filter(post=post_id).count()
    serialized_post["count"] = comment_count
    serialized_post["comments"] = comments_url

    res = json.dumps(serialized_post)
    return HttpResponse(content=res, content_type="application/json", status=200)


# get a single post of a remote author
def single_author_post_get_remote(request: HttpRequest, author_id: str, post_id: str):
    url = post_id
    response: requests.Response = requests.get(url, headers=get_auth_headers(url))

    requesting_author : Author | None = Author.objects.all().filter(userID=request.user.pk).first()
    post = json.loads(response.content)

    if "visibility" not in post:
        return HttpResponse(status=401)

    if requesting_author and post["visibility"] == "FRIENDS" and not check_if_friends_remote(requesting_author,post["author"]["id"]):
        print('DO NOT SHOW')
        return HttpResponse(status=401)
    
    
    return HttpResponse(
        status=response.status_code,
        content_type=response.headers['Content-Type'],
        content=response.content.decode('utf-8')
    )


# get all the posts of an author
def single_author_posts_get(request: HttpRequest, author_id: str):
    author: Author | None = Author.objects.all().filter(pk=author_id).first()
    if author is None:
        return HttpResponse(status=404)
    
    requesting_author : Author | None = Author.objects.all().filter(userID=request.user.pk).first()

    #check if this is a local author requesting. filter posts accordingly
    posts = Post.objects.all().filter(author=author_id, unlisted=False).order_by("published")

    page_num = request.GET.get("page")
    page_size = request.GET.get("size")

    if page_num is not None and page_size is not None:
        paginator = Paginator(posts, page_size)
        posts = paginator.get_page(page_num)

    serialized_data = []
    for post in posts:

        #check if this is a local author requesting. filter posts accordingly
        if requesting_author and post.visibility == "FRIENDS" and not check_if_friends_local(author,requesting_author):
            print('DO NOT SHOW')
            continue

        serialized_post = PostSerializer(post).data
        comments_url = make_comments_url(HOSTNAME, author_id, post.id)
        comment_count = Comment.objects.all().filter(post=post.id).count()
        serialized_post["count"] = comment_count
        serialized_post["comments"] = comments_url
        serialized_data.append(serialized_post)

    res = json.dumps({
        "type": "posts",
        "items": serialized_data
    })

    return HttpResponse(content=res, content_type="application/json", status=200)


# get all the posts of a remote author
def single_author_posts_get_remote(request: HttpRequest, author_id: str):
    requesting_author = Author.objects.filter(userID=request.user.pk).first()
    query = request.META.get('QUERY_STRING', '')
    if query: query = '?' + query
    url = author_id + '/posts' + query
    response: requests.Response = requests.get(url, headers=get_auth_headers(url))
    response_decoded = json.loads(response.content)

    print(requesting_author)
    def filter(post):
        if "visibility" not in post:
            return False
        return not requesting_author or (requesting_author and post["visibility"] == "FRIENDS" and check_if_friends_remote(requesting_author,author_id)) \
                or (requesting_author and post["visibility"] == "PUBLIC")

    if "items" not in response_decoded:
        print("NO ITEMS FIELD IN AUTHORS")
        return HttpResponse(status=404)
    
    response_decoded["items"] = [post for post in response_decoded["items"] if filter(post)]

    print(str([(x["title"],x["visibility"]) for x in response_decoded["items"]]))

    return HttpResponse(
        status=response.status_code,
        content_type=response.headers['Content-Type'],
        content=json.dumps(response_decoded))
    


# update an existing post
def single_author_post_post(request: HttpRequest, author_id: str, post_id: str):
    if not valid_requesting_user(request, author_id):
        return HttpResponse(status=401)

    try:
        post: Post | None = Post.objects.all().filter(author=author_id, pk=post_id).first()

        if post is None:
            return HttpResponse(status=404)
        

    
        body: dict = json.loads(request.data)

        if "title" in body:
            post.title = body["title"]
        if "description" in body:
            post.description = body["description"]
        if "contentType" in body:
            post.contentType = body["contentType"]
        if "content" in body:
            post.content = body["content"]
        if "visibility" in body:
            post.visibility = body["visibility"]
        if "categories" in body:
            post.categories = body["categories"]
        if "unlisted" in body:
            post.unlisted = body["unlisted"]
        post.save()

        return HttpResponse(status=204)
    except Exception as e:
        print(e)
        return HttpResponse(status=400)


# create a new post without a specified post id
def single_author_posts_post(request: HttpRequest, author_id: str):
    if not valid_requesting_user(request, author_id):
        return HttpResponse(status=401)

    try:
        author: Author | None = Author.objects.all().filter(pk=author_id).first()

        if author is None:
            return HttpResponse(status=404)
        
        body: dict = json.loads(request.data)
        #if were creating an image, create a seperate unlisted post with the image to link to
        if body["contentType"] == PNG_CONTENT_TYPE or body["contentType"] == JPEG_CONTENT_TYPE:
            print("CREATING UNLISTED IMAGE POST")
            uri = make_image_post(request,author,author_id)
            body["content"] = f"<img src=\"{uri}\">"
            body["contentType"] = "text/markdown"



        post: Post = Post.objects.create(
            type = "post",
            title = body["title"],
            description = body["description"],
            contentType = body["contentType"],
            content = body["content"],
            visibility = body["visibility"],
            categories = body["categories"],
            unlisted = body["unlisted"],
            author = author
        )
        post.id_url = make_post_url(HOSTNAME, author.id, post.id)
        post.origin = post.id_url if not body["origin"] else body["origin"]
        post.source = post.id_url if not body["source"] else body["source"]
        post.save()

        data : dict = {
            "type" : "post",
            "id" : post.id_url
        }
        send_to_inboxes(author_id, author.id_url, data, body["visibility"])
        send_to_single_inbox(HOSTNAME + "/authors/" + author_id,data)

        return HttpResponse(status=204)
    except Exception as e:
        print(e)
        print("HERE!")
        return HttpResponse(status=400)


#make image post to link to markdown post
def make_image_post(request : HttpRequest,author: Author,author_id : str):
    body: dict = json.loads(request.data)
    post: Post = Post.objects.create(
        type = "post",
        title = "image",
        description = "image",
        contentType = body["contentType"],
        content = body["content"],
        visibility = body["visibility"],
        categories = body["categories"],
        unlisted = True,
        author = author
    )
    post.id_url = make_post_url(HOSTNAME, author.id, post.id)
    post.origin = post.id_url if not body["origin"] else body["origin"]
    post.source = post.id_url if not body["source"] else body["source"]
    post.save()

    return post.id_url + "/image"


# delete a post
def single_author_post_delete(request: HttpRequest, author_id: str, post_id: str):
    if not valid_requesting_user(request, author_id):
        return HttpResponse(status=401)

    post: Post | None = Post.objects.all().filter(author=author_id, pk=post_id).first()

    if post is None:
        return HttpResponse(status=404)
    
    post.delete()

    return HttpResponse(status=204)


# create a new post with a specified post id
def single_author_post_put(request: HttpRequest, author_id: str, post_id: str):
    if not valid_requesting_user(request, author_id):
        return HttpResponse(status=401)

    try:
        author: Author | None = Author.objects.all().filter(pk=author_id).first()

        if author is None:
            return HttpResponse(status=404)
        
        existing_post: Post | None = Post.objects.all().filter(pk=post_id).first()

        if existing_post is not None:
            return single_author_post_post(request, author_id, post_id)
        
        body: dict = json.loads(request.data)
        post: Post = Post.objects.create(
            id = post_id,
            id_url = make_post_url(HOSTNAME, author_id, post_id),
            type = "post",
            title = body["title"],
            description = body["description"],
            contentType = body["contentType"],
            content = body["content"],
            visibility = body["visibility"],
            categories = body["categories"],
            unlisted = body["unlisted"],
            author = author
        )
        post.origin = post.id_url if not body["origin"] else body["origin"]
        post.source = post.id_url if not body["source"] else body["source"]
        post.save()

        data : dict = {
            "type" : "post",
            "id" : post.id_url
        }
        send_to_inboxes(author_id, author.id_url, data, body["visibility"])

        return HttpResponse(status=204)
    except Exception as e:
        print(e)
        return HttpResponse(status=400)
