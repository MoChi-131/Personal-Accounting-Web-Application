from MongoDB import agg_money_in, agg_money_out, Full_Out, Reciept_Link_BS
from OCR import pdf_extract, data_extract, data_cleaning
from save_excel import upload_excel
from Mindee import Scan_Reciept, Upload_Reciept, Embed_Reciept


def Save_BS(file_path):
    print("Saving", file_path)
    pdf_extract(file_path)
    print("PDF")
    data_extract() 
    data_cleaning()
    upload_excel()
    agg_money_in()
    agg_money_out()
    Full_Out()
    Reciept_Link_BS()
    
    return

def Save_Reciept(file_path):
    Scan_Reciept(file_path)
    Upload_Reciept()
    Embed_Reciept()
    Reciept_Link_BS()