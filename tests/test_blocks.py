from django import forms
from django.test import TestCase


from wagtailstreamfieldforms.blocks import (
    FormFieldBlockMixin,
    SingleLineFormFieldBlock,
    MultiLineFormFieldBlock,
    EmailFormFieldBlock,
    NumberFormFieldBlock,
    UrlFormFieldBlock,
    CheckboxFormFieldBlock,
    DropdownFormFieldBlock,
    RadioFormFieldBlock,
    DateFormFieldBlock,
    DateTimeFormFieldBlock,
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


class TestCheckboxFormFieldBlock(TestCase):

    def test_get_field_options(self):
        cffb = CheckboxFormFieldBlock()
        field_options = {
            'label': 'Test Label',
            'help_text': 'There is no help.',
            'required': True,
            'default_checked': True,
        }
        opts = cffb.get_field_options(field_options)
        self.assertEqual(opts['label'], field_options['label'])
        self.assertEqual(opts['help_text'], field_options['help_text'])
        self.assertEqual(opts['required'], field_options['required'])
        self.assertEqual(opts['initial'], field_options['default_checked'])

    def test_get_field_options_bad_options(self):
        cffb = CheckboxFormFieldBlock()
        with self.assertRaises(KeyError):
            cffb.get_field_options({})

    def test_create_field(self):
        cffb = CheckboxFormFieldBlock()
        field_options = {
            'label': 'Test Label',
            'help_text': 'There is no help.',
            'required': True,
            'default_checked': True,
        }
        field = cffb.create_field(field_options)
        self.assertIsInstance(field, forms.BooleanField)
        self.assertEqual(field.initial, field_options['default_checked'])


class TestDropDownFormFieldBlock(TestCase):

    def test_get_field_options(self):
        block = DropdownFormFieldBlock()
        field_options = {
            'label': 'Test Label',
            'help_text': 'There is no help.',
            'required': True,
            'choices': [{'key': 'yes', 'description': 'Yes'}, {'key': 'no', 'description': 'No'}]
        }
        opts = block.get_field_options(field_options)
        self.assertEqual(opts['label'], field_options['label'])
        self.assertEqual(opts['help_text'], field_options['help_text'])
        self.assertEqual(opts['required'], field_options['required'])
        self.assertEqual(len(opts['choices']), len(field_options['choices']))
        self.assertEqual(opts['choices'][0], (field_options['choices'][0]['key'], field_options['choices'][0]['description']))
        self.assertEqual(opts['choices'][1], (field_options['choices'][1]['key'], field_options['choices'][1]['description']))


    def test_get_field_options_bad_options(self):
        block = DropdownFormFieldBlock()
        with self.assertRaises(KeyError):
            block.get_field_options({})

    def test_create_field(self):
        block = DropdownFormFieldBlock()
        field_options = {
            'label': 'Test Label',
            'help_text': 'There is no help.',
            'required': True,
            'choices': [{'key': 'yes', 'description': 'Yes'}, {'key': 'no', 'description': 'No'}],
            'allow_multiple_selections': True,
        }
        field = block.create_field(field_options)
        self.assertIsInstance(field, forms.MultipleChoiceField)

        field_options['allow_multiple_selections'] = False
        field = block.create_field(field_options)
        self.assertIsInstance(field, forms.ChoiceField)


class TestRadioFormFieldBlock(TestCase):

    def test_get_field_options(self):
        block = RadioFormFieldBlock()
        field_options = {
            'label': 'Test Label',
            'help_text': 'There is no help.',
            'required': True,
            'choices': [{'key': 'yes', 'description': 'Yes'}, {'key': 'no', 'description': 'No'}],
        }
        options = block.get_field_options(field_options)
        self.assertEqual(len(options['choices']), len(field_options['choices']))
        self.assertEqual(options['choices'][0][0], field_options['choices'][0]['key'])

    def test_create_field(self):
        block = RadioFormFieldBlock()
        field_options = {
            'label': 'Test Label',
            'help_text': 'There is no help.',
            'required': True,
            'choices': [{'key': 'yes', 'description': 'Yes'}, {'key': 'no', 'description': 'No'}],
        }
        field = block.create_field(field_options)
        self.assertIsInstance(field, forms.ChoiceField)


class TestDateFormFieldBlock(TestCase):

    def test_create_field(self):
        block = DateFormFieldBlock()
        field_options = {
            'label': 'Test Label',
            'help_text': 'There is no help.',
            'required': True,
        }
        field = block.create_field(field_options)
        self.assertIsInstance(field, forms.DateField)


class TestDateTimeFormFieldBlock(TestCase):

    def test_create_field(self):
        block = DateTimeFormFieldBlock()
        field_options = {
            'label': 'Test Label',
            'help_text': 'There is no help.',
            'required': True,
        }
        field = block.create_field(field_options)
        self.assertIsInstance(field, forms.DateTimeField)


