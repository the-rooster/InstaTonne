from django.http import HttpRequest, HttpResponse
import json
from ..models import Post, PostSerializer, Comment, Author, CommentSerializer
from django.core.paginator import Paginator
from .utils import make_comment_url, make_comments_url, get_one_url, make_author_url, send_to_single_inbox, check_authenticated
import re
from InstaTonne.settings import HOSTNAME

def single_post_comments(request: HttpRequest):
    matched = re.search(r"^\/authors\/(.*?)\/posts\/(.*?)\/comments\/?$", request.path)
    if matched:
        author_id: str = matched.group(1)
        post_id: str = matched.group(2)
    else:
        return HttpResponse(status=405)
    
    print("!!!")

    if "/" in post_id and request.method == "GET":
        print('ya')
        return single_post_comments_get_remote(request, author_id, post_id)
    elif "/" in post_id and request.method == "POST":
        return single_post_comments_post_remote(request,author_id,post_id)
    elif "/" in post_id or "/" in author_id:
        return HttpResponse(status=405)
    elif request.method == "GET":
        return single_post_comments_get(request, author_id, post_id)
    elif request.method == "POST":
        return single_post_comments_post(request, author_id, post_id)
    return HttpResponse(status=405)


# get the comments from a post
def single_post_comments_get(request: HttpRequest, author_id: str, post_id: str):
    post_url = Post.objects.all().filter(pk=post_id).first().id_url #type: ignore
    comments = Comment.objects.all().filter(post=post_id).order_by("published")
    page_num = request.GET.get("page")
    page_size = request.GET.get("size")

    if page_num is not None and page_size is not None:
        paginator = Paginator(comments, page_size)
        comments = paginator.get_page(page_num)

    serialized_data = []
    for comment in comments:
        serialized_comment = CommentSerializer(comment).data

        serialized_comment["id"] = serialized_comment["id_url"]
        del serialized_comment["id_url"]

        serialized_data.append(serialized_comment)

    res = json.dumps({
        "type": "comments",
        "page": page_num,
        "size": page_size,
        "post": post_url,
        "id": make_comments_url(request.get_host(), author_id, post_id),
        "comments": serialized_data
    })

    return HttpResponse(content=res, status=200)


def single_post_comments_get_remote(request: HttpRequest, author_id: str, post_id: str):

    query = request.META.get('QUERY_STRING', '')
    if query:
        query = '?' + query
    remote_url = post_id + '/comments' + query


    status_code, text = get_one_url(remote_url)

    if status_code != 200:
        print("GETTING REMOTE COMMENTS FAILED:")
        print(status_code,text)
        return HttpResponse(status=404)

    return HttpResponse(status=status_code, content=text)

def single_post_comments_post_remote(request: HttpRequest, author_id : str, post_id : str):
    author: Author | None = Author.objects.all().filter(userID=request.user.id).first()
    
    if not author:
        return HttpResponse(status=403)
    
    try:
        
        body: dict = json.loads(request.body)
        comment: dict = {
            "type" : "comment",
            "contentType" : body["contentType"],
            "content" : body["comment"],
            "author" : make_author_url(request.get_host(), author.id),
            "post" : post_id
        }

        # comment_id = comment.id #type: ignore
        # comment.id_url = make_comment_url(request.get_host(), author_id, post_id, comment_id)
        # comment.save()

        #get post information to recover author url
        res = get_one_url(post_id)

        if not res:
            print("POST NOT FOUND WHEN TRYING TO MAKE COMMENT!")
            return HttpResponse(status=400)
        
        #assume author.id field. might need adapter for this boy
        res_content = json.loads(res[1])
        print("CONTENT: ",res_content)
        author_inbox_url = res_content["author"]["id"]

        send_to_single_inbox(author_inbox_url,comment)

        return HttpResponse(status=204)
    except Exception as e:
        print(e)
        return HttpResponse(status=400)
# add a comment to a post
def single_post_comments_post(request: HttpRequest, author_id: str, post_id: str):
    #get requester author object (this endpoint should be called from local!)
    author: Author | None = Author.objects.all().filter(userID=request.user.id).first()

    if not author:
        print('yahoooo',request.user.id)
        return HttpResponse(status=403)
    try:
        post: Post | None = Post.objects.all().filter(pk=post_id).first()

        if post is None:
            return HttpResponse(status=404)
        
        body: dict = json.loads(request.body)
        comment: dict = {
            "type" : "comment",
            "contentType" : body["contentType"],
            "content" : body["comment"],
            "author" : make_author_url(request.get_host(), author.id),
            "post" : post.id_url
        }

        # comment_id = comment.id #type: ignore
        # comment.id_url = make_comment_url(request.get_host(), author_id, post_id, comment_id)
        # comment.save()

        author_inbox_url = make_author_url(request.get_host(),author_id)

        send_to_single_inbox(author_inbox_url,comment)

        return HttpResponse(status=204)
    except Exception as e:
        print(e)
        return HttpResponse(status=400)
    
#THIS SHOULD ONLY BE CALLED BY OUR LOCAL SERVER. kinda wack but ya
def get_single_comment_local(request:HttpRequest,author_id : str,post_id : str, comment_id : str):

    post = Post.objects.filter(id=post_id).first()

    if not post:
        return HttpResponse(status=404)
    
    
    comment = Comment.objects.filter(id=comment_id).first()

    res = json.dumps({
        "type": "comment",

        "post": comment.post.id,
        "author" : comment.author,
        "content": comment.comment,
        "contentType": comment.contentType,
        "post" : post.id_url
    })

    return HttpResponse(content=res,status=200)
