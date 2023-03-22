from rest_framework import status
from InstaTonneApis.models import Follow, FollowSerializer, Post, PostSerializer, Comment, CommentSerializer, Like, LikeSerializer, Inbox
from django.http import HttpResponse
import json
from unittest.mock import patch, ANY, MagicMock
from InstaTonneApis.tests.test_api_abstract import AbstractApiTestCase, ORIGIN, HOST, AUTHORIZATION, HOST_ENCODED
import requests


class InboxApiTestCase(AbstractApiTestCase):
    @patch('requests.get')
    def test_get_author_inbox(self, mocked_get: MagicMock):
        inboxes = Inbox.objects.all().filter(author=1)
        return_values = {}
        serialized_data = []

        for inbox in inboxes:
            serialized_object = {}

            if 'like' in inbox.url:
                like: Like | None = Like.objects.all().filter(pk=inbox.url[-1]).first()
                if like is not None:
                    serialized_object = LikeSerializer(like).data
            elif 'follow' in inbox.url:
                follow: Follow | None = Follow.objects.all().filter(pk=inbox.url[-1]).first()
                if follow is not None:
                    serialized_object = FollowSerializer(follow).data
            elif 'comment' in inbox.url:
                comment: Comment | None = Comment.objects.all().filter(id_url=inbox.url).first()
                if comment is not None:
                    serialized_object = CommentSerializer(comment).data
            elif 'post' in inbox.url:
                post: Post | None = Post.objects.all().filter(id_url=inbox.url).first()
                if post is not None:
                    serialized_object = PostSerializer(post).data

            if serialized_object == {}:
                serialized_data.append({'error url': inbox.url})
                return_values[inbox.url] = inbox.url
            else:
                serialized_data.append(serialized_object)
                mock_response = requests.Response()
                mock_response.status_code = 200
                mock_response.headers['Content-Type'] = 'application/json'
                mock_response._content = json.dumps(serialized_object).encode('utf-8')
                return_values[inbox.url] = mock_response

        mocked_get.side_effect = lambda url, headers: return_values.get(url)
    
        response : HttpResponse = self.client.get(
            HOST + '/authors/1/inbox',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )
        
        assert mocked_get.call_count == inboxes.count()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get('Content-Type'), 'application/json')
        self.assertEqual(response.json(), {'type': 'inbox', 'author': HOST + '/authors/1', 'items': serialized_data})


    def test_post_author_inbox_post(self):
        response : HttpResponse = self.client.post(
            HOST + '/authors/1/inbox',
            {
                "type": "post",
                "id": HOST + "/authors/1/posts/1"
            },
            format='json',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        inbox = Inbox.objects.all().filter(
            url = HOST + "/authors/1/posts/1"
        ).first()
        assert inbox is not None


    def test_post_author_inbox_like_post(self):
        like = Like.objects.all().filter(
            summary = "test_post_author_inbox_like_post"
        ).first()
        assert like is None

        assert Inbox.objects.all().count() == 8
    
        response : HttpResponse = self.client.post(
            HOST + '/authors/1/inbox',
            {
                "summary": "test_post_author_inbox_like_post",
                "type": "like",
                "author": HOST + "/authors/2",
                "object": HOST + "/authors/1/posts/1"
            },
            format='json',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        assert Inbox.objects.all().count() == 9

        like = Like.objects.all().filter(
            type = "like",
            summary = "test_post_author_inbox_like_post",
            author = HOST + '/authors/2',
            post = 1
        ).first()
        assert like is not None

        inbox = Inbox.objects.all().filter(
            url = HOST + '/authors/1/posts/1/likes/' + like.id
        ).first()
        assert inbox is not None


    def test_post_author_inbox_like_comment(self):
        like = Like.objects.all().filter(
            summary = "test_post_author_inbox_like_comment"
        ).first()
        assert like is None

        assert Inbox.objects.all().count() == 8
    
        response : HttpResponse = self.client.post(
            HOST + '/authors/1/inbox',
            {
                "summary": "test_post_author_inbox_like_comment",
                "type": "like",
                "author": HOST + "/authors/2",
                "object": HOST + "/authors/1/posts/1/comments/1"
            },
            format='json',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        assert Inbox.objects.all().count() == 9

        like = Like.objects.all().filter(
            type = "like",
            summary = "test_post_author_inbox_like_comment",
            author = HOST + '/authors/2',
            comment = 1
        ).first()
        assert like is not None

        inbox = Inbox.objects.all().filter(
            url = HOST + '/authors/1/posts/1/comments/1/likes/' + like.id
        ).first()
        assert inbox is not None


    def test_post_author_inbox_comment(self):
        comment = Comment.objects.all().filter(
            comment = "test_post_author_inbox_comment"
        ).first()
        assert comment is None

        assert Inbox.objects.all().count() == 8
    
        response : HttpResponse = self.client.post(
            HOST + '/authors/1/inbox',
            {
                "type": "comment",
                "contentType": "content type",
                "comment": "test_post_author_inbox_comment",
                "author": HOST + "/authors/2",
                "post": HOST + "/authors/1/posts/1"
            },
            format='json',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        assert Inbox.objects.all().count() == 9

        comment = Comment.objects.all().filter(
            type = "comment",
            contentType = "content type",
            comment = "test_post_author_inbox_comment",
            author = HOST + '/authors/2',
            post = 1
        ).first()
        assert comment is not None

        inbox = Inbox.objects.all().filter(
            url = HOST + '/authors/1/posts/1/comments/' + comment.id
        ).first()
        assert inbox is not None


    def test_post_author_inbox_follow(self):
        follow = Follow.objects.all().filter(
            summary = "test_post_author_inbox_comment"
        ).first()
        assert follow is None

        assert Inbox.objects.all().count() == 8
    
        response : HttpResponse = self.client.post(
            HOST + '/authors/1/inbox',
            {
                "type": "follow",
                "summary":"test_post_author_inbox_comment",
                "actor":{
                    "id": HOST + "/authors/2"
                }
            },
            format='json',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        assert Inbox.objects.all().count() == 9

        follow = Follow.objects.all().filter(
            accepted = False,
            summary = "test_post_author_inbox_comment",
            follower_url = HOST + '/authors/2',
            object = 1
        ).first()
        assert follow is not None

        inbox = Inbox.objects.all().filter(
            url = HOST + '/authors/1/followers/' + HOST_ENCODED + "%2Fauthors%2F2/request"
        ).first()
        assert inbox is not None


    def test_delete_author_inbox(self):
        assert Inbox.objects.all().filter(author=1).count() == 8
    
        response : HttpResponse = self.client.delete(
            HOST + '/authors/1/inbox',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        assert Inbox.objects.all().filter(author=1).count() == 0
