Getting Started
===============

`wagtailstreamfieldforms` is a developer tool first and foremost.
You should be familiar with Django and Wagtail before you begin working with this module.


Installation
------------

To install `wagtailstreamfieldforms` execute the following command:

.. code-block::bash

    pip install git+git://github.com/didorothy/wagtailstreamfieldforms.git#egg=wagtailstreamfieldforms


Creating a Page Model
---------------------

In order to put form fields in a `StreamField` you have to first create a page model that inherits from `wagtailstreamfieldforms.models.AbstractFormPage`.
Secondly, you have to provide a `StreamField` field that specifies which form field blocks are allowed.
If you want to allow the end user to specify the label on the submit button or the message that shows up after form submission you should also provide some other fields for that.

.. code-block::python

    # myapp.models
    from django.db import models

    from wagtail.wagtailcore.blocks import CharBlock, RichTextBlock
    from wagtail.wagtailcore.fields import StreamField
    from wagtailstreamfieldforms.blocks import *
    from wagtailstreamfieldforms.models import AbstractFormPage

    class FormPage(AbstractFormPage):
        form_body = StreamField([
            ('heading', CharBlock(classname="heading")),
            ('paragraph', RichTextBlock()),
            ('image', ImageChooserBlock()),
            ('singlelinefield', SingleLineFormFieldBlock()),
            ('multilinefield', MultiLineFormFieldBlock()),
            ('numberfield', NumberFormFieldBlock()),
            ('emailfield', EmailFormFieldBlock()),
            ('urlfield', UrlFormFieldBlock()),
            ('checkboxfield', CheckboxFormFieldBlock()),
            ('dropdownfield', DropdownFormFieldBlock()),
            ('radiofield', RadioFormFieldBlock()),
            ('datefield', DateFormFieldBlock()),
            ('datetimefield', DateTimeFormFieldBlock()),
        ])
        submit_label = models.CharField(max_length=255)
        submitted_message = StreamField([
            ('heading', CharBlock(classname="heading")),
            ('paragraph', RichTextBlock()),
            ('image', ImageChooserBlock()),
        ])

Additionally, the page model requires a couple of templates to allow it to render properly: `form_page.html` and `form_page_submitted.html`.
`form_page.html` displays the form and `form_page_submitted.html` displays any messages after submission.

Below you can see examples of `form_page.html`.
Notice that we use the `include_block` tag to render the blocks.
This allows for the block to specify how it is rendered and allows for overriding the output.

.. code-block::html

    {% extends "example/base.html" %}
    {% load wagtailcore_tags %}

    {% block content %}
        <form action="{% pageurl self %}" method="POST">
            {% csrf_token %}
            {% for blck in self.body %}
                {% include_block blck %}
            {% endfor %}
            <input type="submit" value="{{ self.submit_label }}"/>
        </form>
    {% endblock %}

Now, you should be able to run `python manage.py makemigrations myapp`, `python manage.py migrate`, and `python manage.py runserver` to begin creating and viewing your new form pages.
