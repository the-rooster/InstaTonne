# InstaTonne/endpoints/login.py
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
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from ..models import Author
from django.contrib.auth.models import User
from InstaTonne.forms import LoginForm
from django.contrib.auth import authenticate, login as auth_login
import json

@csrf_exempt
def login(request : HttpRequest):

    
    print("HERRHHEEHRHR")
    if request.method != "POST":
        return HttpResponse(status=405)

    try:
        data = json.loads(request.body)
    except Exception as e:
        print("EXCEPTION IN LOGIN: ",e)
        return HttpResponse(status=400)
    print(request.body,request.POST,data)
    form = LoginForm(data)


    if not form.is_valid():
        form.add_error("username","Form is invalid.")
        return HttpResponse(status=400)
        # return render(request,"registration/login.html",context= {"form" : form})


    user = authenticate(request,username=form.data["username"],password=form.data["password"])

    if not user:
        form.add_error("username","Form is invalid.")
        return HttpResponse(status=404)
        #return render(request,"registration/login.html",context= {"form" : form})
        
    authors = Author.objects.filter(userID=user.pk)

    if not authors:
        form.add_error("username","something has gone terribly wrong")
        return render(request,"registration/login.html",context= {"form" : form})

    author = authors[0]

    if not author.active:
        form.add_error("username","Admin has not approved of your account yet.")
        return HttpResponse(content="Admin has not approved of your account yet",status=403)
    
    auth_login(request,user)

    res = json.dumps({
        "authorId": author.id
    })

    print(res)

    return HttpResponse(status=200, content=res)