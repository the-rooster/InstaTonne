from django.http import HttpRequest, HttpResponse
from ..models import Author, Post, Request, Comment, Like, Inbox, PostSerializer, CommentSerializer, LikeSerializer, RequestSerializer
import json
import requests
from InstaTonne.settings import HOSTNAME
from django.views.decorators.csrf import csrf_exempt
from .utils import check_authenticated, get_author
import time
from threading import Thread, Lock

@csrf_exempt
def inbox_endpoint(request : HttpRequest, author_id : str):

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
    
    inbox_lock = Lock()
    threads : list[Thread] = []
    start = time.time()
    for item in inbox:

        print(item.url)
        try:
            def get_item(url : str):
                response : requests.Response = requests.get(url)
                print("STATUS: ",response.status_code)
                if response.status_code >= 200 and response.status_code < 300:
                    print(response.text)
                    inbox_lock.acquire()
                    result['items'] += [json.loads(response.text)]
                    inbox_lock.release()
            thr = Thread(target=get_item,args=(item.url,),daemon=True)
            thr.start()
            threads.append(thr)
        except Exception as e:
            print(e)
            print("requested server dead. oops")
            continue


    for thread in threads:
        thread.join()

    print("TIME: ",time.time() - start)
        
    print(result)
    return HttpResponse(content=json.dumps(result),status=200,content_type="application/json")

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
    
    if "id" not in data:
        return HttpResponse(content="expected id field!",status=400)
    
    #receiver author object
    author = Author.objects.filter(pk=id)

    if not author:
        #author doesn't exist. cannot post to them.
        return HttpResponse(status=404)
    #should only be 1 author so just 0 index
    author = author[0]


    if "type" not in data.keys():
        print('here')
        return HttpResponse(status=400)
    
    obj = Inbox.objects.create(author=author,url=data["id"])

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

