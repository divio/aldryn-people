# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.http import Http404, HttpResponse
from django.views.generic import DetailView, ListView

from menus.utils import set_language_changer
from parler.views import TranslatableSlugMixin

from .models import Group, Person


class LanguageChangerMixin(object):
    """
    Convenience mixin that adds CMS Language Changer support.
    """
    def get(self, request, *args, **kwargs):
        if not hasattr(self, 'object'):
            self.object = self.get_object()
        set_language_changer(request, self.object.get_absolute_url)
        return super(LanguageChangerMixin, self).get(request, *args, **kwargs)


class AllowPKsTooMixin(object):
    def get_object(self, queryset=None):
        """
        Bypass TranslatableSlugMixin if we are using PKs. You would only use
        this if you have a view that supports accessing the object by pk or
        by its translatable slug.

        NOTE: This should only be used on DetailViews and this mixin MUST be
        placed to the left of TranslatableSlugMixin. In fact, for best results,
        declare your view like this:

            MyView(…, AllowPKsTooMixin, TranslatableSlugMixin, DetailView):
        """
        if self.pk_url_kwarg in self.kwargs:
            return super(DetailView, self).get_object(queryset)

        # OK, just let Parler have its way with it.
        return super(AllowPKsTooMixin, self).get_object(queryset)


class DownloadVcardView(AllowPKsTooMixin, TranslatableSlugMixin, DetailView):
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


class PersonDetailView(LanguageChangerMixin, AllowPKsTooMixin,
                       TranslatableSlugMixin, DetailView):
    model = Person


class GroupDetailView(LanguageChangerMixin, AllowPKsTooMixin,
                      TranslatableSlugMixin, DetailView):
    model = Group


class GroupListView(ListView):
    model = Group

    def get_context_data(self, **kwargs):
        context = super(GroupListView, self).get_context_data(**kwargs)
        context['ungrouped_people'] = Person.objects.filter(
            groups__isnull=True)
        return context
