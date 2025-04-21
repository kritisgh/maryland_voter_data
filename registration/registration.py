#create csv
"""import os
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
                county = row.get("COUNTY", "") or row.get("COUNTY_ACTIVE", "")
                county = str(county).strip()

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

final_df.to_csv("voter_registration_summary.csv", index=False)"""

#fix csv
'''pdf_dir = "pdfs"
output_dir = "csvs"

for filename in os.listdir(pdf_dir):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(pdf_dir, filename)
        pdf_name = os.path.splitext(filename)[0]
        output_folder = os.path.join(output_dir, pdf_name)
        os.makedirs(output_folder, exist_ok=True)

        table_processed = False

        for page_num in ["1", "2"]:
            if table_processed:
                break

            tables = camelot.read_pdf(pdf_path, pages=page_num)

            for i, table in enumerate(tables):
                df = table.df

                # Look for 'TOTAL REGISTRATION' or 'TOTAL ACTIVE REGISTRATION'
                header_row_index = None
                for row_index, row in df.iterrows():
                    row_stripped = row.astype(str).str.replace(" ", "").str.upper()
                    if "TOTALREGISTRATION" in row_stripped.values or "TOTALACTIVEREGISTRATION" in row_stripped.values:
                        header_row_index = row_index
                        break

                if header_row_index is not None:
                    new_header_row_index = header_row_index + 1

                    if len(df) > new_header_row_index:
                        # Use the row after "TOTAL REGISTRATION" as header
                        df.columns = df.iloc[new_header_row_index]
                        df = df[new_header_row_index + 1:].reset_index(drop=True)
                    else:
                        print(f"Not enough rows after header in {filename}")
                        continue

                    # Normalize headers
                    df.columns = df.columns.str.upper().str.strip()
                    df.rename(columns={df.columns[0]: "COUNTY"}, inplace=True)

                    # Rename duplicates with _ACTIVE
                    new_columns = []
                    seen = set()
                    for col in df.columns:
                        if col in seen:
                            new_columns.append(f"{col}_ACTIVE")
                        else:
                            new_columns.append(col)
                            seen.add(col)
                    df.columns = new_columns

                    # Save final cleaned CSV
                    output_csv = os.path.join(output_folder, "table-page-1-table-1.csv")
                    df.to_csv(output_csv, index=False)
                    print(f"Processed {filename} (page {page_num})")
                    table_processed = True
                    break

        if not table_processed:
            print(f"Could not find 'TOTAL REGISTRATION' in any table in {filename}")'''




#fix db
"""import pandas as pd
import sqlite3

# Load the clean CSV
df = pd.read_csv("static/voter_registration_summary.csv")

# Normalize county names
def clean_county(name):
    name = str(name).strip().upper()
    name = " ".join(name.split())  # Remove extra spaces

    # Fix specific known typos
    typo_fixes = {
        "BALTIMORE C ITY": "BALTIMORE CITY",
        "BALTIMORE C O.": "BALTIMORE CO.",
        "BALTIMORE C O": "BALTIMORE CO.",
        "BALTIMORE C ITY.": "BALTIMORE CITY"
    }

    return typo_fixes.get(name, name)

df['county'] = df['county'].apply(clean_county)

# Connect to SQLite
conn = sqlite3.connect("registration.db")
cursor = conn.cursor()

# Drop existing table if it exists
cursor.execute("DROP TABLE IF EXISTS registration")

# Create a fresh table
cursor.execute("""
    CREATE TABLE registration (
        year INTEGER,
        month INTEGER,
        county TEXT,
        dem INTEGER,
        rep INTEGER,
        unaf INTEGER,
        other INTEGER
    )
""")

# Insert data into table
df.to_sql("registration", conn, if_exists="append", index=False)

conn.commit()
conn.close()

print("registration.db recreated with cleaned county names.")"""