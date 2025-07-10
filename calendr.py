import Db
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from LLM import convert_calendar
import json
collection = Db.get_db()

def get_calendar_service(credentials_data):
    creds = Credentials(
        token=credentials_data['token'],
        refresh_token=credentials_data['refresh_token'],
        token_uri=credentials_data['token_uri'],
        client_id=credentials_data['client_id'],
        client_secret=credentials_data['client_secret'],
        scopes=credentials_data['scopes']
    )
    return build('calendar', 'v3', credentials=creds)

def create_task(user_number, user_msg):
    creds = collection.find_one({'user_number': user_number})
    if not creds:
        return "User not found. Please authorize with Google first."

    service = get_calendar_service(creds)
    return create_event(service, user_msg)
def create_event(service, user_msg):
    event = convert_calendar(user_msg)
    print(event)

    if "no" in event.get('summary', '').lower():
        return ("Unable to create the task with the provided information. "
                "Please share only the task, event, or deadline details. "
                "For example: 'Submit assignment by 5 PM tomorrow'.")

    event_result = service.events().insert(calendarId='primary', body=event).execute()
    print("Event created:", event_result.get('id'))

    # Extract event summary and start time
    summary = event_result.get('summary', 'No Title')
    start_time = event_result.get('start', {}).get('dateTime', event_result.get('start', {}).get('date'))

    return (f"✅ Event '{summary}' created successfully!\n"
            f"🕒 Starts at: {start_time}\n"
            f"🔔 You will be reminded 30 minutes and 5 minutes before the event.\n"
            f"📅 Please check your Google Calendar app.")

