# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instance',
            name='name',
            field=models.CharField(max_length=30, verbose_name='Instance Name'),
        ),
        migrations.AlterField(
            model_name='instance',
            name='type',
            field=models.CharField(max_length=30, verbose_name='Instance Type'),
        ),
        migrations.AlterField(
            model_name='subnet',
            name='aws_id',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='subnet',
            name='cidr',
            field=models.CharField(max_length=30, verbose_name='Subnet CIDR'),
        ),
        migrations.AlterField(
            model_name='subnet',
            name='name',
            field=models.CharField(max_length=30, verbose_name='Subnet Name'),
        ),
        migrations.AlterField(
            model_name='vpc',
            name='cidr',
            field=models.CharField(max_length=30, verbose_name='Vpc CIDR'),
        ),
        migrations.AlterField(
            model_name='vpc',
            name='name',
            field=models.CharField(max_length=30, verbose_name='Vpc Name'),
        ),
    ]
