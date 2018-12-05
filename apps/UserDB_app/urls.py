from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^logpage/?$', views.logpage, name='ulogpage'),
    url(r'^login/?$', views.login, name='ulogin'),
    url(r'^register/?$', views.register, name='uregister'),
    url(r'^regpage/?$', views.regpage, name='uregpage'),
    url(r'^success/?$', views.success, name='usuccess'),
    url(r'^message/?$', views.message, name='umessage'),
    url(r'^showMsg/msgComment/?$', views.msgComment, name='ushowmsgcomment'),
    url(r'^showUser/(?P<id>\d+)?$', views.showUser, name="ushowUser"),
    url(r'^showMsg/(?P<id>\d+)?$', views.showMsg, name="ushowMsg"),  
    url(r'^logout/?$', views.logout, name='ulogout'),
    url(r'^delete/(?P<id>\d+)?$', views.delete, name='udelete'),
    url(r'^deleteComment/(?P<id>\d+)/(?P<msg_id>\d+)?$', views.deleteComment, name='udeleteComment'),
]