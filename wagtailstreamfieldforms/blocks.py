import django.forms
from django.utils.html import format_html, format_html_join
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

    def render_basic(self, value, context=None):
        if context:
            form = context['form']
        else:
            form = {
                self.clean_name(value): self.create_field(value)
            }
        return format_html('<div class="{}">{}{}</div>', self.__class__.__name__.lower(), form[self.clean_name(value)].label_tag(), form[self.clean_name(value)])

    class Meta:
        icon = 'form'


@formfieldblocks.register('singleline')
class SingleLineFormFieldBlock(FormFieldBlockMixin, StructBlock):
    default_value = CharBlock(required=False)

    class Meta:
        label = 'Single Line Field'
        icon = 'form'

    def get_field_options(self, field):
        options = super(SingleLineFormFieldBlock, self).get_field_options(field)
        options['initial'] = field['default_value']
        options['max_length'] = 255
        return options


@formfieldblocks.register('multiline')
class MultiLineFormFieldBlock(FormFieldBlockMixin, StructBlock):
    default_value = CharBlock(required=False)

    class Meta:
        label = 'Multi-Line Field'
        icon = 'form'

    def get_field_options(self, field):
        options = super(MultiLineFormFieldBlock, self).get_field_options(field)
        options['initial'] = field['default_value']
        return options

    def create_field(self, field):
        options = self.get_field_options(field)
        return django.forms.CharField(widget=django.forms.Textarea, **options)


@formfieldblocks.register('email')
class EmailFormFieldBlock(FormFieldBlockMixin, StructBlock):

    class Meta:
        label = 'Email Field'
        icon = 'mail'

    def create_field(self, field):
        options = self.get_field_options(field)
        return django.forms.EmailField(**options)


@formfieldblocks.register('number')
class NumberFormFieldBlock(FormFieldBlockMixin, StructBlock):

    class Meta:
        label = 'Number Field'
        icon = 'order'

    def create_field(self, field):
        options = self.get_field_options(field)
        return django.forms.DecimalField(**options)


@formfieldblocks.register('url')
class UrlFormFieldBlock(FormFieldBlockMixin, StructBlock):

    class Meta:
        label = 'URL Field'
        icon = 'link'

    def create_field(self, field):
        options = self.get_field_options(field)
        return django.forms.URLField(**options)


@formfieldblocks.register('checkbox')
class CheckboxFormFieldBlock(FormFieldBlockMixin, StructBlock):
    default_checked = BooleanBlock(default=False, required=False)

    class Meta:
        label = 'Checkbox Field'
        icon = 'tick-inverse'

    def get_field_options(self, field):
        options = super(CheckboxFormFieldBlock, self).get_field_options(field)
        options['initial'] = field['default_checked']
        return options

    def create_field(self, field):
        options = self.get_field_options(field)
        return django.forms.BooleanField(**options)

    def render_basic(self, value, context=None):
        if context:
            form = context['form']
        else:
            form = {
                self.clean_name(value): self.create_field(value)
            }
        return format_html('<div class="{}">{}{}</div>', self.__class__.__name__.lower(), form[self.clean_name(value)], form[self.clean_name(value)].label_tag())


class FieldChoiceBlock(StructBlock):
    key = CharBlock(required=True)
    description = CharBlock(required=True)

    class Meta:
        label = 'Choice'
        icon = 'tick'


@formfieldblocks.register('dropdown')
class DropdownFormFieldBlock(FormFieldBlockMixin, StructBlock):
    choices = ListBlock(FieldChoiceBlock)
    allow_multiple_selections = BooleanBlock(default=False, required=False)

    class Meta:
        label = 'Dropdown Field'
        icon = 'arrow-down-big'

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
class RadioFormFieldBlock(FormFieldBlockMixin, StructBlock):
    choices = ListBlock(FieldChoiceBlock)

    class Meta:
        label = 'Radio Field'
        icon = 'radio-empty'

    def get_field_options(self, field):
        options = super(RadioFormFieldBlock, self).get_field_options(field)
        options['choices'] = [(x['key'], x['description']) for x in field['choices']]
        return options

    def create_field(self, field):
        options = self.get_field_options(field)
        return django.forms.ChoiceField(widget=django.forms.RadioSelect, **options)


@formfieldblocks.register('date')
class DateFormFieldBlock(FormFieldBlockMixin, StructBlock):

    class Meta:
        label = 'Date Field'
        icon = 'date'

    def create_field(self, field):
        options = self.get_field_options(field)
        return django.forms.DateField(**options)


@formfieldblocks.register('datetime')
class DateTimeFormFieldBlock(FormFieldBlockMixin, StructBlock):

    class Meta:
        label = 'Date & Time Field'
        icon = 'time'

    def create_field(self, field):
        options = self.get_field_options(field)
        return django.forms.DateTimeField(**options)
