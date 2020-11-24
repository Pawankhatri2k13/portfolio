#!/bin/bash

for file in *.HTM
do
	name=$(basename "$file" .HTM)
	#remove echo when really want to make changes to file names
	echo mv "$file" "$name.html"
done