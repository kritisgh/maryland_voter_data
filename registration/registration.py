import os
import camelot
import pandas as pd

base_dir = "csvs"
data = []

for folder in os.listdir(base_dir):
    folder_path = os.path.join(base_dir, folder)
    if os.path.isdir(folder_path):
        if "_" in folder:
            year, month = folder.split("_")
        else:
            continue

        csv_file = os.path.join(folder_path, "table-page-1-table-1.csv")
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            df.columns = df.columns.str.upper().str.strip()

            required_columns = ["COUNTY", "DEM_ACTIVE", "REP_ACTIVE", "UNAF_ACTIVE", "OTH_ACTIVE", "OTHER_ACTIVE"]
            df = df[[col for col in required_columns if col in df.columns]]

            for _, row in df.iterrows():
                county = str(row.get("COUNTY", "")).strip()

                def safe_int(val):
                    val = str(val).replace(",", "").strip()
                    return int(val) if val.isdigit() else 0

                dem = safe_int(row.get("DEM_ACTIVE", 0))
                rep = safe_int(row.get("REP_ACTIVE", 0))
                unaf = safe_int(row.get("UNAF_ACTIVE", 0))
                oth = safe_int(row.get("OTH_ACTIVE", 0))
                other_parties = safe_int(row.get("OTHER_ACTIVE", 0))

                total_other = oth + other_parties

                if county and county.upper() != "TOTAL":
                    data.append({
                        "year": year,
                        "month": month,
                        "county": county,
                        "dem": dem,
                        "rep": rep,
                        "unaf": unaf,
                        "other": total_other
                    })
final_df = pd.DataFrame(data)
print(final_df)

final_df.to_csv("voter_registration_summary.csv", index=False)

"""pdf_dir = "pdfs"
output_dir = "csvs"

for filename in os.listdir(pdf_dir):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(pdf_dir, filename)
        pdf_name = os.path.splitext(filename)[0]
        output_folder = os.path.join(output_dir, pdf_name)
        os.makedirs(output_folder, exist_ok=True)

        valid_table_found = False

        for page_num in ["1", "2"]:
            if valid_table_found:
                break

            tables = camelot.read_pdf(pdf_path, pages=page_num)

            for i, table in enumerate(tables):
                df = table.df
                header_row_index = None
                for row_index, row in df.iterrows():
                    row_stripped = row.str.replace(" ", "").str.upper()

                    if "TOTALREGISTRATION" in row_stripped.values or "TOTALACTIVEREGISTRATION" in row_stripped.values:
                        header_row_index = row_index
                        break

                if header_row_index is not None:
                    new_header_row_index = header_row_index + 1

                    if len(df) > new_header_row_index:
                        df.columns = df.iloc[new_header_row_index]
                        df = df[new_header_row_index + 1:].reset_index(drop=True)
                    else:
                        print(f"Not enough rows after 'TOTAL REGISTRATION' in {filename}")
                        continue

                    df.columns = df.columns.str.upper().str.strip()
                    df.rename(columns={df.columns[0]: "COUNTY"}, inplace=True)

                    new_columns = []
                    seen_cols = set()
                    for col in df.columns:
                        if col in seen_cols:
                            new_columns.append(f"{col}_ACTIVE")
                        else:
                            new_columns.append(col)
                            seen_cols.add(col)

                    df.columns = new_columns

                    output_csv = os.path.join(output_folder, f"table-page-1-table-1.csv")
                    df.to_csv(output_csv, index=False)
                    valid_table_found = True
                    print(f"Processed page {page_num} of {filename}")
                    break

            if not valid_table_found and page_num == "2":
                print(f"No valid data found in {filename}")"""