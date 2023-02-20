from django.http import HttpRequest, HttpResponse
import json
from ..models import Follow, FollowSerializer, Author
from django.views.decorators.csrf import csrf_exempt

"""
endpoints for /authors/<id>/followers
"""
def single_author_followers(request: HttpRequest, id: int):
    if request.method == "GET":
        return single_author_followers_get(request,id)  
    elif request.method == "POST":
        return HttpResponse(status=405)
    return HttpResponse(status=405)


def single_author_followers_get(request,id: str):
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

"""
endpoints for /authors/<id>/followers/<foreign id>
"""
def author_follower_foreign(request : HttpRequest, id : str,foreign_id : str):

    if request.method == "DELETE":
        return delete_author_follower(request,id,foreign_id)
    elif request.method == "PUT":
        return put_author_follower(request,id,foreign_id)
    elif request.method == "GET":
        return check_author_follower(request,id,foreign_id)
    
    return HttpResponse(status=405)

def delete_author_follower(request : HttpRequest,id : str, foreign_id : str):

    follows = Follow.objects.all().filter(followeeAuthorId=id,followerAuthorId=foreign_id)

    if len(follows) != 1:
        return HttpResponse(status=404)
    
    follows.delete()

    return HttpResponse(status=204)

def put_author_follower(request : HttpRequest,id : str, foreign_id : str):

    if not request.user.is_authenticated:
        print("not authenticated. woopsies!")
        return HttpResponse(status=403)
    
    print(request.user.pk)
    if str(request.user.pk) != id:
        print("requesting someone thats not you. no bueno")
        return HttpResponse(status=403)
    
    if id == foreign_id:
        return HttpResponse(status=403)  
    
    print("wahooo")
    
    followee = Author.objects.filter(userID=id)

    follower = Author.objects.filter(userID=foreign_id)

    if len(followee) != 1:
        return HttpResponse(status=400,content="Author does not exist.")
    
    new_follow = Follow.objects.create(followeeAuthorId=followee[0],followerAuthorId=follower[0])

    new_follow.save()

    return HttpResponse(status=204)

def check_author_follower(request : HttpRequest,id : str, foreign_id : str):

    follows = Follow.objects.all().filter(followeeAuthorId=id,followerAuthorId=foreign_id)

    if len(follows) != 0:
        return HttpResponse(status=204)
    
    return HttpResponse(status=404)
