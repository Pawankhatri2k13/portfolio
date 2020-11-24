#!/bin/bash

if grep "127.0.0.1" /etc/hosts
then 
	echo "Everything ok"
else 
	echo "Error! 127.0.0.1 is not in /etc/hosts"
fi

echo "............Use of Test Command for if else block..............."

if test -n "$PATH"
then 
	echo "Your path is not empty"
else 
	echo "sorry your path is empty"
fi

echo "............Another way of using test command..............."

if [ -n "$PATH" ] 
then 
	echo "Your path is not empty"
else 
	echo "sorry your path is empty"
fi
