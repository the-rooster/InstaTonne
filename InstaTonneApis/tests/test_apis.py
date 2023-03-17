from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from InstaTonneApis.models import Author, AuthorSerializer, Follow, FollowSerializer
from django.http import HttpResponse
import json
from http.cookies import SimpleCookie


ORIGIN = 'http://127.0.0.1:5173'
HOST = 'http://127.0.0.1:8000'
AUTHORIZATION = ''


def equal_dict_lists(list1, list2):
    return len(list1) == len(list2) and all(x in list2 for x in list1)


class APITestCases(TestCase):
    fixtures = ['InstaTonneApis/fixtures/initial_data.json']


    def setUp(self):
        self.client = APIClient()
        self.client.login(username='username1', password='password1')


    def test_authors_get(self):
        expected_author = Author.objects.all().filter(id_url=HOST + '/authors/1').first()
        serialized_expected_author = AuthorSerializer(expected_author).data
    
        response : HttpResponse = self.client.get(
            HOST + '/authors?page=1&size=1',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get('Content-Type'), 'application/json')
        self.assertEqual(response.json()['type'], 'authors')
        self.assertEqual(response.json()['items'], [serialized_expected_author])


    def test_authors_get_remote(self):
        expected_author = Author.objects.all().filter(id_url=HOST + '/authors/1').first()
        serialized_expected_author = AuthorSerializer(expected_author).data
    
        response : HttpResponse = self.client.get(
            HOST + '/remote-authors/http%3A%2F%2F127%2E0%2E0%2E1%3A8000%2Fauthors%3Fpage%3D1%26size%3D1',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get('Content-Type'), 'application/json')
        self.assertEqual(response.json()['type'], 'authors')
        self.assertEqual(response.json()['items'], [serialized_expected_author])


    def test_author_get(self):
        expected_author = Author.objects.all().filter(id_url=HOST + '/authors/1').first()
        serialized_expected_author = AuthorSerializer(expected_author).data
    
        response : HttpResponse = self.client.get(
            HOST + '/authors/1',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get('Content-Type'), 'application/json')
        self.assertEqual(response.json(), serialized_expected_author)


    def test_author_get_remote(self):
        expected_author = Author.objects.all().filter(id_url=HOST + '/authors/1').first()
        serialized_expected_author = AuthorSerializer(expected_author).data
    
        response : HttpResponse = self.client.get(
            HOST + '/authors/http%3A%2F%2F127%2E0%2E0%2E1%3A8000%2Fauthors%2F1',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get('Content-Type'), 'application/json')
        self.assertEqual(response.json(), serialized_expected_author)


    def test_author_post(self):
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

    
    def test_author_followers_get(self):
        follows = Follow.objects.all().filter(object=1)
        serialized_data = []
        for follow in follows:
            serialized_follow = FollowSerializer(follow).data
            actor = Author.objects.all().filter(id_url=serialized_follow['actor']).first()

            if actor is None:
                serialized_data.append({'error': 'url not connected to this server'})
            else:
                serialized_actor = AuthorSerializer(actor).data
                serialized_data.append(serialized_actor)
    
        response : HttpResponse = self.client.get(
            HOST + '/authors/1/followers',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get('Content-Type'), 'application/json')
        self.assertEqual(response.json()['type'], 'followers')
        self.assertTrue(equal_dict_lists(serialized_data, response.json()['items']))
