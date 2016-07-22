#!/usr/bin/python
import sys
sys.path.append("../lib/NetappSDK/")
from NaServer import *

filerIP = raw_input("filer IP: ")
myPass = raw_input("filer password: ")
dir = raw_input("dir path: ")

s = NaServer(filerIP, 1 , 15)
s.set_server_type("FILER")
s.set_transport_type("HTTPS")
s.set_port(443)
s.set_style("LOGIN")
s.set_admin_user("root", myPass)

# Obtain the Data ONTAP version.
api = NaElement("system-get-version")

xo = s.invoke_elem(api)
if (xo.results_status() == "failed") :
      print ("Error:\n")
      print (xo.sprintf())
      sys.exit (1)

print ("Received:\n")
print (xo.sprintf())
# Delete a directory.
print "Deleting....\n"
api = NaElement('file-delete-directory')
# Path of the directory to delete. The value is expected to begin with /vol/<volumename>. The directory must be empty in order for this API to succeed.
api.child_add_string('path',dir)

xo = s.invoke_elem(api)
if (xo.results_status() == 'failed'):
    print 'Error:'
    print xo.results_reason()
    print "\n"
else:
    print "Success!\n"
