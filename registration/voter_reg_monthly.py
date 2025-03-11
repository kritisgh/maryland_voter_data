import os
import requests
from datetime import datetime

def download_maryland_pdfs(start_year=2006, start_month=1, end_year=None, end_month=None, save_dir="voter_reg_pdfs"):
    """
    Downloads PDFs from the Maryland elections website based on a given date range.
    
    :param start_year: The starting year (default 2006)
    :param start_month: The starting month (default 1)
    :param end_year: The ending year (default is the current year)
    :param end_month: The ending month (default is the current month)
    :param save_dir: Directory to save the downloaded PDFs
    """
    if end_year is None or end_month is None:
        today = datetime.today()
        end_year = end_year or today.year
        end_month = end_month or today.month
    
    # Ensure save directory exists
    os.makedirs(save_dir, exist_ok=True)
    
    base_url = "https://elections.maryland.gov/pdf/vrar/"
    
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            if (year == start_year and month < start_month) or (year == end_year and month > end_month):
                continue
            
            month_str = f"{month:02d}"
            url = f"{base_url}{year}_{month_str}.pdf"
            filename = os.path.join(save_dir, f"{year}_{month_str}.pdf")
            
            try:
                response = requests.get(url, stream=True)
                if response.status_code == 200:
                    with open(filename, "wb") as pdf_file:
                        for chunk in response.iter_content(1024):
                            pdf_file.write(chunk)
                    print(f"Downloaded: {filename}")
                else:
                    print(f"Failed to download {url} (Status Code: {response.status_code})")
            except requests.RequestException as e:
                print(f"Error downloading {url}: {e}")

