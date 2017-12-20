from django import forms
from django.test import TestCase


from wagtailstreamfieldforms.blocks import (
    FormFieldBlockMixin,
    SingleLineFormFieldBlock,
    MultiLineFormFieldBlock,
    EmailFormFieldBlock,
    NumberFormFieldBlock,
    UrlFormFieldBlock,
)


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


class TestSingleLineFormFieldBlock(TestCase):

    def test_get_field_options(self):
        slffb = SingleLineFormFieldBlock()
        field_options = {
            'label': 'Test Label',
            'help_text': 'There is no help.',
            'required': True,
            'default_value': 'Test Value'
        }
        opts = slffb.get_field_options(field_options)
        self.assertEqual(opts['label'], field_options['label'])
        self.assertEqual(opts['help_text'], field_options['help_text'])
        self.assertEqual(opts['required'], field_options['required'])
        self.assertEqual(opts['initial'], field_options['default_value'])
        self.assertEqual(opts['max_length'], 255)

    def test_get_field_options_bad_options(self):
        slffb = SingleLineFormFieldBlock()
        with self.assertRaises(KeyError):
            slffb.get_field_options({})

class TestMultiLineFormFieldBlock(TestCase):

    def test_get_field_options(self):
        mlffb = MultiLineFormFieldBlock()
        field_options = {
            'label': 'Test Label',
            'help_text': 'There is no help.',
            'required': True,
            'default_value': 'Test Value'
        }
        opts = mlffb.get_field_options(field_options)
        self.assertEqual(opts['label'], field_options['label'])
        self.assertEqual(opts['help_text'], field_options['help_text'])
        self.assertEqual(opts['required'], field_options['required'])
        self.assertEqual(opts['initial'], field_options['default_value'])

    def test_get_field_options_bad_options(self):
        mlffb = MultiLineFormFieldBlock()
        with self.assertRaises(KeyError):
            mlffb.get_field_options({})

    def test_create_field(self):
        mlffb = MultiLineFormFieldBlock()
        field_options = {
            'label': 'Test Label',
            'help_text': 'There is no help.',
            'required': True,
            'default_value': 'Test Value'
        }
        field = mlffb.create_field(field_options)
        self.assertIsInstance(field, forms.CharField)
        self.assertIsInstance(field.widget, forms.Textarea)
        self.assertEqual(field.initial, field_options['default_value'])


class TestEmailFormFieldBlock(TestCase):

    def test_create_field(self):
        effb = EmailFormFieldBlock()
        field_options = {
            'label': 'Test Label',
            'help_text': 'There is no help.',
            'required': True,
        }
        field = effb.create_field(field_options)
        self.assertIsInstance(field, forms.EmailField)


class TestNumberFormFieldBlock(TestCase):

    def test_create_field(self):
        nffb = NumberFormFieldBlock()
        field_options = {
            'label': 'Test Label',
            'help_text': 'There is no help.',
            'required': True,
        }
        field = nffb.create_field(field_options)
        self.assertIsInstance(field, forms.DecimalField)


class TestUrlFormFieldBlock(TestCase):

    def test_create_field(self):
        uffb = UrlFormFieldBlock()
        field_options = {
            'label': 'Test Label',
            'help_text': 'There is no help.',
            'required': True,
        }
        field = uffb.create_field(field_options)
        self.assertIsInstance(field, forms.URLField)

