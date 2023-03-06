from django.http import HttpRequest, HttpResponse
from ..models import Author, Follow, FollowSerializer
from threading import Thread, Lock
import json
import requests
from typing import Tuple
import urllib.parse


PUBLIC = "PUBLIC"
PRIVATE = "PRIVATE"


def get_all_urls(urls: list[str]):
    inbox_lock = Lock()
    threads : list[Thread] = []
    result = []
    for url in urls:

        print(url)

        def get_item(url : str):
            try:
                response : requests.Response = requests.get(url)
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


def get_one_url(url: str) -> Tuple[int, str]:
    try:
        response: requests.Response = requests.get(url)
        return (response.status_code, response.text)
    except Exception as e:
        return (500, str(e))


def send_to_inboxes(author_id: str, author_url: str, item_url: str, item_visibility: str):
    follows = Follow.objects.all().filter(object=author_id, accepted=True)
    if item_visibility == PUBLIC:
        for follow in follows:
            if not post_to_follower_inbox(follow.follower_url, item_url):
                print("ERROR: bad inbox response, public")
    elif item_visibility == PRIVATE:
        for follow in follows:
            if not author_follows_follower(author_url, follow.follower_url):
                continue
            if not post_to_follower_inbox(follow.follower_url, item_url):
                print("ERROR: bad inbox response, private")
    else:
        print("ERROR: invalid visibility")


def author_follows_follower(author_url: str, follower_url: str) -> bool:
    encoded_author_url = urllib.parse.quote(author_url, safe='')
    check_url: str = follower_url + '/follower/' + encoded_author_url
    check_response: requests.Response = requests.get(check_url)
    return check_response.status_code == 200


def post_to_follower_inbox(follower_url: str, item_url: str) -> bool:
    inbox_url: str = follower_url + '/inbox/'
    response: requests.Response = requests.post(inbox_url, item_url) # this will probs have to get changed when the inbox endpoints get updated
    return response.status_code == 200


def get_author(id : str):
    user = Author.objects.filter(pk=id)
    if not user:
        print("db corrupted probably. user exists but author does not.")
        return None
    return user[0]


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
    print(user.userID,request.user.pk)
    if str(user.userID) != str(request.user.pk):
        print('requesting wrong user!!')
        print(request.user.pk,user.userID)
        return None
    
    return user


def valid_requesting_user(request: HttpRequest, required_author_id: str) -> bool:
    if not request.user.is_authenticated:
        return False

    author: Author | None = Author.objects.all().filter(userID=request.user.pk).first()

    if author is None:
        return False
    
    if author.id != required_author_id:
        return False

    return True


def make_post_url(request_host: str, author_id: str, post_id: str) -> str:
    return "http://" + request_host + "/service/authors/" + author_id + "/posts/" + post_id


def make_comments_url(request_host: str, author_id: str, post_id: str) -> str:
    return make_post_url(request_host, author_id, post_id) + "/comments"


def make_comment_url(request_host: str, author_id: str, post_id: str, comment_id: str) -> str:
    return make_post_url(request_host, author_id, post_id) + "/comments/" + comment_id
