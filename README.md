Simple django based AD password changer
======================================

Change ldaps/AD password via a webform for those without
direct access to the ldap service.

To install:
-----------

Install dependencies:
```
$ sudo apt-get install python-django python-pydns
```

Install web-dependencies:
```
$ (cd static ; ./get.sh)
```

Adjust config.py:
```
$ vi django_project/setting.py
```

Configure apache to use "django_project/wsgi.py" in a https context, the
service will not run on plain http because of the security
implications it has.

To test-run locally:
--------------------
```
$ CHPASSWD_AD_DEBUG=1 python manage.py runserver
```


To run the tests:
-----------------
```
$ PYTHONPATH=. python manage.py test chpasswd
```


