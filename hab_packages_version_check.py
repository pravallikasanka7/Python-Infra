#!/usr/bin/env python3

import sys

master_package = str(sys.argv[0]) # abs path of master file
server_package = str(sys.argv[1]) # abs path of client file

master_packages_dict={}
file = open(master_package, 'r')
for file_line in file:
    line=str(file_line)
    L=line.split("/") # output of this line is [coreapps,splunkforwarder,8.2.1,20210916215256]
    package_name="/".join(L[0:2])            # here the key is coreapps/splunkforwarder
    version="/".join(L[2:])  # value is 8.2.1/20210916215256
    master_packages_dict[str(package_name)]=version
    


server_packages_dict={}
file = open(server_package, 'r')
for file_line in file:
    line=str(file_line)
    L=line.split("/") # output of this line is [coreapp/ssplunkforwarder,8.2.1,20210916215256]
    key="/".join(L[0:2])            # here the key is coreapps/splunkforwarder
    value="/".join(L[2:])  # value is 8.2.1/20210916215256
    server_packages_dict[str(key)]=value
    


for package in master_packages_dict.keys():
    if( package in server_packages_dict.keys() ): # only if package is present in server_package_dict
          if(server_packages_dict[package]==master_packages_dict[package]):
              print(f"{package} {server_packages_dict[package]}:success")
          else:
               print(f"{package} {server_packages_dict[package]}:unsuccess")
