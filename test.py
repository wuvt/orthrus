import getpass
import orthrus

user = input('Username: ')
password = getpass.getpass('Password: ')

o = orthrus.Orthrus(
    ldap_uri='ldap://172.17.0.1:1389',
    user_template_dn='uid={},ou=Users,dc=wuvt,dc=vt,dc=edu',
    group_base_dn='ou=Groups,dc=wuvt,dc=vt,dc=edu',
    role_mapping={
        'admin': ['sudoers', 'webmasters'],
        'library': ['sudoers', 'librarians'],
        'radiothon': ['sudoers', 'missioncontrol'],
        'badrole': ['badgroup'],
    },
    verify=False)

r = o.authenticate(user, password)
print(r)
