import datetime

from unittest import TestCase

from chpasswd.models import (
    ADUser,
    PasswordChangeLog,
)


class ModelsTestCase(TestCase):

    def test_ad_user_moel(self):
        ad_user = ADUser.objects.create(username="foo")
        self.assertEqual(str(ad_user), "ADUser: foo")

    def test_password_changelog_model(self):
        log = PasswordChangeLog.objects.create(
            ad_user=ADUser.objects.create(username="foo"),
            source_ip="192.168.0.1",
            when=datetime.datetime(2010, 01, 01, 23, 00),
            success=False,
            fail_reason="wrong credentials")
        self.assertEqual(
            str(log),
            "PasswordChangeLog: ADUser: foo 192.168.0.1 2010-01-01 "
            "23:00:00 False")
