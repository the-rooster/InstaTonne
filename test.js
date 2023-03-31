


req = fetch("https://social-distribution-media.herokuapp.com/api/authors/d58ab754-ffb4-4bd6-945f-b32b4a2974b9/inbox", {
    method: "POST", body: JSON.stringify({
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "like",
        "summary": "someone liked your post!",
        "author": {
            "type": "author",
            "id": "https://cmput404-group6-instatonne.herokuapp.com/authors/8c1fb0cc4323438aaf3d89b975f82b86",
            "host": "https://cmput404-group6-instatonne.herokuapp.com",
            "displayName": "someone",
            "url": "https://cmput404-group6-instatonne.herokuapp.com/authors/8c1fb0cc4323438aaf3d89b975f82b86",
            "github": "",
            "profileImage": ""
        },
        "object": {
            "type": "like",
            "summary": "johndoe likes your post!",
            "author": {
                "type": "author",
                "id": "https://cmput404-group6-instatonne.herokuapp.com/authors/8c1fb0cc4323438aaf3d89b975f82b86",
                "host": "https://cmput404-group6-instatonne.herokuapp.com",
                "displayName": "someone",
                "url": "https://cmput404-group6-instatonne.herokuapp.com/authors/8c1fb0cc4323438aaf3d89b975f82b86",
                "github": "",
                "profileImage": ""
            },
            "object": "https://social-distribution-media.herokuapp.com/api/authors/d58ab754-ffb4-4bd6-945f-b32b4a2974b9/posts/be303fa1-e75d-4c2c-a9d4-e3279990bac5"
        }
    })
,
"headers" : {"Content-Type": "application/json", "Authorization" : "Basic R3JvdXA2VXNlcjpwdXJwbGVwdXJwbGU="}});