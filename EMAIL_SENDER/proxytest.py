#!/usr/bin/env python

import urllib2
import getpass

user_in = raw_input("Username: ")
pass_in = getpass.getpass()
proxyurl = "10.52.0.202:8080"
proxyport = "8080"

#s = 'http://' + user_in + ':' + pass_in + '@' + proxyurl + ':' + proxyport
#print s
#proxy = urllib2.ProxyHandler({'http': 'http://' + user_in + ':' + pass_in + '@' + proxyurl + ':' + proxyport})
#auth = urllib2.HTTPBasicAuthHandler()
#opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
#urllib2.install_opener(opener)

#conn = urllib2.urlopen('http://python.org')
#return_str = conn.read()

##############################

password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()

# None, with the "WithDefaultRealm" password manager means
# that the user/pass will be used for any realm (where
# there isn't a more specific match).

password_mgr.add_password(None, proxyurl, user_in, pass_in)
auth_handler = urllib2.HTTPBasicAuthHandler(password_mgr)
opener = urllib2.build_opener(auth_handler)
urllib2.install_opener(opener)
print urllib2.urlopen("http://www.example.com/folder/page.html").read()
