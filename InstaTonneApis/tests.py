from django.test import TestCase
from .models import Author, Follow, Post, Request, Comment, Like, Inbox, AuthorSerializer, FollowSerializer, PostSerializer, RequestSerializer, CommentSerializer, LikeSerializer

def get_author_object(index: int):
    if index == 1:
        return Author.objects.create(
            type='author',
            id_url='http://localhost:8000/author/1/',
            url='http://localhost:8000/author/1/',
            host='http://localhost:8000/',
            displayName='John Doe',
            github='https://github.com/johndoe',
            profileImage='https://example.com/johndoe.jpg',
            userID='johndoe',
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
        self.author1 = get_author_object(1)
        self.author2 = get_author_object(2)
        self.valid_author_data = {
            'type': 'author',
            'id_url': 'http://localhost:8000/author/3/',
            'url': 'http://localhost:8000/author/3/',
            'host': 'http://localhost:8000/',
            'displayName': 'Alice Smith',
            'github': 'https://github.com/alicesmith',
            'profileImage': 'https://example.com/alicesmith.jpg',
            'userID': 'alicesmith',
            'active': True
        }
        self.invalid_author_data = { }

    def test_author_creation(self):
        self.assertEqual(self.author1.id.__str__(), self.author1.id)
        self.assertEqual(self.author1.type, 'author')
        self.assertEqual(self.author1.id_url, 'http://localhost:8000/author/1/')
        self.assertEqual(self.author1.url, 'http://localhost:8000/author/1/')
        self.assertEqual(self.author1.host, 'http://localhost:8000/')
        self.assertEqual(self.author1.displayName, 'John Doe')
        self.assertEqual(self.author1.github, 'https://github.com/johndoe')
        self.assertEqual(self.author1.profileImage, 'https://example.com/johndoe.jpg')
        self.assertEqual(self.author1.userID, 'johndoe')
        self.assertEqual(self.author1.active, True)

    def test_author_update(self):
        self.author1 = self.author2
        self.assertEqual(self.author1.type, 'author')
        self.assertEqual(self.author1.id_url, 'http://localhost:8000/author/2/')
        self.assertEqual(self.author1.url, 'http://localhost:8000/author/2/')
        self.assertEqual(self.author1.host, 'http://localhost:8000/')
        self.assertEqual(self.author1.displayName, 'Jane Doe')
        self.assertEqual(self.author1.github, 'https://github.com/janedoe')
        self.assertEqual(self.author1.profileImage, 'https://example.com/janedoe.jpg')
        self.assertEqual(self.author1.userID, 'janedoe')
        self.assertEqual(self.author1.active, True)

    def test_valid_author_serializer(self):
        author_serializer = AuthorSerializer(data=self.valid_author_data)
        self.assertTrue(author_serializer.is_valid())
        author = author_serializer.save()
        self.assertEqual(author.id.__str__(), author.id)
        self.assertEqual(author.type, 'author')
        self.assertEqual(author.id_url, 'http://localhost:8000/author/3/')
        self.assertEqual(author.url, 'http://localhost:8000/author/3/')
        self.assertEqual(author.host, 'http://localhost:8000/')
        self.assertEqual(author.displayName, 'Alice Smith')
        self.assertEqual(author.github, 'https://github.com/alicesmith')
        self.assertEqual(author.profileImage, 'https://example.com/alicesmith.jpg')
        # self.assertEqual(author.userID, 'alicesmith')
        # self.assertEqual(author.active, True)

    def test_invalid_author_serializer(self):
        author_serializer = AuthorSerializer(data=self.invalid_author_data)
        self.assertFalse(author_serializer.is_valid())


class FollowTestCase(TestCase):
    def setUp(self):
        self.author1 = get_author_object(1)
        self.author2 = get_author_object(2)
        self.follow = Follow.objects.create(
            followerAuthorId=self.author1,
            followeeAuthorId=self.author2
        )
        self.valid_author_data = self.author1.__dict__
        self.valid_author_data2 = self.author2.__dict__
        self.valid_follow_data = {
            'followerAuthorId': self.valid_author_data,
            'followeeAuthorId': self.valid_author_data2
        }
        self.invalid_follow_data = { }

    def test_follow_creation(self):
        self.assertEqual(self.follow.followerAuthorId, self.author1)
        self.assertEqual(self.follow.followeeAuthorId, self.author2)

    def test_valid_follow_serializer(self):
        pass        
        # follow_serializer = FollowSerializer(data=self.valid_follow_data)
        # self.assertTrue(follow_serializer.is_valid(), follow_serializer.errors)
        # follow = follow_serializer.save()
        # self.assertEqual(follow.__str__(), follow.id)
        # self.assertEqual(follow.followerAuthorId, self.author1)
        # self.assertEqual(follow.followeeAuthorId, self.author2)

    def test_invalid_follow_serializer(self):
        follow_serializer = FollowSerializer(data=self.invalid_follow_data)
        self.assertFalse(follow_serializer.is_valid())

    def test_on_delete_follower(self):
        follower = get_author_object(1)
        followee = get_author_object(2)
        follow = Follow.objects.create(
            followerAuthorId=follower,
            followeeAuthorId=followee
        )
        follower.delete()
        with self.assertRaises(Follow.DoesNotExist):
            follow.refresh_from_db()

    def test_on_delete_followee(self):
        follower = get_author_object(1)
        followee = get_author_object(2)
        follow = Follow.objects.create(
            followerAuthorId=follower,
            followeeAuthorId=followee
        )
        follower.delete()
        with self.assertRaises(Follow.DoesNotExist):
            follow.refresh_from_db()

    def test_update_follower(self):
        follower = get_author_object(1)
        followee = get_author_object(2)
        follow = Follow.objects.create(
            followerAuthorId=follower,
            followeeAuthorId=followee
        )
        follower2 = get_author_object(3)
        follow.followerAuthorId = follower2
        follow.save()
        self.assertEqual(follow.followerAuthorId, follower2)

    def test_update_followee(self):
        follower = get_author_object(1)
        followee = get_author_object(2)
        follow = Follow.objects.create(
            followerAuthorId=follower,
            followeeAuthorId=followee
        )
        followee2 = get_author_object(3)
        follow.followeeAuthorId = followee2
        follow.save()
        self.assertEqual(follow.followeeAuthorId, followee2)


class PostTestCase(TestCase):
    def setUp(self):
        self.author = get_author_object(1)
        self.post = get_post_object(self.author)
        self.valid_post_data = {
            'type': 'post',
            'id_url': 'http://localhost:8000/posts/2/',
            'title': 'Another Test Post',
            'source': 'http://localhost:8000/posts/2/',
            'origin': 'http://localhost:8000/posts/2/',
            'description': 'This is another test post.',
            'contentType': 'text/plain',
            'content': 'Hello again!',
            'visibility': 'PUBLIC',
            'comments': 'This is another comment.',
            'categories': 'test',
            'unlisted': False,
            'author': self.author.id
        }
        self.invalid_post_data = { }

    def test_post_creation(self):
        self.assertEqual(self.post.type, 'post')
        self.assertEqual(self.post.id_url, 'http://localhost:8000/posts/1/')
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.source, 'http://localhost:8000/posts/1/')
        self.assertEqual(self.post.origin, 'http://localhost:8000/posts/1/')
        self.assertEqual(self.post.description, 'This is a test post.')
        self.assertEqual(self.post.contentType, 'text/plain')
        self.assertEqual(self.post.content, 'Hello, world!')
        self.assertEqual(self.post.visibility, 'PUBLIC')
        self.assertEqual(self.post.categories, 'test')
        self.assertEqual(self.post.unlisted, False)
        self.assertEqual(self.post.author, self.author)

    def test_valid_post_serializer(self):
        pass
        # post_serializer = PostSerializer(data=self.valid_post_data)
        # self.assertTrue(post_serializer.is_valid())
        # post = post_serializer.save()
        # self.assertEqual(post.__str__(), post.id)
        # self.assertEqual(post.type, 'post')
        # self.assertEqual(post.id_url, 'http://localhost:8000/posts/2/')
        # self.assertEqual(post.title, 'Another Test Post')
        # self.assertEqual(post.source, 'http://localhost:8000/posts/2/')
        # self.assertEqual(post.origin, 'http://localhost:8000/posts/2/')
        # self.assertEqual(post.description, 'This is another test post.')
        # self.assertEqual(post.contentType, 'text/plain')
        # self.assertEqual(post.content, 'Hello again!')
        # self.assertEqual(post.visibility, 'PUBLIC')
        # self.assertEqual(post.categories, 'test')
        # self.assertEqual(post.unlisted, False)
        # self.assertEqual(post.author, self.author)

    def test_invalid_post_serializer(self):
        post_serializer = PostSerializer(data=self.invalid_post_data)
        self.assertFalse(post_serializer.is_valid())

    def test_on_delete_author(self):
        author = get_author_object(1)
        post = get_post_object(author)
        author.delete()
        with self.assertRaises(Post.DoesNotExist):
            post.refresh_from_db()

    def test_update_author(self):
        author = get_author_object(1)
        post = get_post_object(author)
        author2 = get_author_object(2)
        post.author = author2
        post.save()
        self.assertEqual(post.author, author2)


