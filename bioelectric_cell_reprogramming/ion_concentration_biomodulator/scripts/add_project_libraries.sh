# Parse downloaded EDA models to store in the repository

accepted_extensions=("kicad_sym" "kicad_mod" "step" "stp")
remote_model_path="../user_downloads/"
file_path="../user_downloads/2x04_socket_IPL1-104-01-L-D-K.pretty" # Change to the path where your EDA model was downloaded 
new_name="test_123.pretty" # Format descriptions as Name_Part#.pretty (e.g. Barrel_Jack_EJ508A.pretty)


new_dir="$remote_model_path/$new_name"
mkdir -p "$new_dir"

for extension in "${accepted_extensions[@]}"
do
    find "$file_path" -type f -name "*.$extension" -exec cp {} "$new_dir" \;
done

