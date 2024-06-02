# heavily based on the Google reader from llamahub
# it adds the ability to paginate through the results
# and discards the ability to compose emails

import os
import base64
import email
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from typing import Any, List, Optional

SCOPES = [
    # "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.readonly",
]

class GmailSearcher:
    query: str = None
    use_iterative_parser: bool = False
    max_results: int = 10
    service = None

    def _cache_service(self) -> None:
        from googleapiclient.discovery import build

        credentials = self._get_credentials()
        if not self.service:
            self.service = build("gmail", "v1", credentials=credentials)

    def _get_credentials(self) -> Any:
        """Get valid user credentials from storage.

        The file token.json stores the user's access and refresh tokens, and is
        created automatically when the authorization flow completes for the first
        time.

        Returns:
            Credentials, the obtained credential.
        """
        import os

        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow

        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=8080)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        return creds
    
    def search_messages(self, query: str, max_results = None, next_token = None):
        if not max_results:
            max_results = self.max_results

        self._cache_service()

        # https://googleapis.github.io/google-api-python-client/docs/dyn/gmail_v1.users.messages.html#list
        messagesResult = (
            self.service.users()
            .messages()
            .list(userId="me", q=query, maxResults=int(max_results), pageToken=next_token)
            .execute()
        )
        messages = messagesResult.get("messages", [])
        next_token = messagesResult.get("nextPageToken", None)

        results = []
        try:
            for message in messages:
                message_data = self.get_message_data(message)
                text = message_data.pop("body")
                extra_info = message_data
                results.append({
                    "text":text, 
                    "extra_info":extra_info
                })
        except Exception as e:
            raise Exception("Can't get message data" + str(e))

        return {
            "messages": results,
            "next_token": next_token
        }
    
    def get_message_data(self, message):
        message_id = message["id"]
        message_data = (
            self.service.users()
            .messages()
            .get(format="raw", userId="me", id=message_id)
            .execute()
        )
        if self.use_iterative_parser:
            body = self.extract_message_body_iterative(message_data)
        else:
            body = self.extract_message_body(message_data)

        if not body:
            return None

        return {
            "id": message_data["id"],
            "threadId": message_data["threadId"],
            "snippet": message_data["snippet"],
            "body": body,
        }

    def extract_message_body_iterative(self, message: dict):
        if message["raw"]:
            body = base64.urlsafe_b64decode(message["raw"].encode("utf8"))
            mime_msg = email.message_from_bytes(body)
        else:
            mime_msg = message

        body_text = ""
        if mime_msg.get_content_type() == "text/plain":
            plain_text = mime_msg.get_payload(decode=True)
            charset = mime_msg.get_content_charset("utf-8")
            body_text = plain_text.decode(charset).encode("utf-8").decode("utf-8")

        elif mime_msg.get_content_maintype() == "multipart":
            msg_parts = mime_msg.get_payload()
            for msg_part in msg_parts:
                body_text += self.extract_message_body_iterative(msg_part)

        return body_text

    def extract_message_body(self, message: dict):
        from bs4 import BeautifulSoup

        try:
            body = base64.urlsafe_b64decode(message["raw"].encode("utf-8"))
            mime_msg = email.message_from_bytes(body)

            # If the message body contains HTML, parse it with BeautifulSoup
            if "text/html" in mime_msg:
                soup = BeautifulSoup(body, "html.parser")
                body = soup.get_text()
            return body.decode("utf-8")
        except Exception as e:
            raise Exception("Can't parse message body" + str(e))

# # authorize accessing gmail.
# # your app needs a credentials.json with access to the scopes listed above
# # unless you get your app verified by google, you'll need to set it to test mode
# # and manually add the emails of users you want to be able to use this app
# creds = None
# if os.path.exists("token.json"):
#     creds = Credentials.from_authorized_user_file("token.json", SCOPES)
# # If there are no (valid) credentials available, let the user log in.
# if not creds or not creds.valid:
#     if creds and creds.expired and creds.refresh_token:
#         creds.refresh(Request())
#     else:
#         flow = InstalledAppFlow.from_client_secrets_file(
#             "credentials.json", SCOPES
#         )
#         creds = flow.run_local_server(port=8080)
#     # Save the credentials for the next run
#     with open("token.json", "w") as token:
#         token.write(creds.to_json())
