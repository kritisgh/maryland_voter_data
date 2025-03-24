import camelot
import os

pdf_dir = "pdfs"
output_dir = "csv"

for filename in os.listdir(pdf_dir):
    pdf_path = os.path.join(pdf_dir, filename)
    pdf_name = os.path.splitext(filename)[0]

    output_folder = os.path.join(output_dir, pdf_name)
    os.makedirs(output_folder, exist_ok=True)

    tables = camelot.read_pdf(pdf_path, pages="all")
    output_csv_pattern = os.path.join(output_folder, "table.csv")
    tables.export(output_csv_pattern, f="csv", compress=False)
