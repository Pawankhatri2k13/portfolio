#!/bin/bash

>oldFiles.txt

names=$(grep ' jane ' namelist.txt | cut -d' ' -f3)

for name in $names
do
	echo "$name">>oldFiles.txt
done

