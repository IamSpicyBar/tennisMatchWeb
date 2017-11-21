from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents = [tools.argparser]).parse_args()
except ImportError:
    flags = None

from apiclient import errors
import base64
import time
from email.mime.text import MIMEText

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://mail.google.com/'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


def getCredentials():
    """
    Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def launchService():
    credentials = getCredentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http = http)

    # results = service.users().labels().list(userId = 'me').execute()
    # labels = results.get('labels', [])

    # if not labels:
    #     print('No labels found.')
    # else:
    #     print('Labels:')
    #     for label in labels:
    #         print(label['name'])

    return service

def fakeRequests():
    outstandingRequests = {}

    maleNames =   ['Bradley Evans',      'James Dean',        'Harrison Richards', \
                   'Alfie May',          'Evan Young',        'Max Mayer',         \
                   'Solomon Wood',       'Jael Bonner',       'Deacon Powers',     \
                   'Jeffery Gray',       'Michael Henderson', 'Reece Foster',      \
                   'Cameron Lloyd',      'Joshua Fraser',     'Ellis Atkinson',    \
                   'Jamari Kramer',      'Dexter Heath',      'Aldo Matthews',     \
                   'Robert Young',       'Charles Cole',      'Gabriel Rogers',    \
                   'Ollie Mills',        'Jenson Cook',       'Grayson Riley',     \
                   'Alfred Cardenas',    'Patrick Booth',     'Moises Alford',     \
                   'Charlie Valentine',  'Riley Ryan',        'Sean Taylor',       \
                   'Riley Ball',         'Frederick Palmer',  'Aidan West',        \
                   'Fernando Wilkinson', 'Briggs Powers',     'Bruno Chaney']

    femaleNames = ['Yasmin Lewis',       'Phoebe Richardson', 'Libby Thompson',    \
                   'Lucy Marsh',         'Harriet Read',      'Samiyah Nash',      \
                   'Karsyn Larsen',      'Madison Marshall',  'Scarlet Dillon',    \
                   'Jewel Vazquez',      'Hollie Mason',      'Lucy Wallace',      \
                   'Victoria Booth',     'Willow Ross',       'Matilda Fraser',    \
                   'Mackenzie Warner',   'Greta Pennington',  'Michaela Callahan', \
                   'Giana Conrad',       'Emelia Buchanan',   'Chloe Howard',      \
                   'Maria Andrews',      'Martha Hart',       'Grace John',        \
                   'Ellie Wilkinson',    'Zaria Larsen',      'Jolene Mayo',       \
                   'Natalya Dillard',    'Carley Stokes',     'Danika O\'neal',    \
                   'Sophia Lowe',        'Niamh Chambers',    'Lydia Lane',        \
                   'Sienna Cox',         'Jodie Parker',      'Maeve Stanton']

    maleCount = 0
    femaleCount = 0
    phone = 7340000001
    ID = 748596123
    t = time.localtime(time.time())
    month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    for i in range(0, 2):
        for gender in ['Male', 'Female']:
            for age in ['10-15', '16-20', '21-25', '26-30', '31-40', '41 or above']:
                for level in ['Beginner', 'Intermediate', 'Advanced']:
                    request = {}
                    request['Gender'] = gender
                    if gender == 'Male':
                        request['Name'] = maleNames[maleCount]
                        maleCount += 1
                    else:
                        request['Name'] = femaleNames[femaleCount]
                        femaleCount += 1
                    request['Age'] = age
                    request['Level'] = level
                    request['Email'] = 'h.mercury.g.2730@gmail.com'
                    request['Phone'] = str(phone)
                    request['Time'] = 'Monday Tuesday Wednesday Thursday Friday Saturday Sunday'
                    request['P_Age'] = '10-15 16-20 21-25 26-30 31-40 41 or above'
                    request['P_Gender'] = 'Male Female'
                    request['P_Level'] = 'Beginner Intermediate Advanced'
                    request['ID'] = ID
                    request['Date'] = month[t[1] - 1] + ' ' + str(t[2]) + ', ' + str(t[0])
                    request['Year_Day'] = t[7]
                    outstandingRequests[ID] = request
                    phone += 1
                    ID += 1

    return outstandingRequests

def listMessagesMatchingQuery(service, user_id, query = ''):
    """
    List all Messages of the user's mailbox matching the query.

    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value 'me'
      can be used to indicate the authenticated user.
      query: String used to filter messages returned.
      Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

    Returns:
      List of Messages that match the criteria of the query. Note that the
      returned list contains Message IDs, you must use get with the
      appropriate ID to get the details of a Message.
    """
    try:
        response = service.users().messages().list(userId = user_id, q = query).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])
        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId = user_id, q = query, pageToken = page_token).execute()
            messages.extend(response['messages'])
        return messages
    except errors.HttpError, error:
        print('An error occurred: %s' % error)

def getMimeMessage(service, userID, msgID):
    """
    Get a Message and use it to create a MIME Message.

    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value 'me'
      can be used to indicate the authenticated user.
      msg_id: The ID of the Message required.

    Returns:
      A MIME Message, consisting of data from Message.
    """
    try:
        message = service.users().messages().get(userId = userID, id = msgID, format = 'raw').execute()
        msgStr = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
        return msgStr

    except errors.HttpError, error:
        print ('An error occurred: %s' % error)

def markAsRead(service, userID, msgID):
    msgLabels = {'removeLabelIds': ['UNREAD'], 'addLabelIds': []}
    service.users().messages().modify(userId = userID, id = msgID, body = msgLabels).execute()

def parseMessage(msgStr):
    idx1 = msgStr.find('Your form has a new entry.')
    idx2 = msgStr.find('Finished.')
    str = msgStr[(idx1 + 28) : (idx2 - 1)]
    strArr = str.splitlines()
    request = {}
    for line in strArr:
        if line.startswith('Name'):
            request['Name'] = line[6 : ]
            print('Name: ' + request['Name'])
        elif line.startswith('Age'):
            request['Age'] = line[5 : ]
            print('Age: ' + request['Age'])
        elif line.startswith('Gender'):
            request['Gender'] = line[8 : ]
            print('Gender: ' + request['Gender'])
        elif line.startswith('Level'):
            request['Level'] = line[7 : ]
            print('Level: ' + request['Level'])
        elif line.startswith('Email'):
            request['Email'] = line[7 : ]
            print('Email: ' + request['Email'])
        elif line.startswith('Phone number'):
            request['Phone'] = line[14 : ]
            print('Phone: ' + request['Phone'])
        elif line.startswith('Time to play'):
            request['Time'] = line[14 : ]
            print('Time to play: ' + request['Time'])
        elif line.startswith('Partner\'s age'):
            request['P_Age'] = line[15 : ]
            print('Partner\'s age: ' + request['P_Age'])
        elif line.startswith('Partner\'s gender'):
            request['P_Gender'] = line[18 : ]
            print('Partner\'s gender: ' + request['P_Gender'])
        elif line.startswith('Partner\'s level'):
            request['P_Level'] = line[17 : ]
            print('Partner\'s level: ' + request['P_Level'])
        elif line.startswith('Response ID'):
            request['ID'] = line[13 : ]
            print('Response ID: ' + request['ID'])
        elif line.startswith('Response Date'):
            request['Date'] = line[15 : ]
            print('Response Date: ' + request['Date'])
    localTime = time.localtime(time.time())
    request['Year_Day'] = localTime[7];

    return request

def checkInbox(service):
    messages = listMessagesMatchingQuery(service, 'me', 'from:entr550.annarbor.tennis@gmail.com is:unread')
    requests = []
    for msg in messages:
        print("*** New request:")
        msgStr = getMimeMessage(service, 'me', msg['id'])
        markAsRead(service, 'me', msg['id'])
        request = parseMessage(msgStr)
        duplicate = False 
        for req in requests:
            if (request['ID'] == req['ID']):
                duplicate = True
                break
        if (not duplicate):
            requests.append(request)
    return requests

def findMatch(newRequest, outstandingRequests):
    times = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for ID, prevRequest in outstandingRequests.iteritems():
        if (ID == newRequest['ID']):
            continue
        commonTime = {}
        timeMatch = False
        for time in times:
            if ((prevRequest['Time'].find(time) >= 0) and (newRequest['Time'].find(time) >= 0)):
                commonTime[time] = True
                timeMatch = True
            else:
                commonTime[time] = False

        if (timeMatch                                                and \
           (prevRequest['P_Age'].find(newRequest['Age']) >= 0)       and \
           (prevRequest['P_Gender'].find(newRequest['Gender']) >= 0) and \
           (prevRequest['P_Level'].find(newRequest['Level']) >= 0)   and \
           (newRequest['P_Age'].find(prevRequest['Age']) >= 0)       and \
           (newRequest['P_Gender'].find(prevRequest['Gender']) >= 0) and \
           (newRequest['P_Level'].find(prevRequest['Level']) >= 0)):
            print('*** Match found: ' + prevRequest['Name'])
            return [prevRequest, commonTime]

    print('*** No match found')
    return 0

def sendEmail(request, matchInfo, service):
    prevRequest = matchInfo[0]
    commonTime = matchInfo[1]
    
    messageText = 'Hi ' + request['Name'] + ' and ' + prevRequest['Name'] + '!\n'
    messageText += '\nBased on your preferences, we found out that you could play tennis together this week at the following day(s):\n'
    times = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for time in times:
        if commonTime[time]:
            messageText += time + '\n'
    messageText += '\nYou could either play at COURT_A, COURT_B, or COURT_C.\n\n'
    messageText += 'Your contact info:\n'
    messageText += request['Name'] + ': ' + request['Email'] + ', ' + request['Phone'] + '\n'
    messageText += prevRequest['Name'] + ': ' + prevRequest['Email'] + ', ' + prevRequest['Phone'] + '\n\n'
    messageText += 'Have fun!\n'

    message = MIMEText(messageText)
    message['to'] = request['Email'] + ',' + prevRequest['Email']
    message['from'] = 'entr550.annarbor.tennis@gmail.com'
    message['subject'] = 'Ann Arbor Tennis'
    message = {'raw': base64.urlsafe_b64encode(message.as_string())}

    try:
        message = (service.users().messages().send(userId = 'me', body = message).execute())
    except errors.HttpError, error:
        print ('An error occurred: %s' % error)

def main():
    service = launchService()
    CHECK_INTERVAL = 60
    outstandingRequests = fakeRequests()
    # outstandingRequests = {}

    while True:
        # Check if new requests are made:
        newRequests = checkInbox(service)

        # See if matches could be found:
        for request in newRequests:
            requestUpdated = False
            # Check if this is a new request or an updated request:
            if outstandingRequests.has_key(request['ID']):
                outstandingRequests[request['ID']] = request
                requestUpdated = True
            matchInfo = findMatch(request, outstandingRequests)
            if matchInfo:
                sendEmail(request, matchInfo, service)
                del outstandingRequests[matchInfo[0]['ID']]
                if requestUpdated:
                    del outstandingRequests[request['ID']]
            else:
                outstandingRequests[request['ID']] = request

        # Every midnight, expire requests which are 7 days old:
        localTime = time.localtime(time.time())
        if ((localTime[3] == 0) and (localTime[4] < (1 + CHECK_INTERVAL / 60))):
            tempRequests = outstandingRequests.copy()
            for ID, request in outstandingRequests.iteritems():
                deltaDay = localTime[7] - request['Year_Day']
                if (deltaDay < 0):
                    deltaDay += 365
                if (deltaDay > 7):
                    del tempRequests[ID]
            outstandingRequests = tempRequests

        print('*** Outstanding requests: ' + str(len(outstandingRequests)))
        print('*****************************************************************************')
        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    main()
