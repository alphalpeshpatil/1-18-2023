from gmailapis import gmail_auth,send_message,getEmails
import os.path
import os
import gmailapis
import flask_mail
import pathlib
from flask import Flask,jsonify,render_template, session, abort, redirect, request
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from Google import Create_Service
import base64
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask_mail import Mail
from flask_cors import CORS,cross_origin
app = Flask(__name__)
CORS(app,supports_credentials=True)
app.secret_key='alpeshpatil'
app.config['Mail_server']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='alpeshpatilalpesh@gmail.com'
app.config['MAIL_PASSWORD']='12345678'
app.config['MAIL_USE_TSL']=False
app.config['MAIL_USE_SSL']=True
mail=Mail(app)
app.config['SECRET_KEY']='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'
app.config['SESSION_PERMANENT']=False
app.config['SESSION_TYPE']="filesystem"

apiKey_global=""
api_endpoint_entry="/api/staging"

@app.route(api_endpoint_entry+'/v1/gmailoauth',methods=['POST'])
def gmailoauth():
    result=gmailapis.gmail_auth()
    return jsonify(result)

@app.route(api_endpoint_entry+'/v1/send_message',methods=['GET',"POST"])
def send_message():
    result=gmailapis.send_message()
    return result

@app.route(api_endpoint_entry+'/v1/get_message',methods=['Get',"POST"])
def get_message():
    result=gmailapis.getEmails()
    return result

if __name__ == '__main__':
    app.run(debug=True)