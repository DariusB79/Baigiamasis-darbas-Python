import os
import os.path
import gspread
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import base64
from email.message import EmailMessage



import os
import base64
import mimetypes
from email.message import EmailMessage
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import base64
import mimetypes
from email.message import EmailMessage
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleSheetsClient:
    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets.readonly",
    ]
    TOKEN_PATH = r"C:\Users\HP\OneDrive\Desktop\phyton_mokymai\Paskaitos\_baigiamasis_darbas\creds\token.json"  # Save token here
    CREDENTIALS_PATH = r"C:\Users\HP\OneDrive\Desktop\phyton_mokymai\Paskaitos\_baigiamasis_darbas\creds\client_secret.json"

    def __init__(self):
        self.creds = None
        self.service = None
        self.authenticate()

    def authenticate(self):
        """Authenticate user and get Gmail API service."""
        if os.path.exists(self.TOKEN_PATH):
            self.creds = Credentials.from_authorized_user_file(
                filename=self.TOKEN_PATH, scopes=self.SCOPES
            )

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.CREDENTIALS_PATH, self.SCOPES
                )
                self.creds = flow.run_local_server(port=0)

            # Save credentials for the next run
            with open(self.TOKEN_PATH, "w") as token:
                token.write(self.creds.to_json())

        # Initialize Gmail API service
        self.service = build("sheets", "v4", credentials=self.creds)

    def get_sheet_data(self, spreadsheet_id, sheet_range):
        """Fetch data from a specific Google Sheet."""
        try:
            sheet = self.service.spreadsheets()
            result = (
                sheet.values()
                .get(spreadsheetId=spreadsheet_id, range=sheet_range)
                .execute()
            )
            values = result.get("values", [])

            if not values:
                print("No data found.")
                return []

            return values

        except HttpError as err:
            print(f"Error fetching Google Sheet data: {err}")
            return []




class GmailClient:
    SCOPES = [
        "https://www.googleapis.com/auth/gmail.send",
    ]
    TOKEN_PATH = r"C:\Users\HP\OneDrive\Desktop\phyton_mokymai\Paskaitos\_baigiamasis_darbas\creds\token_gmail.json"
    CREDENTIALS_PATH = r"C:\Users\HP\OneDrive\Desktop\phyton_mokymai\Paskaitos\_baigiamasis_darbas\creds\client_secret.json"

    def __init__(self):
        self.creds = None
        self.service = None
        self.authenticate()

    def authenticate(self):
        if os.path.exists(self.TOKEN_PATH):
            self.creds = Credentials.from_authorized_user_file(
                filename=self.TOKEN_PATH, scopes=self.SCOPES
            )
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    client_secrets_file=self.CREDENTIALS_PATH, scopes=self.SCOPES
                )
                self.creds = flow.run_local_server(port=0)
            with open(self.TOKEN_PATH, "w") as token:
                token.write(self.creds.to_json())

        self.service = build(serviceName="gmail", version="v1", credentials=self.creds)

    def send_email_with_attachment(self, to_email, subject, content, file_path):
        try:
            message = EmailMessage()
            message.set_content(content)
            message["To"] = to_email
            message["Subject"] = subject

            # Attachment handling
            content_type, encoding = mimetypes.guess_type(file_path)
            if content_type is None or encoding is not None:
                content_type = "application/octet-stream"
            main_type, sub_type = content_type.split("/", 1)

            with open(file_path, "rb") as file:
                file_data = file.read()
                message.add_attachment(file_data, maintype=main_type, subtype=sub_type, filename=os.path.basename(file_path))

            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            create_message = {"raw": encoded_message}

            send_message = (
                self.service.users()
                .messages()
                .send(userId="me", body=create_message)
                .execute()
            )
            print(f'Message Id: {send_message["id"]}')

        except HttpError as error:
            print(f"An error occurred: {error}")




