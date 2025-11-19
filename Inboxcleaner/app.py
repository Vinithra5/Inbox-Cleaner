import streamlit as st
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
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token_file:
            token_file.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def fetch_unsubscribe_links(max_results=20):
    service = get_gmail_service()
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=max_results).execute()
    messages = results.get('messages', [])
    links = []

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='metadata', metadataHeaders=['List-Unsubscribe']).execute()
        headers = msg_data['payload'].get('headers', [])
        for header in headers:
            if header['name'].lower() == 'list-unsubscribe':
                raw = header['value']
                match = re.search(r'<(http.+?)>', raw)
                if match:
                    links.append(match.group(1))
                else:
                    links.append(raw)
    return links

st.title("Inbox Cleaner - Unsubscribe Tool")

if st.button("Fetch Unsubscribe Links"):
    unsubscribe_links = fetch_unsubscribe_links()
    if unsubscribe_links:
        for i, link in enumerate(unsubscribe_links, 1):
            st.write(f"{i}. [Unsubscribe]({link})")
    else:
        st.write("No unsubscribe links found.")
