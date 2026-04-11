import requests
import csv

# API key
api_key = "K88706273088957"

input_image = "input/page_1.png"
output = "output_csv/output.csv"

# Open CSV file for writing
with open(output, mode="w", newline="", encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file)

    # Open image and send to OCR API
    with open(input_image, "rb") as image_file:
        response = requests.post(
            "https://api.ocr.space/parse/image",
            files={"image": image_file},
            data={"apikey": api_key, "language": "eng"}
        )

    # Extract text from API response
        try:
            data = response.json()  # Convert API response to JSON

            if "ParsedResults" in data and len(data["ParsedResults"]) > 0:
                parsed_text = data["ParsedResults"][0].get("ParsedText", "")  # Safely extract text

                if parsed_text:
                    print("Extracted Text:\n", parsed_text)
                else:
                    print("No text extracted.")
            else:
                print("Error: No ParsedResults found in API response.")

        except requests.exceptions.JSONDecodeError:
            print("Error: API response is not valid JSON")
            print("Raw Response Content:", response.text)

        # Write text to CSV
        lines = parsed_text.split("\n")  # Split text into lines
        page_lines = []  # Store lines for this page
        
        for j, line in enumerate(lines):
            if line.strip():  # Ignore empty lines
                #csv_writer.writerow([f"Page {i+1}", j+1-empty_line, line.strip()])  # Write data
                page_lines.append(line.strip())
                
        csv_writer.writerow(page_lines)  # Write data

print(f"✅ OCR process completed! Extracted text saved in {output}")
