from django.http import HttpRequest, HttpResponse
from django.middleware.csrf import CsrfViewMiddleware
from ..models import Author, Follow, FollowSerializer, ConnectedServer
from threading import Thread, Lock
import json
import requests
from typing import Tuple
import urllib.parse
from InstaTonne.settings import HOSTNAME, FRONTEND
from urllib.parse import quote
import copy

PUBLIC = "PUBLIC"
PRIVATE = "FRIENDS"


def get_all_urls(urls: list[str]):
    inbox_lock = Lock()
    threads : list[Thread] = []
    result = []
    for url in urls:

        print(url)

        def get_item(url : str):

            #check if we can make a request to this url
            if not can_send_request(url):
                inbox_lock.acquire()
                result.append({"error" : "url not connected to this server"})
                inbox_lock.release()
                return
            try:
                response : requests.Response = requests.get(url,headers={"Origin":HOSTNAME,
                                                                         "Authentication" : get_auth_header_for_server(url)})
                print("STATUS: ",response.status_code)
                if response.status_code >= 200 and response.status_code < 300:
                    print(response.text)
                    inbox_lock.acquire()
                    print(response.text)
                    result.append(json.loads(response.text))
                    inbox_lock.release()
            except Exception as e:
                print("REQUEST ERROR: ",e)
                inbox_lock.acquire()
                result.append({"error" : "url down"})
                inbox_lock.release()
        thr = Thread(target=get_item,args=(url,),daemon=True)

        thr.start()
        threads.append(thr)

    for thread in threads:
        thread.join()
    
    return result


def get_one_url(url: str) -> Tuple[int, str, str|None]:

    # check if requested hostname in valid hosts here
    if not can_send_request(url):
        print("NOT IN LIST OF ACCEPTED SERVERS")
        return (401, str("NOT IN LIST OF ACCEPTED SERVERS"), None)
    
    try:
        response: requests.Response = requests.get(url,headers={"Origin":HOSTNAME,
                                                                "Authentication" : get_auth_header_for_server(url)})
        
        return (response.status_code, response.text, response.headers['Content-Type'])
    except Exception as e:
        print("ERROR GETTING URL: ",e)
        return (410, str(e), None)


def send_to_single_inbox(author_url : str, data : dict):

    # check if requested hostname in valid hosts here
    if not can_send_request(author_url):
        return (401,str("NOT IN LIST OF ACCEPTED SERVERS"))
    
    inbox_url: str = author_url + '/inbox/'
    try:
        response: requests.Response = requests.post(inbox_url,
                                                    json.dumps(data),headers={"Origin" : HOSTNAME, 
                                                                            "Authentication" : get_auth_header_for_server(author_url)})
    except Exception as e:
        print(e)
        print("SERVER DOWN! Returning 404")
        return 404
    return response.status_code

def send_to_inboxes(author_id: str, author_url: str, data: dict, item_visibility: str):
    follows = Follow.objects.all().filter(object=author_id, accepted=True)

    if item_visibility == PUBLIC:
        for follow in follows:
            if not post_to_follower_inbox(follow.follower_url, data):
                print("ERROR: bad inbox response, public")

    elif item_visibility == PRIVATE:
        print("yoi")
        for follow in follows:
            if not author_follows_follower(author_url, follow.follower_url):
                print('wo')
                continue
            if not post_to_follower_inbox(follow.follower_url, data):
                print("frungle")
                print("ERROR: bad inbox response, private")
            print('yoi yoi')
    else:
        print("ERROR: invalid visibility")


def author_follows_follower(author_url: str, follower_url: str) -> bool:
    encoded_author_url = quote(author_url, safe='').replace('.', '%2E')
    check_url: str = follower_url + '/followers/' + encoded_author_url
    try:
        check_response: requests.Response = requests.get(check_url, headers=get_auth_headers(follower_url))
        return check_response.status_code >= 200 and check_response.status_code < 300
    except:
        return False


def post_to_follower_inbox(follower_url: str, data: dict) -> bool:
    follower_url = follower_url.strip("/")
    inbox_url: str = follower_url + '/inbox/'
    try:
        response: requests.Response = requests.post(inbox_url, json.dumps(data), headers=get_auth_headers(follower_url))
    except Exception as e:
        print("SERVER DOWN!")
        return True
    #print("RESPONSE STATUS CODE!",response.status_code)
    return response.status_code >= 200 and response.status_code < 300


def get_author(id : str):
    user = Author.objects.filter(pk=id)
    if not user:
        print("no requesting user")
        return None
    return user[0]

