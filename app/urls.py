from django.conf.urls import url
from django.contrib import admin
from app import views, api

urlpatterns = [

    # views
    url(r'^$', views.index),
    url(r'^admin/', admin.site.urls),
    url(r'^login$', views.log_in),
    url(r'^logout$', views.log_out),

    # api
    url(r'^api/login$', api.log_in),
    url(r'^api/posts$', api.get_all_posts),
]
