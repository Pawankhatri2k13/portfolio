#!/usr/bin/env python3

import re
import sys
import subprocess
import os
import operator


#################################
#################################
#################################

file = os.popen("grep 'ERROR' syslog.log").read().split('\n')
error_messages = {}
i = 0
lst = []
for item in file:
	if len(item) == 0:
		continue
	else:
		i+=1
		result = re.search(r'ticky: ERROR ([\w \']*) ', item)
		if result is not None:
			lst.append(' '.join(result.group().split(' ')[2:]))
#error_messages["Total error_messages are: "]=i

for item in lst:
	if item in error_messages.keys():
		error_messages[item]+=1
	else:
		error_messages[item]=1

sorted_errordict = sorted(error_messages.items(),key=operator.itemgetter(1), reverse=True)

with open("error_messages.csv",'w') as f:
	f.write("Error, Count\n")
	for key, value in sorted_errordict:
		f.write("{}, {}\n".format(key, value))
	f.close()

##########################################
file = os.popen("grep 'INFO' syslog.log").read().split('\n')
info_messages = {}
i = 0
lst = []
for item in file:
	if len(item) == 0:
		continue
	else:
		i+=1
		result = re.search(r'ticky: INFO ([\w ]*) ', item)
		if result is not None:
			lst.append(' '.join(result.group().split(' ')[2:]))
#info_messages["Total info_messages are: "]=i

for item in lst:
	if item in info_messages.keys():
		info_messages[item]+=1
	else:
		info_messages[item]=1

with open("info_messages.csv",'w') as f:
	f.write("Error, Count\n")
	for key, value in info_messages.items():
		f.write("{}, {}\n".format(key, value))
	f.close()

#################################################################
#################################################################
#################################################################

file_error = os.popen("grep 'ERROR' syslog.log").read().split('\n')
error_messages = {}
i = 0
lst = []
for item in file_error:
	if len(item) == 0:
		continue
	else:
		i+=1
		result = re.search(r'\(([\w. ]*)\)', item)
		if result is not None:
			lst.append(result.group(1))

for item in lst:
	if item in error_messages.keys():
		error_messages[item]+=1
	else:
		error_messages[item]=1
		
########################################
file_info = os.popen("grep 'INFO' syslog.log").read().split('\n')
info_messages = {}
i = 0
lst = []
for item in file_info:
	if len(item) == 0:
		continue
	else:
		i+=1
		result = re.search(r'\(([\w. ]*)\)', item)
		if result is not None:
			lst.append(result.group(1))

for item in lst:
	if item in info_messages.keys():
		info_messages[item]+=1
	else:
		info_messages[item]=1

#####################################

usage_dict = {}
for key, value in error_messages.items():
	lst = []
	lst.append(value)
	try:
	 	lst.append(info_messages[key])
	except KeyError:
	 	lst.append(0)
	 
	usage_dict[key] = lst

names = sorted(usage_dict)

###############

with open("usage_details.csv",'w') as f:
	f.write("Username, INFO, ERROR\n")
	for name in names:
		f.write("{}, {}, {}\n".format(name, usage_dict[name][1], usage_dict[name][0]))
	f.close()
