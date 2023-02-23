from django.http import HttpRequest, HttpResponse
import json
from ..models import Post, PostSerializer, Comment, Author
from django.core.paginator import Paginator
from .utils import make_comments_url, make_post_url, valid_requesting_user

PNG_CONTENT_TYPE = "image/png;base64"
JPEG_CONTENT_TYPE = "image/jpeg;base64"


def single_author_post(request: HttpRequest, author_id: str, post_id: str):
    if request.method == "GET":
        return single_author_post_get(request, author_id, post_id)
    elif request.method == "POST":
        return single_author_post_post(request, author_id, post_id)
    elif request.method == "DELETE":
        return single_author_post_delete(request, author_id, post_id)
    elif request.method == "PUT":
        return single_author_post_put(request, author_id, post_id)
    return HttpResponse(status=405)


def single_author_posts(request: HttpRequest, author_id: str):
    if request.method == "GET":
        return single_author_posts_get(request, author_id)
    elif request.method == "POST":
        return single_author_posts_post(request, author_id)
    return HttpResponse(status=405)


def single_author_post_image(request: HttpRequest, author_id: str, post_id: str):
    if request.method == "GET":
        return single_author_post_image_get(request, author_id, post_id)
    return HttpResponse(status=405)


# get a the encoded image from a single post
def single_author_post_image_get(request: HttpRequest, author_id: str, post_id: str):
    post: Post | None = Post.objects.all().filter(author=author_id, pk=post_id).first()

    if post is None:
        return HttpResponse(status=404)

    serialized_post = PostSerializer(post).data

    if serialized_post["contentType"] != PNG_CONTENT_TYPE and serialized_post["contentType"] != JPEG_CONTENT_TYPE:
        return HttpResponse(status=404)

    res = json.dumps(serialized_post["content"])
    return HttpResponse(content=res, status=200)


# get a single post
def single_author_post_get(request: HttpRequest, author_id: str, post_id: str):
    post: Post | None = Post.objects.all().filter(author=author_id, pk=post_id).first()

    if post is None:
        return HttpResponse(status=404)

    serialized_post = PostSerializer(post).data
    comments_url = make_comments_url(request.get_host(), author_id, post_id)
    comment_count = Comment.objects.all().filter(post=post_id).count()
    serialized_post["count"] = comment_count
    serialized_post["comments"] = comments_url
    serialized_post["id"] = serialized_post["id_url"]
    del serialized_post["id_url"]

    res = json.dumps(serialized_post)
    return HttpResponse(content=res, status=200)


# get all the posts of an author
def single_author_posts_get(request: HttpRequest, author_id: str):
    posts = Post.objects.all().filter(author=author_id).order_by("published")
    page_num = request.GET.get("page")
    page_size = request.GET.get("size")

    if page_num is not None and page_size is not None:
        paginator = Paginator(posts, page_size)
        posts = paginator.get_page(page_num)

    serialized_data = []
    for post in posts:
        post_id = post.id #type: ignore

        serialized_post = PostSerializer(post).data
        comments_url = make_comments_url(request.get_host(), author_id, post_id)
        comment_count = Comment.objects.all().filter(post=post_id).count()
        serialized_post["count"] = comment_count
        serialized_post["comments"] = comments_url
        serialized_post["id"] = serialized_post["id_url"]
        del serialized_post["id_url"]

        serialized_data.append(serialized_post)

    res = json.dumps({
        "type": "posts",
        "items": serialized_data
    })

    return HttpResponse(content=res, status=200)


# update an existing post
def single_author_post_post(request: HttpRequest, author_id: str, post_id: str):
    if not valid_requesting_user(request, author_id):
        return HttpResponse(status=403)

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
        return HttpResponse(status=403)

    try:
        author: Author | None = Author.objects.all().filter(pk=author_id).first()

        if author is None:
            return HttpResponse(status=404)
        
        body: dict = json.loads(request.body)
        post: Post = Post.objects.create(
            type = "post",
            title = body["title"],
            source = body["source"],
            origin = body["origin"],
            description = body["description"],
            contentType = body["contentType"],
            content = body["content"],
            visibility = body["visibility"],
            categories = body["categories"],
            unlisted = body["unlisted"],
            author = author
        )

        post_id = post.id #type: ignore
        post.id_url = make_post_url(request.get_host(), author_id, post_id)
        post.save()

        return HttpResponse(status=204)
    except Exception as e:
        print(e)
        return HttpResponse(status=400)
    

# delete a post
def single_author_post_delete(request: HttpRequest, author_id: str, post_id: str):
    if not valid_requesting_user(request, author_id):
        return HttpResponse(status=403)

    post: Post | None = Post.objects.all().filter(author=author_id, pk=post_id).first()

    if post is None:
        return HttpResponse(status=404)
    
    post.delete()

    return HttpResponse(status=204)


# create a new post with a specified post id
def single_author_post_put(request: HttpRequest, author_id: str, post_id: str):
    if not valid_requesting_user(request, author_id):
        return HttpResponse(status=403)

    try:
        author: Author | None = Author.objects.all().filter(pk=author_id).first()

        if author is None:
            return HttpResponse(status=404)
        
        body: dict = json.loads(request.body)
        Post.objects.create(
            id = post_id,
            id_url = make_post_url(request.get_host(), author_id, post_id),
            type = "post",
            title = body["title"],
            source = body["source"],
            origin = body["origin"],
            description = body["description"],
            contentType = body["contentType"],
            content = body["content"],
            visibility = body["visibility"],
            categories = body["categories"],
            unlisted = body["unlisted"],
            author = author
        )

        return HttpResponse(status=204)
    except Exception as e:
        print(e)
        return HttpResponse(status=400)
