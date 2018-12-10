from django.conf.urls import url
from .views import (
    AccountListAPIView,
    AccountDetailAPIView,
    AccountCreateAPIView,
    AccountLoginAPIView
    )

urlpatterns = [
    url(r'^$', AccountListAPIView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', AccountDetailAPIView.as_view(), 
        name='detail'),
    url(r'^create/$', AccountCreateAPIView.as_view(), name='register'),
    url(r'^login/$', AccountLoginAPIView.as_view(), name='login')
]