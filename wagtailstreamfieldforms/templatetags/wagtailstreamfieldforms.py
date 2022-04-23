from django import template

register = template.Library()


@register.filter(name="unslugify")
def unslugify(value):
    return str(value).replace('-', ' ').capitalize()
