# # -*- coding: utf-8 -*-
# from __future__ import absolute_import, unicode_literals

import json

from django.test import TestCase
from wagtail.core.blocks import CharBlock, ListBlock, RichTextBlock, StreamBlock, StructBlock

from wagtailstreamfieldforms.blocks import *
from wagtailstreamfieldforms.models import FormFieldFinder


class TestFormFieldFinder(TestCase):
    def test_simple_case(self):
        # create a StreamBlock and pass a value in to to_python
        class TestBlock(StreamBlock):
            field = SingleLineFormFieldBlock(icon='placeholder')
            p = CharBlock()

        value = TestBlock().to_python([{
            'type': 'field',
            'value': {
                "required": True,
                "default_value": "",
                "label": "Name",
                "help_text": ""
            }
        }, {
            'type': 'p',
            'value': 'A test',
        }, {
            'type': 'field',
            'value': {
                "required": False,
                "default_value": "",
                "label": "Description",
                "help_text": ""
            }
        }])

        finder = FormFieldFinder()

        fields = finder.find_form_fields(TestBlock(), value)

        self.assertEqual(len(fields), 2)
        self.assertIsInstance(fields[0].block, SingleLineFormFieldBlock)
        self.assertIsInstance(fields[1].block, SingleLineFormFieldBlock)

        self.assertEqual(fields[0].value["label"], 'Name')
        self.assertEqual(fields[1].value["label"], 'Description')

    def test_nested_form_fields(self):
        class TestStructBlock(StructBlock):
            title = CharBlock()
            description = CharBlock()
            field = SingleLineFormFieldBlock()


        class TestBlock(StreamBlock):
            field = SingleLineFormFieldBlock(icon='placeholder')
            p = CharBlock()
            special = TestStructBlock()
            list = ListBlock(SingleLineFormFieldBlock(label='Field'))
            stream = StreamBlock([('field', SingleLineFormFieldBlock()), ('p', CharBlock())])

        value = TestBlock().to_python([{
            'type': 'field',
            'value': {
                "required": True,
                "default_value": "",
                "label": "Name",
                "help_text": ""
            }
        }, {
            'type': 'p',
            'value': 'A test',
        }, {
            'type': 'field',
            'value': {
                "required": False,
                "default_value": "",
                "label": "Description",
                "help_text": ""
            }
        }, {
            'type': 'special',
            'value': {
                'title': 'A Test Special',
                'description': 'A longer description of the test special.',
                'field': {
                    "required": True,
                    "default_value": "",
                    "label": "Book Name",
                    "help_text": ""
                }
            }
        }, {
            'type': 'list',
            'value': [
                {
                    "required": True,
                    "default_value": "",
                    "label": "Field Four",
                    "help_text": ""
                }, {
                    "required": True,
                    "default_value": "",
                    "label": "Field Five",
                    "help_text": ""
                }
            ]
        }, {
            'type': 'stream',
            'value': [
                {
                    'type': 'p',
                    'value': 'A test paragraph'
                },
                {
                    'type': 'field',
                    'value': {
                        "required": True,
                        "default_value": "",
                        "label": "Field Six",
                        "help_text": ""
                    }
                }
            ]
        }])

        finder = FormFieldFinder()

        fields = finder.find_form_fields(TestBlock(), value)

        self.assertEqual(len(fields), 6)
        self.assertIsInstance(fields[0].block, SingleLineFormFieldBlock)
        self.assertIsInstance(fields[1].block, SingleLineFormFieldBlock)
        self.assertIsInstance(fields[2].block, SingleLineFormFieldBlock)
        self.assertIsInstance(fields[3].block, SingleLineFormFieldBlock)
        self.assertIsInstance(fields[4].block, SingleLineFormFieldBlock)
        self.assertIsInstance(fields[5].block, SingleLineFormFieldBlock)
        self.assertEqual(fields[0].value["label"], 'Name')
        self.assertEqual(fields[1].value["label"], 'Description')
        self.assertEqual(fields[2].value["label"], 'Book Name')
        self.assertEqual(fields[3].value["label"], 'Field Four')
        self.assertEqual(fields[4].value["label"], 'Field Five')
        self.assertEqual(fields[5].value["label"], 'Field Six')

    def test_complex_form_fields(self):
        TestBlock = StreamBlock([
            ('h2', CharBlock()),
            ('h3', CharBlock()),
            ('p', RichTextBlock()),
            ('singlelinefield', SingleLineFormFieldBlock()),
            ('multilinefield', MultiLineFormFieldBlock()),
            ('emailfield', EmailFormFieldBlock()),
            ('numberfield', NumberFormFieldBlock()),
            ('urlfield', UrlFormFieldBlock()),
            ('checkboxfield', CheckboxFormFieldBlock()),
            ('dropdownfield', DropdownFormFieldBlock()),
            ('radiofield', RadioFormFieldBlock()),
            ('datefield', DateFormFieldBlock()),
            ('datetimefield', DateTimeFormFieldBlock()),
        ])

        value = TestBlock.to_python(json.loads('''\
[{
    "value": {
        "choices": [{
            "description": "Black",
            "key": "black"
        }, {
            "description": "Blue",
            "key": "blue"
        }, {
            "description": "Green",
            "key": "green"
        }, {
            "description": "Orange",
            "key": "orange"
        }, {
            "description": "Red",
            "key": "red"
        }, {
            "description": "White",
            "key": "white"
        }, {
            "description": "Yellow",
            "key": "yellow"
        }],
        "label": "What is your favorite color?",
        "required": true,
        "allow_multiple_selections": false,
        "help_text": "Choose your favorite color from the list below."
    },
    "type": "dropdownfield"
}, {
    "value": {
        "label": "What animal comes to mind when you think of your favorite color?",
        "default_value": "",
        "required": true,
        "help_text": "Don't think really hard. First animal that comes to mind."
    },
    "type": "singlelinefield"
}, {
    "value": {
        "label": "Why is this your favorite color?",
        "default_value": "",
        "required": false,
        "help_text": "Give us two to three sentences that describe why you like this color."
    },
    "type": "multilinefield"
}, {
    "value": {
        "choices": [{
            "description": "Female",
            "key": "female"
        }, {
            "description": "Male",
            "key": "male"
        }],
        "label": "Gender",
        "required": false,
        "help_text": "Are you male or female?"
    },
    "type": "radiofield"
}, {
    "value": {
        "label": "When is your birthday.",
        "required": false,
        "help_text": "This helps us correlate favorite colors by birth month."
    },
    "type": "datefield"
}, {
    "value": {
        "label": "Can we share your answers?",
        "default_checked": true,
        "required": false,
        "help_text": "If you check this box we will share your responses anonymously with everyone that comes to our website."
    },
    "type": "checkboxfield"
}]'''))

        finder = FormFieldFinder()

        fields = finder.find_form_fields(TestBlock, value)

        self.assertEqual(len(fields), 6)
        self.assertIsInstance(fields[0].block, DropdownFormFieldBlock)
        self.assertIsInstance(fields[1].block, SingleLineFormFieldBlock)
        self.assertIsInstance(fields[2].block, MultiLineFormFieldBlock)
        self.assertIsInstance(fields[3].block, RadioFormFieldBlock)
        self.assertIsInstance(fields[4].block, DateFormFieldBlock)
        self.assertIsInstance(fields[5].block, CheckboxFormFieldBlock)

        self.assertEqual(fields[0].value["label"], 'What is your favorite color?')
        self.assertEqual(fields[1].value["label"], 'What animal comes to mind when you think of your favorite color?')
        self.assertEqual(fields[2].value["label"], 'Why is this your favorite color?')
        self.assertEqual(fields[3].value["label"], 'Gender')
        self.assertEqual(fields[4].value["label"], 'When is your birthday.')
        self.assertEqual(fields[5].value["label"], 'Can we share your answers?')

