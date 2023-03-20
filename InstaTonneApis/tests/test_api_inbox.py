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
