from .group20 import *
from .group2 import *
from urllib.parse import urlparse
def adapter_get_remote_posts(content : dict,url):

    hostname = urlparse(url).hostname

    if hostname == group20_hostname:
        return get_remote_posts_adapter_group20(content)
    

    return content

def adapter_get_remote_single_post(post : dict,url):

    hostname = urlparse(url).hostname

    if hostname == group20_hostname:
        return get_single_remote_post_adapter_group20(post)
    
    return post

def adapter_inbox_like(post : dict,url):

    hostname = urlparse(url).hostname

    if hostname == group2_hostname:
        return group2_like_inbox_adapter(post)
    
    return post

def adapter_inbox_post(post : dict,url):

    hostname = urlparse(url).hostname

    if hostname == group2_hostname:
        return group2_post_inbox_adapter(post)
    
    return post

def adapter_inbox_comment(post : dict,url):

    hostname = urlparse(url).hostname

    if hostname == group2_hostname:
        return group2_comment_inbox_adapter(post)
    
    return post

def adapter_inbox_follow(post : dict,url):

    hostname = urlparse(url).hostname

    if hostname == group2_hostname:
        return group2_follow_inbox_adapter(post)
    
    return post

def adapter_get_comments(content : dict,url):

    hostname = urlparse(url).hostname

    if hostname == group2_hostname:
        return group2_get_comments(content)
    
    return content