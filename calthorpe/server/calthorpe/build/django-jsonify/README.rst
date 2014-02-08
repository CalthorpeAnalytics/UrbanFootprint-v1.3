==============
django-jsonify
==============

Abstract
--------
JSON library for working with django + json

Donors
------
- jsonify filter for Django based on http://djangosnippets.org/snippets/201/
- @ajax_request decorator from django-annoying https://bitbucket.org/offline/django-annoying (Anderson <self.anderson@gmail.com>)

Installation
------------
To install you can use pip:

::

    pip install django-jsonify

Then add `jsonify` to django settings.INSTALLED_APPS


Usage
-----
If you want to convert varianble in django template, you can use jsonify filter:

::

    {% load jsonify %}
    
    {% block content %} <script type="text/javascript">
        <![CDATA[ var items = {{ items|jsonify }}; ]]></script>
    {% endblock %}

If you want to return JSON data from view, you can use @ajax_request decorator

::

    from jsonify.decorators import ajax_request

    @ajax_request
    def my_view(request):
        news = News.objects.all()
        news_titles = [entry.title for entry in news]
        return {'news_titles': news_titles}

