from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView

from wagtail.wagtailcore.models import Page

from .models import Submission


class FormsListView(ListView):
    template_name = 'wagtailstreamfieldforms/formlist.html'
    paginate_by = 20

    def dispatch(self, request, *args, **kwargs):
        if not (request.user and request.user.has_perm('streamfieldforms.list_forms')):
            raise PermissionDenied()
        return super(FormsListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Submission.objects.values('page__id', 'page__title').annotate(count=Count('id')).order_by('page__title')


class FormSubmissionsListView(ListView):
    template_name = 'wagtailstreamfieldforms/submissionlist.html'
    paginate_by = 20

    def dispatch(self, request, *args, **kwargs):
        if not (request.user and request.user.has_perm('streamfieldforms.list_submissions')):
            raise PermissionDenied()

        try:
            self.page_id = int(self.kwargs['page_id'])
            self.page = Page.objects.get(pk=self.page_id)
        except (IndexError, ValueError):
            return redirect(reverse('streamfieldforms:index'))

        return super(FormSubmissionsListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Submission.objects.select_related().filter(page=self.page_id).order_by('-created')

    def get_context_data(self, *args, **kwargs):
        data = super(FormSubmissionsListView, self).get_context_data(*args,**kwargs)
        data['page'] = self.page
        field_names = ['created', 'user']
        data_dicts = []
        for row in data['object_list']:
            values = {
                'created': row.created,
                'user': row.user,
            }
            for key, value in row.fields():
                if key not in field_names:
                    field_names.append(key)
                values[key] = value
            data_dicts.append(values)

        data_rows = []
        for row in data_dicts:
            values = []
            for name in field_names:
                values.append(row.get(name, None))
            data_rows.append(values)

        data['field_names'] = field_names
        data['rows'] = data_rows

        return data
