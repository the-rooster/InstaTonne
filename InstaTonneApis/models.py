from django.db import models
from rest_framework import serializers
import json


class Author(models.Model):
    type = models.TextField()
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
        fields = '__all__'


class Follow(models.Model):
    followerAuthorId = models.ForeignKey(Author, related_name='followerAuthorId', on_delete=models.CASCADE)
    followeeAuthorId = models.ForeignKey(Author, related_name='followeeAuthorId', on_delete=models.CASCADE)


class FollowSerializer(serializers.ModelSerializer):
    followerAuthorId = AuthorSerializer()
    followeeAuthorId = AuthorSerializer()

    class Meta:
        model = Follow
        fields = '__all__'


class Post(models.Model):
    type = models.TextField()
    url = models.TextField()
    title = models.TextField()
    source = models.TextField()
    origin = models.TextField()
    description = models.TextField()
    contentType = models.TextField()
    content = models.TextField()
    visibility = models.TextField()

    categories  = models.CharField(max_length=100)
    unlisted = models.BooleanField(default=False)
    published = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    categories = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'

    def get_categories(self, instance):
        return json.loads(instance.categories.replace("'", '"'))


class Request(models.Model):
    summary = models.TextField()

    published = models.DateTimeField(auto_now_add=True)

    requester = models.ForeignKey(Author, related_name='requester', on_delete=models.CASCADE)
    requestee = models.ForeignKey(Author, related_name='requestee', on_delete=models.CASCADE)


class Like(models.Model):
    type = models.TextField()
    url = models.TextField()
    summary = models.TextField()

    published = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    type = models.TextField()
    url = models.TextField()
    contentType = models.TextField()
    comment = models.TextField()

    published = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
