from django.http import HttpResponseRedirect


def login_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.is_authenticated():
            return view_func(request, *args, **kwargs)
        return HttpResponseRedirect('/login?next={}'.format(request.get_full_path()))
    return _wrapped_view_func