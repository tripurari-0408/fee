import os
import gspread
from google.oauth2.service_account import Credentials

def get_google_sheet():
    # 1. Define the necessary Google scopes
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    # 2. Pull credentials from Wasmer Environment Variables
    client_email = os.environ.get('GOOGLE_SERVICE_ACCOUNT_EMAIL')
    
    # CRITICAL FIX: Environment variables often escape newlines. 
    # This replace() ensures the private key retains its correct multiline format.
    raw_private_key = os.environ.get('GOOGLE_PRIVATE_KEY', '')
    private_key = raw_private_key.replace('\\n', '\n')

    # 3. Construct the credentials dictionary in memory
    credentials_dict = {
        "client_email": client_email,
        "private_key": private_key,
        "token_uri": "https://oauth2.googleapis.com/token",
    }

    try:
        # 4. Authenticate using the dictionary instead of a file
        credentials = Credentials.from_service_account_info(
            credentials_dict, 
            scopes=scopes
        )
        client = gspread.authorize(credentials)

        # 5. Connect to your specific sheet (Best practice: keep the ID in an env var too)
        sheet_id = os.environ.get('GOOGLE_SHEET_ID')
        workbook = client.open_by_key(sheet_id)
        
        # Return the first worksheet
        return workbook.sheet1 

    except Exception as e:
        print(f"Error connecting to Google Sheets: {e}")
        return None

# Usage example:
# my_sheet = get_google_sheet()
# data = my_sheet.get_all_records()