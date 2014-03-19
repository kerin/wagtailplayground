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
