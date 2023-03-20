from rest_framework import status
from InstaTonneApis.models import Comment, CommentSerializer
from django.http import HttpResponse
import json
from unittest.mock import patch, ANY, MagicMock
from InstaTonneApis.tests.test_api_abstract import AbstractApiTestCase, ORIGIN, HOST, AUTHORIZATION, HOST_ENCODED


class CommentApiTestCase(AbstractApiTestCase):
    def test_get_post_comments(self):
        expected_comment = Comment.objects.all().filter(id_url=HOST + '/authors/1/posts/1/comments/1').first()
        serialized_expected_comment = CommentSerializer(expected_comment).data
    
        response : HttpResponse = self.client.get(
            HOST + '/authors/1/posts/1/comments?page=1&size=1',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get('Content-Type'), 'application/json')
        self.assertEqual(response.json(), {
            'type': 'comments',
            'page': '1',
            'size': '1',
            'post': HOST + '/authors/1/posts/1',
            'id': HOST + '/authors/1/posts/1/comments',
            'comments': [serialized_expected_comment]
        })


    @patch('requests.get')
    def test_get_post_comments_remote(self, mocked_get: MagicMock):
        mocked_get.return_value = self.generic_mock_response()

        response : HttpResponse = self.client.get(
            HOST + '/authors/1/posts/' + HOST_ENCODED + '%2Fauthors%2F1%2Fposts%2F1/comments?page=1&size=1',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )

        mocked_get.assert_called_once_with(HOST + '/authors/1/posts/1/comments?page=1&size=1', headers=ANY)

        self.assert_generic_mock_response(response)


    def test_get_post_comment(self):
        comment = Comment.objects.all().filter(id_url=HOST + '/authors/1/posts/1/comments/1').first()
        serialized_comment = CommentSerializer(comment).data
    
        response : HttpResponse = self.client.get(
            HOST + '/authors/1/posts/1/comments/1',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get('Content-Type'), 'application/json')
        self.assertEqual(response.json(), serialized_comment)


    @patch('requests.post')
    def test_post_post_comments(self, mocked_post: MagicMock):
        mocked_post.return_value = self.generic_mock_response()
    
        response : HttpResponse = self.client.post(
            HOST + '/authors/1/posts/1/comments',
            {
                "contentType": "contentType3",
                "comment": "comment3"
            },
            format='json',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = json.dumps({
            "type": "comment",
            "contentType": "contentType3",
            "content": "comment3",
            "author": HOST + '/authors/1',
            "post": HOST + '/authors/1/posts/1'
        })

        mocked_post.assert_called_once_with(HOST + '/authors/1/inbox/', data, headers=ANY)


    @patch('requests.post')
    def test_post_post_comments_remote(self, mocked_post: MagicMock):
        mocked_post.return_value = self.generic_mock_response()
    
        response : HttpResponse = self.client.post(
            HOST + '/authors/1/posts/' + HOST_ENCODED + '%2Fauthors%2F1%2Fposts%2F1/comments',
            {
                "contentType": "contentType3",
                "comment": "comment3"
            },
            format='json',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = json.dumps({
            "type": "comment",
            "contentType": "contentType3",
            "content": "comment3",
            "author": HOST + '/authors/1',
            "post": HOST + '/authors/1/posts/1'
        })

        mocked_post.assert_called_once_with(HOST + '/authors/1/inbox/', data, headers=ANY)
