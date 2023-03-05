from django.http import HttpRequest, HttpResponse
import json
from ..models import Follow, FollowSerializer, Author
from .utils import valid_requesting_user, get_all_urls
from urllib.parse import unquote

# endpoints for /authors/<author_id>/followers
def single_author_followers(request: HttpRequest, author_id: str):
    if request.method == "GET":
        return single_author_followers_get(request, author_id)  
    return HttpResponse(status=405)


# get the followers of an author
def single_author_followers_get(request: HttpRequest, author_id: str):
    follows = Follow.objects.all().filter(object=author_id)

    urls = [item.follower_url for item in follows if item.accepted]
    serialized_data = get_all_urls(urls)

    res = json.dumps([{
        "type": "followers",
        "items": serialized_data
    }])

    return HttpResponse(content=res, status=200)


# endpoints for /authors/<author_id>/followers/<foreign_author_id>
def single_author_follower(request: HttpRequest):
    #parse author_id and foreign_author_id from request url since we gotta use re_path here
    author_id: str = request.get_full_path().split("/")[2]
    foreign_author_id: str = "/".join(request.get_full_path().split("/")[4:])

    print("AUTHOR_ID : ",author_id)
    print("FOREIGN AUTHOR ID: ",foreign_author_id)

    #remove urlencoding on foreign_author_id
    foreign_author_id = unquote(foreign_author_id)

    if request.method == "DELETE":
        return delete_author_follower(request, author_id, foreign_author_id)
    elif request.method == "PUT":
        return put_author_follower(request, author_id, foreign_author_id)
    elif request.method == "GET":
        return check_author_follower(request, author_id, foreign_author_id)
    return HttpResponse(status=405)


# remove the follow where foreign_author follows author
def delete_author_follower(request: HttpRequest, author_id: str, foreign_author_id: str):
    # if not valid_requesting_user(request, foreign_author_id):
    #     return HttpResponse(status=403)
    print(author_id,foreign_author_id)
    follows = Follow.objects.all().filter(object=author_id, follower_url=foreign_author_id)

    if len(follows) == 0:
        return HttpResponse(status=404)
    
    follows.delete()

    return HttpResponse(status=204)


# accept follow request
def put_author_follower(request: HttpRequest, author_id: str, foreign_author_id: str):

    if not valid_requesting_user(request, foreign_author_id):
        return HttpResponse(status=403)
    
    if author_id == foreign_author_id:
        return HttpResponse(status=403)  
    
    user: Author | None = Author.objects.all().filter(pk=author_id).first()
    
    print(foreign_author_id)
    if user is None:
        return HttpResponse(status=404)
    print(user,foreign_author_id)
    follows = Follow.objects.all().filter(object=user,follower_url=foreign_author_id)
    print(follows)
    if not follows:
        return HttpResponse(content="no matching follow request",status=404)
    
    follow = follows[0]

    follow.accepted = True
    follow.save()

    return HttpResponse(status=204)


# return success if foreign_author follows author
def check_author_follower(request: HttpRequest, author_id: str, foreign_author_id: str):
    
    user: Author | None = Author.objects.all().filter(pk=author_id).first()
    


    if user is None:
        print('test')
        return HttpResponse(status=404)
    
    print(foreign_author_id)
    
    follows = Follow.objects.all().filter(object=user, follower_url=foreign_author_id)

    if len(follows) == 0:
        print('here!!!')
        return HttpResponse(status=404)
    
    follow = follows[0]

    serialized_follow = FollowSerializer(follow).data

    urls = [item.follower_url for item in follows]
    serialized_data = get_all_urls(urls)[0]

    serialized_follow['actor'] = serialized_data
    serialized_follow['type'] = 'Follow'

    print("SERIALIZED FOLLOW: ",serialized_follow)

    return HttpResponse(content = json.dumps(serialized_follow),status=200,content_type="application/json")
