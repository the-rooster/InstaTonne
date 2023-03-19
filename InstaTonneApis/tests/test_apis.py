from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from InstaTonneApis.models import Author, AuthorSerializer, Follow, FollowSerializer
from django.http import HttpResponse
import json
from http.cookies import SimpleCookie
from unittest.mock import patch, ANY
import requests


ORIGIN = 'http://127.0.0.1:5173'
HOST = 'http://127.0.0.1:8000'
HOST_ENCODED = 'http%3A%2F%2F127%2E0%2E0%2E1%3A8000'
AUTHORIZATION = ''


def equal_dict_lists(list1, list2):
    return len(list1) == len(list2) and all(x in list2 for x in list1)


class APITestCases(TestCase):
    fixtures = ['InstaTonneApis/fixtures/initial_data.json']


    def setUp(self):
        self.client = APIClient()
        self.client.login(username='username1', password='password1')

    
    def test_get_authors(self):
        self.get_authors(HOST + '/authors?page=1&size=1')
        self.get_authors(HOST + '/remote-authors/' + HOST_ENCODED + '%2Fauthors%3Fpage%3D1%26size%3D1')
    def get_authors(self, path):
        expected_author = Author.objects.all().filter(id_url=HOST + '/authors/1').first()
        serialized_expected_author = AuthorSerializer(expected_author).data
    
        response : HttpResponse = self.client.get(
            path,
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get('Content-Type'), 'application/json')
        self.assertEqual(response.json()['type'], 'authors')
        self.assertEqual(response.json()['items'], [serialized_expected_author])


    def test_get_author(self):
        self.get_author(HOST + '/authors/1')
        self.get_author(HOST + '/authors/' + HOST_ENCODED + '%2Fauthors%2F1')
    def get_author(self, path):
        expected_author = Author.objects.all().filter(id_url=HOST + '/authors/1').first()
        serialized_expected_author = AuthorSerializer(expected_author).data
    
        response : HttpResponse = self.client.get(
            path,
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get('Content-Type'), 'application/json')
        self.assertEqual(response.json(), serialized_expected_author)


    def test_post_author(self):
        expected_author_before = Author.objects.all().filter(id_url=HOST + '/authors/1').first()
        serialized_expected_author_before = AuthorSerializer(expected_author_before).data
    
        response : HttpResponse = self.client.post(
            HOST + '/authors/1',
            {
                "displayName": "displayName2",
                "github": "github2",
                "profileImage": "profileImage2"
            },
            format='json',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )

        serialized_expected_author_before['displayName'] = 'displayName2'
        serialized_expected_author_before['github'] = 'github2'
        serialized_expected_author_before['profileImage'] = 'profileImage2'

        expected_author_after = Author.objects.all().filter(id_url=HOST + '/authors/1').first()
        serialized_expected_author_after = AuthorSerializer(expected_author_after).data

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(serialized_expected_author_before, serialized_expected_author_after)


    @patch('requests.get')
    def test_get_author_followers(self, mocked_get):
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
    def test_get_author_followers_remote(self, mocked_get):
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response.headers['Content-Type'] = 'application/json'
        mock_response._content = '{"mock_key": "mock_value"}'.encode('utf-8')
        return_values = { HOST + '/authors/1/followers': mock_response }

        mocked_get.side_effect = lambda url, headers: return_values.get(url)

        response : HttpResponse = self.client.get(
            HOST + '/authors/' + HOST_ENCODED + '%2Fauthors%2F1/followers',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )

        mocked_get.assert_called_once_with(HOST + '/authors/1/followers', headers=ANY)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get('Content-Type'), 'application/json')
        self.assertEqual(response.json(), {'mock_key': 'mock_value'})


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
    def test_get_author_follower_remote(self, mocked_get):
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response.headers['Content-Type'] = 'application/json'
        mock_response._content = '{"mock_key": "mock_value"}'.encode('utf-8')
        return_values = { HOST + '/authors/1/followers/' + HOST_ENCODED + '%2Fauthors%2F2': mock_response }

        mocked_get.side_effect = lambda url, headers: return_values.get(url)

        response : HttpResponse = self.client.get(
            HOST + '/authors/' + HOST_ENCODED + '%2Fauthors%2F1/followers/' + HOST_ENCODED + '%2Fauthors%2F2',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )

        mocked_get.assert_called_once_with(HOST + '/authors/1/followers/' + HOST_ENCODED + '%2Fauthors%2F2', headers=ANY)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get('Content-Type'), 'application/json')
        self.assertEqual(response.json(), {'mock_key': 'mock_value'})
    

    @patch('requests.post')
    @patch('requests.get')
    def test_post_author_follower(self, mocked_get, mocked_post):
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
