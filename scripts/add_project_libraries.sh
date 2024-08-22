# Parse downloaded EDA models to store in the repository
#!/bin/bash

source ./config.sh
remote_components_path="../EDA_designs/components/"
### For the future

### The following lines can be modularized when given the file paths where to save the information ad
read -p "Enter the local file path for the design file (Users/elijah/Downloads/Barrel_Jack_EJ508A): " local_file_path
read -p "Enter the new folder name (Format descriptions as Name_Part#.pretty (e.g. Barrel_Jack_EJ508A)): " new_folder_name

if [[ "$new_folder_name" != *.pretty ]]; then
    new_folder_name="${new_folder_name}.pretty"
fi


new_dir="$remote_components_path/$new_folder_name"
mkdir -p "$new_dir"
moved_file_count=0

for extension in "${accepted_extensions[@]}"
do
    files=$(find "$local_file_path" -type f -name "*.$extension" 2>/dev/null)
    if [[ -n "$files" ]]; then
        found_files=true
        echo "Found files with extension .$extension, copying them to $new_dir"
        find "$local_file_path" -type f -name "*.$extension" -exec cp {} "$new_dir" \;
        let moved_file_count++
    else
        echo "Could not find any files with extension .$extension"
    fi
done


if [[ moved_file_count -eq 0 ]]; then
    rmdir "$new_dir"
fi