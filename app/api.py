from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from app.models import *


@csrf_exempt
def log_in(request):

    ret = { "status": "FAIL" }

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            ret["error"] = "Missing email / password"
            return JsonResponse(ret)

        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            ret["status"] = "OK"
        else:
            ret["error"] = "Incorrect email / password"

    return JsonResponse(ret)


@csrf_exempt
# @api_login_required - TODO: Steve
def get_all_posts(request):
    ret = { "status": "FAIL" }
    posts = Post.objects.filter(is_active=True)
    ret["posts"] = [p.json() for p in posts]
    ret["status"] = "OK"
    return JsonResponse(ret)
