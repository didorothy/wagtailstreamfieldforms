from django import forms
from django.test import TestCase


from wagtailstreamfieldforms.blocks import FormFieldBlockMixin


class TestFormFieldBlockMixin(TestCase):
    def test_get_field_options_basic(self):
        ffbm = FormFieldBlockMixin()
        field_options = {
            'label': 'Test Label',
            'help_text': 'There is no help.',
            'required': True,
        }
        opts = ffbm.get_field_options(field_options)
        self.assertDictEqual(opts, field_options)

    def test_get_field_options_bad_options(self):
        ffbm = FormFieldBlockMixin()
        with self.assertRaises(KeyError):
            ffbm.get_field_options({})

    def test_create_field(self):
        ffbm = FormFieldBlockMixin()
        field_options = {
            'label': 'Test Label',
            'help_text': 'There is no help.',
            'required': True,
        }
        field = ffbm.create_field(field_options)
        self.assertIsInstance(field, forms.CharField)
        self.assertEqual(field.label, field_options['label'])
        self.assertEqual(field.required, field_options['required'])
        self.assertEqual(field.help_text, field_options['help_text'])

    def test_clean_name(self):
        ffbm = FormFieldBlockMixin()
        field_id = ffbm.clean_name({'label': 'This is A Test'})
        self.assertEqual('this-is-a-test', field_id)

