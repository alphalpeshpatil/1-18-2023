from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
import io
import mimetypes
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
from flask import Flask, jsonify, request
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

def send_message(mailid,cc,bcc,subject,body,file):
    msg=send_message_with_Attachment(mailid,cc,bcc,subject,body,file)
    try:
        client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "credentials.json")
        flow = Flow.from_client_secrets_file(
        client_secrets_file=client_secrets_file,
        scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"]
        # redirect_uri="http://127.0.0.1:5000/callback"
)
        authorization_url, state = flow.authorization_url()
        service =Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

        # message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
        draft = service.users().messages().send(userId="me",body=msg).execute()
        print(draft)
        print("Message sent successfuly!!!!")
    except HttpError as error:
        print(F'An error occurred: {error}')
        draft = None
    return draft
# def convertToBinaryData(filename):
#     # Convert digital data to binary format
#     with open(filename, 'rb') as file:
#         binaryData = file.read()
#     return binaryData
def send_message_with_Attachment(mailid,cc,bcc,subject,body,file):

        message = MIMEMultipart()
        message['to'] = mailid
        message['cc']=cc
        message['bcc']=bcc
        message['subject'] = subject

        msg = MIMEText(body)
        message.attach(msg)
        # buffer = io.BytesIO()     # create file in memory
        # file.save(buffer, 'jpeg') # save in file in memory - it has to be `jpeg`, not `jpg`
        # buffer.seek(0)            # move to the beginning of file

        # file = buffer 
        # file='butterfly.jpg'
        # print((file)
        # print(type(file))
        # file = convertToBinaryData(file)
        file = str(file.filename)
        (content_type, encoding) = mimetypes.guess_type(file)

        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'

        (main_type, sub_type) = content_type.split('/', 1)
        # print(file)
        if main_type == 'text':
            with open(file, 'rb') as f:
                msg = MIMEText(f.read().decode('utf-8'), _subtype=sub_type)
        elif main_type == 'image':
                f=open(file,'rb')
                msg=MIMEImage(f.read(),_subtype=sub_type)
                f.close()
        elif main_type == 'audio':
            with open(file, 'rb') as f:
                msg = MIMEAudio(f.read(), _subtype=sub_type)
            
        else:
            with open(file, 'rb') as f:
                msg = MIMEBase(main_type, sub_type)
                msg.set_payload(f.read())

        filename = os.path.basename(file)
        msg.add_header('Content-Disposition', 'attachment',
                    filename=filename)
        message.attach(msg)

        raw_message = \
            base64.urlsafe_b64encode(message.as_string().encode('utf-8'))
        return {'raw': raw_message.decode('utf-8')}
    



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

