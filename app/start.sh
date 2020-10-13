#!/bin/bash

# Activate virtualenv
# source cmpt383-project/bin/activate

# Compile db verification and create db
g++ dbverify.cpp -l sqlite3
echo Populating database...
python3 main.py

# Get user input
while :
do
    read -n1 -p "Find courses you can take next semester? [y,n]" ans
    case $ans in  
        y|Y) echo -e "\Starting course finder..." && python3 calculate.py ;; 
        n|N) echo  no && break;; 
        *) echo Not valid ;; 
    esac
done
echo Exiting...

