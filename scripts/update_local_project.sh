#!/bin/bash

source ./config.sh
# Copy files from the remote repository to KiCAD

project_dir="../EDA_designs"

for file in "$project_dir"/*;
do 
    echo "Copying $file to your KiCAD project directory"
    cp -f "$file" "$file_path"
done 


