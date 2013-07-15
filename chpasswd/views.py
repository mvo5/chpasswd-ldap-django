#!/usr/bin/python

import datetime

from django.shortcuts import (
    render_to_response,
)
from django.http import (
    HttpResponse,
)

import ldap

from chpasswd import chpasswd_ad
from forms import ChpasswdForm

from models import (
    ADUser,
    PasswordChangeLog,
)

from django_project.settings import (
    CHPASSWD_SERVER,
    CHPASSWD_DOMAIN,
    CHPASSWD_MIN_PASSWORD_SIZE,
)


def chpasswd_prompt(request):
    return render_to_response("chpasswd/chpasswd_prompt.html")


def chpasswd_change(request):
    if request.method == "POST":
        form = ChpasswdForm(request.POST)
        if form.is_valid():
            # sanity checks
            if form.cleaned_data["new_pass1"] != form.cleaned_data["new_pass2"]:
                return HttpResponse("passwords don't match")

            if len(form.cleaned_data["new_pass1"]) < CHPASSWD_MIN_PASSWORD_SIZE:
                return HttpResponse("password too short")

            # auto add domain if not given
            (user, sep, domain) = form.cleaned_data["user"].partition("@")
            if not domain:
                user = "%s@%s" % (user, CHPASSWD_DOMAIN)

            (ad_user, created) = ADUser.objects.get_or_create(username=user)
            log = PasswordChangeLog.objects.create(
                ad_user=ad_user,
                source_ip = request.META["REMOTE_ADDR"],
                when = datetime.datetime.now())
            log.save()

            # now do the actual change
            try:
                chpasswd_ad(CHPASSWD_SERVER, 
                            user,
                            form.cleaned_data["old_pass"], 
                            form.cleaned_data["new_pass1"])
            except ldap.LDAPError as e:
                log.success = False
                log.fail_reason = e
                log.save()
                return HttpResponse("Failed to change password")
            log.success = True
            log.save()
    return HttpResponse("Password changed")
    

