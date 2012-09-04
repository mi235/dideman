# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, render
from django.http import HttpResponse, HttpResponseRedirect
from dideman.dide.models import (Employee, Permanent, School, Application,
                                 ApplicationSet, ApplicationType,
                                 ApplicationChoice, MoveInside)
from dideman.dide.applications.forms import (EmployeeMatchForm,
                                             MoveInsideForm,
                                             TemporaryPositionForm)
from dideman.dide.employee.decorators import match_required
from dideman.dide.applications.actions import ApplicationPrint
from dideman.dide.util.common import get_class
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.db.models.loading import get_model
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from dideman import settings
import reportlab
import datetime
import os


def get_form(klass):
    return get_class('dideman.dide.applications.forms.%s' % klass)


@match_required
def print_app(request, set_id):

    class Positioner(object):
        ll = 50
        ul = 750
        vstep = 20
        col_diff = 300

        def __init__(self):
            self.hpos = self.ll
            self.vpos = self.ul

        def next_pos(self):
            r = (self.hpos, self.vpos)
            self.vpos -= self.vstep
            if self.vpos < 50:
                self.vpos = self.ul - self.vstep * 7
                self.hpos = self.ll + self.col_diff
            return r

    base_app = Application.objects.get(
        set_id=set_id, employee_id=request.session['matched_employee_id'])
    emp = Permanent.objects.get(pk=base_app.employee_id)
    set = base_app.set
    app = get_model('dide', set.klass).objects.get(parent=base_app)
    form = get_form(set.klass)(request.POST)
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=app_report.pdf'
    registerFont(TTFont('DroidSans', os.path.join(settings.MEDIA_ROOT,
                                                  'DroidSans.ttf')))
    c = canvas.Canvas(response)
    c.setFont('DroidSans', 14)
    posn = Positioner()
    c.drawString(*posn.next_pos(), text=u'Δ.Δ.Ε. Δωδεκανήσου - %s' % set.title)
    posn.next_pos()
    c.drawString(*posn.next_pos(), text='%s %s - %s' % (emp.lastname,
                                          emp.firstname,
                                          emp.registration_number))
    posn.next_pos()
    c.drawString(*posn.next_pos(), text=u'Α.Α. Αίτησης : %s' % app.id)
    for field in form.base_fields:
        val = getattr(app, field)
        if val:
            if val == True:
                val = u'Ναι'
            c.drawString(*posn.next_pos(), text='%s: %s' \
                              % (app._meta.get_field(field).verbose_name, val))

    posn.next_pos()
    c.drawString(*posn.next_pos(), text=u'Επιλογές')
    for x in ApplicationChoice.objects.filter(
        application=app).order_by('position'):
        c.drawString(*posn.next_pos(),
                      text='%s. %s' % (x.position + 1, x.choice.name))

    c.drawString(400, 150, text=u'Υπογραφή')
    c.showPage()
    c.save()
    return response


@csrf_protect
@match_required
def edit(request, set_id):
    today = datetime.date.today()
    new_form = False
    if 'logout' in request.GET:
        request.session.clear()
        return HttpResponseRedirect('/employee/match/?next=/applications/edit/%s' % set_id)
    else:
        emp = Permanent.objects.get(pk=request.session['matched_employee_id'])
        try:
            set = ApplicationSet.objects.get(pk=set_id)
        except:
            return HttpResponse('invalid application')

        if not set.start_date <= today <= set.end_date:
            return HttpResponse(u'Λήξη αίτησης')

        model = get_model('dide', set.klass)

        try:
            app = model.objects.get(employee=emp, set=set)
        except:
            new_form = True
            app = model(employee=emp, set=set)
            app.save()

        if 'print' in request.GET:
            return print_app(request, set_id)

        if 'emp-action' in request.POST:
            action = request.POST['emp-action']
            choices = request.POST['emp-choices'].split(';')
            form = get_form(set.klass)(request.POST)

            if form.is_valid():
                for key in form.cleaned_data:
                    if hasattr(app, key) and form.cleaned_data[key]:
                        setattr(app, key, form.cleaned_data[key])
            else:
                for n, f in form.fields.items():
                    try:
                        value = f.clean(f.widget.value_from_datadict(
                                form.data, form.files, form.add_prefix(n)))
                        if hasattr(app, n) and value:
                            setattr(app, n, value)
                    except:
                        pass

            if request.POST['emp-choices']:
                app_choices = []
                for i, choice in enumerate(choices):
                    app_choices.append(
                        ApplicationChoice(application=app, choice_id=choice,
                                           position=i))
                    ApplicationChoice.objects.filter(application=app).delete()
                    ApplicationChoice.objects.bulk_create(app_choices)

            if request.POST['emp-action'] == 'submit' and form.is_valid():
                app.datetime_finalised = datetime.datetime.now()
                app.save()
            else:
                app.save()
            return HttpResponseRedirect('/applications/edit/%s' % set_id)
        else:
            if new_form:
                app_form = get_form(set.klass)()
            else:
                app_form = get_form(set.klass)(app.__dict__)

            schools = app_form.choices(emp)
            choices_schools = [(x.choice_id, x.choice.name) for x in
                       ApplicationChoice.objects
                       .filter(application=app).order_by('position')]
            choices = [x.choice_id for x in
                       ApplicationChoice.objects
                       .filter(application=app).order_by('position')]
            app_len = app_form.choices_length()
            choices += [0] * (app_len - len(choices))
            options = []
            for i in range(0, app_len):
                acc = []
                for s in schools:
                    acc.append({'id': s.id, 'name': s.name,
                                'selected': s.id == choices[i]})
                options.append(acc)

            return render_to_response(
                _template_path + 'application.html',
                RequestContext(request, {'emp': emp,
                                         'form': app_form,
                                         'schools': schools,
                                         'application': app,
                                         'options': options,
                                         'choices_schools': choices_schools}))
