from django.db import models

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, MultiFieldPanel,
                                                InlinePanel, PageChooserPanel)
from modelcluster.fields import ParentalKey


class BlogPage(Page):
    body = RichTextField()
    date = models.DateField("Post date")
    search_name = "Blog Page"

    indexed_fields = ('body', )

BlogPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('date'),
    FieldPanel('body', classname="full"),
]


# class LinkFields(models.Model):
#     link_page = models.ForeignKey('wagtailcore.Page', null=True, blank=True,
#                                   related_name='+')
#     panels = [
#         PageChooserPanel('link_page'),
#     ]

#     class Meta:
#         abstract = True


# class RelatedLink(models.Model):
#     title = models.CharField(max_length=255, help_text="Link title")
#     link_page = models.ForeignKey('wagtailcore.Page', null=True, blank=True,
#                                   related_name='+')

#     panels = [
#         FieldPanel('title'),
#         MultiFieldPanel([
#             PageChooserPanel('link_page'),
#         ], "Link")
#     ]

#     class Meta:
#         abstract = True


# class BlogIndexPageRelatedLink(Orderable):
#     page = ParentalKey('blog.BlogIndexPage', related_name='related_links')


class BlogIndexPageRelatedLink(Orderable):
    page = ParentalKey('blog.BlogIndexPage', related_name='related_links')
    title = models.CharField(max_length=255, help_text="Link title")
    link_page = models.ForeignKey('wagtailcore.Page', null=True, blank=True,
                                  related_name='+')

    # panels = [
    #     FieldPanel('title'),
    #     MultiFieldPanel([
    #         PageChooserPanel('link_page'),
    #     ], "Link")
    # ]

    panels = [
        FieldPanel('title'),
        PageChooserPanel('link_page'),
    ]


class BlogIndexPage(Page):
    intro = models.CharField(max_length=255)
    indexed_fields = ('body', )
    search_name = "Blog Index Page"

BlogIndexPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('intro', classname="full"),
    InlinePanel(BlogIndexPage, 'related_links', label="Related Links"),
]
