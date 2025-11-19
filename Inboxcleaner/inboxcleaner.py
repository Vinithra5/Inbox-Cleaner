from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import re

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('client_secret_224305909151-evfjfb8m6geqbtfv4ckqass4a83q6srg.apps.googleusercontent.com.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def extract_unsubscribe_links():
    service = get_gmail_service()
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=10).execute()
    messages = results.get('messages', [])

    print("Found", len(messages), "emails")

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='metadata', metadataHeaders=['List-Unsubscribe']).execute()
        headers = msg_data['payload'].get('headers', [])
        for header in headers:
            if header['name'].lower() == 'list-unsubscribe':
                raw = header['value']
                match = re.search(r'<(http.+?)>', raw)
                if match:
                    print("Unsubscribe URL:", match.group(1))
                else:
                    print("Unsubscribe Header:", raw)

if __name__ == '__main__':
    extract_unsubscribe_links()
