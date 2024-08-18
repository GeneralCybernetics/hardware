#!/bin/bash

source ./config.sh

# Copy files from KiCAD to the remote respository

project_dir="../EDA_designs"

for file in "$file_path"/*;
do 
    echo "Copying $file to your KiCAD project directory"
    cp -f "$file" "$project_dir"
done