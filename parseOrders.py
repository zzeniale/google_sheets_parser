#!/usr/bin/env python3

# uses google sheets API

from __future__ import print_function
import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import pandas as pd
import numpy as np
import re
from collections import Counter
import sys

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

creds = None

# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first time.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()
spreadsheetID = ''
rangeName = 'responses!A4:K'

result = sheet.values().get(spreadsheetId=spreadsheetID,
                            range=rangeName).execute()
values = result['values'] 

flavours = []
total = []
collect = []
names = []
address = []
contact = []

for row in values:
    flavours.append(row[10])
    total.append(row[4])
    collect.append(row[2])
    names.append(row[5])
    address.append(row[3])
    contact.append(row[9])

flavourMap = {'1':'D',
              '2':'DS',
              '3':'M'}

# extract number of flavours and boxes per person
allBoxes = pd.DataFrame()
allFlavours = pd.DataFrame()
for entryVal in flavours:
    entryVal = entryVal.lower()                  # clean 1: make lowercase
    entryVal = entryVal.replace(' ','')          # clean 2: remove all spaces    # look for flavour numbers in the entered value
    orders = re.findall(r":\d+", entryVal)       # find flavour numbers
    orders = [x.split(':')[1] for x in orders]   # remove colons

    # convert flavour numbers into flavours
    boxes = {}
    flavours = []
    for ind, eachBox in enumerate(orders):
        eachBox = list(eachBox)                  # separate flavour numbers in each box 
        for key in flavourMap:                   # replace numbers with flavour names
            eachBox = [x.replace(key, flavourMap[key]) for x in eachBox]
        flavours.extend(eachBox)                 # get count of flavours in each order
        boxes[f'box{ind+1}'] = eachBox
    
    allBoxes = allBoxes.append(boxes, ignore_index=True)
    allFlavours = allFlavours.append(Counter(flavours), ignore_index=True)

# flavours
output = pd.merge(allFlavours, allBoxes, left_index=True, right_index=True)

# name
output['name'] = names

# mobile
output['contact'] = contact

# cost without delivery
output['subtotal'] = [float(x.split(' - $')[1]) for x in total]

# delivery methods: self collection, mail, delivery
deliveryCost = [x.split('+ $')[-1].split(')')[0] for x in collect]
deliveryCost = [int(x) if x[0] != 'C' else 0 for x in deliveryCost]
output['deliveryCost'] = deliveryCost
output['grandTotal'] = output.subtotal + output.deliveryCost

# address
output['address'] = [x.replace('\n',' ') if type(x) != float else '-' for x in address]

output.fillna(0, inplace=True)

# save out csv
output.to_csv('/Users/test/Desktop/orders_parsed.csv')