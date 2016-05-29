import ldap3
import ssl


class Orthrus(object):
    def __init__(self, ldap_uri, user_template_dn, group_base_dn=None,
                 role_mapping=None, verify=None):
        self.user_template_dn = user_template_dn
        self.group_base_dn = group_base_dn
        self.role_mapping = role_mapping

        if verify is True or verify is None:
            tls_config = ldap3.Tls(validate=ssl.CERT_REQUIRED)
        elif verify is False:
            tls_config = ldap3.Tls(validate=ssl.CERT_NONE)
        else:
            tls_config = ldap3.Tls(validate=ssl.CERT_REQUIRED,
                                   ca_certs_file=verify)

        self.server = ldap3.Server(ldap_uri, tls=tls_config)

    def authenticate(self, user, password, attributes=[]):
        user_dn = self.user_template_dn.format(user)
        conn = ldap3.Connection(self.server, user=user_dn,
                                password=password,
                                auto_bind=ldap3.AUTO_BIND_NONE)
        conn.open()
        conn.start_tls()

        if conn.bind():
            if len(attributes) > 0:
                user_attrs = self.get_attributes(conn, user_dn, attributes)
            else:
                user_attrs = []

            roles = self.get_roles(conn, user)

            conn.unbind()
            return True, user_attrs, roles
        else:
            return False, None, []

    def get_attributes(self, conn, dn, attributes):
        conn.search(search_base=dn,
                    search_filter='(objectclass=*)',
                    search_scope=ldap3.BASE,
                    attributes=attributes)

        if len(conn.response) > 0:
            return conn.response[0]['attributes']
        else:
            return None

    def get_roles(self, conn, user):
        user_roles = []
        for role, groups in self.role_mapping.items():
            for group in groups:
                query = '(&(memberUid={user})(cn={group}))'.format(
                    user=ldap3.utils.dn.escape_attribute_value(user),
                    group=ldap3.utils.dn.escape_attribute_value(group))

                if conn.search(search_base=self.group_base_dn,
                               search_filter=query,
                               search_scope=ldap3.SUBTREE):
                    user_roles.append(role)

        return user_roles
