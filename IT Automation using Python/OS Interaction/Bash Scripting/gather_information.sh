#!/bin/bash

#Defining our own variable line other than environment variables
line='...................................................'

echo "Starting at: $(date)"
echo $line

echo "UPTIME"
uptime
echo $line

echo "FREE"; free; echo $line

echo "WHO"
who
echo $line

echo "Finishing at: $(date)"
