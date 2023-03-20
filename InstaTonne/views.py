from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import *
# Create your views here.

def index(request):

    return render(request,"index.html")

def go_to_the_app(request):

    return redirect("app/")