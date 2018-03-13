from django.conf.urls import include, url
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView

from wagtail.wagtailcore import hooks
from wagtail.wagtailadmin.menu import MenuItem

from .models import Submission, SubmissionField
from . import urls

@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^streamfieldforms/', include(urls, namespace='streamfieldforms'))
    ]

@hooks.register('register_admin_menu_item')
def register_streamfield_forms_menu():
    return MenuItem(
        _('StreamField Forms'),
        reverse('streamfieldforms:index'),
        classnames="icon icon-form",
        order=700
    )
