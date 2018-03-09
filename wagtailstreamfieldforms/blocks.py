import django.forms
from django.utils.six import text_type
from django.utils.text import slugify
from unidecode import unidecode

from wagtail.wagtailcore.blocks import (
    BooleanBlock,
    CharBlock,
    DeclarativeSubBlocksMetaclass,
    ListBlock,
    StructBlock
)

from .forms import formfieldblocks
from .utils import create_field_id

# TODO: consider form validation???


class FormFieldBlockMixin(object, metaclass=DeclarativeSubBlocksMetaclass):
    '''Every Block that can be a form field in a StreamField must use this mixin.

    Inheriting from this class allows for the block to be identified and for the block to generate the needed information for the form.
    '''
    label = CharBlock()
    required = BooleanBlock(default=False, required=False)
    help_text = CharBlock(required=False)

    def get_field_options(self, field):
        options = {}
        options['label'] = field['label']
        options['help_text'] = field['help_text']
        options['required'] = field['required']
        return options

    def create_field(self, field):
        options = self.get_field_options(field)
        return django.forms.CharField(**options)

    def clean_name(self, value):
        '''Converts the label for this form field to a key used as the form element name.

        value - StructValue - holds the stored information about the block.
        '''
        # unidecode will return an ascii string while slugify wants a
        # unicode string on the other hand, slugify returns a safe-string
        # which will be converted to a normal str
        return create_field_id(value['label'])


@formfieldblocks.register('singleline')
class SingleLineFormFieldBlock(StructBlock, FormFieldBlockMixin):
    default_value = CharBlock(required=False)

    def get_field_options(self, field):
        options = super(SingleLineFormFieldBlock, self).get_field_options(field)
        options['initial'] = field['default_value']
        options['max_length'] = 255
        return options


@formfieldblocks.register('multiline')
class MultiLineFormFieldBlock(StructBlock, FormFieldBlockMixin):
    default_value = CharBlock(required=False)

    def get_field_options(self, field):
        options = super(MultiLineFormFieldBlock, self).get_field_options(field)
        options['initial'] = field['default_value']
        return options

    def create_field(self, field):
        options = self.get_field_options(field)
        return django.forms.CharField(widget=django.forms.Textarea, **options)


@formfieldblocks.register('email')
class EmailFormFieldBlock(StructBlock, FormFieldBlockMixin):

    def create_field(self, field):
        options = self.get_field_options(field)
        return django.forms.EmailField(**options)


@formfieldblocks.register('number')
class NumberFormFieldBlock(StructBlock, FormFieldBlockMixin):

    def create_field(self, field):
        options = self.get_field_options(field)
        return django.forms.DecimalField(**options)


@formfieldblocks.register('url')
class UrlFormFieldBlock(StructBlock, FormFieldBlockMixin):

    def create_field(self, field):
        options = self.get_field_options(field)
        return django.forms.URLField(**options)


@formfieldblocks.register('checkbox')
class CheckboxFormFieldBlock(StructBlock, FormFieldBlockMixin):
    default_checked = BooleanBlock(default=False, required=False)

    def get_field_options(self, field):
        options = super(CheckboxFormFieldBlock, self).get_field_options(field)
        options['initial'] = field['default_checked']
        return options

    def create_field(self, field):
        options = self.get_field_options(field)
        return django.forms.BooleanField(**options)


class FieldChoiceBlock(StructBlock):
    key = CharBlock(required=True)
    description = CharBlock(required=True)


@formfieldblocks.register('dropdown')
class DropdownFormFieldBlock(StructBlock, FormFieldBlockMixin):
    choices = ListBlock(FieldChoiceBlock)
    allow_multiple_selections = BooleanBlock(default=False, required=False)

    def get_field_options(self, field):
        options = super(DropdownFormFieldBlock, self).get_field_options(field)
        options['choices'] = [(x['key'], x['description']) for x in field['choices']]
        return options

    def create_field(self, field):
        options = self.get_field_options(field)
        if field['allow_multiple_selections']:
            return django.forms.MultipleChoiceField(**options)
        else:
            return django.forms.ChoiceField(**options)


@formfieldblocks.register('radio')
class RadioFormFieldBlock(StructBlock, FormFieldBlockMixin):
    choices = ListBlock(FieldChoiceBlock)

    def get_field_options(self, field):
        options = super(RadioFormFieldBlock, self).get_field_options(field)
        options['choices'] = [(x['key'], x['description']) for x in field['choices']]
        return options

    def create_field(self, field):
        options = self.get_field_options(field)
        return django.forms.ChoiceField(widget=django.forms.RadioSelect, **options)


@formfieldblocks.register('date')
class DateFormFieldBlock(StructBlock, FormFieldBlockMixin):

    def create_field(self, field):
        options = self.get_field_options(field)
        return django.forms.DateField(**options)


@formfieldblocks.register('datetime')
class DateTimeFormFieldBlock(StructBlock, FormFieldBlockMixin):

    def create_field(self, field):
        options = self.get_field_options(field)
        return django.forms.DateTimeField(**options)
