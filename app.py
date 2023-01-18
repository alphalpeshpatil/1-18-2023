import os
import pathlib
from flask import Flask,session,redirect,request
from google_auth_oauthlib.flow import Flow
from Google import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from Google import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

app = Flask(__name__)
app.secret_key="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"
google_client_id="900829648049-quo4shsm3pa4apj23t6hltih0p2t6tci.apps.googleusercontent.com"
client_secrets_file=os.path.join(pathlib.Path(__file__).parent,"credentials.json")
flow=Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile","https://www.googleapis.com/auth/userinfo.email",open]
)
def login_is_required(function):
    def wrapper(*args,**kwargs):
        if "google_id" not in session:
            return ConnectionAbortedError
        else:
            return function()
    return wrapper
@app.route("/login")
def login():
    authorization_url,state=flow.authorization_url()
    # session['state']=state
    return redirect(authorization_url)
@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)
if __name__=="__main__":
    app.run(debug="true")
