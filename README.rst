Djesi
=====
Django application for handling edge side include (`ESI <http://en.wikipedia.org/wiki/Edge_Side_Includes>`_
) in a simple way.

When to use it
--------------
When you need performance. Every parts of pages that require heavy resources, just put it as ESI.
For instance you have a heavy query category menu and it loads on every single page. In order to apply ESI on it, just put it into separate view, and include the view as ESI fragment.

How to use it
--------------
Djesi take a easiest approach to implement ESI using `Varnish <https://www.varnish-cache.org/>`_.
Djesi works from template tag, invoking other view into main template using django url template tag style.

Installation and Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Clone djesi from https://github.com/herlambang/djesi or download the compressed package. Within the root package run::

    python setup.py install

- Within settings.py add djesi in INSTALLED_APPS::

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        ....
        'djesi',
    )

- Add djesi middleware in MIDDLEWARE_CLASSES::
    
    MIDDLEWARE_CLASSES = (
        ....
        'djesi.middleware.esi.DjangoEsiMiddleware',
    )

- Enable request context processor in TEMPLATE_CONTEXT_PROCESSORS::

    TEMPLATE_CONTEXT_PROCESSORS = (
                                ....
                                "django.core.context_processors.request",
                                )

- Set whether esi template tag will draw ESI tag or view response. If not defined, default value will be settings.DEBUG ::

    USE_ESI = True


Varnish Configuration
^^^^^^^^^^^^^^^^^^^^^
In varnish configuration file (default.vcl) put these lines within vcl_fetch section

::

    sub vcl_fetch {

        ### check if header contains surrogate-control to enable esi ###
        if (beresp.http.Surrogate-Control ~ "ESI/1.0") {
            unset beresp.http.Surrogate-Control;
            set beresp.do_esi = true;
        }

    }

Djesi initialize Surrogate-Control header, so varnish could know when it should enable ESI feature, because not all requests need this header, and not all requests is contains ESI tag. Djesi only send this header, through it's middleware, whenever a response contains ESI tag and ESI are enabled in the settings.  

Usage (Sample Case)
^^^^^^^^^^^^^^^^^^^^^
For example, you have a view that display category and article content::

    from django.shortcuts import render

    def show_article(request, id):
        article = Article.objects.get(pk=id)
        categories = Category.objects.all()
        return render(request, 'article.html', {'article': article, 'categories': categories})

With URL::

    url(r'^article/(?P<id>\d+)/$', 'myapp.views.show_article', name='show_article'),

And template (article.html)::

    <html>
    <body>
        <div class="menu">
        <ul>
        {% for category in categories %}
            <li>{{ category.title }}</li>
        {% endfor %}
        <ul>
        </div>
        <div class="content">
            <h1>{{ article.title }}</h1>
            <div>{{ article.content }}</div>
        </div>
    </body>
    </html>

And you want to cache the category as an ESI page for 1 day. 

This is what you should do. 

- Pull out the category processing and put it on different view. 
- Define s-maxage parameter using cache control decorator on your category view.


::

    from django.shortcuts import render
    from django.views.decorators.cache import cache_control

    def show_article(request, id):
        article = Article.objects.get(pk=id)
        return render(request, 'article.html', {'article': article,})

    @cache_control(s_maxage=86400)
    def show_categories(request):
        category = Category.objects.all()
        return render(request, 'category.html', {'category': category})

With URL::

    url(r'^article/(?P<id>\d+)/$', 'myapp.views.show_article', name='show_article'),
    url(r'^categories/$', 'myapp.views.show_categories', name='show_categories'),

Templates:

- category.html

::

    <div class="menu">
        <ul>
        {% for category in categories %}
            <li>{{ category.title }}</li>
        {% endfor %}
        <ul>
    </div>

- article.html (main template which will include category view as ESI page)

::

    {% load djesi %}
    <html>
    <body>
        {% esi 'show_categories' %}
        <div class="content">
            <h1>{{ article.title }}</h1>
            <div>{{ article.content }}</div>
        </div>
    </body>
    </html>

The esi template tag used just like django url template tag. For example if you have url pattern with parameters, the esi template tag call will be like this::

    {% esi 'show_category' id=10 %}
    {% esi 'show_articles' year=10 month=03 %}

or 

::

    {% esi 'myapp.views.show_category' id=10 %}
    {% esi 'myapp.views.show_articles' year=10 month=03 %}



