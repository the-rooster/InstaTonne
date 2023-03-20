# InstaTonne/endpoints/connectedservers.py
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
 

from django.http import HttpRequest,HttpResponse
from ..models import ConnectedServer, ConnectedServerSerializer
import json

#gets all connected servers so we can list them in the user search screen
def get_all_connected_servers(request):
 
    connected = ConnectedServer.objects.all()
    serialized = [ConnectedServerSerializer(x).data for x in connected]

    resp = {"servers" : serialized}

    return HttpResponse(content=json.dumps(resp),status=200)