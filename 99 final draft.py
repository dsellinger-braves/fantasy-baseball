# Add in flexibility for different audio in the first round

import pyautogui
import pyscreeze
import pygetwindow as gw
import datetime
import gspread
import datetime
import random
import time
from time import gmtime, strftime
from oauth2client.service_account import ServiceAccountCredentials

# Define the scope

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']



# Add credentials from the downloaded JSON file
creds = ServiceAccountCredentials.from_json_keyfile_name(r"C:\Users\danie\Documents\Fantasy Baseball\Python\linear-range-448102-c7-43679adbf0d5.json", scope) # Replace 'your_credentials.json'

# Authorize the clientsheet
client = gspread.authorize(creds)

# Get the instance of the Spreadsheet
sheet = client.open('2025 Keeper Kit').worksheet('Helper')
most_recent_message = 'placeholder'
time_remaining = ''
drafter = ''
prior_pick=''
current_pick = 51

#while int(current_pick) <=250:
while 1==1:
    key = sheet.acell('I22').value
    time_remaining, current_pick, drafter, prior_pick = key.split("_")

    try: 
        if int(time_remaining)>=60 and most_recent_message != ('?'+drafter): 
            time_remaining, current_pick, drafter, prior_pick = key.split("_")
            win = gw.getWindowsWithTitle('Discord')[0]
            win.activate()                
            pyautogui.press('tab')  
            pyautogui.write('?'+drafter)     
            pyautogui.press('enter') 
            most_recent_message = '?'+drafter
            print('over_85')
            print(most_recent_message)
            print(drafter)
            print(key)
            win = gw.getWindowsWithTitle('Visual')[0]
            win.activate() 
            time.sleep(1.1)
            
        if 0<int(time_remaining)<=10 and most_recent_message != '?Countdown':
            time_remaining, current_pick, drafter, prior_pick = key.split("_")
            win = gw.getWindowsWithTitle('Discord')[0]
            win.activate()  
            pyautogui.press('enter')      
            pyautogui.write('?Countdown')
            pyautogui.press('enter')
            most_recent_message = '?Countdown'
            win = gw.getWindowsWithTitle('Visual')[0]
            win.activate() 
            print('under_10')
            print(most_recent_message)

            print(key)
            time.sleep(1.1)
        else: 
            time.sleep(1.1)     
            print('else') 
            print(time_remaining)
            print(most_recent_message) 
            print(key)           
    except: 
            time.sleep(1.1)
            print('except')
            print(time_remaining)
            print(most_recent_message)
            print(key)