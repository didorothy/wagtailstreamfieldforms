import os.path

from django.db import models
from django.contrib.auth.models import User

from wagtail.wagtailcore.blocks import ListBlock, StreamBlock, StructBlock
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Page

from .blocks import FormFieldBlockMixin
from .forms import BlockField, FormBuilder


class Submission(models.Model):
    '''Represents a submission for a form.'''
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Submission - {0} - {1}'.format(
            self.page.title,
            self.created.strftime('%Y-%m-%d %H:%M:%s')
        )


class SubmissionField(models.Model):
    '''Represents a sbumitted field in a submission form.'''
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    field_name = models.CharField(max_length=255)
    field_value = models.TextField(blank=True)
    field_type = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return '{0}: {1}'.format(self.field_name, self.field_value)





class FormFieldFinder(object):
    '''Class that handles finding all nested form fields recursively.

    Adding to this class requires adding new handle methods and overriding the find_form_fields function.
    If you have a special form field that needs special handling:

        class SpecialFormFieldFinder(FormFieldFinder):
            def handle_special_form_field_block(self, block, value):
                return [SpecialAbstractField(**value)]

            def find_form_fields(self, block, value):
                if isinstance(block, SpecialFormFieldBlock):
                    return self.handle_special_form_field(block, value)
                else:
                    return super(SpecialFormFieldFinder, self).find_form_fields(block, value)

    If you have a special block that does not inherit from StructBlock, StreamBlock, or ListBlock but has child blocks:

        class SpecialFormFieldFinder(FormFieldFinder):
            def handle_special_block(self, block, value):
                form_fields = []
                for val in value:
                    form_fields += self.find_form_fields(block.block, val)
                return form_fields

            def find_form_fields(self, block, value):
                if isinstance(block, SpecialBlock):
                    return self.handle_special_block(block, value)
                else:
                    return super(SpecialFormFieldFinder, self).find_form_fields(block, value)
    '''

    def handle_form_field_block(self, block, value):
        '''This is the base case and allows the recursion to stop.'''
        if isinstance(block, FormFieldBlockMixin):
            return [BlockField(block, value)]
        else:
            raise Exception('Block does not inherit from FormFieldBlockMixin.')

    def handle_struct_block(self, block, value):
        '''Handles looping through StructBlock fields.'''
        form_fields = []
        for key in block.child_blocks:
            form_fields += self.find_form_fields(block.child_blocks[key], value[key])
        return form_fields

    def handle_stream_block(self, block, value):
        '''Handles looping through StreamBlock values.'''
        form_fields = []
        for val in value:
            form_fields += self.find_form_fields(val.block, val.value)
        return form_fields

    def handle_list_block(self, block, value):
        '''Handles looping through ListBlock values.'''
        form_fields = []
        for val in value:
            form_fields += self.find_form_fields(block.child_block, val)
        return form_fields

    def find_form_fields(self, block, value):
        '''Finds all form fields by determining block type and recursively
        calling various handle methods for each block type.
        '''
        if isinstance(block, FormFieldBlockMixin):
            return self.handle_form_field_block(block, value)
        elif isinstance(block, StreamBlock):
            return self.handle_stream_block(block, value)
        elif isinstance(block, StructBlock):
            return self.handle_struct_block(block, value)
        elif isinstance(block, ListBlock):
            return self.handle_list_block(block, value)
        else:
            return []


class AbstractFormPage(Page):

    def __init__(self, *args, **kwargs):
        super(AbstractFormPage, self).__init__(*args, **kwargs)
        if not hasattr('form_submitted_template'):
            name, ext = os.path.splitext(self.template)
            self.form_submitted_template = name + '_submitted' + ext

    class Meta:
        abstract = True

    def get_form_field_finder(self):
        return FormFieldFinder()

    def get_form_builder(self):
        return FormBuilder(self.get_form_fields())

    def get_form_fields(self):
        finder = self.get_form_field_finder()
        form_fields = []
        for field in self.__class__._meta.get_fields():
            if isinstance(field, StreamField):
                form_fields += finder.find_form_fields(field.stream_block, getattr(self, field.name))
        return form_fields

    def get_form_class(self):
        return self.get_form_builder().get_form_class()

    def process_form_submission(self, form):
        sub = Submission()
        sub.page = self
        sub.save()
        for key in form.cleaned_data:
            sub_field = SubmissionField()
            sub_field.submission = sub
            sub_field.field_name = key
            sub_field.field_value = form.cleaned_data[key]
            sub_field.field_type = None # oops bad.

