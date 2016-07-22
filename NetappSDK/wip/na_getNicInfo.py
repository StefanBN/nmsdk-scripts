#!/usr/bin/python
import sys
sys.path.append("../lib/NetappSDK/")
from NaServer import *
import getpass

# default stuff
user = "root"

# Interactive stuff
filer = raw_input("Filername: ")
# password prompt (echo disabled)
pw = getpass.getpass(prompt="Filer password: ")

# Setup the session with the filer
s = NaServer(filer, 1 , 19)
s.set_server_type("FILER")
s.set_transport_type("HTTPS")
s.set_port(443)
s.set_style("LOGIN")
s.set_admin_user(user, pw)

# Obtain the Data ONTAP version.
api_sys_ver = NaElement("system-get-version")

out = s.invoke_elem(api_sys_ver)
if (out.results_status() == "failed") :
    print ("Error:\n")
    print (out.sprintf())
    sys.exit (1)
print ("\nResults:\n")

print "Filer version:", out.child_get_string("version"), "\n"

api_ifconfig_get = NaElement("net-ifconfig-get")
# This is the name of the interface to display. If not provided, all interfaces will be displayed.
#api_ifconfig_get.child_add_string("interface-name","<name>")
out = s.invoke_elem(api_ifconfig_get)
if (out.results_status() == "failed") :
     print ("Error:\n")
     print (out.sprintf())
     sys.exit (1)
nics = out.child_get("interface-config-info")
results = nics.children_get()
for nic in results:
  print "\tinterface-name:", nic.child_get_string("interface-name")
  print "\t\tipspace-name:", nic.child_get_string("ipspace-name")
  print "\t\tmac-address:", nic.child_get_string("mac-address")
  print "\t\tmediatype:", nic.child_get_string("mediatype")
  #ip_info = nic.child_get("v4-primary-address").child_get("ip-address-info")
  ip_info = nic.child_get("v4-primary-address")
  if (ip_info):
    ip = ip_info.child_get("ip-address-info")
    print "\t\taddress:", ip.child_get_string("address")
    print "\t\tnetmask:", ip.child_get_string("netmask-or-prefix")
    print "\t\tbroadcast:", ip.child_get_string("broadcast")
    print "\t\tno-ddns:", ip.child_get_string("no-ddns")
