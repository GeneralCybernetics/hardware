#!/usr/bin/env bash

# Function to update sym-lib-table
update_sym_lib_table() {
    local file="$1"
    local dirname=$(dirname "$file")
    local filename=$(basename "$file")
    local libname="${filename%.*}"
    
    echo "  (lib (name \"$libname\")(type \"KiCad\")(uri \"\${KIPRJMOD}/../../../../common/kicad/$file\")(options \"\")(descr \"\"))" >> sym-lib-table
}

# Function to update fp-lib-table
update_fp_lib_table() {
    local dir="$1"
    local dirname=$(basename "$dir")
    
    echo "  (lib (name \"$dirname\")(type \"KiCad\")(uri \"\${KIPRJMOD}/../../../../common/kicad/$dir\")(options \"\")(descr \"\"))" >> fp-lib-table
}

# Main script
echo "(sym_lib_table" > sym-lib-table
echo "(fp_lib_table" > fp-lib-table

find . -type d | while read -r dir; do
    if [[ -n $(find "$dir" -maxdepth 1 -name "*.kicad_sym") ]]; then
        find "$dir" -maxdepth 1 -name "*.kicad_sym" | while read -r file; do
            update_sym_lib_table "${file#./}"
        done
    fi
    
    if [[ -n $(find "$dir" -maxdepth 1 -name "*.kicad_mod") ]]; then
        update_fp_lib_table "${dir#./}"
    fi
done

echo ")" >> sym-lib-table
echo ")" >> fp-lib-table

echo "Library tables updated successfully!"