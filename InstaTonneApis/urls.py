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
from .endpoints.authors import get_author_id
from .endpoints.followers import get_request_object
from .endpoints.register import register_author
from .endpoints.login import login
from .endpoints.csrf import get_csrf
from .endpoints.connectedservers import get_all_connected_servers

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from InstaTonneApis.endpoints.authors import AuthorsAPIView, RemoteAuthorsAPIView, SingleAuthorApiView
from InstaTonneApis.endpoints.followers import SingleAuthorFollowersAPIView, SingleAuthorFollowerAPIView
from InstaTonneApis.endpoints.posts import SingleAuthorPostsAPIView, SingleAuthorPostAPIView, SingleAuthorPostImageAPIView
from InstaTonneApis.endpoints.comments import SingleAuthorPostCommentsAPIView, SingleAuthorPostCommentAPIView
from InstaTonneApis.endpoints.likes import SingleAuthorPostLikesAPIView, SingleAuthorPostCommentLikesAPIView, SingleAuthorLikesAPIView, SingleAuthorPostCommentLikeAPIView, SingleAuthorPostLikeAPIView
from InstaTonneApis.endpoints.inbox import InboxAPIView, GInboxAPIView
from InstaTonneApis.endpoints.github import GithubAPIView

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

schema_view = get_schema_view(
   openapi.Info(
      title="InstaTonne API",
      default_version='v1',
      #description="This is our API LOL",
      #terms_of_service="https://www.google.com/policies/terms/",
      #contact=openapi.Contact(email="contact@dummy.local"),
      #license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("register/",register_author),
    path("login/",login),
    path("authors/id/",get_author_id),
    path("connected-servers/",get_all_connected_servers),

    re_path(r"^remote-authors\/(?P<remote>.+?)\/?$", RemoteAuthorsAPIView.as_view()),
    re_path(r"^authors\/(?P<author_id>.+?)\/inbox\/?$", InboxAPIView.as_view()),
    re_path(r"^authors\/(?P<author_id>.+?)\/ginbox\/?$", GInboxAPIView.as_view()),
    re_path(r"^authors\/(?P<author_id>.+?)\/liked\/?$", SingleAuthorLikesAPIView.as_view()),
    re_path(r"^authors\/(.+?)\/followers\/(.+?)\/request\/?$", get_request_object),
    re_path(r"^authors\/(?P<author_id>.+?)\/posts\/(?P<post_id>.+?)\/image\/?$", SingleAuthorPostImageAPIView.as_view()),
    re_path(r"^authors\/(?P<author_id>.+?)\/github\/?$", GithubAPIView.as_view()),

    re_path(r"^authors\/(?P<author_id>.+?)\/posts\/(?P<post_id>.+?)\/comments\/(?P<comment_id>.+?)\/likes\/(?P<like_id>.+?)\/?$", SingleAuthorPostCommentLikeAPIView.as_view()),
    re_path(r"^authors\/(?P<author_id>.+?)\/posts\/(?P<post_id>.+?)\/comments\/(?P<comment_id>.+?)\/likes\/?$", SingleAuthorPostCommentLikesAPIView.as_view()),
    re_path(r"^authors\/(?P<author_id>.+?)\/posts\/(?P<post_id>.+?)\/comments\/(?P<comment_id>.+?)\/?$", SingleAuthorPostCommentAPIView.as_view()),
    re_path(r"^authors\/(?P<author_id>.+?)\/posts\/(?P<post_id>.+?)\/comments\/?$", SingleAuthorPostCommentsAPIView.as_view()),
    re_path(r"^authors\/(?P<author_id>.+?)\/posts\/(?P<post_id>.+?)\/likes\/(?P<like_id>.+?)\/?$", SingleAuthorPostLikeAPIView.as_view()),
    re_path(r"^authors\/(?P<author_id>.+?)\/posts\/(?P<post_id>.+?)\/likes\/?$", SingleAuthorPostLikesAPIView.as_view()),
    re_path(r"^authors\/(?P<author_id>.+?)\/posts\/(?P<post_id>.+?)\/?$", SingleAuthorPostAPIView.as_view()),
    re_path(r"^authors\/(?P<author_id>.+?)\/posts\/?$", SingleAuthorPostsAPIView.as_view()),
    re_path(r"^authors\/(?P<author_id>.+?)\/followers\/(?P<foreign_author_id>.+?)\/?$", SingleAuthorFollowerAPIView.as_view()),
    re_path(r"^authors\/(?P<author_id>.+?)\/followers\/?$", SingleAuthorFollowersAPIView.as_view()),
    re_path(r"^authors\/(?P<author_id>.+?)\/?$", SingleAuthorApiView.as_view()),
    re_path(r"^authors\/?$", AuthorsAPIView.as_view()),

    path("docs/", schema_view.with_ui('swagger', cache_timeout=0)),

    path("csrf/", get_csrf)
]
