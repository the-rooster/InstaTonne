from django.http import HttpRequest, HttpResponse
from InstaTonne.settings import GITHUB_TOKEN
from ..models import Author, GithubResponseSerializer
import requests

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.views import APIView


class GithubAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        operation_description="get the github activity of author_id\nurl to the full docs: https://docs.github.com/en/rest/activity/events?apiVersion=2022-11-28#list-events-for-the-authenticated-user",
        operation_id="github_get",
        responses={200: GithubResponseSerializer(),},
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
        return get_github(request, author_id)


def get_github(request: HttpRequest, author_id: str):

    author = Author.objects.filter(pk=author_id).first()

    if not author:
        return HttpResponse(status=404)

    
    url = 'https://api.github.com/users/' + author.github.strip('/').split('/')[-1] + '/events'
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": "Bearer " + GITHUB_TOKEN,
        "X-GitHub-Api-Version": "2022-11-28",
    }

    response: requests.Response = requests.get(url, headers=headers)

    return HttpResponse(
        status=response.status_code,
        content_type=response.headers['Content-Type'],
        content=response.content.decode('utf-8')
    )
