from django.http import HttpRequest
from ..models import Author

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
