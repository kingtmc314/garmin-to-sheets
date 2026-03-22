import os
import json
import datetime
import gspread
from garminconnect import Garmin

def main():
    # 1. Load Secrets from GitHub Environment Variables
    garmin_email = os.environ.get("GARMIN_EMAIL")
    garmin_password = os.environ.get("GARMIN_PASSWORD")
    google_json_string = os.environ.get("GOOGLE_CREDENTIALS_JSON")

    if not all([garmin_email, garmin_password, google_json_string]):
        print("Error: Missing credentials in environment variables.")
        return

    # 2. Connect to Garmin
    try:
        print("Logging into Garmin...")
        client = Garmin(garmin_email, garmin_password)
        client.login()
    except Exception as e:
        print(f"Garmin login failed: {e}")
        return

    # 3. Fetch Today's Data
    today = datetime.date.today().isoformat()
    print(f"Fetching data for {today}...")
    stats = client.get_stats(today)
    
    data = [
        today,
        stats.get('totalSteps', 0),
        stats.get('restingHeartRate', 0),
        stats.get('vigorousIntensityMinutes', 0)
    ]

    # 4. Connect to Google Sheets
    try:
        print("Connecting to Google Sheets...")
        # Parse the JSON string back into a dictionary
        credentials_dict = json.loads(google_json_string)
        
        # Authenticate using the dictionary
        gc = gspread.service_account_from_dict(credentials_dict)
        
        # Open the sheet (Make sure it is named exactly this)
        sheet = gc.open("GarminDataSheet").sheet1
        
        # Append the data to the next available row
        sheet.append_row(data)
        print(f"Successfully added data to Google Sheets: {data}")
        
    except Exception as e:
        print(f"Google Sheets upload failed: {e}")

if __name__ == "__main__":
    main()
