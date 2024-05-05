#!/bin/bash

# try to remove old ./requirements.txt
rm -f ./requirements.txt

# Create a new requirements.txt file or overwrite the existing one
touch ./requirements.txt

# Find all requirements.txt files in subdirectories only
# shellcheck disable=SC2044
for file in $(find */ -name 'requirements.txt')
do
    echo "Reading file: $file"
    # Append the content of the file to the new requirements.txt
    cat "$file" >> requirements.txt
done

# run install total libraries
pip install -r ./requirements.txt