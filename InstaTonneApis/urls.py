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
from django.urls import path, include
from rest_framework import routers, serializers, viewsets
from rest_framework.schemas import get_schema_view
from .endpoints.authors import *
from .endpoints.followers import single_author_followers, author_follower_foreign
from .endpoints.register import register_author
from .endpoints.login import login
from .endpoints.posts import single_author_posts, single_author_post
from .endpoints.comments import single_post_comments


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()


urlpatterns = [
    path("authors", page_all_authors),
    path("authors/<str:id>/", single_author),
    path("authors/<str:id>/followers/", single_author_followers),
    path("authors/<str:id>/followers/<str:foreign_id>/", author_follower_foreign),
    path("register/",register_author),
    path("login/",login),
    path("authors/<int:author_id>/posts/", single_author_posts),
    path("authors/<int:author_id>/posts/<int:post_id>/", single_author_post),
    path("authors/<int:author_id>/posts/<int:post_id>/comments/", single_post_comments)
]
