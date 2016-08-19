import boto
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView, View
from .forms import InstanceForm, SubnetForm, VpcForm

from models import Vpc


def index(request):
    conn = boto.connect_vpc()
    vpc_list = conn.get_all_vpcs()
    return TemplateResponse(request, 'polls/index.html', {'vpc_list': vpc_list})


class VpcCreate(CreateView):
    model = Vpc
    fields = ['name', 'cidr']


class VpcUpdate(UpdateView):
    model = Vpc
    fields = ['name', 'cidr']


class VpcDelete(DeleteView):
    model = Vpc
    success_url = reverse_lazy('vpc-list')


class VpcFormView(View):
    template_name = "polls/vpc_form.html"

    def get(self, request, *args, **kwargs):
        context = dict()
        context['formA'] = VpcForm()
        context['formB'] = SubnetForm()
        context['formC'] = InstanceForm()
        return TemplateResponse(request, template=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        vpc = VpcForm(request.POST)
        subnet = SubnetForm(request.POST)
        instance = InstanceForm(request.POST)
        if vpc.is_valid() and subnet.is_valid() and instance.is_valid():
            vpc = vpc.save()
            subnet.instance.vpc = vpc
            subnet = subnet.save()
            instance.instance.subnet = subnet
            instance.save()
            return redirect("/")

        return TemplateResponse(request, template=self.template_name,
                                context={'formA': vpc, 'formB': subnet, 'formC': instance})
