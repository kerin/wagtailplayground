import json

from django.db import models
from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import render_to_string

from modelcluster.fields import ParentalKey

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import (FieldPanel,
                                                InlinePanel, PageChooserPanel)


def ajax_serve(obj, request):
    base = 'base_fragment.html' if request.is_ajax() else 'base.html'

    ctx = RequestContext(request, {
        'base': base,
        'self': obj
    })
    html = render_to_string(obj.template, ctx)

    if request.is_ajax():
        return HttpResponse(json.dumps({'html': html}),
                            content_type='application/json')
    else:
        return HttpResponse(html)


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

    @property
    def menu_lists(self):
        return MenuList.objects.filter(path__startswith=self.path).order_by('path')

    @property
    def menu_pages(self):
        return MenuPage.objects.filter(path__startswith=self.path).order_by('path')

    def serve(self, request):
        return ajax_serve(self, request)

HomePage.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('intro', classname='full'),
    InlinePanel(HomePage, 'featured_sections', label='Featured sections')
]


class MenuList(Page):
    intro = RichTextField(blank=True, default='')

MenuList.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('intro', classname='full'),
]


class MenuItem(Orderable):
    section = ParentalKey('restaurant.MenuSection', related_name='menu_items')
    name = models.CharField(max_length=254)
    description = RichTextField(blank=True, default='')
    pricing = models.CharField(max_length=254)
    featured = models.BooleanField(default=False)

    panels = [
        FieldPanel('name'),
        FieldPanel('description'),
        FieldPanel('pricing'),
        FieldPanel('featured'),
    ]


class MenuPage(Page):
    intro = RichTextField(blank=True, default='')
    footer = RichTextField(blank=True, default='')

    @property
    def sections(self):
        return MenuSection.objects.filter(path__startswith=self.path).order_by('path')

MenuPage.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('intro', classname='full'),
    FieldPanel('footer', classname='full'),
]


class MenuSection(Page):
    intro = RichTextField(blank=True, default='')

MenuSection.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('intro', classname='full'),
    InlinePanel(MenuSection, 'menu_items', label='Menu Items'),
]
