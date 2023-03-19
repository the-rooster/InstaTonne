from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import *
# Create your views here.

def index(request):

    return HttpResponse(content="instatonne backend. go away")