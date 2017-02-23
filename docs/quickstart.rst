Prerequisites
===============

This requirements are automatically installed with pip and are include in the setup.py file

reportlab => The ReportLab Toolkit. An Open Source Python library for generating PDFs and graphics.

django-auxiliare => core package which provides static content and basics views.


Installing
============

Install the apps with pip ::

    $ pip install nxt-simplecost

Configure your settings file
-------------------------------

Add django-paperworks to your installed_apps ::

    INSTALLED_APPS = [
        ...
        'auxiliare'
        'simplecost',
    ]

Configure your urls file
-----------------------------

Add django-paperworks to urls file ::

    from django.conf.urls import url, include
    from simplecost import urls
    ...
    urlpatterns = [
        ...
        url(r'^', include('simplecost.urls')),
    ]

