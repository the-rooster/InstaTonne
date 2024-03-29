from django.db import models
from rest_framework import serializers
import json
import uuid
from InstaTonne.settings import HOSTNAME
from django.utils import timezone

def default_id_generator():
    return ''.join(str(uuid.uuid4()).split("-"))



class Author(models.Model):
    id = models.TextField(primary_key=True, default=default_id_generator, editable=False)
    type = models.TextField()
    id_url = models.TextField()
    url = models.TextField()
    host = models.TextField()
    displayName = models.TextField()
    github = models.TextField()
    profileImage = models.TextField()

    userID = models.TextField()
    active = models.BooleanField(default=False)


class AuthorSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='id_url')

    class Meta:
        model = Author
        fields = ['type', 'id', 'url', 'host', 'displayName', 'github', 'profileImage'] # ??? userID and active not here, should they be?

    def create(self, validated_data):
        return Author.objects.create(**validated_data)

class AuthorExampleSerializer(serializers.Serializer):
    type = serializers.CharField(default='author')
    id = serializers.CharField(default='http://servicehost/author/1')
    url = serializers.CharField(default='http://servicehost/author/1')
    host = serializers.CharField(default='http://servicehost')
    displayName = serializers.CharField(default='displayname1')
    github = serializers.CharField(default='http://github.com/username1')
    profileImage = serializers.CharField(default='http://imagehost/img.jpeg')

class AuthorsResponseSerializer(serializers.Serializer):
    type = serializers.CharField(default='authors')
    items = AuthorExampleSerializer(many=True)


class Follow(models.Model):
    id = models.TextField(primary_key=True, default=default_id_generator, editable=False)
    object = models.ForeignKey(Author,on_delete=models.CASCADE)
    follower_url = models.TextField()
    summary = models.TextField()
    accepted = models.BooleanField()


class FollowSerializer(serializers.ModelSerializer):
    object = AuthorSerializer()
    actor = serializers.CharField(source='follower_url')

    class Meta:
        model = Follow
        fields = ['object','summary','accepted','actor']


class FollowersResponseSerializer(serializers.Serializer):
    type = serializers.CharField(default='followers')
    items = AuthorExampleSerializer(many=True)


class Post(models.Model):
    id = models.TextField(primary_key=True, default=default_id_generator, editable=False)
    type = models.TextField()
    id_url = models.TextField()
    title = models.TextField()
    source = models.TextField()
    origin = models.TextField()
    description = models.TextField()
    contentType = models.TextField()
    content = models.TextField()
    visibility = models.TextField()
    comments = models.TextField()  # ??? Should this be a FK for list of models.Comments?
    
    categories  = models.CharField(max_length=100)
    unlisted = models.BooleanField(default=False)
    published = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(Author, on_delete=models.CASCADE,blank=True,null=True)


class PostSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='id_url')
    author = AuthorSerializer()
    categories = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ['type', 'title', 'id', 'source', 'origin', 'description', 'contentType',
                  'content', 'author', 'categories', 'published', 'visibility', 'unlisted']

    def get_categories(self, instance):
        return json.loads(instance.categories.replace("'", '"'))
    
    def create(self, validated_data):
        return Post.objects.create(**validated_data)


class PostExampleSerializer(serializers.Serializer):
    type = serializers.CharField(default='post')
    title = serializers.CharField(default='title1')
    id = serializers.CharField(default='http://servicehost/posts/1')
    source = serializers.CharField(default='http://servicehost/posts/1')
    origin = serializers.CharField(default='http://servicehost/posts/1')

    description = serializers.CharField(default='description1')
    contentType = serializers.CharField(default='text/plain')
    content = serializers.CharField(default='content1')

    author = AuthorExampleSerializer()
    categories = serializers.ListField(child=serializers.CharField(), default=[])

    published = serializers.DateTimeField(default=timezone.now)
    visibility = serializers.CharField(default='PUBLIC')
    unlisted = serializers.BooleanField(default=False)

    count = serializers.IntegerField(default=1)
    comments = serializers.CharField(default='http://servicehost/posts/1/comments')


class PostsResponseSerializer(serializers.Serializer):
    type = serializers.CharField(default='posts')
    items = PostExampleSerializer(many=True)


class Request(models.Model):
    type = models.TextField()
    summary = models.TextField()

    published = models.DateTimeField(auto_now_add=True)

    actor = models.ForeignKey(Author, related_name='requester', on_delete=models.CASCADE)
    object = models.ForeignKey(Author, related_name='requestee', on_delete=models.CASCADE)


class RequestSerializer(serializers.ModelSerializer):
    actor = AuthorSerializer()
    object = AuthorSerializer()
    class Meta:
        model = Request
        fields = ['type','summary','published','actor','object']


class RequestResponseSerializer(serializers.Serializer):
    type = serializers.CharField(default='request')
    items = RequestSerializer(many=True)


class Comment(models.Model):
    id = models.TextField(primary_key=True, default=default_id_generator, editable=False)
    type = models.TextField()
    id_url = models.TextField()
    contentType = models.TextField()
    comment = models.TextField()
    author = models.TextField()

    published = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='id_url')
    class Meta:
        model = Comment
        fields = ['type', 'id', 'contentType', 'comment', 'published', 'author']


