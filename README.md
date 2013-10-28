Simple django based AD password changer
======================================

[![Build Status](https://travis-ci.org/mvo5/chpasswd-ldap-django.png)](https://travis-ci.org/mvo5/chpasswd-ldap-django)
[![Coverage Status](https://coveralls.io/repos/mvo5/chpasswd-ldap-django/badge.png?branch=master)](https://coveralls.io/r/mvo5/chpasswd-ldap-django)


Change ldaps/AD password via a webform for those without
direct access to the ldap service.

To install:
-----------

Install dependencies:
```
$ sudo apt-get install python-django python-dnspython
```

Install web-dependencies via nodejs & "bower"
```
$ npm install bower
$ bower install
```

Adjust config.py:
```
$ vi django_project/setting_production.py
```

Run first time init:
```
$ python django_project/first_time_init.py
```

Init database:
```
$ python manage.py syncdb
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

The normal python/django unittest framework is used.
```
$ PYTHONPATH=. python manage.py test chpasswd
```

Get Coverage report:
--------------------

There is a .coveragerc so running python-coverage will work out of the box.
```
$ python-coverage run manage.py test chpasswd
$ python-coverage report
$ python-coverage html
$ firefox htmlcov/index.html
```

Todo:
-----
* Send mail to alternative email address when the AD password got
  changed successfully
