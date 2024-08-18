# Parse downloaded EDA models to store in the repository
#!/bin/bash

source ./config.sh

accepted_extensions=("kicad_sym" "kicad_mod" "step" "stp")
remote_components_path="../components/"


local_file_path="../components/2x04_socket_IPL1-104-01-L-D-K.pretty" # Change to the path where your EDA model was downloaded 
new_folder_name="test_123.pretty" # Format descriptions as Name_Part#.pretty (e.g. Barrel_Jack_EJ508A.pretty)


new_dir="$remote_components_path/$new_folder_name"
mkdir -p "$new_dir"

for extension in "${accepted_extensions[@]}"
do
    find "$local_file_path" -type f -name "*.$extension" -exec cp {} "$new_dir" \;
done

