import csv
import pandas as pd
from datetime import datetime
from openpyxl import load_workbook
import os
from .extracting import data_extract


def data_cleaning():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # File names
    input_total = os.getenv("INPUT_TOTAL") or os.path.join(current_dir, '..', 'output_csv', 'Total.csv')
    input_detail = os.getenv("INPUT_DETAIL") or os.path.join(current_dir, '..', 'output_csv', 'Details.csv')
    excel_file = os.getenv("EXCEL_FILE") or os.path.join(current_dir, '..','..', 'extracted_data.xlsx')

    #data from extracting module
    total_data_dict, detail_data_dict = data_extract()

    # Convert date strings to "YYYY-MM-DD" format
    detail_data_dict["Date"] = [datetime.strptime(date, "%d %b %Y").strftime("%Y-%m-%d") for date in detail_data_dict["Date"]]

    # Process transaction descriptions and amounts
    filtered = []
    new_Money_in = []
    new_Money_out = []

    old_Money_in = detail_data_dict["Money in"][:]
    old_Money_out = detail_data_dict["Money out"][:]

    old_Money_in_index = 0
    old_Money_out_index = 0

    # Filtering transaction details
    i = 0
    for detail in detail_data_dict["Description"]:
        if i % 2 != 1:
            if "transfer from revolut user" in detail.lower():
                    i += 1
            elif ("from" in detail.lower()) or ("top-up" in detail.lower()):  
                new_Money_in.append(old_Money_in[old_Money_in_index] if old_Money_in_index < len(old_Money_in) else 0.0)
                old_Money_in_index += 1
                new_Money_out.append(0.0)
                filtered.append(detail)
            elif "transfer to revolut user" in detail.lower():
                i += 1
            elif ("to" in detail.lower()) or  ("reference: to" in detail.lower()):
                if ("to:" in detail.lower()) or ("to'" in detail.lower()):
                    print(previous_detail)
                    filtered.append(previous_detail)
                else:
                    filtered.append(detail)
                    
                new_Money_out.append(old_Money_out[old_Money_out_index] if old_Money_out_index < len(old_Money_out) else 0.0)
                old_Money_out_index += 1
                new_Money_in.append(0.0)
            else:
                i +=1
        i += 1
        previous_detail = detail
    print(filtered)
    
    # Update filtered data in dictionary
    detail_data_dict["Description"] = filtered
    detail_data_dict["Money in"] = new_Money_in
    detail_data_dict["Money out"] = new_Money_out

    # List to store separated transactions
    separated_transactions = []

    # Structure transaction details properly
    for i in range(len(detail_data_dict['Date'])):
        transaction = {
            'Date': detail_data_dict['Date'][i],
            'Description': detail_data_dict['Description'][i],
            'Money Out': detail_data_dict['Money out'][i],
            'Money In': detail_data_dict['Money in'][i],
            'Balance': detail_data_dict['Balance'][i]
        }
        separated_transactions.append(transaction)

    #Write extracted data to CSV (Ensuring Correct Structure)**
    with open(input_total, mode="w", newline="", encoding="utf-8") as csv_f:
        csv_writer = csv.writer(csv_f)

        # **Write total financial summary**
        csv_writer.writerow(["Total Financial Summary"])
        for key, value in total_data_dict.items():
            csv_writer.writerow([key, value])


    with open(input_detail, mode="w", newline="", encoding="utf-8") as csv_f:
        csv_writer = csv.writer(csv_f)
        # **Write transaction details**
        csv_writer.writerow(["Date", "Description", "Money Out", "Money In", "Balance"])  # Write headers

        for transaction in separated_transactions:
            csv_writer.writerow(transaction.values())  # Write each row properly

    #Ensure the CSV file is completely written before converting to Excel**
    try:
        df = pd.read_csv(input_detail, sep=",", skip_blank_lines=True, engine="python")  # Properly detect columns
        df.to_excel(excel_file, index=False, engine='openpyxl')  # Save as Excel file
        print(f"Data successfully saved to {excel_file}")
        
        #Adjust column width automatically
        wb = load_workbook(excel_file)
        ws = wb.active  # Get the active worksheet

        for col in ws.columns:
            max_length = 0
            col_letter = col[0].column_letter  # Get column letter (A, B, C, etc.)

            for cell in col:
                try:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                except:
                    pass

            adjusted_width = max_length + 2  # Add extra space
            ws.column_dimensions[col_letter].width = adjusted_width  # Set width

        # Save the adjusted Excel file
        wb.save(excel_file)

    except Exception as e:
        print(f"Error: {e}")
