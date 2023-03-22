from rest_framework import status
from InstaTonneApis.models import Author, AuthorSerializer, Follow
from django.http import HttpResponse
import json
from unittest.mock import patch, ANY, MagicMock
import requests
from InstaTonneApis.tests.test_api_abstract import AbstractApiTestCase, ORIGIN, HOST, AUTHORIZATION, HOST_ENCODED


class FollowerApiTestCase(AbstractApiTestCase):
    @patch('requests.get')
    def test_get_author_followers(self, mocked_get: MagicMock):
        follows = Follow.objects.all().filter(object=1)
        return_values = {}
        serialized_data = []

        for follow in follows:
            author: Author | None = Author.objects.all().filter(id_url=follow.follower_url).first()

            if author is None:
                serialized_data.append({'error url': follow.follower_url})

                return_values[follow.follower_url] = follow.follower_url
            else:
                serialized_author = AuthorSerializer(author).data
                serialized_data.append(serialized_author)
            
                mock_response = requests.Response()
                mock_response.status_code = 200
                mock_response.headers['Content-Type'] = 'application/json'
                mock_response._content = json.dumps(serialized_author).encode('utf-8')
                return_values[follow.follower_url] = mock_response

        mocked_get.side_effect = lambda url, headers: return_values.get(url)
    
        response : HttpResponse = self.client.get(
            HOST + '/authors/1/followers',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )
        
        assert mocked_get.call_count == follows.count()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get('Content-Type'), 'application/json')
        self.assertEqual(response.json(), {'type': 'followers', 'items': serialized_data})


    @patch('requests.get')
    def test_get_author_followers_remote(self, mocked_get: MagicMock):
        mocked_get.return_value = self.generic_mock_response()

        response : HttpResponse = self.client.get(
            HOST + '/authors/' + HOST_ENCODED + '%2Fauthors%2F1/followers',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )

        mocked_get.assert_called_once_with(HOST + '/authors/1/followers', headers=ANY)

        self.assert_generic_mock_response(response)


    def test_get_author_follower(self):
        follow = Follow.objects.all().filter(object=1, follower_url=HOST + '/authors/2').first()
        assert follow is not None
    
        response : HttpResponse = self.client.get(
            HOST + '/authors/1/followers/' + HOST_ENCODED + '%2Fauthors%2F2',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    @patch('requests.get')
    def test_get_author_follower_remote(self, mocked_get: MagicMock):
        mocked_get.return_value = self.generic_mock_response()

        response : HttpResponse = self.client.get(
            HOST + '/authors/' + HOST_ENCODED + '%2Fauthors%2F1/followers/' + HOST_ENCODED + '%2Fauthors%2F2',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )

        mocked_get.assert_called_once_with(HOST + '/authors/1/followers/' + HOST_ENCODED + '%2Fauthors%2F2', headers=ANY)

        self.assert_generic_mock_response(response)
    

    @patch('requests.post')
    @patch('requests.get')
    def test_post_author_follower(self, mocked_get: MagicMock, mocked_post: MagicMock):
        author_local = Author.objects.all().filter(id_url=HOST + '/authors/1').first()
        serialized_author_local = AuthorSerializer(author_local).data

        author_foreign = Author.objects.all().filter(id_url=HOST + '/authors/2').first()
        serialized_author_foreign = AuthorSerializer(author_foreign).data

        data = json.dumps({
            "type": "follow",
            "actor": serialized_author_local,
            "object": serialized_author_foreign,
            "summary": serialized_author_local['displayName'] + " wants to follow " + serialized_author_foreign['displayName']
        })

        mock_response_get = requests.Response()
        mock_response_get.status_code = 200
        mock_response_get.headers['Content-Type'] = 'application/json'
        mock_response_get._content = json.dumps(serialized_author_foreign).encode('utf-8')

        mock_response_post = requests.Response()
        mock_response_post.status_code = 200
        mock_response_post.headers['Content-Type'] = 'application/json'
        mock_response_post._content = ''.encode('utf-8')

        mocked_get.return_value = mock_response_get
        mocked_post.return_value = mock_response_post

        response : HttpResponse = self.client.post(
            HOST + '/authors/1/followers/' + HOST_ENCODED + '%2Fauthors%2F2',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )

        mocked_get.assert_called_once_with(HOST + '/authors/2', headers=ANY)
        mocked_post.assert_called_once_with(HOST + '/authors/2/inbox/', data, headers=ANY)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    def test_delete_author_follower(self):
        follow = Follow.objects.all().filter(object=1, follower_url=HOST + '/authors/2').first()
        assert follow is not None

        response : HttpResponse = self.client.delete(
            HOST + '/authors/1/followers/' + HOST_ENCODED + '%2Fauthors%2F2',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        follow = Follow.objects.all().filter(object=1, follower_url=HOST + '/authors/2').first()
        assert follow is None

    
    def test_put_author_follower(self):
        follow = Follow.objects.all().filter(object=1, follower_url=HOST + '/authors/2').first()
        assert follow is not None
        follow.accepted = False
        follow.save()

        response : HttpResponse = self.client.put(
            HOST + '/authors/1/followers/' + HOST_ENCODED + '%2Fauthors%2F2',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        follow = Follow.objects.all().filter(object=1, follower_url=HOST + '/authors/2').first()
        assert follow is not None
        assert follow.accepted == True