class CommentResponseSerializer(serializers.Serializer):
    type = serializers.CharField(default='comment')
    id = serializers.CharField(default='http://servicehost/authors/1/posts/1/comments/1')
    contentType = serializers.CharField(default='text/plain')
    comment = serializers.CharField(default='comment1')
    published = serializers.DateTimeField(default=timezone.now)
    author = AuthorExampleSerializer()


class CommentsResponseSerializer(serializers.Serializer):
    type = serializers.CharField(default='comments')
    page = serializers.CharField(default='1')
    size = serializers.CharField(default='1')
    post = serializers.CharField(default='http://servicehost/authors/1/posts/1')
    id = serializers.CharField(default='http://servicehost/authors/1/posts/1/comments')
    items = CommentResponseSerializer(many=True)


class Like(models.Model):
    id = models.TextField(primary_key=True, default=default_id_generator, editable=False)
    type = models.TextField()
    summary = models.TextField()
    author = models.TextField()

    published = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)


class LikeSerializer(serializers.ModelSerializer):
    comment = CommentSerializer()
    post = PostSerializer()
    
    class Meta:
        model = Like
        fields = ['type', 'summary', 'author', 'comment', 'post']


class LikePostResponseSerializer(serializers.Serializer):
    type = serializers.CharField(default='like')
    summary = serializers.CharField(default='summary1')
    author = serializers.CharField(default='http://servicehost/author/1')
    object = serializers.CharField(default='http://servicehost/author/1/posts/1')


class LikeCommentResponseSerializer(serializers.Serializer):
    type = serializers.CharField(default='like')
    summary = serializers.CharField(default='summary1')
    author = serializers.CharField(default='http://servicehost/author/1')
    object = serializers.CharField(default='http://servicehost/author/1/posts/1/comments/1')


class LikesPostResponseSerializer(serializers.Serializer):
    type = serializers.CharField(default='likes')
    items = LikePostResponseSerializer(many=True)


class LikesCommentResponseSerializer(serializers.Serializer):
    type = serializers.CharField(default='likes')
    items = LikeCommentResponseSerializer(many=True)


class Inbox(models.Model):
    id = models.TextField(primary_key=True, default=default_id_generator, editable=False)
    author = models.ForeignKey(Author,on_delete=models.CASCADE)
    url = models.TextField()

    published = models.DateTimeField(auto_now_add=True)


class InboxSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='id_url')
    class Meta:
        model = Inbox
        fields = ['id', 'author', 'url', 'published']

class InboxExampleSerializer(serializers.Serializer):
    type = serializers.CharField(default='like')
    summary = serializers.CharField(default='summary1')
    author = serializers.CharField(default='http://servicehost/author/1')
    object = serializers.CharField(default='http://servicehost/author/1/posts/1')

class InboxResponseSerializer(serializers.Serializer):
    type = serializers.CharField(default='inbox')
    author = serializers.CharField(default='http://servicehost/author/1')
    items = InboxExampleSerializer(many=True)


class GInboxSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='id_url')
    created_at = serializers.DateTimeField(source='published')
    class Meta:
        model = Inbox
        fields = ['id', 'author', 'url', 'published', 'created_at']

class GInboxExampleSerializer(serializers.Serializer):
    type = serializers.CharField(default='like')
    summary = serializers.CharField(default='summary1')
    author = serializers.CharField(default='http://servicehost/author/1')
    object = serializers.CharField(default='http://servicehost/author/1/posts/1')
    created_at = serializers.DateTimeField(default=timezone.now)

class GInboxResponseSerializer(serializers.Serializer):
    type = serializers.CharField(default='ginbox')
    author = serializers.CharField(default='http://servicehost/author/1')
    items = GInboxExampleSerializer(many=True)


class ConnectedServer(models.Model):
    host = models.TextField()
    api = models.TextField()
    accepted_creds = models.TextField()
    our_creds = models.TextField()


class ConnectedServerSerializer(serializers.ModelSerializer):

    class Meta:
        model=ConnectedServer
        fields = ['host','api']


class GithubActorResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField(default=1)
    login = serializers.CharField(default='username1')
    display_login = serializers.CharField(default='username1')
    gravatar_id = serializers.CharField(default='')
    url = serializers.CharField(default='https://api.github.com/users/username1')
    avatar_url = serializers.CharField(default='https://avatars.githubusercontent.com/u/1?')

class GithubRepoResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField(default=1)
    name = serializers.CharField(default='username1/repo1')
    url = serializers.CharField(default='https://api.github.com/repos/username1/repo1')

class GithubPayloadResponseSerializer(serializers.Serializer):
    pass

class GithubResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField(default='1')
    type = serializers.CharField(default='DeleteEvent')
    actor = GithubActorResponseSerializer()
    repo = GithubRepoResponseSerializer()
    payload = GithubPayloadResponseSerializer()
    public = serializers.BooleanField(default=True)
    created_at = serializers.DateTimeField(default=timezone.now)
