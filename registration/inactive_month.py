import pandas as pd

# Load the cleaned voter registration summary
final_df = pd.read_csv("inactive_voter_summary.csv")

# Filter out any rows where year or month aren't digits
final_df = final_df[
    final_df["year"].astype(str).str.isdigit() &
    final_df["month"].astype(str).str.isdigit()
]

# Convert year/month to datetime
final_df["date"] = pd.to_datetime(
    final_df["year"].astype(str) + "-" + final_df["month"].astype(str).str.zfill(2),
    errors="coerce"  # This will turn bad dates into NaT (null)
)

# Drop any rows where datetime conversion failed
final_df = final_df.dropna(subset=["date"])

# Sum inactive voters by month
monthly_totals = (
    final_df.groupby("date")["inactive"]
    .sum()
    .reset_index()
    .sort_values("date")
)

# Save output
monthly_totals.to_csv("monthly_inactive_totals.csv", index=False)
print(monthly_totals.head())
