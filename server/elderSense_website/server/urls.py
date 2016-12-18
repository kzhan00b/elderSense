from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ssProcessing/$', views.ssProcessing, name='ssProcessing'),
    url(r'^androidResponse/$', views.androidResponse, name='androidResponse')
    
]