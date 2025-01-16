import csv
import re

INPUT_CSV  = "../../src/bioelectric_cell_reprogramming/acdc_stimulator/kicad/bom_v0.0.1.csv"
OUTPUT_CSV = "../../src/bioelectric_cell_reprogramming/acdc_stimulator/kicad/formatted_bom_v0.0.1.csv"

def extract_jlcpcb_part_number(url: str) -> str:
    """
    Given a URL like:
        https://jlcpcb.com/partdetail/XXXX-YYYYYY/C99999
    Extract the 'C99999' portion if it exists.
    """
    # A simple regex looking for a slash followed by 'C' and then digits:
    match = re.search(r'/(C\d+)$', url)
    if match:
        return match.group(1)
    return ""  # Return empty string if there's no match

def main():
    # Read the original CSV
    with open(INPUT_CSV, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        rows = list(reader)
    
    # If the first row is a header, you might want to preserve it:
    header = rows[0]
    data_rows = rows[1:]  # Everything else
    
    # Process each data row
    for row in data_rows:
        if len(row) < 8:
            # Ensure row has enough columns
            continue
        
        distributor_link = row[6]
        # Extract the JLCPCB part number from the link
        jlcpcb_number = extract_jlcpcb_part_number(distributor_link)
        # Place extracted number in the "JLCPCB Part #" column
        row[7] = jlcpcb_number
    
    # Write the modified CSV
    with open(OUTPUT_CSV, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        # Write header row back
        writer.writerow(header)
        # Write modified data rows
        writer.writerows(data_rows)

if __name__ == "__main__":
    main()