class RequestTestCase(TestCase):
    def setUp(self):
        self.actor = get_author_object(1)
        self.object = get_author_object(2)
        self.request = get_request_object(self.actor, self.object)
        self.valid_request_data = {
            'type': 'follow',
            'summary': 'John Doe wants to follow Jane Doe',
            'actor': self.actor.id,
            'object': self.object.id
        }
        self.invalid_request_data = { }

    def test_request_creation(self):
        self.assertEqual(self.request.type, 'follow')
        self.assertEqual(self.request.summary, 'John Doe wants to follow Jane Doe')
        self.assertEqual(self.request.actor, self.actor)
        self.assertEqual(self.request.object, self.object)

    def test_valid_request_serializer(self):
        pass
        # request_serializer = RequestSerializer(data=self.valid_request_data)
        # self.assertTrue(request_serializer.is_valid())
        # request = request_serializer.save()
        # self.assertEqual(request.__str__(), str(request.id))
        # self.assertEqual(request.type, 'follow')
        # self.assertEqual(request.summary, 'John Doe wants to follow Jane Doe')
        # self.assertEqual(request.actor, self.actor)
        # self.assertEqual(request.object, self.object)

    def test_invalid_request_serializer(self):
        request_serializer = RequestSerializer(data=self.invalid_request_data)
        self.assertFalse(request_serializer.is_valid())

    def test_on_delete_actor(self):
        actor = get_author_object(1)
        request = get_request_object(actor, self.object)
        actor.delete()
        with self.assertRaises(Request.DoesNotExist):
            request.refresh_from_db()

    def test_on_delete_object(self):
        object = get_author_object(2)
        request = get_request_object(self.actor, object)
        object.delete()
        with self.assertRaises(Request.DoesNotExist):
            request.refresh_from_db()

    def test_update_actor(self):
        actor = get_author_object(1)
        request = get_request_object(actor, self.object)
        actor2 = get_author_object(2)
        request.actor = actor2
        request.save()
        self.assertEqual(request.actor, actor2)

    def test_update_object(self):
        object = get_author_object(2)
        request = get_request_object(self.actor, object)
        object2 = get_author_object(3)
        request.object = object2
        request.save()
        self.assertEqual(request.object, object2)

    
