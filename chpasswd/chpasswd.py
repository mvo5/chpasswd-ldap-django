#!/usr/bin/python

import getpass
import random
import socket
import sys

import ldap
import ldap.modlist

import dns.resolver


def get_ad_server(domain):
    """ pick a AD server """
    resolver = dns.resolver.Resolver()
    res = resolver.query("_ldap._tcp.%s" % domain, "SRV")
    # build data structure
    servers = {}
    for srv in res:
        priority = int(srv.priority)
        l = servers.get(priority, [])
        target = srv.target.to_text().strip(".")
        port = srv.port
        l.append( (target, port) )
        servers[priority] = l
    # shuffle
    for prio in servers.keys():
        server_list = servers[prio]
        random.shuffle(server_list)
    # and try to pick one that answers
    for prio in sorted(servers.keys(), reverse=True):
        server_list = servers[prio]
        for server, port in server_list:
            try:
                conn = socket.create_connection( (server, port), timeout=1.0)
                conn.close()
                return "%s:%s" % (server, port)
            except socket.error:
                pass
    return None


def chpasswd_ad(domain, user, old_pass, new_pass):
    server = get_ad_server(domain)
    return chpasswd_ad_lowlevel(server, user, old_pass, new_pass)


def chpasswd_ad_lowlevel(server, user, old_pass, new_pass):
    # we could simply use, but that has weaker transport security than
    # using ldaps:
    # res = subprocess.Popen(["smbpasswd", "-r", server, "-U", user],
    #                        stdin=subprocess.PIPE)
    l = ldap.initialize("ldap://%s" % server)
    l.set_option(ldap.OPT_REFERRALS, 0)
    l.start_tls_s()
    res = l.simple_bind_s(user, old_pass)
    encoded_old = ('"%s"' % old_pass).encode("utf-16-le")
    encoded_new = ('"%s"' % new_pass).encode("utf-16-le")
    ldif = [
        (ldap.MOD_DELETE, 'unicodePwd', [encoded_old]),
        (ldap.MOD_ADD, 'unicodePwd', [encoded_new])]
    dn="CN=%s,cn=Users,dc=uni-trier,dc=de" % user.split("@")[0]
    res = l.modify_s(dn, ldif)
    return res


if __name__ == "__main__":
    domain = sys.argv[1]
    user = sys.argv[2]
    old_password = getpass.getpass("Enter current password: ")
    passwd_new1 = getpass.getpass("Enter new pw: ")
    passwd_new2 = getpass.getpass("Enter new pw (again): ")
    if passwd_new1 != passwd_new2:
        print "pw does not match"
        sys.exit(1)
    res = chpasswd_ad(domain, user, old_password, passwd_new1)

    # error
    if not res:
        sys.exit(1)

