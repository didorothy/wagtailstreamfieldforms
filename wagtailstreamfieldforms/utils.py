from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

FORM_FIELD_CHOICES = (
    ('singleline', _('Single line text')),
    ('multiline', _('Multi-line text')),
    ('email', _('Email')),
    ('number', _('Number')),
    ('url', _('URL')),
    ('checkbox', _('Checkbox')),
    ('checkboxes', _('Checkboxes')),
    ('dropdown', _('Drop down')),
    ('radio', _('Radio buttons')),
    ('date', _('Date')),
    ('datetime', _('Date/time')),
)

def create_field_id(label):
    '''Converts a label to a slugified version we can use to identify the field.'''
    return str(slugify(label))
