from collections import OrderedDict
from django.test import TestCase
from ..models import Author, Follow, Post, Request, Comment, Like, Inbox, AuthorSerializer, FollowSerializer, PostSerializer, RequestSerializer, CommentSerializer, LikeSerializer

def get_author_object(index: int):
    if index == 1:
        return Author.objects.create(
            type='author',
            id_url='https://example.com/author/1',
            url='https://example.com/author/1',
            host='example.com',
            displayName='John Doe',
            github='https://github.com/johndoe',
            profileImage='https://example.com/profile.jpg',
            userID='johndoe123',
            active=True
        )
    elif index == 2:
        return Author.objects.create(
            type='author',
            id_url='http://localhost:8000/author/2/',
            url='http://localhost:8000/author/2/',
            host='http://localhost:8000/',
            displayName='Jane Doe',
            github='https://github.com/janedoe',
            profileImage='https://example.com/janedoe.jpg',
            userID='janedoe',
            active=True
        )
    elif index == 3:
        return Author.objects.create(
            type='author',
            id_url='http://localhost:8000/author/3/',
            url='http://localhost:8000/author/3/',
            host='http://localhost:8000/',
            displayName='Alice Smith',
            github='https://github.com/alicesmith',
            profileImage='https://example.com/alicesmith.jpg',
            userID='alicesmith',
            active=True
        )
    
def get_author_data(index: int):
    if index == 1:
        return {
            'type': 'author',
            'id_url': 'https://example.com/author/1',
            'url': 'https://example.com/author/1',
            'host': 'example.com',
            'displayName': 'John Doe',
            'github': 'https://github.com/johndoe',
            'profileImage': 'https://example.com/profile.jpg',
            'userID': 'johndoe123',
            'active': True
        }
    elif index == 2:
        return {
            'type': 'author',
            'id_url': 'https://example.com/author/2',
            'url': 'https://example.com/author/2',
            'host': 'example.com',
            'displayName': 'Jane Doe',
            'github': 'https://github.com/janedoe',
            'profileImage': 'https://example.com/profile.jpg',
            'userID': 'janedoe123',
            'active': False
        }

    
def get_post_object(author: Author):
    return Post.objects.create(
        type='post',
        id_url='http://localhost:8000/posts/1/',
        title='Test Post',
        source='http://localhost:8000/posts/1/',
        origin='http://localhost:8000/posts/1/',
        description='This is a test post.',
        contentType='text/plain',
        content='Hello, world!',
        visibility='PUBLIC',
        comments='This is a comment.',
        categories='test',
        unlisted=False,
        author=author
    )

def get_post_data(index: int, author: Author):
        if index == 1:
            return {
                'type': 'post',
                'id_url': 'https://example.com/post/1',
                'title': 'Test post',
                'source': 'https://example.com/post/1',
                'origin': 'https://example.com',
                'description': 'This is a test post',
                'contentType': 'text/plain',
                'content': 'Hello, world!',
                'visibility': 'PUBLIC',
                'categories': '["test", "django"]',
                'unlisted': False,
                'author': author
            }

def get_comment_object(author: Author, post: Post):
    return Comment.objects.create(
        type='comment',
        id_url='http://localhost:8000/comments/1/',
        comment='This is a comment.',
        contentType='text/plain',
        author=author,
        post=post
    )

def get_like_object(author: Author, post: Post, comment: Comment):
    return Like.objects.create(
        type='like',
        context='http://localhost:8000/posts/1/',
        summary='John Doe likes Test Post',
        author=author,
        post=post,
        comment=comment
    )

def get_request_object(actor: Author, object: Author):
    return Request.objects.create(
        type='follow',
        summary='John Doe wants to follow Jane Doe',
        actor=actor,
        object=object
    )

def get_inbox_object(ownerId: Author, post: Post, comment: Comment, like: Like, request: Request):
    return Inbox.objects.create(
        ownerId=ownerId,
        post=post,
        comment=comment,
        like=like,
        request=request
    )


