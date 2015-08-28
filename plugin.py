def results(fields, original_query):
    import json, ldap
    html = ""
    if '~type' in fields and '~data' in fields:
        field = fields['~type']
        data = fields['~data']
        settings = json.load(open('preferences.json'))

        hostname = settings.get('hostname', ' ')
        port = settings.get('port', ' ')
        basedn = settings.get('basedn', ' ')
        searchscope = ldap.SCOPE_SUBTREE
        retrieveAttributes = None

        searchFilter = format(field + "=" + data + "*")

        try:
            l = ldap.initialize('ldaps://' + hostname + ':' + port)
            l.simple_bind_s()
        except ldap.LDAPError, e:
            print e

        result_set = []

        try:
            ldap_result_id = l.search(basedn, searchscope, searchFilter, retrieveAttributes)
            while l:
                result_type, result_data = l.result(ldap_result_id, 0)
                if (result_data == []):
                    break
                else:
                    if result_type == ldap.RES_SEARCH_ENTRY:
                        result_set.append(result_data)
        except ldap.LDAPError, e:
            print e

        html = buildhtml(result_set)

        return {
            "title": "LDAP Query '{0}'".format(field + "=" + data),
            "html": html
        }

def buildhtml(results):
    import pdb
    html = ""

    if len(results) == 0:
        html = "No Results."
        return html
    for i in range(len(results)):
        for entry in results[i]:
            try:
                name = entry[1]['cn'][0]
                title = entry[1]['title'][0]
                email = entry[1]['mail'][0]
                phone = entry[1]['telephoneNumber'][0]
                html = html + name.title() + '<br />' + title.title() + '<br />' + email + "<br />" + phone + "<br /><hr />"
            except:
                pass
    return html
