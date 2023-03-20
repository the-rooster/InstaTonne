# InstaTonne/endpoints/register.py
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
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from InstaTonneApis.models import Author
from InstaTonne.forms import RegisterForm
from InstaTonne.settings import HOSTNAME

def register_author(request : HttpRequest):

    if request.method != "POST":
        return HttpResponse(status=405)

    form = RegisterForm(request.data)

    if not form.is_valid():
        form.add_error("username","Form is invalid.")
        return HttpResponse(status=400)

    if len(User.objects.filter(username=form.data["username"])) != 0:
        form.add_error("username","User already exists!")
        return HttpResponse(status=400)

    user = User.objects.create_user(username=form.data["username"],password=form.data["password"])
    obj = Author.objects.create(displayName=form.data["username"],type="author",url="none",host=HOSTNAME,github="none",profileImage="none",userID=user.pk,active=False,id_url="none")

    obj.id_url = HOSTNAME + "/authors/" + obj.id
    obj.url = HOSTNAME + "/authors/" + obj.id
    obj.save()
    
    return HttpResponse(status=200)