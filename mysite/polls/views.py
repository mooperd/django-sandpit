from django.shortcuts import render
from django.http import HttpResponse
from .models import Instance
from django.template import loader
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from models import Vpc
import boto

def index(request):
    conn = boto.connect_vpc()
    vpc_list = conn.get_all_vpcs()
    # template = loader.get_template('polls/index.html')
    return render(request, 'polls/index.html', {'vpc_list':vpc_list})

class VpcCreate(CreateView):
    model = Vpc
    fields = ['name', 'cidr']

class VpcUpdate(UpdateView):
    model = Vpc
    fields = ['name', 'cidr']

class VpcDelete(DeleteView):
    model = Vpc
    success_url = reverse_lazy('vpc-list')
