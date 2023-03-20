# InstaTonne/endpoints/auth_wrapper.py
# Copyright (c) 2023 CMPUT 404 W2023 Group 6
#
# This file is part of InstaTonne.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
 

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