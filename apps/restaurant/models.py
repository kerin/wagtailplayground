from django.db import models
from django.template.response import TemplateResponse

from modelcluster.fields import ParentalKey

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import (FieldPanel,
                                                InlinePanel, PageChooserPanel)


def ajax_serve(obj, request):
    base = 'base_fragment.html' if request.is_ajax() else 'base.html'

    return TemplateResponse(request, obj.template, {
        'base': base,
        'self': obj
    })


class Section(Page):
    intro = RichTextField()

    def serve(self, request):
        return ajax_serve(self, request)

Section.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('intro', classname='full'),
]


class BlogPost(Page):
    body = RichTextField()

    def serve(self, request):
        return ajax_serve(self, request)


BlogPost.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('body', classname='full')
]


class HomePageFeaturedSection(Orderable):
    homepage = ParentalKey('restaurant.HomePage',
                           related_name='featured_sections')
    section = models.ForeignKey('restaurant.Section')

    panels = [
        PageChooserPanel('section'),
    ]


class HomePage(Page):
    intro = RichTextField()

    def serve(self, request):
        return ajax_serve(self, request)

HomePage.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('intro', classname='full'),
    InlinePanel(HomePage, 'featured_sections', label='Featured sections')
]
