# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from dideman.dide.models import (ApplicationSet)
from django.template import RequestContext
import datetime
import os


_template_path = 'menu' + os.path.sep


def menu(request):
    today = datetime.date.today()
    set = ApplicationSet.objects.filter(end_date__gte=today)
    return render_to_response(_template_path + 'menu.html',
                              RequestContext(request, {'app': set}))