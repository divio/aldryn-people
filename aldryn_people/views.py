from django.http import Http404, HttpResponse
from django.views.generic import DetailView

from aldryn_people.models import Person


class DownloadVcardView(DetailView):
    model = Person

    def get(self, request, *args, **kwargs):
        person = self.get_object()
        if not person.vcard_enabled:
            raise Http404

        filename = "%s.vcf" % person.name
        response = HttpResponse(person.get_vcard(request), mimetype="text/x-vCard")
        response['Content-Disposition'] = 'attachment; filename="%s"' % filename
        return response


class PersonView(DetailView):
    model = Person