class CommentTestCase(TestCase):
    def setUp(self):
        self.author = get_author_object(1)
        self.post = get_post_object(self.author)
        self.comment = get_comment_object(self.author, self.post)
        self.valid_comment_data = {
            'type': 'comment',
            'id_url': 'http://localhost:8000/comments/2/',
            'contentType': 'text/plain',
            'comment': 'This is another comment.',
            'author': self.author.id,
            'post': self.post.id
        }
        self.invalid_comment_data = {
            'type': '',
            'id_url': '',
            'contentType': '',
            'comment': '',
            'author': '',
            'post': ''
        }

    def test_comment_creation(self):
        self.assertEqual(self.comment.type, 'comment')
        self.assertEqual(self.comment.id_url, 'http://localhost:8000/comments/1/')
        self.assertEqual(self.comment.contentType, 'text/plain')
        self.assertEqual(self.comment.comment, 'This is a comment.')
        self.assertEqual(self.comment.author, self.author)
        self.assertEqual(self.comment.post, self.post)

    def test_valid_comment_serializer(self):
        pass
        # comment_serializer = CommentSerializer(data=self.valid_comment_data)
        # self.assertTrue(comment_serializer.is_valid())
        # comment = comment_serializer.save()
        # self.assertEqual(comment.__str__(), str(comment.id))
        # self.assertEqual(comment.type, 'comment')
        # self.assertEqual(comment.id_url, 'http://localhost:8000/comments/2/')
        # self.assertEqual(comment.contentType, 'text/plain')
        # self.assertEqual(comment.comment, 'This is another comment.')
        # self.assertEqual(comment.author, self.author)
        # self.assertEqual(comment.post, self.post)

    def test_invalid_comment_serializer(self):
        comment_serializer = CommentSerializer(data=self.invalid_comment_data)
        self.assertFalse(comment_serializer.is_valid())

    def test_on_delete_author(self):
        author = get_author_object(1)
        comment = get_comment_object(author, self.post)
        author.delete()
        with self.assertRaises(Comment.DoesNotExist):
            comment.refresh_from_db()

    def test_on_delete_post(self):
        post = get_post_object(self.author)
        comment = get_comment_object(self.author, post)
        post.delete()
        with self.assertRaises(Comment.DoesNotExist):
            comment.refresh_from_db()

    def test_update_author(self):
        author = get_author_object(1)
        comment = get_comment_object(author, self.post)
        author2 = get_author_object(2)
        comment.author = author2
        comment.save()
        self.assertEqual(comment.author, author2)

    def test_update_post(self):
        post = get_post_object(self.author)
        comment = get_comment_object(self.author, post)
        author = get_author_object(3)
        post2 = get_post_object(author)
        comment.post = post2
        comment.save()
        self.assertEqual(comment.post, post2)


