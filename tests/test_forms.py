# -*- coding: utf-8 -*-
from django import forms
from django.test import TestCase

from wagtail.core.blocks import StructBlock

from wagtailstreamfieldforms.blocks import FormFieldBlockMixin
from wagtailstreamfieldforms.forms import FormFieldBlockRegistry, BlockField, FormBuilder


class TestFormFieldBlockRegistry(TestCase):

    def test_register_and_lookup(self):
        registry = FormFieldBlockRegistry()

        @registry.register("test")
        class TestFieldBlock(StructBlock, FormFieldBlockMixin):
            '''Created for testing purposes only so no extra customization.'''
            pass

        self.assertEqual(list(registry.field_types.keys()), ['test'])
        self.assertEqual(registry.field_types['test'], TestFieldBlock)
        self.assertEqual(registry.lookup_type('test'), TestFieldBlock)

    def test_register_as_function(self):
        registry = FormFieldBlockRegistry()

        class TestFieldBlock(StructBlock, FormFieldBlockMixin):
            '''Created for testing purposes only so no extra customization.'''
            pass
        registry.register('test', TestFieldBlock)

        self.assertEqual(list(registry.field_types.keys()), ['test'])
        self.assertEqual(registry.field_types['test'], TestFieldBlock)
        self.assertEqual(registry.lookup_type('test'), TestFieldBlock)

    def test_register_duplicate_name_raises_exception(self):
        '''When you try to register a block with the same name it should raise an Exception.'''
        registry = FormFieldBlockRegistry()

        @registry.register("test")
        class TestFieldBlock(StructBlock, FormFieldBlockMixin):
            '''Created for testing purposes only so no extra customization.'''
            pass

        with self.assertRaises(ValueError):
            @registry.register("test")
            class TestFieldBlock2(StructBlock, FormFieldBlockMixin):
                '''Created for testing purposes only so no extra customization.'''
                pass
        self.assertEqual(registry.lookup_type('test'), TestFieldBlock)


class TestFieldBlock(StructBlock, FormFieldBlockMixin):
    '''Created for testing purposes only so no extra customization.'''
    pass


class TestBlockField(TestCase):

    def test_get_form_field(self):
        block = TestFieldBlock()
        value = {
            'label': 'Test Block',
            'help_text': '',
            'required': True,
        }
        bf = BlockField(block, value)
        self.assertIsInstance(bf.get_form_field(), forms.Field)

    def test_get_field_id(self):
        block = TestFieldBlock()
        value = {
            'label': 'Test Block',
            'help_text': '',
            'required': True,
        }
        bf = BlockField(block, value)
        self.assertEqual(bf.get_field_id(), 'test-block')


class TestFormBuilder(TestCase):

    def test_form_fields_property(self):
        fields = [
            BlockField(TestFieldBlock(), {
                'label': 'Test Block',
                'help_text': '',
                'required': True
            }),
        ]

        form_builder = FormBuilder(fields)
        self.assertEqual(len(form_builder.formfields), 1)
        self.assertIsInstance(form_builder.formfields['test-block'], forms.Field)

    def test_get_form_class(self):
        fields = [
            BlockField(TestFieldBlock(), {
                'label': 'Test Block',
                'help_text': '',
                'required': True
            }),
        ]

        form_builder = FormBuilder(fields)
        form_cls = form_builder.get_form_class()
        form = form_cls()
        self.assertIsInstance(form, forms.Form)
        self.assertIsInstance(form['test-block'], forms.BoundField)
