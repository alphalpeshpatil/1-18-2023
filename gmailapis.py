import pathlib
from flask import jsonify
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
import base64
import pickle
from googleapiclient.errors import HttpError
import os
import json
import base64
from email.message import EmailMessage

from Google import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from bs4 import BeautifulSoup

from login import API_NAME, API_VERSION, CLIENT_SECRET_FILE
# app.config['SECRET_KEY']='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'
# app.config['SESSION_PERMANENT']=False
# app.config['SESSION_TYPE']="filesystem"
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
global_creds=[]
home_dir=os.path.expanduser('~')
pickle_path=os.path.join(home_dir,'gmail.pickle')
global_creds_set=""
global_creds.clear()
global_creds.append(global_creds_set)

def gmail_auth():
    try:
        home_dir=os.path.expanduser('~')
        flow=InstalledAppFlow.from_client_secrets_file('credentials.json',SCOPES)
        print(flow)
        creds=flow.run_local_server(port=5001)
        pickle_path=os.path.join(home_dir,'gmail.pickle')

        with open(pickle_path,'wb') as token:
            pickle.dimp(creds,token)
        global_creds_set=pickle.load(open(pickle_path),'rb')
        global_creds.clear()
        global_creds.append(global_creds_set)
        return 'Authentication Done successfuly'
    except Exception as ex:
        print(ex)
        return str(ex)

def send_message():
    try:
        client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "credentials.json")
        flow = Flow.from_client_secrets_file(
        client_secrets_file=client_secrets_file,
        scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"]
        # redirect_uri="http://127.0.0.1:5000/callback"
)

        authorization_url, state = flow.authorization_url()
        service =Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

        emailMsg = 'You won rs 100,000'
        mimeMessage = MIMEMultipart()
        mimeMessage['to'] = 'alpeshpatilalpesh91@gmail.com'
        mimeMessage['subject'] = 'You won'
        mimeMessage.attach(MIMEText(emailMsg, 'plain'))
        raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

        message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
        print(message)

    except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None
    # print(send_message)
    return message

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly','https://www.googleapis.com/auth/gmail.modify']

def getEmails():
    client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "credentials.json")
    flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"])
        # redirect_uri="http://127.0.0.1:5000/callback"


    authorization_url, state = flow.authorization_url()
    service =Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    try:
        # Call the Gmail API
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
        messages = results.get('messages',[]);
        if not messages:
            print('No new messages.')
        else:
            message_count = 0
            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id']).execute()                
                email_data = msg['payload']['headers']
                for values in email_data:
                    name = values['name']
                    if name == 'From':
                        from_name= values['value']                
                        for part in msg['payload']['parts']:
                            try:
                                data = part['body']["data"]
                                byte_code = base64.urlsafe_b64decode(data)

                                text = byte_code.decode("utf-8")
                                print ("This is the message: "+ str(text))

                                # mark the message as read (optional)
                                msg  = service.users().messages().modify(userId='me', id=message['id'], body={'removeLabelIds': ['UNREAD']}).execute()   
                                print(msg)
                                return msg                                                    
                            except BaseException as error:
                                msg="no unread message"
                                return msg                         
    except Exception as error:
        msg="no unread messages"
        return msg


