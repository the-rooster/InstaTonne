from rest_framework import status
from InstaTonneApis.models import Author, Follow, Post, PostSerializer, Comment
from django.http import HttpResponse
import json
from unittest.mock import patch, ANY, MagicMock
from InstaTonneApis.tests.test_api_abstract import AbstractApiTestCase, ORIGIN, HOST, AUTHORIZATION, HOST_ENCODED


class PostApiTestCase(AbstractApiTestCase):
    def test_get_author_posts(self):
        author: Author | None = Author.objects.all().filter(id_url=HOST + '/authors/1').first()

        if author is None:
            return HttpResponse(status=404)

        posts = Post.objects.all().filter(author=1).order_by("published")

        serialized_data = []
        for post in posts:
            serialized_post = PostSerializer(post).data
            comments_url = HOST + '/authors/' + author.id + '/posts/' + post.id + '/comments'
            comment_count = Comment.objects.all().filter(post=post.id).count()
            serialized_post["count"] = comment_count
            serialized_post["comments"] = comments_url

            serialized_data.append(serialized_post)

        response : HttpResponse = self.client.get(
            HOST + '/authors/1/posts?page=1&size=5',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get('Content-Type'), 'application/json')
        self.assertEqual(response.json(), {'type': 'posts', 'items': serialized_data})


    @patch('requests.get')
    def test_get_authors_posts_remote(self, mocked_get: MagicMock):
        mocked_get.return_value = HttpResponse(content=json.dumps({"items" : [{"visibility" : "PUBLIC","title" : "MOCK TITLE"}]}),status=200,content_type="application/json")

        response : HttpResponse = self.client.get(
            HOST + '/authors/' + HOST_ENCODED + '%2Fauthors%2F1/posts?page=1&size=1',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )

        mocked_get.assert_called_once_with(HOST + '/authors/1/posts?page=1&size=1', headers=ANY)

        self.assertEqual(mocked_get.return_value.status_code,response.status_code)
        self.assertEqual(mocked_get.return_value.content,response.content)


    @patch('requests.post')
    def test_post_author(self, mocked_post: MagicMock):
        mocked_post.return_value = self.generic_mock_response()

        post = Post.objects.all().filter(
            type="post",
            title="title3",
            source="source3",
            origin="origin3",
            description="description3",
            contentType="contentType3",
            content="content3",
            visibility="PUBLIC",
            categories=["cat0", "cat1", "cat2"],
            unlisted=False,
            author=1
        ).first()
        assert post is None
    
        response : HttpResponse = self.client.post(
            HOST + '/authors/1/posts',
            {
                "title" : "title3",
                "source" : "source3",
                "origin" : "origin3",
                "description" : "description3",
                "contentType" : "contentType3",
                "content" : "content3",
                "visibility" : "PUBLIC",
                "categories" : ["cat0", "cat1", "cat2"],
                "unlisted" : False
            },
            format='json',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        post = Post.objects.all().filter(
            type="post",
            title="title3",
            source="source3",
            origin="origin3",
            description="description3",
            contentType="contentType3",
            content="content3",
            visibility="PUBLIC",
            categories=["cat0", "cat1", "cat2"],
            unlisted=False,
            author=1
        ).first()
        assert post is not None

        data = json.dumps({
            "type" : "post",
            "id" : post.id_url
        })
        follows = Follow.objects.all().filter(object=1)
        print("TESTTEST: ",mocked_post.call_count,follows.count())
        assert mocked_post.call_count == follows.count() + 1
        for follow in follows:
            mocked_post.assert_any_call(follow.follower_url + '/inbox/', data, headers=ANY)

    
    def test_get_author_post(self):
        post = Post.objects.all().filter(id_url=HOST + '/authors/1/posts/1').first()
        serialized_post = PostSerializer(post).data
    
        response : HttpResponse = self.client.get(
            HOST + '/authors/1/posts/1',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )

        serialized_post['count'] = Comment.objects.all().filter(post=1).count()
        serialized_post['comments'] = HOST + '/authors/1/posts/1/comments'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get('Content-Type'), 'application/json')
        self.assertEqual(response.json(), serialized_post)


    @patch('requests.get')
    def test_get_author_post_remote(self, mocked_get: MagicMock):
        mocked_get.return_value = HttpResponse(content=json.dumps({"visibility" : "PUBLIC"}),status=200,content_type="application/json")

        response : HttpResponse = self.client.get(
            HOST + '/authors/1/posts/' + HOST_ENCODED + '%2Fauthors%2F1%2Fposts%2F1',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )

        mocked_get.assert_called_once_with(HOST + '/authors/1/posts/1', headers=ANY)

        self.assertEqual(mocked_get.return_value.status_code,response.status_code)
        self.assertEqual(mocked_get.return_value.content,response.content)


    def test_post_author_post(self):
        expected_post_before = Post.objects.all().filter(id_url=HOST + '/authors/1/posts/1').first()
        serialized_expected_post_before = PostSerializer(expected_post_before).data
    
        response : HttpResponse = self.client.post(
            HOST + '/authors/1/posts/1',
            {
                "title": "title3",
                "description": "description3",
                "contentType": "contentType3",
                "content": "content3",
                "visibility": "PUBLIC",
                "categories": ["cat0", "cat1", "cat2"],
                "unlisted": False
            },
            format='json',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )

        serialized_expected_post_before["title"] = "title3"
        serialized_expected_post_before["description"] = "description3"
        serialized_expected_post_before["contentType"] = "contentType3"
        serialized_expected_post_before["content"] = "content3"
        serialized_expected_post_before["visibility"] = "PUBLIC"
        serialized_expected_post_before["categories"] = ["cat0", "cat1", "cat2"]
        serialized_expected_post_before["unlisted"] = False

        expected_author_after = Post.objects.all().filter(id_url=HOST + '/authors/1/posts/1').first()
        serialized_expected_author_after = PostSerializer(expected_author_after).data

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(serialized_expected_post_before, serialized_expected_author_after)


    def test_delete_author_post(self):
        post = Post.objects.all().filter(id_url=HOST + '/authors/1/posts/1').first()
        assert post is not None

        response : HttpResponse = self.client.delete(
            HOST + '/authors/1/posts/1',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        post = Post.objects.all().filter(id_url=HOST + '/authors/1/posts/1').first()
        assert post is None

    
    @patch('requests.post')
    def test_put_author_post(self, mocked_post: MagicMock):
        mocked_post.return_value = self.generic_mock_response()

        post = Post.objects.all().filter(
            id_url=HOST + '/authors/1/posts/4'
        ).first()
        assert post is None
    
        response : HttpResponse = self.client.put(
            HOST + '/authors/1/posts/4',
            {
                "title" : "title3",
                "source" : "source3",
                "origin" : "origin3",
                "description" : "description3",
                "contentType" : "contentType3",
                "content" : "content3",
                "visibility" : "PUBLIC",
                "categories" : ["cat0", "cat1", "cat2"],
                "unlisted" : False
            },
            format='json',
            HTTP_AUTHORIZATION=AUTHORIZATION,
            HTTP_ORIGIN=ORIGIN
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        post = Post.objects.all().filter(
            id_url=HOST + '/authors/1/posts/4',
            title="title3",
            source="source3",
            origin="origin3",
            description="description3",
            contentType="contentType3",
            content="content3",
            visibility="PUBLIC",
            categories=["cat0", "cat1", "cat2"],
            unlisted=False
        ).first()
        assert post is not None

        data = json.dumps({
            "type" : "post",
            "id" : post.id_url
        })
        follows = Follow.objects.all().filter(object=1)
        assert mocked_post.call_count == follows.count()
        for follow in follows:
            mocked_post.assert_any_call(follow.follower_url + '/inbox/', data, headers=ANY)
