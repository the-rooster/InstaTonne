from django.http import HttpRequest, HttpResponse
import json
from ..models import Follow, FollowSerializer, Author, AuthorSerializer
from .utils import valid_requesting_user, get_all_urls, get_one_url, get_author, send_to_single_inbox, check_auth_header
from urllib.parse import unquote, quote
import re


def single_author_followers(request: HttpRequest):
    matched = re.search(r"^\/authors\/(.*?)\/followers\/?$", request.path)
    if matched:
        author_id: str = matched.group(1)
    else:
        return HttpResponse(status=405)

    if "/" in author_id and request.method == "GET":
        return single_author_followers_get_remote(request, author_id)
    elif "/" in author_id:
        return HttpResponse(status=405)
    elif request.method == "GET":
        return single_author_followers_get(request, author_id)  
    return HttpResponse(status=405)


def single_author_follower(request: HttpRequest):
    matched = re.search(r"^\/authors\/(.*?)\/followers\/(.*?)\/?$", request.path)
    if matched:
        author_id: str = matched.group(1)
        foreign_author_id: str = matched.group(2)
    else:
        return HttpResponse(status=405)

    #delete follower / follow request
    if request.method == "DELETE":
        return delete_author_follower(request, author_id, foreign_author_id)
    #accept follow request
    elif request.method == "PUT":
        return put_author_follower(request, author_id, foreign_author_id)
    #this endpoint is for checking if a local author is following a remote author.
    elif request.method == "GET" and "/" in author_id:
        print("GETTING REMOTE AUTHOR")
        return check_author_follower_remote(request,author_id,foreign_author_id)
    #return if foreign_author_id is a follower of author_id
    elif request.method == "GET":
        return check_author_follower(request, author_id, foreign_author_id)
    #if method is post, then foreign_author_id must be a url. we then make a follow request from author_id to foreign_author_id
    #author_id should be a local id, as this api endpoint is only for our local web interface
    elif request.method == "POST" and "/" in author_id:
        print("sending follow to inbox")
        return post_author_follower(request,author_id,foreign_author_id)
    return HttpResponse(status=405)

def post_author_follower(request: HttpRequest, author_id : str, foreign_author_id : str):

    print("USER ID",foreign_author_id)
    if not valid_requesting_user(request, foreign_author_id):
        print("invalid requesting user! post_author_follower")
        return HttpResponse(status=401)
    
    author = get_author(foreign_author_id)

    status, foreign_author = get_one_url(author_id)

    if status != 200:
        return HttpResponse(status=status)
    try:
        foreign_author_json = json.loads(foreign_author)
        summary = author.displayName + " wants to follow " + foreign_author_json["displayName"]
    except Exception as e:
        print("INCORRECT FOLLOW REQUEST FORMAT RECEIVED!")
        print(foreign_author)
        return HttpResponse(status=400,content="Incorrect follow request format received from foreign author url")
    

    #make follow request object
    request : dict = {
        "type" : "follow",
        "actor" : AuthorSerializer(author).data,
        "object" : foreign_author_json,
        "summary" : summary
    }


    print("SENDING FOLLOW REQUEST TO INBOX!")


    status = send_to_single_inbox(author_id,request)

    if status != 200:
        print("SENDING TO INBOX FAILED!")
        return HttpResponse(status=status)
    
    return HttpResponse(status=200)
# get the followers of an author
def single_author_followers_get(request: HttpRequest, author_id: str):

    if not check_auth_header(request):
        return HttpResponse(status=401)
    
    follows = Follow.objects.all().filter(object=author_id)

    urls = [item.follower_url for item in follows if item.accepted]
    serialized_data = get_all_urls(urls)

    res = json.dumps({
        "type": "followers",
        "items": serialized_data
    })

    return HttpResponse(content=res, content_type="application/json", status=200)


# get the followers of a remote author
def single_author_followers_get_remote(request: HttpRequest, author_id: str):
    remote_url = author_id + '/followers/'
    status_code, text = get_one_url(remote_url)
    return HttpResponse(status=status_code, content_type="application/json", content=text)


# remove the follow where foreign_author follows author
def delete_author_follower(request: HttpRequest, author_id: str, foreign_author_id: str):
    # if not valid_requesting_user(request, foreign_author_id):
    #     return HttpResponse(status=401)
    print(author_id,foreign_author_id)
    follows = Follow.objects.all().filter(object=author_id, follower_url=foreign_author_id)

    if len(follows) == 0:
        return HttpResponse(status=404)
    
    follows.delete()

    return HttpResponse(status=204)


# accept follow request
def put_author_follower(request: HttpRequest, author_id: str, foreign_author_id: str):

    if not valid_requesting_user(request, author_id):
        print("invalid requesting user!")
        return HttpResponse(status=401)
    
    if author_id == foreign_author_id:
        return HttpResponse(status=401)  
    
    user: Author | None = Author.objects.all().filter(id=author_id).first()
    
    print(foreign_author_id)
    if user is None:
        print("HERE!!!")
        return HttpResponse(status=404)
    print(user,foreign_author_id)
    follows = Follow.objects.all().filter(object=user,follower_url=foreign_author_id)
    print(follows)
    if not follows:
        print('wawaweewaa')
        return HttpResponse(content="no matching follow request",status=404)
    
    follow = follows[0]

    follow.accepted = True
    follow.save()

    return HttpResponse(status=204)


# return success if foreign_author follows author
def check_author_follower(request: HttpRequest, author_id: str, foreign_author_id: str):

    #check that request is authenticated. remote or local
    if not check_auth_header(request):
        return HttpResponse(status=401)
    
    user: Author | None = Author.objects.all().filter(pk=author_id).first()
    
    if user is None:
        return HttpResponse(status=404)
    
    print("FOREIGN AUTHOR: ",foreign_author_id)

    #if foreign author is local author return 404
    if user.id_url == foreign_author_id:
        return HttpResponse(status=200)
    
    follows = Follow.objects.all().filter(object=user, follower_url=foreign_author_id)

    if len(follows) == 0:
        return HttpResponse(status=404)
    
    follow = follows[0]

    if not follow.accepted:
        return HttpResponse(status=404)

    return HttpResponse(status=200)

#check if a local author is following a remote author. foreign_author_id in this case should be a local author
def check_author_follower_remote(request : HttpRequest, author_id : str, foreign_author_id : str):

    if not valid_requesting_user(request, foreign_author_id):
        print("invalid requesting user!")
        return HttpResponse(status=401)
    
    author = get_author(foreign_author_id)



    if not author:
        print("local author does not exist :(")
        return HttpResponse(status=404,content="Local author does not exist")
    

    follower_url = author_id + "/followers/" + quote(author.id_url)

    print("CHECKING IF ",foreign_author_id, " CAN FOLLOW ",author_id)

    status,_ = get_one_url(follower_url)

    print("GOT CODE: ",status)

    return HttpResponse(status=status)

#get the actual request object. this is for our local front end ONLY (for the inbox to retrieve follow requests)
def get_request_object(request: HttpRequest):

    print("GETTING REQUEST OBJECT")
    if request.method != "GET":
        return HttpResponse(status=405)

    matched = re.search(r"^\/authors\/(.*?)\/followers\/(.*?)\/request\/?$", request.path)
    print(request.path)
    if matched:
        author_id: str = matched.group(1)
        foreign_author_id: str = matched.group(2)
    else:
        print("id broken")
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
