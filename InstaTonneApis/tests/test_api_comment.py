from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from InstaTonneApis.models import Comment, CommentSerializer
from django.http import HttpResponse
import json
from unittest.mock import patch, ANY, MagicMock
import requests


ORIGIN = 'http://127.0.0.1:5173'
HOST = 'http://127.0.0.1:8000'
HOST_ENCODED = 'http%3A%2F%2F127%2E0%2E0%2E1%3A8000'
AUTHORIZATION = ''


class CommentAPI(TestCase):
    fixtures = ['InstaTonneApis/fixtures/initial_data.json']


    def setUp(self):
        self.client = APIClient()
        self.client.login(username='username1', password='password1')


    def generic_mock_response(self) -> requests.Response:
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response.headers['Content-Type'] = 'application/json'
        mock_response._content = '{"mock_key": "mock_value"}'.encode('utf-8')
        return mock_response


    def assert_generic_mock_response(self, response: HttpResponse) -> None:
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get('Content-Type'), 'application/json')
        self.assertEqual(response.json(), {'mock_key': 'mock_value'})


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
