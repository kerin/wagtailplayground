Vagrant setup
=============

1. Install [Ansible](http://docs.ansible.com/): `brew install ansible`
2. `vagrant up`
3. `vagrant ssh`
4. `./manage.py syncdb`
5. `./manage.py migrate`
6. `./manage.py runserver 0.0.0.0:8000`
7. [http://127.0.0.1:8001](http://127.0.0.1:8001) in your browser


Django / wagtail notes
======================

Everything of interest is in the 'restaurants' app - the blog app is a vestigial early experiment.

## AJAX response handling

Wagtail Page models are responsible for returning a rendered template, rather than a view function as is standard for django apps, via the `serve()` method. Pages that can be retrieved as both full HTML pages and HTML fragments for use via AJAX calls override this `serve()` method and return either a full page or JSON response like `{html: '<h1>...</h1>'}` with the appropriate content-type header.

The template itself is assembled by setting the `base` context variable to either `base.html` (full HTML page) or `base_fragment.html` (AJAX responses) before rendering the response. This allows both full and partial pages to use the same page template with minimal django gymnastics.

## MenuPage / MenuSection / MenuItem structure

As it's not possible for wagtail's admin UI to represent a Parent -> Child -> Child relationship (and nor is it in Django admin), menus are currently being handled like this:

```
MenuPage (type: Page)
    MenuSection (type: Page)
        MenuItem (type: Model)
```

So, menu item **objects** are edited as inlines on menu section **pages** which are child pages of menu pages. Menu section pages do not need to be treated as actual pages by the frontend, or appear in navigation menus.

For ease of use in templates, MenuPage models have a `sections` property, which uses the MPTT path to efficiently retrieve child MenuSections only:

```
@property
def sections(self):
    return MenuSection.objects.filter(path__startswith=self.path).order_by('path')
```


## Content panels

Example:

```
class BlogPageThing(models.Model):
	page = ParentalKey('app.BlogPage', related_name='page_things')
	name = models.CharField(max_length=255)
	
	panels = [
		FieldPanel('name'),
	]
	
class BlogPage(Page):
	intro = RichTextField()
	
BlogPage.content_panels = [
	FieldPanel('title', classname='full title'),
    FieldPanel('intro', classname='full'),
    InlinePanel(BlogPage, 'page_things', label='Page Things')
]
```

Page content panels define which fields are available in Wagtail admin edit/create views - equivalent to django ModelAdmin - and include some wagtail-specific fields like PageChooserPanel, ImageChooserPanel and DocumentChooserPanel.

`content_panels` are defined outside of the class definition seemingly because InlinePanel requires the class name of the page as its first argument.

`panels` are applicable to non-page objects that are included as inlines, and as they can't include InlinePanels themselves, they can be defined directly in the class definition.

## Maps
`apps.restaurant.models` contains an abstract django model, `MapModel`, which provides a google map URL field, which validates for a [new-style Google maps URL](https://www.google.com/maps/place/Berwick+St/@51.5142102,-0.1343658,17z), and provides longitude, latitude and zoomlevel properties via regexing the URL. This could be handled as a custom django field type instead, but this was the simplest approach in the short term.

## Known Issues

1. There seems to be an issue where pages lose their computed URLs if the root page is renamed - this has been [filed as a bug](https://github.com/torchbox/wagtail/issues/157)
2. Page DateTimeFields using the `auto_now_add` argument seem to cause a DB error on save. The root cause of this hasn't been uncovered, but it seems to be related to Wagtail's use of [django-modelcluster](https://pypi.python.org/pypi/django-modelcluster). This can be worked around in the models' `save()` method until this is fixed in Wagtail.


Frontend notes
==============

The frontend currently uses require.js for JS management, and Backbone.js for the homepage 'app'. The structure of this is on the quick and dirty side, but is really only a placeholder at present. There are however...

## Known Issues

### History handling
There is a browser history-related bug in webkit browsers which manifests itself when multiple backbone URL pushstates have occurred, then one of the detail URLs is hit directly in the same browser window - hitting the back button changes the URL but does not change the page.

This is arguably an edge case, but this could potentially also be worked around by using hash links in Backbone world and issuing a redirect to detail pages on initial page load where necessary, or by monitoring window.onpushstate on pages other than the homepage, or possibly by using a custom Backbone router. Or by not using Backbone.

### JS on homepage HTML fragments
As Backbone retrieves and displays fragments of full HTML detail pages, any Javascript required for that fragment (ie. Google Maps) must be executed after Backbone has rendered the view - see the use of gmaps.js as an example.