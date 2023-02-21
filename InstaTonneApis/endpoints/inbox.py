from django.http import HttpRequest, HttpResponse
from ..models import Author, Post, Request, Comment, Like, Inbox, PostSerializer, CommentSerializer, LikeSerializer, RequestSerializer
import json
import uuid
from InstaTonne.settings import HOSTNAME

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
    
    user = Author.objects.filter(pk=id)
    if not user:
        print("db corrupted probably. user exists but author does not.")
        return HttpResponse(status=500)
    
    user = user[0]
    if str(user.userID) != str(request.user.pk):
        print('requesting wrong user')
        print(request.user.pk,user.userID)
        return HttpResponse(status=403)
    
    #user is now authenticated
    #get all posts from followers

    #get author object
    

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
            # temp = data["post"]
            # data["id"] = temp
            # del temp

        elif item.like:

            data = LikeSerializer(item.like).data
            print(data)
            #change object to just be the url to the post to match the spec
            #to do this, we must fetch the url from the post object

            data["object"] = item.like.post.id_url
            del data["post"]
        elif item.request:
            data = RequestSerializer(item.request).data


        resp["items"].append(data)

    print(resp)
    return HttpResponse(content=json.dumps(resp),status=200)

"""
Post an item to a users inbox!
"""
def post_inbox(request : HttpRequest, id : str):
    
    #parse request body
    data = request.body
    data = json.loads(data)

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
    
    #format type to be consistent
    data["type"] = str(data["type"]).lower()

    try:
        if data["type"] == "post":
            #need to create author object if it doesn't exist here

            author_id = data["author"]["id"]
            author_id = author_id.split("/")[-1]

            check_author = Author.objects.filter(id=author_id)

            if not check_author:
                data["author"]["id"] = author_id
                creator = Author.objects.create(**(data["author"]))
            else:
                creator = Author.objects.get(id=author_id)

            data["author"] = creator
            data["id_url"] = data["id"]
            del data["id"]
            

            new_post = Post.objects.create(**data)
            new_post.save()

            inbox = Inbox.objects.create(ownerId=author,post=new_post)
            inbox.save()
        elif data["type"] == "follow":
            
            actor_id = data["actor"]["id"]
            actor_id = actor_id.split("/")[-1]

            print(actor_id)
            check_actor = Author.objects.filter(id=actor_id)
            print(check_actor)

            data["object"] = author

            if not check_actor:
                data["actor"]["id"] = actor_id
                actor = Author.objects.create(**(data["actor"]))
                print("here")
            else:
                actor = Author.objects.get(id=actor_id)
            data["actor"] = actor

            print("request object being made!")
            new_request = Request.objects.create(**data)
            new_request.save()
            inbox = Inbox.objects.create(ownerId=author,request=new_request)
            inbox.save()
        elif data["type"] == "like":
            author_id = data["author"]["id"]
            author_id = author_id.split("/")[-1]

            check_author = Author.objects.filter(id=author_id)

            if not check_author:
                data["author"]["id"] = author_id

                creator = Author.objects.create(**(data["author"]))
            else:
                creator = Author.objects.get(id=author_id)


            #need to create the post object here
            post = Post.objects.create(type="post",id_url=data["object"])

            #object field is no longer needed, and not used in our db (it is the url in post)
            del data["object"]

            #format data for db
            data["author"] = creator
            data["post"] = post

            #save to db
            new_like = Like.objects.create(**data)
            new_like.save()
            inbox = Inbox.objects.create(ownerId=author,like=new_like)
            inbox.save()
        elif data["type"] == "comment":
            #parse incoming comment data
            author_id = data["author"]["id"]
            author_id = author_id.split("/")[-1]

            check_author = Author.objects.filter(pk=author_id)

            if not check_author:
                del data["author"]["id"]
                author_id = Author.objects.create(**(data["author"]))

            data["author"] = author_id

            #save id to url field. incoming ids are urls, and we make a custom id on our end for stuff
            temp = data["id"]
            data["id_url"] = temp
            del data["id"]

            #create a new comment object, and send to the receivers inbox
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
