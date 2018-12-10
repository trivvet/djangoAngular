from django.conf.urls import url
from django.contrib import admin

from .views import (
    CommentListAPIView,
    CommentCreateAPIView,
    CommentDetailAPIView
    # CommentChildListAPIView
    )

urlpatterns = [
    url(r'^$', CommentListAPIView.as_view(), 
        name='comments_list'),
    # url(r'^(?P<id>\d+)/children/$', CommentChildListAPIView.as_view(), 
    #     name='comments_child_list'),
    url(r'^(?P<pk>\d+)/$', CommentDetailAPIView.as_view(), 
        name='comment_detail'),
    url(r'^create/$', CommentCreateAPIView.as_view(),
        name='comment_create'),
    # url(r'^(?P<id>\d+)/delete/$', comment_delete, name='delete'),
]