from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index(request):
    """View function for home page of site."""

    return render(request, 'index.html')

@login_required
def user(request, username):
    """View function for user page of site."""

    return render(request, 'user.html')

@login_required
def post(request, post_id):
    """View function for post page of site."""

    return render(request, 'post.html')

@login_required
def edit_post(request, post_id):
    """View function for edit post page of site."""

    return render(request, 'edit_post.html')

@login_required
def friends(request):
    """View function for friends page of site."""

    return render(request, 'friends.html')  

@login_required
def friend_requests(request):
    """View function for friend requests page of site."""

    return render(request, 'friend_requests.html')

@login_required
def profile(request):
    """View function for profile page of site."""

    return render(request, 'profile.html')