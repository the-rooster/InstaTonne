from django.http import HttpRequest, HttpResponse

local_origins = {
    "127.0.0.1",
    "localhost"
}

#TODO:make this work with other servers HTTP auth creds
def checkAuthorization(func):

    def wrap(request : HttpRequest,**kwargs):

        print(request.META)
       
        if request.get_host() in local_origins:
            result = func(request,**kwargs)
        else:
            return HttpResponse(status=403)

        return result

    return wrap