class AuthorTestCase(TestCase):
    def setUp(self):
        self.author = get_author_object(1)
        self.author_data = get_author_data(1)
        self.author = Author.objects.create(**self.author_data)
        self.serializer = AuthorSerializer(instance=self.author)


    def test_author_creation(self):
        self.assertIsInstance(self.author, Author)
        self.assertEqual(self.author.type, 'author')
        self.assertEqual(self.author.id_url, 'https://example.com/author/1')
        self.assertEqual(self.author.url, 'https://example.com/author/1')
        self.assertEqual(self.author.host, 'example.com')
        self.assertEqual(self.author.displayName, 'John Doe')
        self.assertEqual(self.author.github, 'https://github.com/johndoe')
        self.assertEqual(self.author.profileImage, 'https://example.com/profile.jpg')
        self.assertEqual(self.author.userID, 'johndoe123')
        self.assertTrue(self.author.active)

    def test_author_reading(self):
        author = Author.objects.get(id=self.author.id)
        self.assertEqual(author.type, 'author')
        self.assertEqual(author.id_url, 'https://example.com/author/1')
        self.assertEqual(author.url, 'https://example.com/author/1')
        self.assertEqual(author.host, 'example.com')
        self.assertEqual(author.displayName, 'John Doe')
        self.assertEqual(author.github, 'https://github.com/johndoe')
        self.assertEqual(author.profileImage, 'https://example.com/profile.jpg')
        self.assertEqual(author.userID, 'johndoe123')
        self.assertTrue(author.active)

    def test_author_updating(self):
        self.author.type = 'Organization'
        self.author.save()
        author = Author.objects.get(id=self.author.id)
        self.assertEqual(author.type, 'Organization')

    def test_author_deleting(self):
        author_id = self.author.id
        self.author.delete()
        with self.assertRaises(Author.DoesNotExist):
            Author.objects.get(id=author_id)


class FollowModelTestCase(TestCase):
    def setUp(self):
        self.author_data = get_author_data(1)
        self.author = Author.objects.create(**self.author_data)
        self.follow_data = {
            'object': self.author,
            'follower_url': 'https://example.com/follower/1',
            'summary': 'John Doe follows Jane Doe',
            'accepted': True
        }
        self.follow = Follow.objects.create(**self.follow_data)

    def test_follow_creation(self):
        self.assertIsInstance(self.follow, Follow)
        self.assertEqual(self.follow.object, self.author)
        self.assertEqual(self.follow.follower_url, 'https://example.com/follower/1')
        self.assertEqual(self.follow.summary, 'John Doe follows Jane Doe')
        self.assertTrue(self.follow.accepted)

    def test_follow_reading(self):
        follow = Follow.objects.get(id=self.follow.id)
        self.assertEqual(follow.object, self.author)
        self.assertEqual(follow.follower_url, 'https://example.com/follower/1')
        self.assertEqual(follow.summary, 'John Doe follows Jane Doe')
        self.assertTrue(follow.accepted)

    def test_follow_updating(self):
        self.follow.summary = 'John Doe unfollows Jane Doe'
        self.follow.save()
        follow = Follow.objects.get(id=self.follow.id)
        self.assertEqual(follow.summary, 'John Doe unfollows Jane Doe')

    def test_follow_deleting(self):
        follow_id = self.follow.id
        self.follow.delete()
        with self.assertRaises(Follow.DoesNotExist):
            Follow.objects.get(id=follow_id)


