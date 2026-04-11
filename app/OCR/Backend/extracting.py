import csv
import re
import os

def data_extract():
    
    current_dir = os.path.dirname(os.path.abspath(__file__))

    input= os.path.join(current_dir, '..', 'output_csv', 'output.csv')


    # Keywords for financial data extraction
    key_words = ["Opening balance", "Money out", "Money in", "Closing",
                "Date", "Description", "Money out", "Money in", "Balance"]

    # Initialize total financial values
    total_data_dict = {
        "Opening balance": 0.0,
        "Money out": 0.0,
        "Money in": 0.0,
        "Closing": 0.0
    }

    # Initialize transaction details
    detail_data_dict = {
        "Date": [],
        "Description": [],
        "Money out": [],
        "Money in": [],
        "Balance": []
    }
        
        
    def print_output(pages):
        """Print extracted data for the given page."""
        print(f"Page {pages[0] + 1}\n")
        for key, value in total_data_dict.items():
            print(f"{key}: {value}\n")
        for key, value in detail_data_dict.items():
            print(f"{key}: {value}\n")
        

    def extract_values(pages, line, data_dict, keyword_index, row_offset):
        """
        Extracts values from CSV and updates the dictionary.
        Cleans special characters and converts numbers.
        """
        value = pages[1][line[0] + row_offset]

        # Fix special cases like "Él .59" → "1.59"
        if value.startswith("Él"):
            value = value.replace("Él ", "1")
        
        # Extract numerical values
        if keyword_index < 4 or keyword_index > 5:
            number = re.findall(r"[-+]?\d*\.\d+|\d+", value)
            value = float(number[0]) if number else None
            if value == 0.0:
                value = 10.0
        
        # Store extracted data
        if keyword_index < 4 and value != None:
            data_dict[key_words[keyword_index]] = value
        elif value != None:
            data_dict[key_words[keyword_index]].append(value)

    def process_csv(csv_reader):
        """Processes CSV file, extracting financial and transaction details."""
        for pages in enumerate(csv_reader):  # Process each page
            keyword_index = 0 if pages[0] == 0 else 4  # Define starting index
            start_index_2nd = 0
            
            # Extract total financial values
            if keyword_index < 4:
                for line in enumerate(pages[1]):
                    if line[1] == key_words[keyword_index]:  # Match keyword
                        extract_values(pages, line, total_data_dict, keyword_index, 2)
                        
                        if keyword_index == 2:
                            start_index_2nd = line[0] + 3  # Mark start of second section
                        if keyword_index == 3:
                            del pages[1][line[0]:line[0] + 4]  # Remove processed rows
                        keyword_index += 1  # Move to the next category

            # Extract transactional details
            if keyword_index >= 4:
                for line in enumerate(pages[1][start_index_2nd:]):
                    if keyword_index < len(key_words) and line[1] in key_words[4:]:  # Match transaction field
                        row_offset = 1 + start_index_2nd  # Adjust row offset
                        
                        if keyword_index <= 7:  # Extract transaction data
                            while pages[1][line[0] + row_offset] not in key_words[4:]:
                                extract_values(pages, line, detail_data_dict, keyword_index, row_offset)
                                row_offset += 1
                            keyword_index += 1  # Move to next transaction field

                        else:  # Extract balance details
                            last_sentence_1 = "@ Report lost or stolen card"
                            last_sentence_2 = "Report lost or stolen card"
                            while (pages[1][line[0] + row_offset] != last_sentence_1) and (pages[1][line[0] + row_offset] != last_sentence_2):
                                extract_values(pages, line, detail_data_dict, keyword_index, row_offset)
                                row_offset += 1

            print_output(pages)  # Print results
            
            
            
    # Read CSV and extract data
    with open(input, mode="r", newline="", encoding="utf-8") as csv_file:
        csv_reader = list(csv.reader(csv_file))  # Convert to a list
        process_csv(csv_reader)
        
    return total_data_dict, detail_data_dict

if __name__ == "__main__":
    data_extract()
        

        

