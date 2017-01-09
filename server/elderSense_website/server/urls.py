from django.conf.urls import url, include
from . import views
from . import deviceConnect

urlpatterns = [
    url(r'fcm/', include('fcm.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^ssProcessing/$', views.ssProcessing, name='ssProcessing'),
    url(r'^androidResponse/$', views.androidResponse, name='androidResponse'),
    url(r'^deviceLogin/$', deviceConnect.login, name='androidLogin'),
    url(r'^deviceSignUp/$', deviceConnect.signup, name='androidSignup'),
    url(r'^deviceRegisterToken/$', deviceConnect.registerToken, name='androidRegisterToken')
]