class PostModelTestCase(TestCase):
    def setUp(self):
        self.author_data = get_author_data(1)
        self.author = Author.objects.create(**self.author_data)
        self.post_data = get_post_data(1, self.author)
        self.post = Post.objects.create(**self.post_data)

    def test_post_creation(self):
        self.assertIsInstance(self.post, Post)
        self.assertEqual(self.post.type, 'post')
        self.assertEqual(self.post.id_url, 'https://example.com/post/1')
        self.assertEqual(self.post.title, 'Test post')
        self.assertEqual(self.post.source, 'https://example.com/post/1')
        self.assertEqual(self.post.origin, 'https://example.com')
        self.assertEqual(self.post.description, 'This is a test post')
        self.assertEqual(self.post.contentType, 'text/plain')
        self.assertEqual(self.post.content, 'Hello, world!')
        self.assertEqual(self.post.visibility, 'PUBLIC')
        self.assertEqual(self.post.categories, '["test", "django"]')
        self.assertFalse(self.post.unlisted)
        self.assertEqual(self.post.author, self.author)

    def test_post_reading(self):
        post = Post.objects.get(id=self.post.id)
        self.assertEqual(post.type, 'post')
        self.assertEqual(post.id_url, 'https://example.com/post/1')
        self.assertEqual(post.title, 'Test post')
        self.assertEqual(post.source, 'https://example.com/post/1')
        self.assertEqual(post.origin, 'https://example.com')
        self.assertEqual(post.description, 'This is a test post')
        self.assertEqual(post.contentType, 'text/plain')
        self.assertEqual(post.content, 'Hello, world!')
        self.assertEqual(post.visibility, 'PUBLIC')
        self.assertEqual(post.categories, '["test", "django"]')
        self.assertFalse(post.unlisted)
        self.assertEqual(post.author, self.author)

    def test_post_updating(self):
        self.post.title = 'Updated post'
        self.post.save()
        post = Post.objects.get(id=self.post.id)
        self.assertEqual(post.title, 'Updated post')

    def test_post_deleting(self):
        post_id = self.post.id
        self.post.delete()
        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(id=post_id)


class RequestModelTestCase(TestCase):
    def setUp(self):
        self.actor_data = get_author_data(1)
        self.actor = Author.objects.create(**self.actor_data)
        self.object_data = get_author_data(2)
        self.object = Author.objects.create(**self.object_data)
        self.request_data = {
            'type': 'Follow',
            'summary': 'John Doe has requested to follow Jane Doe',
            'actor': self.actor,
            'object': self.object
        }
        self.request = Request.objects.create(**self.request_data)

    def test_request_creation(self):
        self.assertIsInstance(self.request, Request)
        self.assertEqual(self.request.type, 'Follow')
        self.assertEqual(self.request.summary, 'John Doe has requested to follow Jane Doe')
        self.assertEqual(self.request.actor, self.actor)
        self.assertEqual(self.request.object, self.object)

    def test_request_reading(self):
        request = Request.objects.get(id=self.request.id)
        self.assertEqual(request.type, 'Follow')
        self.assertEqual(request.summary, 'John Doe has requested to follow Jane Doe')
        self.assertEqual(request.actor, self.actor)
        self.assertEqual(request.object, self.object)

    def test_request_updating(self):
        self.request.summary = 'John Doe has requested to follow Jane Doe (updated)'
        self.request.save()
        request = Request.objects.get(id=self.request.id)
        self.assertEqual(request.summary, 'John Doe has requested to follow Jane Doe (updated)')

    def test_request_deleting(self):
        request_id = self.request.id
        self.request.delete()
        with self.assertRaises(Request.DoesNotExist):
            Request.objects.get(id=request_id)


class CommentModelTestCase(TestCase):
    def setUp(self):
        self.author_data = get_author_data(1)
        self.author = Author.objects.create(**self.author_data)
        self.post_data = get_post_data(1, self.author)
        self.post = Post.objects.create(**self.post_data)
        self.comment_data = {
            'type': 'Comment',
            'id_url': 'https://example.com/comment/1',
            'contentType': 'text/plain',
            'comment': 'This is a test comment',
            'author': 'John Doe',
            'post': self.post
        }
        self.comment = Comment.objects.create(**self.comment_data)

    def test_comment_creation(self):
        self.assertIsInstance(self.comment, Comment)
        self.assertEqual(self.comment.type, 'Comment')
        self.assertEqual(self.comment.id_url, 'https://example.com/comment/1')
        self.assertEqual(self.comment.contentType, 'text/plain')
        self.assertEqual(self.comment.comment, 'This is a test comment')
        self.assertEqual(self.comment.author, 'John Doe')
        self.assertEqual(self.comment.post, self.post)

    def test_comment_reading(self):
        comment = Comment.objects.get(id=self.comment.id)
        self.assertEqual(comment.type, 'Comment')
        self.assertEqual(comment.id_url, 'https://example.com/comment/1')
        self.assertEqual(comment.contentType, 'text/plain')
        self.assertEqual(comment.comment, 'This is a test comment')
        self.assertEqual(comment.author, 'John Doe')
        self.assertEqual(comment.post, self.post)

    def test_comment_updating(self):
        self.comment.comment = 'This is an updated comment'
        self.comment.save()
        comment = Comment.objects.get(id=self.comment.id)
        self.assertEqual(comment.comment, 'This is an updated comment')

    def test_comment_deleting(self):
        comment_id = self.comment.id
        self.comment.delete()
        with self.assertRaises(Comment.DoesNotExist):
            Comment.objects.get(id=comment_id)