class LikeTestCase(TestCase):
    def setUp(self):
        self.author = get_author_object(1)
        self.post = get_post_object(self.author)
        self.comment = get_comment_object(self.author, self.post)
        self.like = get_like_object(self.author, self.post, self.comment)
        self.valid_like_data = {
            'type': 'like',
            'context': 'http://localhost:8000/posts/1/',
            'summary': 'John Doe likes Test Post',
            'author': self.author.id,
            'post': self.post.id,
            'comment': self.comment.id
        }
        self.invalid_like_data = {
            'type': '',
            'context': '',
            'summary': '',
            'author': '',
            'post': '',
            'comment': ''
        }

    def test_like_creation(self):
        self.assertEqual(self.like.type, 'like')
        self.assertEqual(self.like.context, 'http://localhost:8000/posts/1/')
        self.assertEqual(self.like.summary, 'John Doe likes Test Post')
        self.assertEqual(self.like.author, self.author)
        self.assertEqual(self.like.post, self.post)
        self.assertEqual(self.like.comment, self.comment)

    def test_valid_like_serializer(self):
        pass
        # like_serializer = LikeSerializer(data=self.valid_like_data)
        # self.assertTrue(like_serializer.is_valid())
        # like = like_serializer.save()
        # self.assertEqual(like.__str__(), str(like.id))
        # self.assertEqual(like.type, 'like')
        # self.assertEqual(like.context, 'http://localhost:8000/posts/1/')
        # self.assertEqual(like.summary, 'John Doe likes Test Post')
        # self.assertEqual(like.author, self.author)
        # self.assertEqual(like.post, self.post)
        # self.assertEqual(like.comment, self.comment)

    def test_invalid_like_serializer(self):
        like_serializer = LikeSerializer(data=self.invalid_like_data)
        self.assertFalse(like_serializer.is_valid())

    def test_on_delete_author(self):
        author = get_author_object(1)
        like = get_like_object(author, self.post, self.comment)
        author.delete()
        with self.assertRaises(Like.DoesNotExist):
            like.refresh_from_db()

    def test_on_delete_post(self):
        post = get_post_object(self.author)
        like = get_like_object(self.author, post, self.comment)
        post.delete()
        with self.assertRaises(Like.DoesNotExist):
            like.refresh_from_db()

    def test_on_delete_comment(self):
        comment = get_comment_object(self.author, self.post)
        like = get_like_object(self.author, self.post, comment)
        comment.delete()
        with self.assertRaises(Like.DoesNotExist):
            like.refresh_from_db()

    def test_update_author(self):
        author = get_author_object(1)
        like = get_like_object(author, self.post, self.comment)
        author2 = get_author_object(2)
        like.author = author2
        like.save()
        self.assertEqual(like.author, author2)

    def test_update_post(self):
        post = get_post_object(self.author)
        like = get_like_object(self.author, post, self.comment)
        author = get_author_object(3)
        post2 = get_post_object(author)
        like.post = post2
        like.save()
        self.assertEqual(like.post, post2)

    def test_update_comment(self):
        comment = get_comment_object(self.author, self.post)
        like = get_like_object(self.author, self.post, comment)
        author = get_author_object(3)
        comment2 = get_comment_object(author, self.post)
        like.comment = comment2
        like.save()
        self.assertEqual(like.comment, comment2)


