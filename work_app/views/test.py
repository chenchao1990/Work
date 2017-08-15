from django.shortcuts import render

# Create your idc_views here.

from backend.auth.login_auth import login_auth
from django.contrib.sessions.models import Session


@login_auth
def test(request):

    return render(request, 'base/index.html')
