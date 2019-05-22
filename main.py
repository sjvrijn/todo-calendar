import pickle
import os.path
import requests
import todoist
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def asUTC(t):
    return t.isoformat() + 'Z'  # 'Z' indicates UTC time


def getcurrentevent(calendar_name):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if not os.path.exists('credentials.json'):
            raise FileNotFoundError("'credentials.json' not found, please "
                                    "obtain some Google Calendar API "
                                    "credentials first.")

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.utcnow()

    calendars = service.calendarList().list().execute().get('items', [])
    cal = [c for c in calendars if c['summary'] == calendar_name][0]

    cur_event = service.events().list(calendarId=cal['id'], orderBy='startTime',
                                      maxResults=1, singleEvents=True,
                                      timeMax=asUTC(now + timedelta(seconds=1)),
                                      timeMin=asUTC(now)).execute()
    events = cur_event.get('items', [])
    if not events:
        raise Exception('No upcoming events found.')

    return events[0]


def getfirsttask(filter_name):
    with open('todoist.key', 'r') as keyfile:
        key = keyfile.read()

    api = todoist.TodoistAPI(key)
    api.sync()
    f = [f for f in api.state['filters'] if f['name'] == filter_name][0]

    tasks = requests.get(
        "https://beta.todoist.com/API/v8/tasks",
        params={
            "filter": f['query']
        },
        headers={
            "Authorization": f"Bearer {key}"
        }).json()

    return tasks[0]


if __name__ == '__main__':
    # getcurrentevent('Day-planning')

    task = getfirsttask(filter_name='Desk-Widget')
    print(task)
    print()
    print(task['content'])
