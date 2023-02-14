from django.http import HttpRequest, HttpResponse
import json
from ..models import Post, PostSerializer, Comment, Author
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def single_author_posts(request: HttpRequest, author_id: int):
    if request.method == "GET":
        return single_author_posts_get(request, author_id)
    elif request.method == "POST":
        return single_author_posts_post(request, author_id)
    return HttpResponse(status=405)


def single_author_posts_get(request: HttpRequest, author_id: int):
    posts = Post.objects.all().filter(author=author_id)
    comment_count = Comment.objects.all().count()

    serialized_data = []
    for post in posts:
        serialized_post = PostSerializer(post).data

        post_id = post.id #type: ignore
        comment_count = Comment.objects.all().filter(post=post_id).count()
        serialized_post["count"] = comment_count
        serialized_post["comments"] = make_comments_url(request, post_id)

        serialized_data.append(serialized_post)

    res = json.dumps([{
        "type": "posts",
        "items": serialized_data
    }])

    return HttpResponse(content=res, status=200)


def single_author_posts_post(request: HttpRequest, author_id: int):
    try:
        body: dict = json.loads(request.body)

        if not valid_body_for_posts(body):
            print("invalid post body")
            return HttpResponse(status=400)

        Post.objects.create(
            url=body["url"],
            title=body["title"],
            source=body["source"],
            origin=body["origin"],
            description=body["description"],
            contentType=body["contentType"],
            content=body["content"],
            visibility=body["visibility"],
            categories=body["categories"],
            unlisted=body["unlisted"],
            author=Author.objects.all().filter(pk=author_id).first()
        )

        return HttpResponse(status=204)
    except Exception as e:
        print(e)
        return HttpResponse(status=400)


def valid_body_for_posts(body: dict):
    return\
    "url" in body and\
    "title" in body and\
    "source" in body and\
    "origin" in body and\
    "description" in body and\
    "contentType" in body and\
    "content" in body and\
    "visibility" in body and\
    "categories" in body and\
    "unlisted" in body


def make_comments_url(request: HttpRequest, post_id: int) -> str:
    return "http://" + request.get_host() + request.get_full_path() + str(post_id) + "/comments"
