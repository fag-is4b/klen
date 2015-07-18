# This Python file uses the following encoding: utf-8

from django.db import models
from datetime import datetime
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

class Main(models.Model):
    date_time = models.DateTimeField(default=datetime.now, verbose_name=_(u'Дата'))
    dollar = models.DecimalField(max_digits=17, decimal_places=4,verbose_name=_(u'Доллар'))
    euro = models.DecimalField(max_digits=17, decimal_places=4,verbose_name=_(u'Евро'))
    au = models.DecimalField(max_digits=17, decimal_places=4,verbose_name=_(u'Золото'))
    data = models.TextField(verbose_name=_(u'Котировки'))

    #def __unicode__(self):
    #    return self.date_time


class MainModelForm(ModelForm):

    class Meta:
        model = Main
