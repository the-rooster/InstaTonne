from django.http import HttpRequest, HttpResponse
import json
from InstaTonneApis.models import Follow, FollowSerializer, Author, AuthorSerializer
from InstaTonneApis.endpoints.utils import valid_requesting_user, get_all_urls, get_author, check_auth_header, isaURL, get_auth_headers
from urllib.parse import quote
import requests
import re


# handle requests for the followers of an author
def single_author_followers(request: HttpRequest, author_id: str):
    if not check_auth_header(request):
        return HttpResponse(status=401)

    if isaURL(author_id) and request.method == "GET":
        return single_author_followers_get_remote(request, author_id)
    
    if isaURL(author_id):
        return HttpResponse(status=405)
    
    if request.method == "GET":
        return single_author_followers_get(request, author_id)  
    
    return HttpResponse(status=405)


# handle requests for a follower of an author
def single_author_follower(request: HttpRequest, author_id: str, foreign_author_id: str):
    if not check_auth_header(request):
        return HttpResponse(status=401)

    if isaURL(author_id) and request.method == "GET":
        return check_author_follower_remote(request, author_id, foreign_author_id)

    if isaURL(author_id):
        return HttpResponse(status=405)
    
    if request.method == "GET":
        return check_author_follower(request, author_id, foreign_author_id)
    
    if request.method == "POST":
        return post_author_follower(request, author_id, foreign_author_id)

    if request.method == "DELETE":
        return delete_author_follower(request, author_id, foreign_author_id)
    
    if request.method == "PUT":
        return put_author_follower(request, author_id, foreign_author_id)
    
    return HttpResponse(status=405)


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

    inbox_response: requests.Response = requests.post(foreign_author_id + '/inbox/', json.dumps(serialized_follow), headers=get_auth_headers(foreign_author_id))

    return HttpResponse(
        status=inbox_response.status_code,
        content_type=inbox_response.headers['Content-Type'],
        content=inbox_response.content.decode('utf-8')
    )


# get the followers of an author
def single_author_followers_get(request: HttpRequest, author_id: str):
    follows = Follow.objects.all().filter(object=author_id)

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
