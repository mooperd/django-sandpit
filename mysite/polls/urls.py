from django.conf.urls import url
from views import VpcCreate, VpcUpdate, VpcDelete, index, VpcFormView

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^vpc/add/?$', VpcCreate.as_view(), name='vpc-add'),
    url(r'^vpc/addall/?$',VpcFormView.as_view(), name='vpc-add-all'),
    url(r'^vpc/(?P<pk>[0-9]+)/?$', VpcUpdate.as_view(), name='vpc-update'),
    url(r'^vpc/(?P<pk>[0-9]+)/delete/?$', VpcDelete.as_view(), name='vpc-delete'),
]
