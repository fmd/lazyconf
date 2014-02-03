===============
django-lazyconf
===============
django-lazyconf is an insultingly simple tool for configuring and deploying Django 1.7+ applications. 

Dependencies
------------
* `Django 1.7 <https://github.com/django/django>`_
* `Fabric <http://docs.fabfile.org/en/1.8/>`_

Usage
-----
The basic idea is that you include lazyconf in your fabfile::

    from lazyconf import Lazyconf