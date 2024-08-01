import csv

def check_and_fix_csv(file_path):
    problematic_rows = []

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        corrected_rows = [headers]

        for row in reader:
            if len(row) != len(headers):
                problematic_rows.append(row)
            else:
                corrected_rows.append(row)
    
    if problematic_rows:
        print("Found problematic rows:")
        for row in problematic_rows:
            print(f"Problematic row: {row}")
    
    with open('corrected_data.csv', 'w', newline='') as corrected_file:
        writer = csv.writer(corrected_file)
        writer.writerows(corrected_rows)
    
    print("Corrected data saved to 'corrected_data.csv'.")

# Specify the path to your CSV file
file_path = 'data/titles.csv'
check_and_fix_csv(file_path)
