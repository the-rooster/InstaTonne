from django.http import HttpRequest, HttpResponse
import json
from InstaTonneApis.models import Follow, FollowSerializer, Author, AuthorSerializer, FollowersResponseSerializer
from InstaTonneApis.endpoints.utils import valid_requesting_user, get_all_urls, get_author, check_auth_header, isaURL, get_auth_headers
from urllib.parse import quote
import requests
from InstaTonneApis.endpoints.permissions import CustomPermission
from InstaTonne.settings import HOSTNAME

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from ..adapters.adapters import adapter_inbox_follow


class SingleAuthorFollowersAPIView(APIView):
    #permission_classes = (permissions.AllowAny,CustomPermission,)
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        operation_description="Get a list of authors who are AUTHOR_ID's followers.",
        responses={200: FollowersResponseSerializer(),},
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
            return single_author_followers_get_remote(request, author_id)
        else:
            return single_author_followers_get(request, author_id)


class SingleAuthorFollowerAPIView(APIView):
    #permission_classes = (permissions.AllowAny,CustomPermission,)
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        operation_description="Check if foreign_author_id is following author_id.",
        responses={204: 'success',},
        manual_parameters=[
            openapi.Parameter(
                'author_id',
                in_=openapi.IN_PATH,
                description='- ID of an author stored on this server\n\nOR\n\n- URL to an author [FOR LOCAL USE]',
                type=openapi.TYPE_STRING,
                default='1',
            ),
            openapi.Parameter(
                'foreign_author_id',
                in_=openapi.IN_PATH,
                description='a URL to an author',
                type=openapi.TYPE_STRING,
                default=HOSTNAME + '/authors/2',
            ),
        ],
    )
    def get(self, request: HttpRequest, author_id: str, foreign_author_id: str):
        if isaURL(author_id):
            return check_author_follower_remote(request, author_id, foreign_author_id)
        else:
            return check_author_follower(request, author_id, foreign_author_id)
        
    @swagger_auto_schema(
        operation_description="Send a follow request to foreign_author_id from author_id.",
        responses={204: 'success',},
        manual_parameters=[
            openapi.Parameter(
                'author_id',
                in_=openapi.IN_PATH,
                description='ID of an author stored on this server',
                type=openapi.TYPE_STRING,
                default='2',
            ),
            openapi.Parameter(
                'foreign_author_id',
                in_=openapi.IN_PATH,
                description='a URL to an author',
                type=openapi.TYPE_STRING,
                default=HOSTNAME + '/authors/1',
            ),
        ],
    )
    def post(self, request: HttpRequest, author_id: str, foreign_author_id: str):
        return post_author_follower(request, author_id, foreign_author_id)

    @swagger_auto_schema(
        operation_description="Remove foreign_author_id as a follower of author_id.",
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
                'foreign_author_id',
                in_=openapi.IN_PATH,
                description='a URL to an author',
                type=openapi.TYPE_STRING,
                default=HOSTNAME + '/authors/2',
            ),
        ],
    )
    def delete(self, request: HttpRequest, author_id: str, foreign_author_id: str):
        return delete_author_follower(request, author_id, foreign_author_id)

    @swagger_auto_schema(
        operation_description="Accept a follow request from foreign_author_id as author_id.",
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
                'foreign_author_id',
                in_=openapi.IN_PATH,
                description='a URL to an author',
                type=openapi.TYPE_STRING,
                default=HOSTNAME + '/authors/2',
            ),
        ],
    )
    def put(self, request: HttpRequest, author_id: str, foreign_author_id: str):
        return put_author_follower(request, author_id, foreign_author_id)


# author_id makes follow request to foreign_author_id
def post_author_follower(request: HttpRequest, author_id : str, foreign_author_id : str):
    if not valid_requesting_user(request, author_id):
        return HttpResponse(status=401)
    
    author: Author | None = Author.objects.all().filter(pk=author_id).first()

    if author is None:
        return HttpResponse(status=404)
    
    author_response: requests.Response = requests.get(foreign_author_id, headers=get_auth_headers(foreign_author_id))

    if author_response.status_code != 200:
        return HttpResponse(
            status=author_response.status_code,
            content_type=author_response.headers['Content-Type'],
            content=author_response.content.decode('utf-8')
        )
    
    serialized_follow = {
        "type": "follow",
        "actor": AuthorSerializer(author).data,
        "object": author_response.json(),
        "summary": author.displayName + " wants to follow " + author_response.json()["displayName"]
    }

    serialized_follow = adapter_inbox_follow(serialized_follow, foreign_author_id)

    headers = get_auth_headers(foreign_author_id)

    headers["Content-Type"] = "application/json"

    inbox_response: requests.Response = requests.post(foreign_author_id + '/inbox/', json.dumps(serialized_follow), headers=headers)
    
    # if content type is not set, it will be set to text/html
    if 'Content-Type' not in inbox_response.headers:
        inbox_response.headers['Content-Type'] = 'application/json'

    return HttpResponse(
        status=inbox_response.status_code,
        content_type=inbox_response.headers['Content-Type'],
        content=inbox_response.content.decode('utf-8')
    )


