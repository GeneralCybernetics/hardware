# Copy files from KiCAD to the remote respository

project_dir="../EDA_designs"
file_path="$HOME/Documents/KiCad/projects/ion_concentration_biomodulator" # Replace with your project directory

for file in "$file_path"/*;
do 
    echo "Copying $file to your KiCAD project directory"
    cp -f "$file" "$project_dir"
done