from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index(request):
    """View function for home page of site."""

    return render(request, 'index.html')
