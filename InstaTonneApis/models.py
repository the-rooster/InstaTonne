from django.db import models
from rest_framework import serializers


class Author(models.Model):
    url = models.TextField()
    host = models.TextField()
    displayName = models.TextField()
    github = models.TextField()
    profileImage = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)


class AuthorSerializer(serializers.Serializer):
    url = serializers.CharField()
    host = serializers.CharField()
    displayName = serializers.CharField()
    github = serializers.CharField()
    profileImage = serializers.CharField()

    created_at = serializers.DateTimeField()

class Follows(models.Model):

    author1Id = models.TextField()
    author2Id = models.TextField()

class Post(models.Model):
    url = models.TextField()
    title = models.TextField()
    source = models.TextField()
    origin = models.TextField()
    description = models.TextField()
    content_type = models.TextField()
    content = models.TextField()
    visibility = models.TextField()

    catagories  = models.CharField(max_length=100)
    unlisted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)


class Request(models.Model):
    summary = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    requester = models.ForeignKey(Author, related_name='requester', on_delete=models.CASCADE)
    requestee = models.ForeignKey(Author, related_name='requestee', on_delete=models.CASCADE)


class Like(models.Model):
    url = models.TextField()
    summary = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    url = models.TextField()
    content_type = models.TextField()
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
