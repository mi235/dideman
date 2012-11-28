# -*- coding: utf-8 -*-
from dideman.dide.actions import DocxReport
from dideman.dide.util.settings import SETTINGS
import os


def cc(obj):
    ret = [obj['organization_serving'].organization.name]
    if obj['employee__permanent__permanent_post'].organization.name \
            not in [obj['organization_serving'].organization.name, '-']:
        ret.append(obj['employee__permanent__permanent_post'].\
                       organization.name)
    if obj['leave__not_paying']:
        ret.append(u'Εκκαθαριστής')
    ret.append(u'Α.Φ.')
    return ret


class LeaveDocxReport(DocxReport):
    def __init__(self, short_description, body_template_path,
                 fields=None, custom_context=None, model_fields=None,
                 include_header=True, include_footer=True):

        fields = fields or ['employee__firstname', 'employee__lastname',
                            'profession', 'organization_serving',
                            'employee__permanent__permanent_post',
                            'employee__fathername', 'order',
                            'date_from', 'date_to', 'protocol_number',
                            'duration', 'date_issued', 'leave__not_paying']

        context = {'telephone_number':
                       SETTINGS['leaves_contact_telephone_number'],
                   'contact_person': SETTINGS['leaves_contact_person'],
                   'email': SETTINGS['email_leaves']}
        if custom_context:
            context.update(custom_context)

        if not model_fields:
            model_fields = {'header_date': '{{date_issued}}',
                            'recipient':
                                '{{employee__firstname}}'
                            ' {{employee__lastname}}'}

            model_fields['cc'] = cc
        super(LeaveDocxReport, self).__init__(
            short_description, os.path.join('leave', body_template_path),
            fields, context, model_fields, include_header, include_footer)


leave_docx_reports = [
    LeaveDocxReport(u'Αιμοδοτική', 'adeia_aimodosias.xml',
                    custom_context={'subject': u'Χορήγηση άδειας αιμοδοσίας'}),

    LeaveDocxReport(u'Συνδικαλιστική',
                    'adeia_syndikalistiki.xml',
                    custom_context={'subject':
                                        u'Χορήγηση Συνδικαλιστικής Άδειας '}),

    LeaveDocxReport(u'Τοκετού (πατέρα)', 'adeia_goniki_patera_toketou.xml',
                    custom_context={'subject': u'Χορήγηση ειδικής άδειας'
                                    u' λόγω τοκετού'}),

    LeaveDocxReport(u'Ειδική 22 ημερών', 'adeia_22.xml',
                    custom_context={'subject': u'Χορήγηση ειδικής άδειας'}),

    LeaveDocxReport(u'Διευκόλυνσης', 'adeia_diefkolinsis.xml',
                    custom_context={'subject':
                                        u'Χορήγηση άδειας διευκόλυνσης'}),

    LeaveDocxReport(u'Κανονική', 'adeia_kanoniki.xml',
                    custom_context={'subject': u'Χορήγηση κανονικής άδειας '
                                    u'απουσίας'}),

    LeaveDocxReport(u'Εκλογική', 'adeia_eklogon.xml',
                    custom_context={'subject': u'Χορήγηση ειδικής άδειας λόγω'
                                    u' εκλογών'}),

    LeaveDocxReport(u'Ανατροφής (Άνευ Αποδοχών)', 'adeia_anatrofis_no_pay.xml',
                    custom_context={'subject':
                                    u'Χορήγηση άδειας χωρίς αποδοχές'
                                    u' για ανατροφή παιδιού'}),

    LeaveDocxReport(u'Ειδική Άδεια αιρετών μελών Ο.Τ.Α. άνευ αποδοχών',
                    'adeia_eidiki_airetoi_no_pay.xml',
                    custom_context={'subject':
                                        u'Χορήγηση άδειας άνευ αποδοχών σε '
                                    u'αιρετό εκπρόσωπο'
                                    u' Ο.Τ.Α'}),

    LeaveDocxReport(u'Άνευ Αποδοχών', 'adeia_eidiki_no_pay.xml',
                    custom_context={'subject':
                                        u'Χορήγηση άδειας άνευ αποδοχών'}),

    LeaveDocxReport(u'Αναρρωτική (από Α\'Βάθμια Υγειονομική Επιτροπή)',
                    'adeia_anarrotiki_yg_ep.xml',
                    custom_context={'subject':
                                        u'Χορήγηση αναρρωτικής άδειας'}),

    LeaveDocxReport(u'Αναρρωτική (Βραχυχρόνια)',
                    'adeia_anarrotiki_short.xml',
                    custom_context={'subject':
                                        u'Χορήγηση αναρρωτικής άδειας'}),

    LeaveDocxReport(u'Ανατροφής (3 μήνες - τρίτου τέκνου)',
                    'adeia_anatrofis_3months.xml',
                    custom_context={'subject':
                                        u'Χορήγηση άδειας τριών μηνών για '
                                    u'ανατροφή τρίτου τέκνου και άνω.'}),

    LeaveDocxReport(u'Ανατροφής (9 μήνες)', 'adeia_anatrofis_9months.xml',
                    custom_context={'subject':
                                        u'Χορήγηση άδειας ανατροφής τέκνου'}),

    LeaveDocxReport(u'Ανατροφής (10 μήνες)', 'adeia_anatrofis_10months.xml',
                    custom_context={'subject':
                                        u'Χορήγηση άδειας ανατροφής τέκνου'}),

    LeaveDocxReport(u'Γονική', 'adeia_goniki.xml',
                    custom_context={'subject':
                                        u'Χορήγηση γονικής άδειας απουσίας'}),

    LeaveDocxReport(u'Εξετάσεων', 'adeia_eidiki_eksetaseon.xml',
                    custom_context={'subject':
                                        u'Χορήγηση ειδικής άδειας εξετάσεων'}),

    LeaveDocxReport(u'Κύησης', 'adeia_pregnancy.xml',
                    custom_context={'subject':
                                        u'Χορήγηση άδειας κύησης'}),

    LeaveDocxReport(u'Λοχείας', 'adeia_maternity.xml',
                    custom_context={'subject':
                                        u'Χορήγηση άδειας λοχείας'}),

    LeaveDocxReport(u'Κυοφορίας',
                    'adeia_pregnancy_normal.xml',
                    custom_context={'subject':
                                        u'Χορήγηση κανονικής άδειας κυοφορίας με αποδοχές'}),

    LeaveDocxReport(u'Επαπειλούμενης κύησης', 'adeia_epapiloumenis.xml',
                    custom_context={'subject':
                                        u'Χορήγηση αναρρωτικής άδειας'})
    ]
