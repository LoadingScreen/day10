from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime
from datetime import timedelta
import random
import sys

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

interventions = [
["Avoid interrupting people"],
["Play smash bros. before doing anything else"],
["Stay in bed until getting up feels good"],
["Go to bed by 10"],
["Be less reserved in conversation"],
["Text a friend after eating", "Kill two birbs with 1 Stone!"],
["Shower talks", "they're so good man"],
["Eat few carbs"],
["5 hour feeding window"],
["Phone a friend for 30 minutes"]
]

# Put such an intervention in the calendar for 10 days
print('Adding a randomly selected intervention...')
intervention = interventions[random.randint(0,len(interventions))]
summary = intervention[0]
if len(sys.argv) > 1:
    delay = int(sys.argv[1])
else:
    delay = 0
for i in range(1,6):
    # startingDay = datetime.datetime.today() + timedelta(days=delay)
    startingDay = datetime.datetime.now().replace(hour=0, minute=0, second=0)

    event = {
      'summary': "Day %s/10: %s" %(i,summary),
      'description': intervention[-1],
      'start': {'dateTime':(startingDay+timedelta(days=i, hours=10)).isoformat()+'Z'},
      'end': {'dateTime': (startingDay+timedelta(
      days=i, hours=10, minutes=30)).isoformat()+"Z"},
      'reminders': {
        'useDefault': False,
        'overrides': [
          {'method': 'popup', 'minutes': 180},
          {'method': 'popup', 'minutes': 720}
        ],
      },
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))