def check_if_friends_local(author1 : Author,author2: Author):

    followers_author1 = Follow.objects.filter(object=author1,follower_url=author2.url)
    followers_author2 = Follow.objects.filter(object=author2,follower_url=author1.url)

    if followers_author1 and followers_author2:
        print('they was local friends')
        return True
    
    if author1.pk == author2.pk:
        return True
    
    print("THEY WAS NOT FRIENDS")
    return False

def check_if_friends_remote(local_author : Author,remote_author_url : str):
    followers_local = Follow.objects.filter(object=local_author,follower_url=remote_author_url)

    local_is_following_remote = author_follows_follower(local_author.url,remote_author_url)

    if followers_local and local_is_following_remote:
        print('they was friends')
        return True
    
    if local_author.url == remote_author_url:
        return True
    print("THEY WAS NOT FRIENDS")
    return False

# check if a user is authenticated
def check_authenticated(request : HttpRequest, id : str):

    if not request.user.is_authenticated:
        print('not authenticated')
        return None
    
    user = Author.objects.filter(pk=id)
    if not user:
        print("db corrupted probably. user exists but author does not.")
        return None
    
    user = user[0]
    if str(user.userID) != str(request.user.pk):
        print('requesting wrong user!!')
        print(request.user.pk,user.userID)
        return None
    
    return user


def valid_requesting_user(request: HttpRequest, required_author_id: str) -> bool:
    if not request.user.is_authenticated:
        print('here1')
        return False

    author: Author | None = Author.objects.all().filter(userID=request.user.pk).first()

    if author is None:
        print('here2')
        return False
    
    if author.id != required_author_id:
        print('here3')
        return False

    return True


def make_author_url(request_host: str, author_id: str) -> str:
    return request_host + "/authors/" + author_id


def make_post_url(request_host: str, author_id: str, post_id: str) -> str:
    return make_author_url(request_host, author_id) + "/posts/" + post_id


def make_comments_url(request_host: str, author_id: str, post_id: str) -> str:
    return make_post_url(request_host, author_id, post_id) + "/comments"


def make_comment_url(request_host: str, author_id: str, post_id: str, comment_id: str) -> str:
    return make_post_url(request_host, author_id, post_id) + "/comments/" + comment_id

def make_inbox_url(request_host: str, author_id: str) -> str:
    return make_author_url(request_host,author_id) + "/inbox"

# checks that the request is authenticated either with our connected servers table in the DB,
# or the request is coming from our frontend/backend
def check_auth_header(request : HttpRequest):

    # print("CHECKING AUTH HEADER")
    
    origin = request.META.get('HTTP_ORIGIN')

    print("ORIGIN:",origin)
    print("SHOULD BE",HOSTNAME,FRONTEND)

    #check if the request is from us
    if origin == FRONTEND or origin == HOSTNAME:
        print("SUCCESS")
        return True

    if 'HTTP_AUTHORIZATION'  in request.META:
        print("MISSING AUTH HEADER")
        
    
        #check if the request is from a connected server
        auth_header = request.META['HTTP_AUTHORIZATION']

        connected = ConnectedServer.objects.filter(accepted_creds=auth_header)

        print("CHECKING AUTH HEADER!")

        if connected:
            return True

        


    
    return False

#check if the url is in our list of allowed servers to make requests to. otherwise, return 401
def can_send_request(url : str):

    #print("TEST: ",urllib.parse.urlparse(url).netloc)
    #print("URL: ",url)
    parsed_url = copy.copy(urllib.parse.urlparse(url).netloc)

    parsed_hostname = urllib.parse.urlparse(HOSTNAME).netloc
    #print("HOSTNAME PARSED",parsed_hostname)
    #print("HERE2","HOST:" + parsed_hostname + " URL: " + parsed_url)
    #print("WHAT " + parsed_url)
    print("HOST ",parsed_hostname," URL HOST ",parsed_url," test ",url)
    if parsed_url == parsed_hostname:
        #print("REQUEST TO SELF")
        return True
    
    connected = ConnectedServer.objects.filter(host=parsed_url)

    if connected:
        #print("SUCCESS. THIS URL IS CONNECTED")
        return True
    
    print("FAIL!")
    return False

def get_auth_header_for_server(url : str):
    parsed_url = urllib.parse.urlparse(url)

    connected = ConnectedServer.objects.filter(host=parsed_url.hostname)

    if connected:

        return connected[0].our_creds
    
    return ""

def get_auth_headers(url: str):
    return {"Origin": HOSTNAME, "Authentication": get_auth_header_for_server(url)}

def isaURL(s: str):
    return "/" in s
