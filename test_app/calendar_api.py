from unittest import result
from httplib2 import Credentials
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
scopes=['https://www.googleapis.com/auth/calendar']
flow=InstalledAppFlow.from_client_secrets_file("client_secret.json",scopes=scopes)
credentials=flow.run_console()

import pickle
pickle.dump(credentials,open("token.pkl","wb"))
credentials=pickle.load(open("token.pkl","rb"))

service=build("calendar","v3",credentials=credentials)

#GET CALENDAR
result=service.calendarList().list().execute()
result['items'][0]

#GET EVENT
calendar_id = result['items'][0]['id']
result = service.events().list(calendarId=calendar_id, timeZone="Asia/Kolkata").execute()
result['items'][0]


#CREATE
from datetime import datetime, timedelta
start_time = datetime(2019, 5, 12, 19, 30, 0)
end_time = start_time + timedelta(hours=4)
timezone = 'Asia/Kolkata'
event = {
  'summary': 'IPL Final 2022',
  'location': 'Hyderabad',
  'description': 'MI vs TBD',
  'start': {
    'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
    'timeZone': timezone,
  },
  'end': {
    'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
    'timeZone': timezone,
  },
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'email', 'minutes': 24 * 60},
      {'method': 'popup', 'minutes': 10},
    ],
  },
}
service.events().insert(calendarId=calendar_id, body=event).execute()

#UTILITY FUNCTION
import datefinder
matches = datefinder.find_dates("5 may 9 PM")
list(matches)


def create_event(start_time_str, summary, duration=1, description=None, location=None):
    matches = list(datefinder.find_dates(start_time_str))
    if len(matches):
        start_time = matches[0]
        end_time = start_time + timedelta(hours=duration)
    
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'Asia/Kolkata',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    return service.events().insert(calendarId='primary', body=event).execute()
create_event("15 may 9 PM", "Meeting")



