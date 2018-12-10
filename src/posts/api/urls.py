from django.conf.urls import url
from django.contrib import admin

from .views import (
    PostListAPIView,
    PostDetailAPIView,
    PostCreateAPIView,
    PostUpdateAPIView,
    PostDestroyAPIView
    )

urlpatterns = [
    url(r'^$', PostListAPIView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', PostDetailAPIView.as_view(), 
        name='post_detail'),
    url(r'^create/$', PostCreateAPIView.as_view(), 
        name='post_create'),
    url(r'^(?P<pk>\d+)/edit/$', PostUpdateAPIView.as_view(), 
        name='post_update'),
    url(r'^(?P<pk>\d+)/delete/$', PostDestroyAPIView.as_view(), 
        name='post_delete'),
   
]