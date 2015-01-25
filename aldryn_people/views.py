# -*- coding: utf-8 -*-

from __future__ import unicode_literals

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
        vcard = person.get_vcard(request)
        try:
            vcard = vcard.decode('utf-8').encode('ISO-8859-1')
        except:
            pass
        response = HttpResponse(vcard, content_type="text/x-vCard")
        response['Content-Disposition'] = 'attachment; filename="{0}"'.format(
            filename)
        return response


class PersonView(DetailView):
    model = Person
