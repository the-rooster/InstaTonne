from .group20 import *
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