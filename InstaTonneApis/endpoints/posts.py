from django.http import HttpRequest, HttpResponse
import json
from InstaTonneApis.models import Post, PostSerializer, Comment, Author
from django.core.paginator import Paginator
from InstaTonneApis.endpoints.utils import make_comments_url, make_post_url, valid_requesting_user, send_to_inboxes, check_auth_header, isaURL, get_auth_headers
import requests
import base64
from InstaTonne.settings import HOSTNAME

PNG_CONTENT_TYPE = "image/png;base64"
JPEG_CONTENT_TYPE = "image/jpeg;base64"


# handle requests for a single post of an author
def single_author_post(request: HttpRequest, author_id: str, post_id: str):
    if not check_auth_header(request):
        return HttpResponse(status=401)

    if isaURL(post_id) and request.method == "GET":
        return single_author_post_get_remote(request, author_id, post_id)

    if isaURL(post_id):
        return HttpResponse(status=405)

    if request.method == "GET":
        return single_author_post_get(request, author_id, post_id)

    if request.method == "POST":
        return single_author_post_post(request, author_id, post_id)

    if request.method == "DELETE":
        return single_author_post_delete(request, author_id, post_id)

    if request.method == "PUT":
        return single_author_post_put(request, author_id, post_id)
    
    return HttpResponse(status=405)


# handle requests for the posts of an author
def single_author_posts(request: HttpRequest, author_id: str):
    if not check_auth_header(request):
        return HttpResponse(status=401)
    
    if isaURL(author_id) and request.method == "GET":
        return single_author_posts_get_remote(request, author_id)
    
    if isaURL(author_id):
        return HttpResponse(status=405)
    
    if request.method == "GET":
        return single_author_posts_get(request, author_id)
    
    if request.method == "POST":
        return single_author_posts_post(request, author_id)
    
    return HttpResponse(status=405)


# handle requests for an image post
def single_author_post_image(request: HttpRequest, author_id: str, post_id: str):
    if not check_auth_header(request):
        return HttpResponse(status=401)

    if request.method == "GET":
        return single_author_post_image_get(request, author_id, post_id)
    
    return HttpResponse(status=405)


# get a the encoded image from a single post
def single_author_post_image_get(request: HttpRequest, author_id: str, post_id: str):
    post: Post | None = Post.objects.all().filter(pk=post_id).first()

    if post is None:
        return HttpResponse(status=404)

    serialized_post = PostSerializer(post).data

    if serialized_post["contentType"] != PNG_CONTENT_TYPE and serialized_post["contentType"] != JPEG_CONTENT_TYPE:
        return HttpResponse(status=404)

    res : str = serialized_post["content"]
    res = res.split(",")[-1]

    res_bytes = base64.decodebytes(res.encode("UTF-8"))

    return HttpResponse(content=res_bytes, content_type=serialized_post["contentType"], status=200)


# get a single post
def single_author_post_get(request: HttpRequest, author_id: str, post_id: str):
    post: Post | None = Post.objects.all().filter(author=author_id, pk=post_id).first()

    if post is None:
        return HttpResponse(status=404)

    serialized_post = PostSerializer(post).data
    comments_url = make_comments_url(HOSTNAME, author_id, post_id)
    comment_count = Comment.objects.all().filter(post=post_id).count()
    serialized_post["count"] = comment_count
    serialized_post["comments"] = comments_url

    res = json.dumps(serialized_post)
    return HttpResponse(content=res, content_type="application/json", status=200)


# get a single post of a remote author
def single_author_post_get_remote(request: HttpRequest, author_id: str, post_id: str):
    url = post_id
    response: requests.Response = requests.get(url, headers=get_auth_headers(url))
    return HttpResponse(
        status=response.status_code,
        content_type=response.headers['Content-Type'],
        content=response.content.decode('utf-8')
    )


# get all the posts of an author
def single_author_posts_get(request: HttpRequest, author_id: str):
    author: Author | None = Author.objects.all().filter(pk=author_id).first()
    if author is None:
        return HttpResponse(status=404)

    posts = Post.objects.all().filter(author=author_id, unlisted=False).order_by("published")
    page_num = request.GET.get("page")
    page_size = request.GET.get("size")

    if page_num is not None and page_size is not None:
        paginator = Paginator(posts, page_size)
        posts = paginator.get_page(page_num)

    serialized_data = []
    for post in posts:
        serialized_post = PostSerializer(post).data
        comments_url = make_comments_url(HOSTNAME, author_id, post.id)
        comment_count = Comment.objects.all().filter(post=post.id).count()
        serialized_post["count"] = comment_count
        serialized_post["comments"] = comments_url

        serialized_data.append(serialized_post)

    res = json.dumps({
        "type": "posts",
        "items": serialized_data
    })

    return HttpResponse(content=res, content_type="application/json", status=200)


