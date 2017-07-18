#!/bin/bash

python Test.py > temp.txt
DIFF=$(diff correct_output.yes temp.txt)
if [ ! -z "$DIFF" ] ; then
    echo "Test result: failure"
else
    echo "Test result: success!"
fi
rm temp.txt

