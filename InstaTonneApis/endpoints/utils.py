from django.http import HttpRequest
from ..models import Author

def valid_requesting_user(request: HttpRequest, required_author_id: int) -> bool:
    if not request.user.is_authenticated:
        return False

    author: Author | None = Author.objects.all().filter(userID=request.user.pk).first()

    if author is None:
        return False
    
    author_id = author.id #type: ignore
    
    if author_id != required_author_id:
        return False

    return True


def make_post_url(request_host: str, author_id: int, post_id: int) -> str:
    return "http://" + request_host + "/service/authors/" + str(author_id) + "/posts/" + str(post_id)


def make_comments_url(request_host: str, author_id: int, post_id: int) -> str:
    return make_post_url(request_host, author_id, post_id) + "/comments"


def make_comment_url(request_host: str, author_id: int, post_id: int, comment_id: int) -> str:
    return make_post_url(request_host, author_id, post_id) + "/comments/" + str(comment_id)
