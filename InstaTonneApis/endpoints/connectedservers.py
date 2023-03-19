
from django.http import HttpRequest,HttpResponse
from ..models import ConnectedServer, ConnectedServerSerializer
import json

#gets all connected servers so we can list them in the user search screen
def get_all_connected_servers(request):
 
    connected = ConnectedServer.objects.all()
    serialized = [ConnectedServerSerializer(x).data for x in connected]

    resp = {"servers" : serialized}

    return HttpResponse(content=json.dumps(resp),status=200)