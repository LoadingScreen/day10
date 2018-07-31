"""
Shows basic usage of the Google Calendar API. Creates a Google Calendar API
service object and outputs a list of the next 10 events on the user's calendar.
"""
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime
from datetime import timedelta

# Setup the Calendar API
SCOPES = 'https://www.googleapis.com/auth/calendar'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))

# Call the Calendar API
now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
"""
print('Getting the upcoming 10 events')
events_result = service.events().list(calendarId='primary', timeMin=now,
                                      maxResults=10, singleEvents=True,
                                      orderBy='startTime').execute()
events = events_result.get('items', [])

if not events:
    print('No upcoming events found.')
for event in events:
    start = event['start'].get('dateTime', event['start'].get('date'))
    print(start, event['summary'])
"""

print('Adding a randomly selected intervention...')
# Refer to the Python quickstart on how to setup the environment:
# https://developers.google.com/calendar/quickstart/python
# Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
# stored credentials.

interventions = [
["Avoid interrupting people"],
["Play smash bros. before doing anything else"],
["Stay in bed until getting up feels good"],
["Go to bed by 10"],
["Be less reserved in conversation"],
["Text a friend after eating", "Kill two birbs with 1 Stone!"],
["Shower talks", "they're so good man"]
]

intervention = interventions[3]
summary = intervention[0]
for i in range(1,4):
    startingDay = datetime.date.today()

    event = {
      'summary': "Day %s/10: %s" %(i,summary),
      'description': intervention[1],
      'start': {'date':(startingDay+timedelta(days=i)).isoformat()},
      'end': {'date': (startingDay+timedelta(days=i)).isoformat()}, #(startingDay+timedelta(days=i)).isoformat(),
      'reminders': {
        'useDefault': False,
        'overrides': [
          {'method': 'popup', 'minutes': 180},
          {'method': 'popup', 'minutes': 720}
        ],
      },
    }
    print('testing...')
    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))
