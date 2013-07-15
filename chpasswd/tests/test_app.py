import unittest
from django.test import TestCase
from django.core.urlresolvers import reverse

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
        self.assertEqual(resp.content, "passwords don't match")

    def test_chpasswd_change_too_short(self):
        chpasswd.CHPASSWD_MIN_PASSWORD_SIZE = 8
        resp = self.client.post(reverse("chpasswd:chpasswd_change"),
                                data={"user": "user1",
                                      "old_pass": "oldpass",
                                      "new_pass1": "1234",
                                      "new_pass2": "1234",
                                      })
        self.assertEqual(resp.content, "password too short")

    @patch("chpasswd.views.chpasswd_ad")
    def test_chpasswd_change(self, mock_chpasswd):
        resp = self.client.post(reverse("chpasswd:chpasswd_change"),
                                data={"user": "user1",
                                      "old_pass": "oldpass",
                                      "new_pass1": "new_pass123",
                                      "new_pass2": "new_pass123",
                                      })
        self.assertEqual(resp.content, "Password changed")
        mock_chpasswd.assert_called_with(
            "ad.example.com", "user1@example.com", "oldpass", "new_pass123")


if __name__ == '__main__':
    unittest.main()
