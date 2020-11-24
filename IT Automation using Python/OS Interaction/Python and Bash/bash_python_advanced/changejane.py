#!/usr/bin/env python3

import sys
import subprocess

name_file = sys.argv[1]

with open(name_file, 'r') as f:
	for name in f.readlines():
		name_pure = name.strip()

		#print(name_pure)
		#print(name_pure.replace("jane","jdoe"))

		subprocess.run(["mv",name_pure,name_pure.replace("jane","jdoe")])
	f.close()

