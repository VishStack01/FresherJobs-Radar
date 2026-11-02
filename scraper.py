import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# 1. Connect to Google Sheets
scope = ["[suspicious link removed]", "[suspicious link removed]"]
# Retrieve service account credentials from GitHub Secrets
creds_dict = json.loads(os.environ["GCP_SA_KEY"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

sheet = client.open("Job_Board_Database").sheet1

# 2. Get existing apply links to guarantee NO duplicates
existing_links = set(sheet.col_values(8)[1:])  # Column 8 is 'Apply Link'

# 3. Example Job Fetcher (Targeting ATS boards / job APIs)
def fetch_jobs():
    # Replace or extend with your target scrapers / ATS APIs
    # (e.g., Greenhouse, Lever, or direct company feeds)
    sample_scraped_jobs = [
        # {
        #   "role": "...", "company": "...", "location": "...",
        #   "ctc": "...", "desc": "...", "eligibility": "...",
        #   "skills": "...", "link": "..."
        # }
    ]
    return sample_scraped_jobs

# 4. Filter and append new records
new_jobs = fetch_jobs()
rows_to_add = []

for job in new_jobs:
    if job["link"] not in existing_links:
        rows_to_add.append([
            job["role"],
            job["company"],
            job["location"],
            job["ctc"],
            job["desc"],
            job["eligibility"],
            job["skills"],
            job["link"],
            datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        ])
        existing_links.add(job["link"])

if rows_to_add:
    sheet.append_rows(rows_to_add)
    print(f"Successfully added {len(rows_to_add)} fresh jobs.")
else:
    print("No new unique jobs found this hour.")
