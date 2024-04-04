import os, sys
import pandas as pd

def extract_excel_data(serial_number, output_file):
    # Specify the root directory where you want to search for folders
    root_directory = 'C:/Alphawave Services/EA Production - SARAO - SARAO/DocumentControl/Test data/317-022005'  # Replace with your actual directory path

    # Search for the folder with the specified serial number
    for folder_name in os.listdir(root_directory):
        folder_path = os.path.join(root_directory, folder_name)
        if os.path.isdir(folder_path) and folder_name == serial_number:
            # Look for an Excel file (.xlsx) within the serialNumber folder
            for file_name in os.listdir(folder_path):
                if file_name.lower().endswith('.xlsx'):
                    excel_file_path = os.path.join(folder_path, file_name)
                    break
            else:
                print(f"No Excel file found in folder '{serial_number}'.")
                return

            # Read the Excel file and extract relevant data
            try:
                df = pd.read_excel(excel_file_path, sheet_name="Introduction", header=None)
                serial_row = df.iloc[10, 8]  # Columns I to N (0-based index)
                # print(serial_row)
                if serial_row == serial_number:
                    performance_df = pd.read_excel(excel_file_path, sheet_name="Performance")
                    data_to_write = performance_df.iloc[2:11, 3].tolist()  # D4 to D17
                    data_to_write.append(performance_df.iloc[15, 3])
                else:
                    print(f"Serial number '{serial_number}' not found in the Excel file.")
                    return
            except Exception as e:
                print(f"Error reading Excel file: {e}")
                return

            # Write the extracted data to a text file
            output_file = root_directory + "/" + serial_number + "/" + output_file
            with open(output_file, 'w') as txt_file:
                for line, cell_value in enumerate(data_to_write, start=1):
                    txt_file.write(f"{cell_value}\n")
                print(f"Data written to '{output_file}' successfully.")
            return

    print(f"Folder '{serial_number}' not found in the specified directory.")

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python dataExtract.py <Serial Number>")
        sys.exit(1)
    serial_number_arg = sys.argv[1]
    output_file_arg = serial_number_arg + ".txt"

    extract_excel_data(serial_number_arg, output_file_arg)