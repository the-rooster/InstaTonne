from rest_framework import status
from InstaTonneApis.models import Like, LikeSerializer
from django.http import HttpResponse
import json
from unittest.mock import patch, ANY, MagicMock
from InstaTonneApis.tests.test_api_abstract import AbstractApiTestCase, ORIGIN, HOST, AUTHORIZATION, HOST_ENCODED


class LikeApiTestCase(AbstractApiTestCase):
    def test_get_post_likes(self):
        expected_like = Like.objects.all().filter(pk=1).first()
        serialized_expected_like = LikeSerializer(expected_like).data
        serialized_expected_like['object'] = HOST + '/authors/1/posts/1'
        del serialized_expected_like['post']
        del serialized_expected_like['comment']
    
        response : HttpResponse = self.client.get(
            HOST + '/authors/1/posts/1/likes',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get('Content-Type'), 'application/json')
        self.assertEqual(response.json(), {
            'type': 'likes',
            'items': [serialized_expected_like]
        })

    
    def test_get_comment_likes(self):
        expected_like = Like.objects.all().filter(pk=2).first()
        serialized_expected_like = LikeSerializer(expected_like).data
        serialized_expected_like['object'] = HOST + '/authors/1/posts/1/comments/1'
        del serialized_expected_like['post']
        del serialized_expected_like['comment']
    
        response : HttpResponse = self.client.get(
            HOST + '/authors/1/posts/1/comments/1/likes',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get('Content-Type'), 'application/json')
        self.assertEqual(response.json(), {
            'type': 'likes',
            'items': [serialized_expected_like]
        })


    @patch('requests.get')
    def test_get_post_likes_remote(self, mocked_get: MagicMock):
        mocked_get.return_value = self.generic_mock_response()

        response : HttpResponse = self.client.get(
            HOST + '/authors/1/posts/' + HOST_ENCODED + '%2Fauthors%2F1%2Fposts%2F1/likes',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )

        mocked_get.assert_called_once_with(HOST + '/authors/1/posts/1/likes', headers=ANY)

        self.assert_generic_mock_response(response)


    @patch('requests.get')
    def test_get_comment_likes_remote(self, mocked_get: MagicMock):
        mocked_get.return_value = self.generic_mock_response()

        response : HttpResponse = self.client.get(
            HOST + '/authors/1/posts/1/comments/' + HOST_ENCODED + '%2Fauthors%2F1%2Fposts%2F1%2Fcomments%2F1/likes',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )

        mocked_get.assert_called_once_with(HOST + '/authors/1/posts/1/comments/1/likes', headers=ANY)

        self.assert_generic_mock_response(response)


    def test_get_post_like(self):
        like = Like.objects.all().filter(pk=1).first()
        serialized_like = LikeSerializer(like).data
        serialized_like['object'] = HOST + '/authors/1/posts/1'
        del serialized_like['post']
        del serialized_like['comment']
    
        response : HttpResponse = self.client.get(
            HOST + '/authors/1/posts/1/likes/1',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get('Content-Type'), 'application/json')
        self.assertEqual(response.json(), serialized_like)


    def test_get_comment_like(self):
        like = Like.objects.all().filter(pk=2).first()
        serialized_like = LikeSerializer(like).data
        serialized_like['object'] = HOST + '/authors/1/posts/1/comments/1'
        del serialized_like['post']
        del serialized_like['comment']
    
        response : HttpResponse = self.client.get(
            HOST + '/authors/1/posts/1/comments/1/likes/2',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get('Content-Type'), 'application/json')
        self.assertEqual(response.json(), serialized_like)


    @patch('requests.post')
    def test_post_post_likes(self, mocked_post: MagicMock):
        mocked_post.return_value = self.generic_mock_response()
    
        response : HttpResponse = self.client.post(
            HOST + '/authors/1/posts/1/likes',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = json.dumps({
            "type": "like",
            "author": HOST + '/authors/1',
            "object": HOST + '/authors/1/posts/1',
            "summary": "An author liked your post!"
        })

        mocked_post.assert_called_once_with(HOST + '/authors/1/inbox/', data, headers=ANY)


    @patch('requests.post')
    def test_post_comment_likes(self, mocked_post: MagicMock):
        mocked_post.return_value = self.generic_mock_response()
    
        response : HttpResponse = self.client.post(
            HOST + '/authors/1/posts/1/comments/1/likes',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = json.dumps({
            "type": "like",
            "author": HOST + '/authors/1',
            "object": HOST + '/authors/1/posts/1/comments/1',
            "summary": "An author liked your comment!"
        })

        mocked_post.assert_called_once_with(HOST + '/authors/1/inbox/', data, headers=ANY)


    @patch('requests.post')
    def test_post_post_likes_remote(self, mocked_post: MagicMock):
        mocked_post.return_value = self.generic_mock_response()
    
        response : HttpResponse = self.client.post(
            HOST + '/authors/1/posts/' + HOST_ENCODED + '%2Fauthors%2F1%2Fposts%2F1/likes',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = json.dumps({
            "type": "like",
            "author": HOST + '/authors/1',
            "object": HOST + '/authors/1/posts/1',
            "summary": "An author liked your post!"
        })

        mocked_post.assert_called_once_with(HOST + '/authors/1/inbox/', data, headers=ANY)


    @patch('requests.post')
    def test_post_comment_likes_remote(self, mocked_post: MagicMock):
        mocked_post.return_value = self.generic_mock_response()
    
        response : HttpResponse = self.client.post(
            HOST + '/authors/1/posts/' + HOST_ENCODED + '%2Fauthors%2F1%2Fposts%2F1%2Fcomments%2F1/likes',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = json.dumps({
            "type": "like",
            "author": HOST + '/authors/1',
            "object": HOST + '/authors/1/posts/1/comments/1',
            "summary": "An author liked your comment!"
        })

        mocked_post.assert_called_once_with(HOST + '/authors/1/inbox/', data, headers=ANY)
