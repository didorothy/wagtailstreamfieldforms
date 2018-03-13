from django.conf.urls import url

from .views import FormsListView, FormSubmissionsListView

urlpatterns = [
    url(r'^$', FormsListView.as_view(), name="index"),
    url(r'^(?P<page_id>[0-9]+)$', FormSubmissionsListView.as_view(), name="submissions"),
]
