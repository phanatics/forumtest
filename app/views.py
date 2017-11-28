from django.shortcuts import render
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from app.decorators import *


@login_required
def index(request):
    return render(request, "index.html")

def log_in(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")
    return render(request, "login.html")


def log_out(request):
    logout(request)
    return HttpResponseRedirect("/login")