from django.shortcuts import render

# Create your views here.

from backend.auth.login_auth import login_auth
from django.contrib.sessions.models import Session


@login_auth
def index(request):

    return render(request, 'asset/home.html', {'username': request.username})
