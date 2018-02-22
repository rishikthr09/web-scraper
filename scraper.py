import urllib2
import requests
import difflib
import sys
import notify2
import os.path
import time
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

max_string_limit = 1000
start_delimiter = "^"
end_delimiter = "$"
notification_timeout = 10000



# path to notification window icon
ICON_PATH = os.path.abspath("resources/notify.png")
 
# initialise the d-bus connection
notify2.init("New item notification")
# create Notification object
n = notify2.Notification(None, icon = ICON_PATH)
# set urgency level
n.set_urgency(notify2.URGENCY_NORMAL)
# set timeout for a notification
n.set_timeout(notification_timeout)



def load_settings():
    settings_file = open('settings','r')
    settings = settings_file.readlines()
    if len(settings)!=2:
        print '"settings" file expected containing "url" and "text"'
        sys.exit(1)
    return settings



def load_properties():
    try:
        properties_file = open('properties.yaml','r')
        for line in properties_file.readlines():
            if "max_string_limit" in line:
                max_string_limit = int(line[:-1].split(':')[1].strip())
    except:
        pass
    


def find_in_children(current_object, text, temp_file):
    for child in list(current_object.find_all()):
        try:
            if text in child.string:
                if(len(child.string.encode('utf-8').strip()) < max_string_limit):
                    temp_file.write(child.getText().encode('utf-8').strip()+"\n")
            else:
                find_in_children(child, text, temp_file)
        except:
            pass



load_properties()

settings = load_settings()
url = settings[0][:-1]
text = settings[1][:-1]


page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')


temp_file = open('cache/tempFile','w')
find_in_children(soup, text, temp_file)
temp_file.close()

if(os.path.exists('cache/originalFile')):
    original_file = open('cache/originalFile','r')
    temp_file = open('cache/tempFile','r')
    diff = difflib.ndiff(original_file.readlines(), temp_file.readlines())
    original_file.close()
    temp_file.close()

    for item in diff:
        if(item[0]!='+'):
            continue
        n.update("WebScraper - New item added", item[2:-1].strip())
        n.show()
        time.sleep(15)
    temp_file.close()
    original_file.close()
else:
    temp_file = open('cache/tempFile','r')
    print "********************************"
    print "Found these items on initial run"
    print "********************************"
    for line in temp_file:
        print line[:-1]
    print "********************************"
    temp_file.close()

original_file = open('cache/originalFile','w')
temp_file = open('cache/tempFile','r')
for line in temp_file.readlines():
    original_file.write(line)
original_file.close()
temp_file.close()
