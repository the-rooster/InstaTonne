from django.http import HttpRequest, HttpResponse
from ..models import Author, Post, Request, Comment, Like, Inbox, PostSerializer, CommentSerializer, LikeSerializer
import json

def inbox_endpoint(request : HttpRequest, author_id : str):

    if request.method == "GET":
        return get_inbox(request,author_id)
    elif request.method == "POST":
        return post_inbox(request,author_id)
    elif request.method == "DELETE":
        return delete_inbox(request,author_id)
    
    return HttpResponse(status=405)

def get_inbox(request : HttpRequest, id : str):

    resp = {
        "type" : "inbox",
        "author" : "http://" + request.get_host() + "/authors/" + str(id) + "/",
        "items" : []
    }
    if not request.user.is_authenticated:
        print('not authenticated')
        return HttpResponse(status=403)
    
    if request.user.pk != id:
        print('requesting wrong user')
        return HttpResponse(status=403)
    
    #user is now authenticated
    #get all posts from followers

    #get author object
    user = Author.objects.get(userID=id)

    if not user:
        #this shouldn't happen
        return HttpResponse(status=500)
    

    inbox = Inbox.objects.filter(ownerId=user)

    #TODO: do id and object fields correctly. use the url, not their object id in our local db
    for item in inbox:
        print(item)
        data = None
        if item.post:
            data = PostSerializer(item.post).data
        elif item.comment:
            data = CommentSerializer(item.comment).data

            #change object to just be the url and also call it id according to spec
            temp = data["post"]
            data["id"] = temp
            del temp

        elif item.like:

            data = LikeSerializer(item.like).data

            #change object to just be the url to the post to match the spec
            data["object"] = data["object"]["url"]

        resp["items"].append(data)

    print(resp)
    return HttpResponse(content=json.dumps(resp),status=200)

def post_inbox(request : HttpRequest, id : str):

    data = request.body

    data = json.loads(data)



    author = Author.objects.filter(userID=id)

    if not author:
        return HttpResponse(status=404)
    
    author = author[0]

    if "type" not in data.keys():
        print('here')
        return HttpResponse(status=400)
    
    try:
        if data["type"] == "post":
            #need to create author object if it doesn't exist here

            author_id = data["author"]["id"]

            check_author = Author.objects.filter(userID=author_id)

            if not check_author:
                author_id = Author.objects.create(**(data["author"]))

            data["author"] = author_id
            new_post = Post.objects.create(**data)
            new_post.save()

            inbox = Inbox.objects.create(ownerId=author,post=new_post)
            inbox.save()
        elif data["type"] == "follow":
            new_request = Request.objects.create(**data)
            new_request.save()
            inbox = Inbox.objects.create(ownerId=author,request=new_request)
            inbox.save()
        elif data["type"] == "like":
            new_like = Like.objects.create(**data)
            new_like.save()
            inbox = Inbox.objects.create(ownerId=author,like=new_like)
            inbox.save()
        elif data["type"] == "comment":

            author_id = data["author"]["id"]

            check_author = Author.objects.filter(userID=author_id)

            if not check_author:
                del data["author"]["id"]
                author_id = Author.objects.create(**(data["author"]))

            data["author"] = author_id

            temp = data["id"]
            data["url"] = temp
            del data["id"]

            
            new_comment = Comment.objects.create(**data)
            new_comment.save()

            inbox = Inbox.objects.create(ownerId=author,comment=new_comment)
            inbox.save()
        else:
            #not a valid type
            print("here")
            return HttpResponse(status=400)

    except Exception as e:
        #something in the request schema is broken
        print(e)
        print("oooooo")
        return HttpResponse(status=400)

    return HttpResponse(status=200)

def delete_inbox(request : HttpRequest, id : str):

    if not request.user.is_authenticated:
        print('not authenticated')
        return HttpResponse(status=403)
    
    if request.user.pk != id:
        print('requesting wrong user')
        return HttpResponse(status=403)
    
    #user is now authenticated
    #get all posts from followers

    #get author object
    user = Author.objects.get(userID=id)

    if not user:
        #this shouldn't happen
        return HttpResponse(status=500)
    
    #now clear the inbox
    print(id)
    res = Inbox.objects.filter(ownerId=user).delete()
    print(res)
    return HttpResponse(status=200)

