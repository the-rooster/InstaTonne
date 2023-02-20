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