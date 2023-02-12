from django.db import models
from rest_framework import serializers


class Author(models.Model):
    url = models.TextField()
    host = models.TextField()
    displayName = models.TextField()
    github = models.TextField()
    profileImage = models.TextField()

    published = models.DateTimeField(auto_now_add=True)


class AuthorSerializer(serializers.Serializer):
    url = serializers.CharField()
    host = serializers.CharField()
    displayName = serializers.CharField()
    github = serializers.CharField()
    profileImage = serializers.CharField()

    published = serializers.DateTimeField()


class Follow(models.Model):
    followerAuthorId = models.TextField()
    followeeAuthorId = models.TextField()


class Post(models.Model):
    url = models.TextField()
    title = models.TextField()
    source = models.TextField()
    origin = models.TextField()
    description = models.TextField()
    contentType = models.TextField()
    content = models.TextField()
    visibility = models.TextField()

    catagories  = models.CharField(max_length=100)
    unlisted = models.BooleanField(default=False)
    published = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)


class Request(models.Model):
    summary = models.TextField()

    published = models.DateTimeField(auto_now_add=True)

    requester = models.ForeignKey(Author, related_name='requester', on_delete=models.CASCADE)
    requestee = models.ForeignKey(Author, related_name='requestee', on_delete=models.CASCADE)


class Like(models.Model):
    url = models.TextField()
    summary = models.TextField()

    published = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    url = models.TextField()
    contentType = models.TextField()
    content = models.TextField()

    published = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
