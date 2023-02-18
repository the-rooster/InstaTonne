from django.http import HttpRequest, HttpResponse
import json
from ..models import Post, PostSerializer, Comment, Author
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator


def single_author_post(request: HttpRequest, author_id: int, post_id: int):
    if request.method == "GET":
        return single_author_post_get(request, author_id, post_id)
    elif request.method == "POST":
        return single_author_post_post(request, author_id, post_id)
    elif request.method == "DELETE":
        return single_author_post_delete(request, author_id, post_id)
    elif request.method == "PUT":
        return single_author_post_put(request, author_id, post_id)
    return HttpResponse(status=405)


def single_author_posts(request: HttpRequest, author_id: int):
    if request.method == "GET":
        return single_author_posts_get(request, author_id)
    elif request.method == "POST":
        return single_author_posts_post(request, author_id)
    return HttpResponse(status=405)


# get a single post
def single_author_post_get(request: HttpRequest, author_id: int, post_id: int):
    post: Post | None = Post.objects.all().filter(author=author_id, pk=post_id).first()

    if post is None:
        return HttpResponse(status=404)

    serialized_post = PostSerializer(post).data
    comments_url = make_comments_url(request.get_host(), author_id, post_id)
    add_comments_to_post(serialized_post, post_id, comments_url)

    res = json.dumps(serialized_post)
    return HttpResponse(content=res, status=200)


# get all the posts of an author
def single_author_posts_get(request: HttpRequest, author_id: int):
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
        add_comments_to_post(serialized_post, post_id, comments_url)

        serialized_data.append(serialized_post)

    res = json.dumps({
        "type": "posts",
        "items": serialized_data
    })

    return HttpResponse(content=res, status=200)


# update an existing post
def single_author_post_post(request: HttpRequest, author_id: int, post_id: int):
    try:
        post: Post | None = Post.objects.all().filter(author=author_id, pk=post_id).first()

        if post is None:
            return HttpResponse(status=404)
    
        body: dict = json.loads(request.body)

        post.title = body["title"]
        post.description = body["description"]
        post.contentType = body["contentType"]
        post.content = body["content"]
        post.visibility = body["visibility"]
        post.categories = body["categories"]
        post.unlisted = body["unlisted"]
        post.save()

        return HttpResponse(status=204)
    except Exception as e:
        print(e)
        return HttpResponse(status=400)
    

# create a new post without a specified post id
def single_author_posts_post(request: HttpRequest, author_id: int):
    try:
        author: Author | None = Author.objects.all().filter(pk=author_id).first()

        if author is None:
            return HttpResponse(status=404)
        
        body: dict = json.loads(request.body)
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

        post_id = post.id #type: ignore
        post.url = make_post_url(request.get_host(), author_id, post_id)
        post.save()

        return HttpResponse(status=204)
    except Exception as e:
        print(e)
        return HttpResponse(status=400)
    

# delete a post
def single_author_post_delete(request: HttpRequest, author_id: int, post_id: int):
    post: Post | None = Post.objects.all().filter(author=author_id, pk=post_id).first()

    if post is None:
        return HttpResponse(status=404)
    
    post.delete()

    return HttpResponse(status=200)


# create a new post with a specified post id
def single_author_post_put(request: HttpRequest, author_id: int, post_id: int):
    try:
        author: Author | None = Author.objects.all().filter(pk=author_id).first()

        if author is None:
            return HttpResponse(status=404)
        
        body: dict = json.loads(request.body)
        Post.objects.create(
            id = post_id,
            url = make_post_url(request.get_host(), author_id, post_id),
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

        return HttpResponse(status=204)
    except Exception as e:
        print(e)
        return HttpResponse(status=400)
    

def add_comments_to_post(serialized_post, post_id: int, comments_url: str) -> None:
    comment_count = Comment.objects.all().filter(post=post_id).count()
    serialized_post["count"] = comment_count
    serialized_post["comments"] = comments_url


def make_post_url(request_host: str, author_id: int, post_id: int) -> str:
    return "http://" + request_host + "/service/authors/" + str(author_id) + "/posts/" + str(post_id)


def make_comments_url(request_host: str, author_id: int, post_id: int) -> str:
    return make_post_url(request_host, author_id, post_id) + "/comments"
