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
    new_obj = {

        "type": "author",
        "host": content["author"],
        "id" : content["author"],
        "displayName" : content["author"],
        "url" : content["author"],
        "github" : "",
        "profileImage" : ""
    }
    content["author"] = new_obj


    print("ADAPTER TIME:",content)


    return content


