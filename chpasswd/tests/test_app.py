import datetime

import ldap

from django.test import TestCase
from django.core.urlresolvers import reverse

from chpasswd.models import (
    ADUser,
    PasswordChangeLog,
)

from django_project.settings import (
    CHPASSWD_RATE_LIMIT_ATTEMPTS,
)

from mock import (
    patch,
)

import chpasswd


class ChpasswdTestCase(TestCase):

    def test_chpasswd_show(self):
        resp = self.client.get(reverse("chpasswd:chpasswd_prompt"))
        self.assertTrue("Change Password" in resp.content)

    def test_chpasswd_change_not_match(self):
        resp = self.client.post(reverse("chpasswd:chpasswd_change"),
                               data={"user": "user1",
                                     "old_pass": "oldpass",
                                     "new_pass1": "new_pass1",
                                     "new_pass2": "new_pass2",
                                     })
        self.assertTrue("passwords don&#39;t match" in resp.content)

    def test_chpasswd_change_too_short(self):
        chpasswd.CHPASSWD_MIN_PASSWORD_SIZE = 8
        resp = self.client.post(reverse("chpasswd:chpasswd_change"),
                                data={"user": "user1",
                                      "old_pass": "oldpass",
                                      "new_pass1": "1234",
                                      "new_pass2": "1234",
                                      })
        self.assertTrue("password too short" in resp.content)

    @patch("chpasswd.views.chpasswd_ad")
    def test_chpasswd_change(self, mock_chpasswd):
        for i in range(2):
            resp = self.client.post(reverse("chpasswd:chpasswd_change"),
                                    data={"user": "user%s" % i,
                                          "old_pass": "oldpass",
                                          "new_pass1": "new_pass123",
                                          "new_pass2": "new_pass123",
                                          })
            self.assertTrue("Password changed" in resp.content)
            mock_chpasswd.assert_called_with(
                "example.com", "user%s@example.com" % i,
                "oldpass", "new_pass123")
        self.assertEqual(len(PasswordChangeLog.objects.all()), 2)
        log_entries = PasswordChangeLog.objects.filter(
            ad_user__username="user0@example.com")
        self.assertEqual(len(log_entries), 1)
        self.assertEqual(log_entries[0].ad_user.username, "user0@example.com")

    @patch("chpasswd.views.chpasswd_ad")
    def test_chpasswd_rate_limit(self, mock_chpasswd):
        data = {"user": "user0",
                "old_pass": "wrong-pass",
                "new_pass1": "new_pass123",
                "new_pass2": "new_pass123",
                }
        # simulate wrong login
        mock_chpasswd.side_effect = ldap.LDAPError("wrong password")
        for i in range(CHPASSWD_RATE_LIMIT_ATTEMPTS):
            resp = self.client.post(reverse("chpasswd:chpasswd_change"),
                                    data=data)
            self.assertTrue("Failed to change password" in resp.content)
        # now we should see rate limit
        resp = self.client.post(reverse("chpasswd:chpasswd_change"),
                                data=data)
        self.assertTrue(
            "Too many wrong attempts, try again later" in resp.content)

    @patch("chpasswd.views.chpasswd_ad")
    def test_chpasswd_rate_limit_allows_change_after_time(self, mock_chpasswd):
        data = {"user": "user0",
                "old_pass": "wrong-pass",
                "new_pass1": "new_pass123",
                "new_pass2": "new_pass123",
                }
        when = datetime.datetime.now() - datetime.timedelta(days=10)
        for i in range(CHPASSWD_RATE_LIMIT_ATTEMPTS + 10):
            ad_user = ADUser.objects.create(username="user0")
            PasswordChangeLog.objects.create(ad_user=ad_user,
                                             when=when,
                                             success=False)
        # now we should see rate limit
        resp = self.client.post(reverse("chpasswd:chpasswd_change"),
                                data=data)
        self.assertTrue(
            "Password changed" in resp.content)

    def test_chpasswd_change_needs_post(self):
        resp = self.client.get(reverse("chpasswd:chpasswd_change"))
        self.assertEqual(resp.status_code, 400)
