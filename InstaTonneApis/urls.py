"""InstaTonne URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers, serializers, viewsets
from rest_framework.schemas import get_schema_view
from .endpoints.authors import single_author, authors, get_author_id
from .endpoints.followers import single_author_followers, single_author_follower
from .endpoints.register import register_author
from .endpoints.login import login
from .endpoints.posts import single_author_posts, single_author_post, single_author_post_image
from .endpoints.comments import single_post_comments, get_single_comment_local
from .endpoints.likes import single_comment_likes, single_post_likes, single_author_likes, get_single_like_post_local, get_single_like_comment_local
from .endpoints.inbox import inbox_endpoint
from .endpoints.csrf import get_csrf
# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()


urlpatterns = [
    path("register/",register_author),
    path("login/",login),
    path("authors/id/",get_author_id),

    re_path(r"^authors\/.+?\/liked\/?$", single_author_likes),
    re_path(r"^authors\/.+?\/posts\/.+?\/comments\/.+?\/likes\/?$", single_comment_likes),
    re_path(r"^authors\/.+?\/posts\/.+?\/comments\/?$", single_post_comments),
    path("authors/<str:author_id>/posts/<str:post_id>/comments/<str:comment_id>",get_single_comment_local),
    re_path(r"^authors\/.+?\/posts\/.+?\/likes\/?$", single_post_likes),
    path("authors/<str:author_id>/posts/<str:post_id>/comments/<str:comment_id>/likes/<str:like_id>",get_single_like_comment_local),
    path("authors/<str:author_id>/posts/<str:post_id>/likes/<str:like_id>",get_single_like_post_local),
    re_path(r"^authors\/.+?\/posts\/.+?\/?$", single_author_post),
    re_path(r"^authors\/.+?\/posts\/?$", single_author_posts),
    re_path(r"^authors\/.+?\/inbox\/?$",inbox_endpoint),
    re_path(r"^authors\/.+?\/followers\/.+?\/?$", single_author_follower),
    re_path(r"^authors\/.+?\/followers\/?$", single_author_followers),
    re_path(r"^authors\/.+?\/?$", single_author),
    re_path(r"^authors\/?$", authors),
    path("authors/<str:author_id>/posts/<str:post_id>/image", single_author_post_image),
    path("csrf/", get_csrf)
]
