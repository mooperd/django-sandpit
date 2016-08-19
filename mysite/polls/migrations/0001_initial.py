# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Instance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('type', models.CharField(max_length=30)),
                ('aws_id', models.CharField(default='', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Subnet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('cidr', models.CharField(max_length=30)),
                ('availability_zone', models.CharField(default='', max_length=30)),
                ('aws_id', models.CharField(default=None, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Vpc',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('cidr', models.CharField(max_length=30)),
                ('region', models.CharField(default='', max_length=30)),
                ('aws_id', models.CharField(default='', max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='subnet',
            name='vpc',
            field=models.ForeignKey(to='polls.Vpc'),
        ),
        migrations.AddField(
            model_name='instance',
            name='subnet',
            field=models.ForeignKey(to='polls.Subnet'),
        ),
    ]