# get all the posts of a remote author
def single_author_posts_get_remote(request: HttpRequest, author_id: str):
    query = request.META.get('QUERY_STRING', '')
    if query: query = '?' + query
    url = author_id + '/posts' + query
    response: requests.Response = requests.get(url, headers=get_auth_headers(url))
    return HttpResponse(
        status=response.status_code,
        content_type=response.headers['Content-Type'],
        content=response.content.decode('utf-8')
    )


# update an existing post
def single_author_post_post(request: HttpRequest, author_id: str, post_id: str):
    if not valid_requesting_user(request, author_id):
        return HttpResponse(status=401)

    try:
        post: Post | None = Post.objects.all().filter(author=author_id, pk=post_id).first()

        if post is None:
            return HttpResponse(status=404)
    
        body: dict = json.loads(request.body)

        if "title" in body:
            post.title = body["title"]
        if "description" in body:
            post.description = body["description"]
        if "contentType" in body:
            post.contentType = body["contentType"]
        if "content" in body:
            post.content = body["content"]
        if "visibility" in body:
            post.visibility = body["visibility"]
        if "categories" in body:
            post.categories = body["categories"]
        if "unlisted" in body:
            post.unlisted = body["unlisted"]
        post.save()

        return HttpResponse(status=204)
    except Exception as e:
        print(e)
        return HttpResponse(status=400)


# create a new post without a specified post id
def single_author_posts_post(request: HttpRequest, author_id: str):
    if not valid_requesting_user(request, author_id):
        return HttpResponse(status=401)

    try:
        author: Author | None = Author.objects.all().filter(pk=author_id).first()

        if author is None:
            return HttpResponse(status=404)
        
        body: dict = json.loads(request.body)
        #if were creating an image, create a seperate unlisted post with the image to link to
        if body["contentType"] == PNG_CONTENT_TYPE or body["contentType"] == JPEG_CONTENT_TYPE:
            print("CREATING UNLISTED IMAGE POST")
            uri = make_image_post(request,author,author_id)
            body["content"] = f"<img src=\"{uri}\">"
            body["contentType"] = "text/markdown"

        post: Post = Post.objects.create(
            type = "post",
            title = body["title"],
            description = body["description"],
            contentType = body["contentType"],
            content = body["content"],
            visibility = body["visibility"],
            categories = body["categories"],
            unlisted = body["unlisted"],
            author = author
        )
        post.id_url = make_post_url(HOSTNAME, author.id, post.id)
        post.origin = post.id_url if not body["origin"] else body["origin"]
        post.source = post.id_url if not body["source"] else body["source"]
        post.save()

        data : dict = {
            "type" : "post",
            "id" : post.id_url
        }
        send_to_inboxes(author_id, author.id_url, data, body["visibility"])

        return HttpResponse(status=204)
    except Exception as e:
        print(e)
        print("HERE!")
        return HttpResponse(status=400)


#make image post to link to markdown post
def make_image_post(request : HttpRequest,author: Author,author_id : str):
    body: dict = json.loads(request.body)
    post: Post = Post.objects.create(
        type = "post",
        title = "image",
        description = "image",
        contentType = body["contentType"],
        content = body["content"],
        visibility = body["visibility"],
        categories = body["categories"],
        unlisted = True,
        author = author
    )
    post.id_url = make_post_url(HOSTNAME, author.id, post.id)
    post.origin = post.id_url if not body["origin"] else body["origin"]
    post.source = post.id_url if not body["source"] else body["source"]
    post.save()

    return post.id_url + "/image"


# delete a post
def single_author_post_delete(request: HttpRequest, author_id: str, post_id: str):
    if not valid_requesting_user(request, author_id):
        return HttpResponse(status=401)

    post: Post | None = Post.objects.all().filter(author=author_id, pk=post_id).first()

    if post is None:
        return HttpResponse(status=404)
    
    post.delete()

    return HttpResponse(status=204)


# create a new post with a specified post id
def single_author_post_put(request: HttpRequest, author_id: str, post_id: str):
    if not valid_requesting_user(request, author_id):
        return HttpResponse(status=401)

    try:
        author: Author | None = Author.objects.all().filter(pk=author_id).first()

        if author is None:
            return HttpResponse(status=404)
        
        existing_post: Post | None = Post.objects.all().filter(pk=post_id).first()

        if existing_post is not None:
            return single_author_post_post(request, author_id, post_id)
        
        body: dict = json.loads(request.body)
        post: Post = Post.objects.create(
            id = post_id,
            id_url = make_post_url(HOSTNAME, author_id, post_id),
            type = "post",
            title = body["title"],
            description = body["description"],
            contentType = body["contentType"],
            content = body["content"],
            visibility = body["visibility"],
            categories = body["categories"],
            unlisted = body["unlisted"],
            author = author
        )
        post.origin = post.id_url if not body["origin"] else body["origin"]
        post.source = post.id_url if not body["source"] else body["source"]
        post.save()

        data : dict = {
            "type" : "post",
            "id" : post.id_url
        }
        send_to_inboxes(author_id, author.id_url, data, body["visibility"])

        return HttpResponse(status=204)
    except Exception as e:
        print(e)
        return HttpResponse(status=400)
