from mindee import Client, PredictResponse, product
import csv
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

file_1 = os.path.join(current_dir, "Receipt_Detail.csv")
file_2 = os.path.join(current_dir, "Receipt_Items.csv")

# Initialize the Mindee client
mindee_client = Client(api_key="b3419d2b5496291a0cf32219c99d4de1")

def Scan_Reciept(upload_file):
    # Load the file
    input_doc = mindee_client.source_from_path(upload_file)

    attribute_1 = [
        "Supplier Name", "Receipt Number", "Date", "Time", "Category", "Document Type", 
        "Supplier Address", "Supplier Phone Number", "Locale", "Total Amount", 
        "Total Net", "Total Tax", "Tip and Gratuity"
    ]

    attribute_2 = ["Supplier Name", "Receipt Number", "Date", "Description", "Quantity", "Unit Price", "Total Price"]

    # Parse the receipt
    result: PredictResponse = mindee_client.parse(product.ReceiptV5, input_doc)

    # Extract prediction results
    prediction = result.document.inference.prediction

    data_1 = {
        "Supplier Name": prediction.supplier_name.value if prediction.supplier_name else None,
        "Receipt Number": prediction.receipt_number.value if prediction.receipt_number else None,
        "Date": prediction.date.value if prediction.date else None,
        "Time": prediction.time.value if prediction.time else None,
        "Category": prediction.category.value if prediction.category else None,
        "Document Type": prediction.document_type.value if prediction.document_type else None,
        "Supplier Address": prediction.supplier_address.value if prediction.supplier_address else None,
        "Supplier Phone Number": prediction.supplier_phone_number.value if prediction.supplier_phone_number else None,
        "Locale": prediction.locale.value if prediction.locale else None,
        "Total Amount": prediction.total_amount.value if prediction.total_amount else None,
        "Total Net": prediction.total_net.value if prediction.total_net else None,
        "Total Tax": prediction.total_tax.value if prediction.total_tax else None,
        "Tip and Gratuity": prediction.tip.value if prediction.tip else None,
    }

    print(prediction)

    with open(file_1, mode="w", newline="", encoding="utf-8") as csv_f:
        csv_writer = csv.writer(csv_f)
        # **Write transaction details**
        
        csv_writer.writerow(attribute_1)
        
        csv_writer.writerow(data_1.values())


    with open(file_2, mode="w", newline="", encoding="utf-8") as csv_f:
        csv_writer = csv.writer(csv_f)
        # **Write transaction details**
        
        csv_writer.writerow(attribute_2)
        
        for item in prediction.line_items:
            data_2 = {
                "Supplier Name": prediction.supplier_name.value if prediction.supplier_name else None,
                "Receipt Number": prediction.receipt_number.value if prediction.receipt_number else None,
                "Date": prediction.date.value if prediction.date else None,
                "Description": item.description if item.description else None,
                "Quantity": item.quantity if item.quantity else None,
                "Unit Price": item.unit_price if item.unit_price else None,
                "Total Price": item.total_amount if item.total_amount else None
            }
            csv_writer.writerow(data_2.values())  
            
    return
        
        
        
        


