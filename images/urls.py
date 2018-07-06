from django.urls import path, include
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^create/$', views.image_create, name='create'),
    url('^detail/(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.image_detail, name='details'),
    url('^like/$', views.image_like, name='like'),
    url(r'^$', views.image_list, name='list')
]