class InboxTestCase(TestCase):
    def setUp(self):
        self.owner = get_author_object(1)
        self.author = get_author_object(2)
        self.post = get_post_object(self.author)
        self.comment = get_comment_object(self.author, self.post)
        self.like = get_like_object(self.author, self.post, self.comment)
        self.request = get_request_object(self.author, self.owner)
        self.inbox = get_inbox_object(self.owner, self.post, self.comment, self.like, self.request)

    def test_inbox_creation(self):
        self.assertEqual(self.inbox.ownerId, self.owner)
        self.assertEqual(self.inbox.post, self.post)
        self.assertEqual(self.inbox.comment, self.comment)
        self.assertEqual(self.inbox.like, self.like)
        self.assertEqual(self.inbox.request, self.request)

    def test_inbox_with_null_values(self):
        inbox = get_inbox_object(self.owner, None, None, None, None)
        self.assertEqual(inbox.post, None)
        self.assertEqual(inbox.comment, None)
        self.assertEqual(inbox.like, None)
        self.assertEqual(inbox.request, None)

    def test_on_delete_owner(self):
        owner = get_author_object(1)
        inbox = get_inbox_object(owner, self.post, self.comment, self.like, self.request)
        owner.delete()
        with self.assertRaises(Inbox.DoesNotExist):
            inbox.refresh_from_db()

    def test_on_delete_post(self):
        post = get_post_object(self.author)
        inbox = get_inbox_object(self.owner, post, self.comment, self.like, self.request)
        post.delete()
        with self.assertRaises(Inbox.DoesNotExist):
            inbox.refresh_from_db()

    def test_on_delete_comment(self):
        comment = get_comment_object(self.author, self.post)
        inbox = get_inbox_object(self.owner, self.post, comment, self.like, self.request)
        comment.delete()
        with self.assertRaises(Inbox.DoesNotExist):
            inbox.refresh_from_db()

    def test_on_delete_like(self):
        like = get_like_object(self.author, self.post, self.comment)
        inbox = get_inbox_object(self.owner, self.post, self.comment, like, self.request)
        like.delete()
        with self.assertRaises(Inbox.DoesNotExist):
            inbox.refresh_from_db()

    def test_on_delete_request(self):
        request = get_request_object(self.owner, self.author)
        inbox = get_inbox_object(self.owner, self.post, self.comment, self.like, request)
        request.delete()
        with self.assertRaises(Inbox.DoesNotExist):
            inbox.refresh_from_db()
        
    def test_update_owner(self):
        owner = get_author_object(1)
        inbox = get_inbox_object(owner, self.post, self.comment, self.like, self.request)
        owner2 = get_author_object(2)
        inbox.ownerId = owner2
        inbox.save()
        self.assertEqual(inbox.ownerId, owner2)

    def test_update_post(self):
        post = get_post_object(self.author)
        inbox = get_inbox_object(self.owner, post, self.comment, self.like, self.request)
        author = get_author_object(3)
        post2 = get_post_object(author)
        inbox.post = post2
        inbox.save()
        self.assertEqual(inbox.post, post2)

    def test_update_comment(self):
        comment = get_comment_object(self.author, self.post)
        inbox = get_inbox_object(self.owner, self.post, comment, self.like, self.request)
        author = get_author_object(3)
        comment2 = get_comment_object(author, self.post)
        inbox.comment = comment2
        inbox.save()
        self.assertEqual(inbox.comment, comment2)

    def test_update_like(self):
        like = get_like_object(self.author, self.post, self.comment)
        inbox = get_inbox_object(self.owner, self.post, self.comment, like, self.request)
        author = get_author_object(3)
        like2 = get_like_object(author, self.post, self.comment)
        inbox.like = like2
        inbox.save()
        self.assertEqual(inbox.like, like2)

    def test_update_request(self):
        request = get_request_object(self.owner, self.author)
        inbox = get_inbox_object(self.owner, self.post, self.comment, self.like, request)
        author = get_author_object(3)
        request2 = get_request_object(self.owner, author)
        inbox.request = request2
        inbox.save()
        self.assertEqual(inbox.request, request2)