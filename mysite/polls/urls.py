from django.conf.urls import url
from polls.views import VpcCreate, VpcUpdate, VpcDelete
from . import views

app_name = 'polls'
urlpatterns = [
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    url(r'vpc/add/$', VpcCreate.as_view(), name='vpc-add'),
    url(r'vpc/(?P<pk>[0-9]+)/$', VpcUpdate.as_view(), name='vpc-update'),
    url(r'vpc/(?P<pk>[0-9]+)/delete/$', VpcDelete.as_view(), name='vpc-delete'),
]
