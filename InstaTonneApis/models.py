from django.db import models
from rest_framework import serializers
import json
import uuid
from InstaTonne.settings import HOSTNAME

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
    class Meta:
        model = Author
        fields = ['type', 'id_url', 'url', 'host', 'displayName', 'github', 'profileImage'] # ??? userID and active not here, should they be?

    def create(self, validated_data):
        return Author.objects.create(**validated_data)


class Follow(models.Model):
    id = models.TextField(primary_key=True, default=default_id_generator, editable=False)
    object = models.ForeignKey(Author,on_delete=models.CASCADE)
    follower_url = models.TextField()
    summary = models.TextField()
    accepted = models.BooleanField()


class FollowSerializer(serializers.ModelSerializer):
    object = AuthorSerializer()

    class Meta:
        model = Follow
        fields = ['object','summary','accepted']


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
    author = AuthorSerializer()
    categories = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ['type', 'title', 'id_url', 'source', 'origin', 'description', 'contentType',
                  'content', 'author', 'categories', 'published', 'visibility', 'unlisted']

    def get_categories(self, instance):
        return json.loads(instance.categories.replace("'", '"'))
    
    def create(self, validated_data):
        return Post.objects.create(**validated_data)


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

class Comment(models.Model):
    id = models.TextField(primary_key=True, default=default_id_generator, editable=False)
    type = models.TextField()
    id_url = models.TextField()
    contentType = models.TextField()
    comment = models.TextField()

    published = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,null=True)


class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Comment
        fields = ['type', 'id_url', 'contentType', 'comment', 'published', 'author']


class Like(models.Model):
    id = models.TextField(primary_key=True, default=default_id_generator, editable=False)
    type = models.TextField()
    context = models.TextField()
    summary = models.TextField()

    published = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)


class LikeSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Like
        fields = ['type', 'context', 'summary', 'author', 'post', 'comment']


class Inbox(models.Model):
    author = models.ForeignKey(Author,on_delete=models.CASCADE)
    url = models.TextField()