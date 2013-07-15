import getpass
import sys

import ldap
import ldap.modlist


def chpasswd_ad(server, user, old_pass, new_pass):
    # we could simply use, but that has weaker transport security than
    # using ldaps:
    # res = subprocess.Popen(["smbpasswd", "-r", server, "-U", user],
    #                        stdin=subprocess.PIPE)

    l = ldap.initialize("ldaps://%s" % server)
    l.set_option(ldap.OPT_REFERRALS, 0)
    #l.start_tls_s()
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
    server = sys.argv[1]
    user = sys.argv[2]
    old_password = getpass.getpass("Enter current password: ")
    passwd_new1 = getpass.getpass("Enter new pw: ")
    passwd_new2 = getpass.getpass("Enter new pw (again): ")
    if passwd_new1 != passwd_new2:
        print "pw does not match"
        sys.exit(1)
    chpasswd_ad(server, user, old_password, passwd_new1)

    # error
    if not res:
        sys.exit(1)
