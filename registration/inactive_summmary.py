import os
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

            if "COUNTY" not in df.columns or "INACTIVE" not in df.columns:
                print(f"Skipping {csv_file} — missing required columns.")
                continue

            for _, row in df.iterrows():
                county = str(row.get("COUNTY", "")).strip()
                
                def safe_int(val):
                    val = str(val).replace(",", "").strip()
                    return int(val) if val.isdigit() else 0

                inactive = safe_int(row.get("INACTIVE", 0))

                if county and county.upper() != "TOTAL":
                    data.append({
                        "year": year,
                        "month": month,
                        "county": county,
                        "inactive": inactive
                    })

# Build the final DataFrame and export
final_df = pd.DataFrame(data)
print(final_df.head())

final_df.to_csv("inactive_voter_summary.csv", index=False)
