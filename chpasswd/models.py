

from django.db import models


class ADUser(models.Model):
    username = models.CharField(max_length=100)

    def __unicode__(self):
        return "ADUser: %s" % self.username


class PasswordChangeLog(models.Model):
    ad_user = models.ForeignKey('ADUser')
    source_ip = models.CharField(max_length=25)
    when = models.DateTimeField()
    success = models.BooleanField()
    fail_reason = models.TextField()

    def __unicode__(self):
        return "PasswordChangeLog: %s %s %s %s" % (
            self.ad_user, self.source_ip, self.when, self.success)
