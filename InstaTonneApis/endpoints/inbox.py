from django.http import HttpRequest, HttpResponse
from ..models import Author, Follow, Inbox, Comment, Like, Post
import json
import requests
from InstaTonne.settings import HOSTNAME
from django.views.decorators.csrf import csrf_exempt
from .utils import check_authenticated, get_author, get_all_urls, check_auth_header
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
        return HttpResponse(status=401)
    

    inbox = Inbox.objects.filter(author=user)
    
    urls = [item.url for item in inbox]

    print(urls)

    result['items'] = get_all_urls(urls)
        
    print(result)
    return HttpResponse(content=json.dumps(result),status=200,content_type="application/json")

def parse_inbox_post(data : dict, user : Author):

    if "type" not in data:
        print("NO TYPE ON INBOX POST!")
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
    # comment: dict = {
    #     "type" : "comment",
    #     "contentType" : body["contentType"],
    #     "content" : body["comment"],
    #     "author" : make_author_url(request.get_host(), author.id),
    #     "post" : post_id
    # }

    #get post from post_id (get last non empty field after splitting on /)
    
    print("POST LINK",data["post"])
    post_local_id = [x for x in data["post"].split("/") if x][-1]

    #now get the post

    post = Post.objects.filter(id=post_local_id).first()

    if not post:
        print("POST WITH ID ",post_local_id, " DOES NOT EXIST")
        return None
    
    obj = Comment.objects.create(type="comment",id_url="",contentType=data["contentType"],comment=data["content"],author=data["author"],post=post)
    
    url = HOSTNAME + "/authors/" + user.id + "/posts/" + post_local_id + '/comments/' + obj.id
    obj.id_url = url
    
    obj.save()

    return url

def parse_inbox_like(data,user):
    print("Data: ", data)
    local_id = [x for x in data["object"].split("/") if x][-1]

    is_comment = "comments" in data["object"]
    print(local_id)

    #now get the post

    obj = None
    like = None

    #decide if local_id is post or comment
    post = True
    obj = Post.objects.filter(id=local_id).first()

    if obj and not is_comment:

        #determine if the author has already liked this post
        if not Like.objects.filter(post=obj,author=data["author"]):
            like = Like.objects.create(type="like",summary=data["summary"],author=data["author"],post=obj)
        else:
            print('yeehaw')
            return None

    elif not obj or is_comment:  
        #no post, try comments

        obj = Comment.objects.filter(id=local_id).first()
        post = False
        if obj:
            if not Like.objects.filter(comment=obj,author=data["author"]):
                like = Like.objects.create(type="like",summary=data["summary"],author=data["author"],comment=obj)
            else:
                print('yeesnaw')
                return None
    
    if not obj:
        print('yeespaw')
        return None
    
    like.save()

    url = ""

    if post:
        url = HOSTNAME + "/authors/" + user.id + "/posts/" + local_id + "/likes/" + like.id
    else:
        url = HOSTNAME + "/authors/" + user.id + "/posts/" + obj.post.id + "/comments/" + obj.id + "/likes/" + like.id
    like.id_url = url
    
    like.save()

    return url

def parse_inbox_post_post(data,user):

    print("INBOX POST SENT: ",data)
    if "id" not in data:
        print('yahoo')
        return None
    

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

        return HOSTNAME + "/authors/" + user.id + "/followers/" + quote(actor_id) + "/request"
"""
Post an item to a users inbox!
"""
def post_inbox(request : HttpRequest, id : str):

    #check that request is authenticated. remote or local
    if not check_auth_header(request):
        return HttpResponse(status=401)
    
    #parse request body
    data = request.body
    try:
        data = json.loads(data)
        print("INBOX POST DATA: ",data)
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
        print('here')
        return HttpResponse(status=400)
    
    obj = Inbox.objects.create(author=author,url=url)

    obj.save()

    return HttpResponse(status=200)

def delete_inbox(request : HttpRequest, id : str):

    # user = check_authenticated(request,id)
    user = get_author(id)

    if not user:
        print("test")
        return HttpResponse(status=401)


    
    #user is now authenticated
    #get all posts from followers

    
    #now clear the inbox
    print(id)
    res = Inbox.objects.filter(author=user).delete()
    print(res)
    return HttpResponse(status=200)

