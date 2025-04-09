import pandas as pd
import matplotlib.pyplot as plt

# Load your monthly totals
monthly_totals = pd.read_csv("monthly_inactive_totals.csv")

# Make sure the date column is in datetime format
monthly_totals["date"] = pd.to_datetime(monthly_totals["date"])

# Plot it
plt.figure(figsize=(12, 6))
plt.plot(monthly_totals["date"], monthly_totals["inactive"], marker="o", label="Inactive Voters")
plt.title("Inactive Voter Trends in Maryland Over Time")
plt.xlabel("Date")
plt.ylabel("Total Inactive Voters")
plt.grid(True)

# Highlight presidential election Novembers
election_months = ["2008-11", "2012-11", "2016-11", "2020-11", "2024-11"]
for em in election_months:
    em_date = pd.to_datetime(em)
    plt.axvline(em_date, color="red", linestyle="--", alpha=0.6)
    plt.text(em_date, plt.ylim()[1]*0.95, em[:4], color="red", ha="center", fontsize=9)

plt.legend()
plt.tight_layout()
plt.savefig("inactive_voter_trend.png")  # ✅ Save as image file
print("Plot saved as inactive_voter_trend.png")