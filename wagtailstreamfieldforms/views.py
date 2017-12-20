from django.core.exceptions import PermissionDenied
from django.views.generic import ListView

from .models import Submission


class FormsListView(ListView):
    template_name = 'wagtailstreamfieldforms/formlist.html'

    def dispatch(self, request, *args, **kwargs):
        if not (request.user and request.user.has_perm('streamfieldforms.list_forms')):
            raise PermissionDenied()
        return super(FormsListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Submission.objects.order_by('page__name').distinct('page')