# InstaTonne/urls.py
# Copyright (c) 2023 CMPUT 404 W2023 Group 6
#
# This file is part of InstaTonne.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
 

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
from InstaTonneApis.endpoints.inbox import InboxAPIView
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
