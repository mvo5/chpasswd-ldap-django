#!/usr/bin/python

import datetime

from django.shortcuts import (
    render_to_response,
)
from django.template import RequestContext
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
)

from chpasswd import chpasswd_ad
from forms import ChpasswdForm

from models import (
    ADUser,
    PasswordChangeLog,
)

from django_project.settings import (
    CHPASSWD_DOMAIN,
    CHPASSWD_MIN_PASSWORD_SIZE,
    CHPASSWD_RATE_LIMIT_TIME,
    CHPASSWD_RATE_LIMIT_ATTEMPTS,
)


def chpasswd_prompt(request):
    return render_without_msg(request)

def render_without_msg(request):
    return render_with_msg(request)

def render_with_msg(request, msg = None, success = None):
    return render_to_response("chpasswd/chpasswd_prompt.html",
                              dictionary={"msg" : msg, "success" : success},
                              context_instance=RequestContext(request))

def chpasswd_change(request):
    if request.method == "POST":
        form = ChpasswdForm(request.POST)
        if form.is_valid():
            # sanity checks
            new_pass1 = form.cleaned_data["new_pass1"]
            new_pass2 = form.cleaned_data["new_pass2"]
            if new_pass1 != new_pass2:
                return render_with_msg(request, 
                                        msg="passwords don't match",
                                        success=False)

            if len(new_pass1) < CHPASSWD_MIN_PASSWORD_SIZE:
                return render_with_msg(request,
                                        msg="password too short",
                                        success=False)

            # auto add domain if not given
            (user, sep, domain) = form.cleaned_data["user"].partition("@")
            if not domain:
                user = "%s@%s" % (user, CHPASSWD_DOMAIN)

            now = datetime.datetime.now()
            start = now - datetime.timedelta(seconds=CHPASSWD_RATE_LIMIT_TIME)
            attempts = PasswordChangeLog.objects.filter(
                ad_user__username=user,
                when__range=[start, now],
                success=False)
            if len(attempts) >= CHPASSWD_RATE_LIMIT_ATTEMPTS:
                return render_with_msg(request,
                                        msg="Too many wrong attempts, try again later",
                                        success=False)

            (ad_user, created) = ADUser.objects.get_or_create(username=user)
            log = PasswordChangeLog.objects.create(
                ad_user=ad_user,
                source_ip=request.META["REMOTE_ADDR"],
                when=now)
            log.save()

            # now do the actual change
            try:
                chpasswd_ad(CHPASSWD_DOMAIN,
                            user,
                            form.cleaned_data["old_pass"],
                            form.cleaned_data["new_pass1"])
            except Exception as e:
                log.success = False
                log.fail_reason = "%s: %s" % (type(e), str(e))
                log.save()
                return render_with_msg(request,
                                        msg="Failed to change password",
                                        success=False)
            log.success = True
            log.save()

            return render_with_msg(request,
                                    msg="Password changed",
                                    success=True)
    return HttpResponseBadRequest("Need POST")
