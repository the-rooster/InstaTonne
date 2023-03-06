from django.http import HttpRequest, HttpResponse
from ..models import Author, Follow, Inbox
import json
import requests
from InstaTonne.settings import HOSTNAME
from django.views.decorators.csrf import csrf_exempt
from .utils import check_authenticated, get_author, get_all_urls
import time
from threading import Thread, Lock
from InstaTonne.settings import HOSTNAME
from urllib.parse import quote
import re

@csrf_exempt
def inbox_endpoint(request : HttpRequest):

    matched = re.search(r"^\/authors\/(.*?)\/inbox\/?$", request.path)
    if matched:
        author_id: str = matched.group(1)
    else:
        return HttpResponse(status=405)
    
    if request.method == "GET":
        return get_inbox(request,author_id)
    elif request.method == "POST":
        return post_inbox(request,author_id)
    elif request.method == "DELETE":
        return delete_inbox(request,author_id)
    
    return HttpResponse(status=405)

def get_inbox(request : HttpRequest, id : str):

    result = {
        "type" : "inbox",
        "author" : "http://" + request.get_host() + "/authors/" + str(id) + "/",
        "items" : []
    }
    
    # user = check_authenticated(request,id)
    user = get_author(id)
    if not user:
        return HttpResponse(status=403)
    

    inbox = Inbox.objects.filter(author=user)
    
    urls = [item.url for item in inbox]

    print(urls)

    result['items'] = get_all_urls(urls)
        
    print(result)
    return HttpResponse(content=json.dumps(result),status=200,content_type="application/json")

def parse_inbox_post(data : dict, user : Author):

    if "type" not in data:
        return None
    
    data_type = str(data["type"].lower())

    if data_type == "follow":
        return parse_inbox_follow_request(data,user)
    elif data_type == "post":
        return parse_inbox_post_post(data,user)
    elif data_type == "comment":
        return parse_inbox_comment(data,user)
    elif data_type == "like":
        return parse_inbox_like(data,user)


def parse_inbox_comment(data,user):

    
    pass

def parse_inbox_like(data,user):
    pass

def parse_inbox_post_post(data,user):

    if "id" not in data:
        return None
    
    obj = Inbox.objects.create(user=user,url=data["id"])

    obj.save()

    return data["id"]

def parse_inbox_follow_request(data : dict, user: Author):
        
        try:
            #parse expected fields in follow request here
            actor_id = data["actor"]["id"]
            summary = data["summary"]
        except Exception as e:
            print("INBOX FOLLOW REQUEST BROKEN!")
            print(e)
            return None

        obj = Follow.objects.create(object=user,follower_url=actor_id,accepted=False,summary=summary)

        obj.save()

        return HOSTNAME + "/authors/" + user.id + "/followers/" + quote(actor_id)
"""
Post an item to a users inbox!
"""
def post_inbox(request : HttpRequest, id : str):
    
    #parse request body
    data = request.body
    try:
        data = json.loads(data)
    except Exception as e:
        return HttpResponse(content="expected json!",status=400)
    

    
    #receiver author object
    author = Author.objects.filter(pk=id)

    if not author:
        #author doesn't exist. cannot post to them.
        return HttpResponse(status=404)
    #should only be 1 author so just 0 index
    author = author[0]

    #parse inbox request
    url = parse_inbox_post(data,author)

    if not url:
        return HttpResponse(status=400)
    
    obj = Inbox.objects.create(author=author,url=url)

    obj.save()

    return HttpResponse(status=200)

def delete_inbox(request : HttpRequest, id : str):

    # user = check_authenticated(request,id)
    user = get_author(id)

    if not user:
        print("test")
        return HttpResponse(status=403)


    
    #user is now authenticated
    #get all posts from followers

    
    #now clear the inbox
    print(id)
    res = Inbox.objects.filter(author=user).delete()
    print(res)
    return HttpResponse(status=200)

