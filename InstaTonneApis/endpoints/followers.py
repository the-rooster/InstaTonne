from django.http import HttpRequest, HttpResponse
import json
from ..models import Follow, FollowSerializer


def single_author_followers(request: HttpRequest, id: int):
    if request.method == "GET":
        return single_author_followers_get(id)
    elif request.method == "POST":
        return HttpResponse(status=405)
    return HttpResponse(status=405)


def single_author_followers_get(id: int):
    follows = Follow.objects.all().filter(followeeAuthorId=id)

    serialized_data = []
    for follow in follows:
        serialized_follow = FollowSerializer(follow).data
        serialized_data.append(serialized_follow['followerAuthorId'])

    res = json.dumps([{
        "type": "followers",
        "items": serialized_data
    }])

    return HttpResponse(content=res, status=200)
