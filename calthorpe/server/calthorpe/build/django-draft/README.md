Django-Draft
===============

Allow the creation of drafts in the admin. It is compatible with both the default django admin and django-grappelli.

Installation
------------

    pip install git+git://github.com/platypus-creation/django-draft.git

or:

    git clone git://github.com/platypus-creation/django-draft.git
    cd django-draft
    python setup.py install


Add `draft` to your INSTALLED_APPS

    INSTALLED_APPS = (
        ...
        'draft',
    )

Create the database table
    
    python manage.py syncdb

or if you are using South (you should)

    python manage.py migrate draft

You are done.

Django-draft detects if grappelli is installed and will display accordingly.

Usage
-----

Add draft support in the admin to your model by registering them with a DraftAdmin Class which inherits the ModelAdmin Class


    from myapp.models import MyModel
    from draft.admin import DraftAdmin

    class MyModelAdmin(DraftAdmin):
        """
        Declare everything as usual here
        """
        pass
    
    
    admin.site.register(MyModel, MyModelAdmin)
    
You should now have a save as draft button available in the admin for this model !

As soon as you have a draft, you'll be able to reload it later, or discard it

Under the hood
--------------

Django draft save the serialized current form and is able to reload it later. It has no knowledge of your models whatsoever, it simply saves a query dict and is able to reload it in Javascript.