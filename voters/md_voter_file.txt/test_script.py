import os
import pandas as pd 
from datawrapper import Datawrapper

# Retrieve the API token from environment variables
api_token = os.getenv('DATAWRAPPER_MD_DATA')
if api_token is None:
    raise ValueError("API token not found. Please set the DATAWRAPPER_MD_DATA environment variable.")

print("Using API token: {}".format(api_token))  # Print the API token for verification

# Initialize the Datawrapper object
dw = Datawrapper(api_token)

# Verify the connection by fetching account information
try:
    account_info = dw.get_my_account()
    if account_info:
        print("Account Information Retrieved Successfully:")
        print(account_info)
    else:
        print("No account information returned.")
except Exception as e:
    print(f"An error occurred: {e}")