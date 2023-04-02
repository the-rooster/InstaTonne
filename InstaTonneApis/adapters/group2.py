from uuid import uuid4

group2_hostname = "social-distribution-media-2.herokuapp.com"



def group2_like_inbox_adapter(content : dict):
    """
            like: dict = {
            "type" : "like",
            "author" : author.id_url,
            "object" : post_id,
            "summary" : "An author liked your post!"
        }

        translate to

            like: dict = {
            "type" : "like",
            "author" : author object or something like it
            "object" : post_id,
            "summary" : "An author liked your post!"
        }
    """
    new_author = {

        "type": "author",
        "host": content["author"],
        "id" : content["author"],
        "displayName" : content["author"],
        "url" : content["author"],
        "github" : "",
        "profileImage" : ""
    }


    new_obj = {
        "type" : "like",
        "summary" : content["summary"],
        "author" : new_author,
        "object" : content["object"]
    }




    content["author"] = new_author
    content["object"] = new_obj

    


    print("ADAPTER TIME:",content)


    return content

def group2_post_inbox_adapter(content : dict):
    """
    Translate:
        {
            "type" : "post",
            "id" : post.id_url,
            "author" : AuthorSerializer(author).data
        } 

        TO

        {
    "@context": "jaskdljklsda",
    "type": "post",
    "author": {
        "type": "author",
        "id": "https://social-distribution-media-2.herokuapp.com/api/authors/81cb28ce-2d2a-4bb0-9098-fd9738b05672",
        "url": "https://social-distribution-media-2.herokuapp.com/api/authors/81cb28ce-2d2a-4bb0-9098-fd9738b05672",
        "host": "https://social-distribution-media-2.herokuapp.com/api",
        "displayName": "joshdoe",
        "github": "",
        "profileImage": ""
    },
    "object": {
        "type": "post",
        "id": "https://social-distribution-media-2.herokuapp.com/authors/81cb28ce-2d2a-4bb0-9098-fd9738b05672/posts/b35d0c95-13a8-4fb3-9985-cb7ce1281ca5",
        "title": "Sample post!",
        "source": "https://social-distribution-media-2.herokuapp.com/authors/81cb28ce-2d2a-4bb0-9098-fd9738b05672/posts/b35d0c95-13a8-4fb3-9985-cb7ce1281ca5",
        "origin": "https://social-distribution-media-2.herokuapp.com/authors/81cb28ce-2d2a-4bb0-9098-fd9738b05672/posts/b35d0c95-13a8-4fb3-9985-cb7ce1281ca5",
        "description": "Sample post!",
        "contentType": "text/markdown",
        "content": "# Hello world!",
        "author": {
            "type": "author",
            "id": "https://social-distribution-media-2.herokuapp.com/api/authors/81cb28ce-2d2a-4bb0-9098-fd9738b05672",
            "url": "https://social-distribution-media-2.herokuapp.com/api/authors/81cb28ce-2d2a-4bb0-9098-fd9738b05672",
            "host": "https://social-distribution-media-2.herokuapp.com/api",
            "displayName": "joshdoe",
            "github": "",
            "profileImage": ""
        },
        "categories": [],
        "count": 0,
        "comments": "https://social-distribution-media-2.herokuapp.com/authors/81cb28ce-2d2a-4bb0-9098-fd9738b05672/posts/b35d0c95-13a8-4fb3-9985-cb7ce1281ca5/comments",
        "commentsSrc": {},
        "published": "2023-03-22T23:40:46.374745Z",
        "visibility": "FRIENDS",
        "unlisted": false
    }
}


    
    """

    new_content : dict = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "post",
        "author": {
            "type": "author",
            "id": content["author"]["id"],
            "url": content["author"]["id"],
            "host": content["author"]["host"],
            "displayName": content["author"]["displayName"],
            "github": "",
            "profileImage": ""
        },
        "object": {
            "type": "post",
            "id": content["id"],
            "title": content["title"],
            "source": content["source"],
            "origin": content["origin"],
            "description": content["description"],
            "contentType": content["contentType"],
            "content": content["content"],
            "author": {
                "type": "author",
                "id": content["author"]["id"],
                "url": content["author"]["id"],
                "host": content["author"]["host"],
                "displayName": content["author"]["displayName"],
                "github": "",
                "profileImage": ""
            },
            "categories": content["categories"],
            "count": content["count"],
            "comments": content["comments"],
            "commentsSrc": content["commentsSrc"],
            "published": content["published"],
            "visibility": content["visibility"],
            "unlisted": content["unlisted"]
        }
    }

    return new_content


