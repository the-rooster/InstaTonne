from django.http import HttpRequest, HttpResponse
import json
from ..models import Post, PostSerializer, Comment, Author, CommentSerializer
from django.core.paginator import Paginator
from .utils import make_comment_url, make_comments_url


def single_post_comments(request: HttpRequest, author_id: int, post_id: int):
    if request.method == "GET":
        return single_post_comments_get(request, author_id, post_id)
    elif request.method == "POST":
        return single_post_comments_post(request, author_id, post_id)
    return HttpResponse(status=405)


# get the comments from a post
def single_post_comments_get(request: HttpRequest, author_id: int, post_id: int):
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


# add a comment to a post
def single_post_comments_post(request: HttpRequest, author_id: int, post_id: int):
    try:
        post: Post | None = Post.objects.all().filter(pk=post_id).first()

        if post is None:
            return HttpResponse(status=404)
        
        body: dict = json.loads(request.body)
        comment: Comment = Comment.objects.create(
            type = "comment",
            contentType = body["contentType"],
            comment = body["comment"],
            author = Author.objects.all().filter(pk=author_id).first(),
            post = post
        )

        comment_id = comment.id #type: ignore
        comment.id_url = make_comment_url(request.get_host(), author_id, post_id, comment_id)
        comment.save()

        return HttpResponse(status=204)
    except Exception as e:
        print(e)
        return HttpResponse(status=400)
