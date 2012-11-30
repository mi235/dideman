# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from dide.models import (RankCode, PaymentFileName, PaymentCategoryTitle,
                         PaymentReportType, PaymentCode)
from dideman import settings
from dideman.dide.util.settings import SETTINGS
from dide.util import xml
import os


class Command(BaseCommand):
    args = '<file ...>'
    help = 'XML database import.'

    def handle(self, *args, **options):
        for rec in args:
            try:
                pf = PaymentFileName.objects.get(pk=rec)
                pth = '%s' % pf.xml_file
                fldr, fl = pth.split('/', 1)
                status = xml.reset(os.path.join(settings.MEDIA_ROOT,
                                                         fldr, fl))
                pf.status = status
                pf.save()

            except PaymentFileName.DoesNotExist:
                raise CommandError('Record %s not found.' % rec)