import csv

output = "../output_csv/output.csv"

with open(output, mode="r", newline="", encoding="utf-8") as csv_file:
    csv_reader = csv.reader(csv_file)
    for i, pages in enumerate (csv_reader):
        print ("Page : ", i+1)
        for line in enumerate(pages):
            print(line)
        print()
        print()