def group2_comment_inbox_adapter(content : dict):
    """
    Translate:
    {
            "type" : "comment",
            "contentType" : body["contentType"],
            "comment" : body["comment"],
            "author" : author.id_url,
            "post" : post_id
        }

    To:

    {
        "@context": "https://www.w3.org/ns/activitystreams",
        "summary": "johndoe commented on your post!",
        "type": "comment",
        "actor": {
            "type": "author",
            "id": "https://social-distribution-media.herokuapp.com/api/authors/d58ab754-ffb4-4bd6-945f-b32b4a2974b9",
            "host": "https://social-distribution-media.herokuapp.com/api",
            "displayName": "johndoe",
            "url": "https://social-distribution-media.herokuapp.com/api/authors/d58ab754-ffb4-4bd6-945f-b32b4a2974b9",
            "github": "",
            "profileImage": ""
        },
        "object": {
            "type": "comment",
            "summary": "johndoe commented on your post!",
            "author": {
                "type": "author",
                "id": "https://social-distribution-media.herokuapp.com/api/authors/d58ab754-ffb4-4bd6-945f-b32b4a2974b9",
                "host": "https://social-distribution-media.herokuapp.com/api",
                "displayName": "johndoe",
                "url": "https://social-distribution-media.herokuapp.com/api/authors/d58ab754-ffb4-4bd6-945f-b32b4a2974b9",
                "github": "",
                "profileImage": ""
            },
            "id": "https://social-distribution-media-2.herokuapp.com/api/authors/81cb28ce-2d2a-4bb0-9098-fd9738b05672/posts/b35d0c95-13a8-4fb3-9985-cb7ce1281ca5/comments/{{$randomUUID}}",
            "comment": "Hello world!",
            "contentType": "text/plain",
            "object": "https://social-distribution-media-2.herokuapp.com/api/authors/81cb28ce-2d2a-4bb0-9098-fd9738b05672/posts/b35d0c95-13a8-4fb3-9985-cb7ce1281ca5"
        }
    }
    """

    new_content : dict = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "summary": content["author"] + " commented on your post!",
        "type": "comment",
        "actor": {
            "type": "author",
            "host": content["author"],
            "id" : content["author"],
            "displayName" : content["author"],
            "url" : content["author"],
            "github" : "",
            "profileImage" : ""
        },
        "object": {
            "type": "comment",
            "summary": content["author"] + " commented on your post!",
            "author": {
                "type": "author",
                "host": content["author"],
                "id" : content["author"],
                "displayName" : content["author"],
                "url" : content["author"],
                "github" : "",
                "profileImage" : ""
            },
            "id": content["post"] + "/comments/" + str(uuid4()),
            "comment": content["comment"],
            "contentType": content["contentType"],
            "object": content["post"]
        }
    }

    return new_content


def group2_follow_inbox_adapter(content : dict):
    """
    Translate:
    {
        "type": "follow",
        "actor": AuthorSerializer(author).data,
        "object": author_response.json(),
        "summary": author.displayName + " wants to follow " + author_response.json()["displayName"]
    }

    To:

    {
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "follow",
        "summary": "Group2Person wants to follow testjamesdoe",
        "actor": {
            "type": "author",
            "id": "https://quickcomm-dev1.herokuapp.com/api/authors/287eeb25-01d3-450a-93bc-2d9b15459984/",
            "url": "https://quickcomm-dev1.herokuapp.com/api/authors/287eeb25-01d3-450a-93bc-2d9b15459984/",
            "host": "https://quickcomm-dev1.herokuapp.com/api/",
            "displayName": "Group2Person",
            "github": "https://github.com/abramhindle",
            "profileImage": "https://github.com/abramhindle"
        },
        "object": {
            "type": "author",
            "id": "https://social-distribution-media.herokuapp.com/api/authors/11f981fb-f76f-4dbd-ae98-e55282c6d293",
            "host": "https://social-distribution-media.herokuapp.com/api",
            "displayName": "testjamesdoe",
            "url": "https://social-distribution-media.herokuapp.com/api/authors/11f981fb-f76f-4dbd-ae98-e55282c6d293",
            "github": "",
            "profileImage": ""
        }
    }
    """

    new_content : dict = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "follow",
        "summary": content["actor"] + " wants to follow " + content["object"]["displayName"],
        "actor": {
            "type": "author",
            "id": content["actor"],
            "url": content["actor"],
            "host": content["actor"],
            "displayName": content["actor"],
            "github": "",
            "profileImage": ""
        },
        "object": {
            
            "type": "author",
            "id": content["object"]["id"],
            "host": content["object"]["host"],
            "displayName": content["object"]["displayName"],
            "url": content["object"]["url"],
            "github": "",
            "profileImage": ""
        }
    }

    return new_content
