group20_hostname = "t20-social-distribution.herokuapp.com"


def get_remote_posts_adapter_group20(content : dict):


    for post in content["items"]:
        post["id"] = post["origin"]

    return content

def get_single_remote_post_adapter_group20(post : dict):

    post["id"] = post["origin"]

    return post
