# Copy files from the remote repository to KiCAD

project_dir="../EDA_designs"
file_path="$HOME/Documents/KiCad/projects/ion_concentration_biomodulator" # Replace with your project directory

for file in "$project_dir"/*;
do 
    echo "Copying $file to your KiCAD project directory"
    cp -f "$file" "$file_path"
done 


