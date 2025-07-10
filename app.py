from flask import Flask, request, redirect, session, url_for,make_response
from twilio.twiml.messaging_response import MessagingResponse
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import os
from Db import add_tokens
app = Flask(__name__)
import calendr
app.secret_key = 'your-very-secret-key'
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # Allow HTTP for dev

SCOPES = ['https://www.googleapis.com/auth/calendar']
CLIENT_SECRETS_FILE = "/etc/secrets/client_secret.json"
import os
redirect_uri = os.getenv("REDIRECT_URI")

@app.route('/', methods=['POST'])
def sms_reply():
    user_num = request.values.get("From")
    user_msg = request.values.get("Body", "").strip().lower()
    response = MessagingResponse()
    print(user_msg)
    if "setup calendar" in user_msg:
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE,
            scopes=SCOPES,
            redirect_uri = redirect_uri
        )
        auth_url, _ = flow.authorization_url(prompt='consent',state=user_num)
        response.message(f"Click to connect your Google Calendar: {auth_url}")
    else:
        result = calendr.create_task(user_num,user_msg)
        response.message(str(result))
    print("returning")
    return str(response)

@app.route('/oauth2callback')
def oauth2callback():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=redirect_uri
    )
    flow.fetch_token(authorization_response=request.url)
    user_number = request.args.get('state')
    credentials = flow.credentials
    credentials_data = {
        'user_number': user_number,
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    response = add_tokens(credentials_data)
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