class LikeModelTestCase(TestCase):
    def setUp(self):
        self.author_data = get_author_data(1)
        self.author = Author.objects.create(**self.author_data)
        self.post_data = get_post_data(1, self.author)
        self.post = Post.objects.create(**self.post_data)
        self.comment_data = {
            'type': 'Comment',
            'id_url': 'https://example.com/comment/1',
            'contentType': 'text/plain',
            'comment': 'This is a test comment',
            'author': 'John Doe',
            'post': self.post
        }
        self.comment = Comment.objects.create(**self.comment_data)
        self.like_data = {
            'type': 'Like',
            'summary': 'John Doe likes the post',
            'author': 'John Doe',
            'published': '2019-01-01T00:00:00Z',
            'post': self.post,
            'comment': self.comment
        }
        self.like = Like.objects.create(**self.like_data)

    def test_like_creation(self):
        self.assertIsInstance(self.like, Like)
        self.assertEqual(self.like.type, 'Like')
        self.assertEqual(self.like.summary, 'John Doe likes the post')
        self.assertEqual(self.like.author, 'John Doe')
        self.assertEqual(self.like.post, self.post)
        self.assertEqual(self.like.comment, self.comment)

    def test_like_reading(self):
        like = Like.objects.get(id=self.like.id)
        self.assertEqual(like.type, 'Like')
        self.assertEqual(like.summary, 'John Doe likes the post')
        self.assertEqual(like.author, 'John Doe')
        self.assertEqual(like.post, self.post)
        self.assertEqual(like.comment, self.comment)

    def test_like_updating(self):
        self.like.summary = 'John Doe likes the post (updated)'
        self.like.save()
        like = Like.objects.get(id=self.like.id)
        self.assertEqual(like.summary, 'John Doe likes the post (updated)')

    def test_like_deleting(self):
        like_id = self.like.id
        self.like.delete()
        with self.assertRaises(Like.DoesNotExist):
            Like.objects.get(id=like_id)


class InboxModelTestCase(TestCase):
    def setUp(self):
        self.author_data = get_author_data(1)
        self.author = Author.objects.create(**self.author_data)
        self.inbox_data = {
            'author': self.author,
            'url': 'https://example.com/inbox'
        }
        self.inbox = Inbox.objects.create(**self.inbox_data)

    def test_inbox_creation(self):
        self.assertIsInstance(self.inbox, Inbox)
        self.assertEqual(self.inbox.author, self.author)
        self.assertEqual(self.inbox.url, 'https://example.com/inbox')

    def test_inbox_reading(self):
        inbox = Inbox.objects.get(id=self.inbox.id)
        self.assertEqual(inbox.author, self.author)
        self.assertEqual(inbox.url, 'https://example.com/inbox')

    def test_inbox_updating(self):
        self.inbox.url = 'https://example.com/inbox/updated'
        self.inbox.save()
        inbox = Inbox.objects.get(id=self.inbox.id)
        self.assertEqual(inbox.url, 'https://example.com/inbox/updated')

    def test_inbox_deleting(self):
        inbox_id = self.inbox.id
        self.inbox.delete()
        with self.assertRaises(Inbox.DoesNotExist):
            Inbox.objects.get(id=inbox_id)