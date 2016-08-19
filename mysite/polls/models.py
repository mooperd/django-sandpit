from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from ext.amazon_aws import AWSProvider


class Vpc(models.Model):
    # It might be better to pass in AWSProvider from the view.
    amazon_aws = AWSProvider()
    name = models.CharField(max_length=30, verbose_name='Vpc Name')
    cidr = models.CharField(max_length=30, verbose_name='Vpc CIDR')
    region = models.CharField(max_length=30, default="")
    aws_id = models.CharField(max_length=30, default="")

    def get_absolute_url(self):
        return reverse('vpc-detail', kwargs={'pk': self.pk})

    # Check if the vpc is deployed.
    def is_active(self):
        return self.aws_id != ""

    def deploy(self):
        if self.is_active() == True:
            return True
        if self.is_active() == False:
            cloud_network = self.amazon_aws.create_vpc(
                self.name,
                self.region,
                self.cidr
            )


# def __str__(self):              # __unicode__ on Python 2
#        return "%s %s" % (self.first_name, self.last_name)

class Subnet(models.Model):
    name = models.CharField(max_length=30, verbose_name='Subnet Name')
    cidr = models.CharField(max_length=30, verbose_name='Subnet CIDR')
    availability_zone = models.CharField(max_length=30, default="")
    aws_id = models.CharField(max_length=30, default="")
    vpc = models.ForeignKey(Vpc)

    def get_absolute_url(self):
        return reverse('subnet-detail', kwargs={'pk': self.pk})


# def __str__(self):              # __unicode__ on Python 2
#        return "%s %s" % (self.name, self.cidr)

class Instance(models.Model):
    name = models.CharField(max_length=30, verbose_name='Instance Name')
    type = models.CharField(max_length=30, verbose_name='Instance Type')
    # the ID is only used for deployed instances
    aws_id = models.CharField(max_length=30, default="")
    subnet = models.ForeignKey(Subnet)

    def get_absolute_url(self):
        return reverse('instance-detail', kwargs={'pk': self.pk})

# def __str__(self):              # __unicode__ on Python 2
#        return "%s %s" % (self.name, self.type)

# class Question(models.Model):
#    conn = boto.connect_vpc()
#    vpcs = conn.get_all_vpcs()
#    vpc_ids = tuple(map(lambda v: v.id, vpcs))
#    def __str__(self):
#        return self.vpc_ids
