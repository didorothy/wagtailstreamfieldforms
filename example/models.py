from django.db import models

from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.blocks import CharBlock, RichTextBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock

from wagtailstreamfieldforms.blocks import (
    SingleLineFormFieldBlock,
    MultiLineFormFieldBlock,
    NumberFormFieldBlock,
    EmailFormFieldBlock,
    UrlFormFieldBlock,
    CheckboxFormFieldBlock,
    DropdownFormFieldBlock,
    RadioFormFieldBlock,
    DateFormFieldBlock,
    DateTimeFormFieldBlock
)
from wagtailstreamfieldforms.models import AbstractFormPage

class HomePage(AbstractFormPage):
    '''Basic page type for our example site.'''
    author = models.CharField(max_length=255)
    date = models.DateField("Post Date")
    body = StreamField([
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
    submit_label = models.CharField(max_length=255, default='Submit')
    submitted_body = StreamField([
        ('heading', CharBlock(classname="heading")),
        ('paragraph', RichTextBlock()),
        ('image', ImageChooserBlock()),
    ])

    content_panels = Page.content_panels + [
        FieldPanel('author'),
        FieldPanel('date'),
        StreamFieldPanel('body'),
        FieldPanel('submit_label'),
        StreamFieldPanel('submitted_body')
    ]
