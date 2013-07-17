from django.test import TestCase


from mock import (
    Mock,
    patch,
)

from chpasswd.chpasswd import get_ad_server
import dns.resolver


class LdapTestCase(TestCase):

    @patch.object(dns.resolver.Resolver, "query")
    @patch("socket.create_connection")
    def test_chpasswd_ldap_sorting(self, mock_connection, mock_query):
        mock_connection.return_value = Mock()
        l = []
        for i in range(10):
            mock = Mock()
            mock.priority = i / 2
            mock.target.to_text.return_value = "srv%i.%i" % (i / 2, i)
            mock.port = 69
            l.append(mock)
        mock_query.return_value = l
        res = get_ad_server("example.com")
        self.assertIn(res, ["srv4.8:69", "srv4.9:69"])
