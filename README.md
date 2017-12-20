Wagtail Streamfield Forms
=========================

Streamfield Forms allows you to create a form by including the form fields in
the content stream of a Wagtail Page.


Usage Notes
-----------

Creating forms inside ``StreamField``s works like most other ``StreamField`` interactions.
From the end user's perspective, adding form fields in a StreamField works like any other Page.

To set up a Page that contains forms in a ``StreamField``, create a class that inherits from ``StreamFieldAbstractFormMixin`` and ``wagtail.wagtailforms.models.AbstractForm``.
Any class that has ``wagtail.wagtailforms.models.AbstractForm`` as a base class will work so you can also use ``wagtail.wagtailforms.models.AbstractEmailForm``.
Next, add one or more ``StreamField``s to the class and include ``FormFieldBlock`` as one of the blocks that can be in the stream.
See the example below.

```python
    from wagtail.wagtailcore.blocks import CharBlock, RichTextBlock
    from wagtail.wagtailcore.fields import StreamField
    from wagtail.wagtailforms.models import AbstractForm

    from streamfieldforms.blocks import FormFieldBlock
    from streamfieldforms.models import StreamFieldAbstractFormMixin

    class MyStreamFieldFormPage(StreamFieldAbstractFormMixin, AbstractForm):
        body = StreamField([
            ('h2', CharBlock()),
            ('h3', CharBlock()),
            ('p', RichTextBlock()),
            ('field', FormFieldBlock()),
        ])
        thanks = StreamField([
            ('h2', CharBlock()),
            ('h3', CharBlock()),
            ('p', RichTextBlock()),
        ])

    MyStreamFieldFormPage.content_panels = [
        FieldPanel('title', classname='full title'),
        StreamFieldPanel('body'),
        StreamFieldPanel('thank_you_text'),
```

Please notice that no ``form_fields`` member or reference to another model class is necessary as in a normal form class.
Instead the ``StreamFieldAbstractFormMixin`` class provides this for you.

Now when an instance of ``MyStreamFieldFormPage`` is created the form may be displayed on the page.
When the form is submitted it work in the same way as other Form Builder pages by showing a template that ends with ``_landing``.
Also, all values that are submitted are stored in the same way as other Form Builder pages so that exporting and viewing the submissions in the Wagtail admin work exactly the same way.

To render the form into the template you must use a ``get_form_field`` template tag.
This tag allows the form field instance to be stored in a template variable and used to render the form one field at a time.
See the example usage below.

```html
{% load wagtailcore_tags streamfieldforms %}
<html>
<head><title></title></head>
<body>
    <h1>{{ self.title }}</h1>

    <form action="{% pageurl page %}" method="POST">
        {% csrf_token %}

        {% for block in self.body %}
            {% if block.block_type == 'h2' %}
                <h2 id="{{ block|slugify }}">{{ block }}</h2>
            {% elif block.block_type == 'h3' %}
                <h3>{{ block }}</h3>
            {% elif block.block_type == 'p' %}
                {{ block.value|richtext }}
            {% elif block.block_type == 'field' %}
                {% get_form_field block form as field %}
                <div class="form-field">
                    {{ field.label_tag }}
                    {{ field }}
                    {{ field.errors }}
                </div>
            {% else %}
                {{ block }}
            {% endif %}
        {% endfor %}

        <input type="submit" class="button"/>
    </form>
</body>
</html>
```