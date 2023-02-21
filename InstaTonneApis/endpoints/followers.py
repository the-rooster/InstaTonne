from django.http import HttpRequest, HttpResponse
import json
from ..models import Follow, FollowSerializer, Author
from .utils import valid_requesting_user


# endpoints for /authors/<author_id>/followers
def single_author_followers(request: HttpRequest, author_id: int):
    if request.method == "GET":
        return single_author_followers_get(request, author_id)  
    elif request.method == "POST":
        return HttpResponse(status=405)
    return HttpResponse(status=405)


# get the followers of an author
def single_author_followers_get(request: HttpRequest, author_id: int):
    follows = Follow.objects.all().filter(followeeAuthorId=author_id)

    serialized_data = []
    for follow in follows:
        serialized_follow = FollowSerializer(follow).data
        serialized_data.append(serialized_follow['followerAuthorId'])

    res = json.dumps([{
        "type": "followers",
        "items": serialized_data
    }])

    return HttpResponse(content=res, status=200)


# endpoints for /authors/<author_id>/followers/<foreign_author_id>
def single_author_follower(request: HttpRequest, author_id: int, foreign_author_id: int):
    if request.method == "DELETE":
        return delete_author_follower(request, author_id, foreign_author_id)
    elif request.method == "PUT":
        return put_author_follower(request, author_id, foreign_author_id)
    elif request.method == "GET":
        return check_author_follower(request, author_id, foreign_author_id)
    return HttpResponse(status=405)


# remove the follow where foreign_author follows author
def delete_author_follower(request: HttpRequest, author_id: int, foreign_author_id: int):
    if not valid_requesting_user(request, foreign_author_id):
        return HttpResponse(status=403)

    follows = Follow.objects.all().filter(followeeAuthorId=author_id, followerAuthorId=foreign_author_id)

    if len(follows) == 0:
        return HttpResponse(status=404)
    
    follows.delete()

    return HttpResponse(status=204)


# create a follow where foreign_author follows author
def put_author_follower(request: HttpRequest, author_id: int, foreign_author_id: int):
    if not valid_requesting_user(request, foreign_author_id):
        return HttpResponse(status=403)
    
    if author_id == foreign_author_id:
        return HttpResponse(status=403)  
    
    followee: Author | None = Author.objects.all().filter(pk=author_id).first()
    follower: Author | None = Author.objects.all().filter(pk=foreign_author_id).first()

    if followee is None or follower is None:
        return HttpResponse(status=404)
    
    follows = Follow.objects.all().filter(followeeAuthorId=author_id, followerAuthorId=foreign_author_id)

    if len(follows) != 0:
        return HttpResponse(status=403)
    
    Follow.objects.create(followeeAuthorId=followee, followerAuthorId=follower)

    return HttpResponse(status=204)


# return success if foreign_author follows author
def check_author_follower(request: HttpRequest, author_id: int, foreign_author_id: int):
    follows = Follow.objects.all().filter(followeeAuthorId=author_id, followerAuthorId=foreign_author_id)

    if len(follows) != 0:
        return HttpResponse(status=204)
    
    return HttpResponse(status=404)