# get the followers of an author
def single_author_followers_get(request: HttpRequest, author_id: str):
    follows = Follow.objects.all().filter(object=author_id, accepted=True)

    serialized_data = []
    for follow in follows:
        try:
            response: requests.Response = requests.get(follow.follower_url, headers=get_auth_headers(follow.follower_url))
            serialized_data.append(response.json())
        except Exception as e:
            serialized_data.append({"error url": follow.follower_url})

    res = json.dumps({
        "type": "followers",
        "items": serialized_data
    })

    return HttpResponse(content=res, content_type="application/json", status=200)


# get the followers of a remote author
def single_author_followers_get_remote(request: HttpRequest, author_id: str):
    url = author_id + '/followers'
    response: requests.Response = requests.get(url, headers=get_auth_headers(url))
    return HttpResponse(
        status=response.status_code,
        content_type=response.headers['Content-Type'],
        content=response.content.decode('utf-8')
    )


# delete the follow where foreign_author_id follows author_id
def delete_author_follower(request: HttpRequest, author_id: str, foreign_author_id: str):
    if not valid_requesting_user(request, author_id):
        return HttpResponse(status=401)

    follow: Follow | None = Follow.objects.all().filter(object=author_id, follower_url=foreign_author_id).first()

    if follow is None:
        return HttpResponse(status=404)
    
    follow.delete()

    return HttpResponse(status=204)


# author_id accepts follow request from foreign_author_id
def put_author_follower(request: HttpRequest, author_id: str, foreign_author_id: str):
    if not valid_requesting_user(request, author_id):
        return HttpResponse(status=401)
    
    author: Author | None = Author.objects.all().filter(pk=author_id).first()

    if author is None:
        return HttpResponse(status=404)
    
    follow: Follow | None = Follow.objects.all().filter(object=author, follower_url=foreign_author_id).first()

    if follow is None:
        return HttpResponse(status=404)

    follow.accepted = True
    follow.save()

    return HttpResponse(status=204)


# return success if foreign_author_id follows author_id
def check_author_follower(request: HttpRequest, author_id: str, foreign_author_id: str):
    author: Author | None = Author.objects.all().filter(pk=author_id).first()
    
    if author is None:
        return HttpResponse(status=404)
    
    follow: Follow | None = Follow.objects.all().filter(object=author, follower_url=foreign_author_id).first()

    if follow is None:
        return HttpResponse(status=404)

    if not follow.accepted:
        return HttpResponse(status=404)

    return HttpResponse(status=204)


# return success if foreign_author_id follows remote author_id
def check_author_follower_remote(request : HttpRequest, author_id : str, foreign_author_id : str):
    url = author_id + '/followers/' + quote(foreign_author_id, safe='').replace('.', '%2E')
    response: requests.Response = requests.get(url, headers=get_auth_headers(url))
    return HttpResponse(
        status=response.status_code,
        content_type=response.headers['Content-Type'],
        content=response.content.decode('utf-8')
    )


#get the actual request object. this is for our local front end ONLY (for the inbox to retrieve follow requests)
def get_request_object(request: HttpRequest, author_id: str, foreign_author_id: str):
    # if not check_auth_header(request):
    #     return HttpResponse(status=401)

    print("GETTING REQUEST OBJECT")
    if request.method != "GET":
        print('yahoo?')
        return HttpResponse(status=405)
    
    user: Author | None = get_author(author_id)
    
    if user is None:
        return HttpResponse(status=404)
    
    print(foreign_author_id)
    
    follows = Follow.objects.all().filter(object=user, follower_url=foreign_author_id)

    if len(follows) == 0:
        return HttpResponse(status=404)
    
    follow = follows[0]

    serialized_follow = FollowSerializer(follow).data

    urls = [item.follower_url for item in follows]
    serialized_data = get_all_urls(urls)[0]

    serialized_follow['actor'] = serialized_data
    serialized_follow['type'] = 'Follow'

    return HttpResponse(content = json.dumps(serialized_follow),status=200,content_type="application/json")
