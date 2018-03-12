from collections import OrderedDict

import django.forms
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailcore.blocks import Block

from .utils import create_field_id

class FormFieldBlockRegistry(object):
    '''Registry holding a mapping of field names to Blocks that represent those fields.'''
    def __init__(self):
        self.field_types = {}

    def register(self, name:str, block:Block=None):
        '''Register a new form field Block class.'''
        if name in self.field_types:
            raise ValueError("Duplicate form field block name.")
        if block == None:
            def wrapper(cls):
                self.field_types[name] = cls
                return cls
            return wrapper
        else:
            self.field_types[name] = block

    def lookup_type(self, name):
        '''Return a Block class based on the passed in form field type name.'''
        return self.field_types[name]


formfieldblocks = FormFieldBlockRegistry()


class BlockField(object):
    '''Represents a field specified by a block in a StreamField.'''
    def __init__(self, block, value):
        self.block = block
        self.value = value

    def get_form_field(self):
        return self.block.create_field(self.value)

    def get_field_id(self):
        opts = self.block.get_field_options(self.value)
        return create_field_id(opts['label'])


class BaseForm(django.forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')

        self.user = kwargs.pop('user', None)
        self.page = kwargs.pop('page', None)

        super(BaseForm, self).__init__(*args, **kwargs)


class FormBuilder(object):
    '''Builds a form class from a list of passed in form fields.'''

    def __init__(self, fields):
        self.fields = fields

    @property
    def formfields(self):
        '''Changes the fields into an OrderedDict of fields with keys that are slugified versions of the field label.'''
        fields = OrderedDict()
        for field in self.fields:
            fields[field.get_field_id()] = field.get_form_field()
        return fields

    def get_form_class(self):
        '''Creates a Form class based on the fields passed in at initialization.'''
        # TODO: consider only creating the class on the first call an then returning the originally created class on subsequent calls to save cycles and to prevent class type conflicts.
        return type('StreamForm', (BaseForm,), self.formfields)
