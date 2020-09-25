from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from inference import infer_rankings

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
RANKINGS_SPREADSHEET_ID = 'INSERT_SPREADSHEET_ID_HERE'
DATA_RANGE = 'Data!A:D'
BACKUP_RANKINGS_RANGE = 'AutoRankings!C:D'
RANKINGS_RANGE = 'AutoRankings!A:B'

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    print('Found credentials')
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    
    result = sheet.values().get(spreadsheetId=RANKINGS_SPREADSHEET_ID,
                                range=DATA_RANGE).execute()
    print('Downloaded match results')
    values = result.get('values', [])
    result = sheet.values().get(spreadsheetId=RANKINGS_SPREADSHEET_ID,
                                range=RANKINGS_RANGE).execute()
    previous_rankings = result.get('values', [])
    print('Downloaded old rankings')

    if not values or not previous_rankings:
        print('No data found.')
    else:
        entries = ["\t".join(row) for row in values]
        rankings = infer_rankings(entries)

        print('Calculated old rankings')

        old_rankings = dict([(r[0], r[1]) for r in previous_rankings])

        changes = sorted([(name, float(rankings[name]) - float(old_rankings.get(name, 0))) for name in rankings],
           key=lambda r: -abs(r[1]))

        print()
        print('Largest changes:')
        for i in range(0, min(10, len(changes))):
            name, change = changes[i]
            if abs(change) < 1:
                break
            print(f"{name}: {'+' if int(change) > 0 else ''}{int(change)}")
        print()

        rankings_cells = [[name, rankings[name]] for name in rankings]

        sheet.values().update(spreadsheetId=RANKINGS_SPREADSHEET_ID,
                                range=BACKUP_RANKINGS_RANGE, 
                                valueInputOption="USER_ENTERED",
                                body={'values': previous_rankings}).execute()

        sheet.values().update(spreadsheetId=RANKINGS_SPREADSHEET_ID,
                                range=RANKINGS_RANGE, 
                                valueInputOption="USER_ENTERED",
                                body={'values': rankings_cells}).execute()
        print('Updated rankings in spreadsheet')

if __name__ == '__main__':
    main()
