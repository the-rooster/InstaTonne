from rest_framework import status
from InstaTonneApis.models import Author, AuthorSerializer
from django.http import HttpResponse
from unittest.mock import patch, ANY, MagicMock
from InstaTonneApis.tests.test_api_abstract import AbstractApiTestCase, ORIGIN, HOST, AUTHORIZATION, HOST_ENCODED


class AuthorApiTestCase(AbstractApiTestCase):
    def test_get_authors(self):
        expected_author = Author.objects.all().filter(id_url=HOST + '/authors/1').first()
        serialized_expected_author = AuthorSerializer(expected_author).data
    
        response : HttpResponse = self.client.get(
            HOST + '/authors?page=1&size=1',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get('Content-Type'), 'application/json')
        self.assertEqual(response.json(), {'type': 'authors', 'items': [serialized_expected_author]})


    @patch('requests.get')
    def test_get_authors_remote(self, mocked_get: MagicMock):
        mocked_get.return_value = self.generic_mock_response()

        response : HttpResponse = self.client.get(
            HOST + '/remote-authors/' + HOST_ENCODED + '%2Fauthors%3Fpage%3D1%26size%3D1',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )

        mocked_get.assert_called_once_with(HOST + '/authors?page=1&size=1', headers=ANY)

        self.assert_generic_mock_response(response)


    def test_get_author(self):
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


    @patch('requests.get')
    def test_get_author_remote(self, mocked_get: MagicMock):
        mocked_get.return_value = self.generic_mock_response()

        response : HttpResponse = self.client.get(
            HOST + '/authors/' + HOST_ENCODED + '%2Fauthors%2F1',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )

        mocked_get.assert_called_once_with(HOST + '/authors/1', headers=ANY)

        self.assert_generic_mock_response(response)


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
