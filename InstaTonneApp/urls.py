from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('user/<str:username>', views.user, name='user'),
    path('post/<int:post_id>', views.post, name='post'),
    path('post/<int:post_id>/edit', views.edit_post, name='edit_post'),
    path('friends/', views.friends, name='friends'),
    path('friends/requests', views.friend_requests, name='friend_requests'),
]
