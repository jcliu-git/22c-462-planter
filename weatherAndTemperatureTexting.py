from bs4 import BeautifulSoup
import requests
import os
from twilio.rest import Client

# College Station info
# "id": 4682464,
#         "name": "College Station",
#         "state": "TX",
#         "country": "US",
#         "coord": {
#             "lon": -96.334412,
#             "lat": 30.627979
#         }

# URL = r"https://www.wunderground.com/precipitation/us/tx/college-station?cm_ven=localwx_modprecip"
# APIURL = r"https://api.openweathermap.org/data/2.5/weather?q=college%20Station&appid=788b67304f5503442959c61cd1f122af&units=imperial"
# APIURL5day3hourXML = r"https://api.openweathermap.org/data/2.5/forecast?lat=30.627979&lon=-96.334412&appid=788b67304f5503442959c61cd1f122af&units=imperial&mode=xml"
# r = requests.get(APIURL)
# content = BeautifulSoup(r.content)
# # print(content)
# # print(soup.prettify())
# content = str(content)
# # Weather part
# weatherIndex1 = content.find("[")
# weatherIndex2 = content.find("]")
# weather = content[weatherIndex1 + 2:weatherIndex2 - 1].split(",")
# print(weather)
# weatherDescription = weather[2][weather[2].find(":") + 2:-1]
# print(weatherDescription)

# Temperature Part
APIURL5day3hourXML = r"https://api.openweathermap.org/data/2.5/forecast?lat=30.627979&lon=-96.334412&appid=788b67304f5503442959c61cd1f122af&units=imperial&mode=xml"
r = requests.get(APIURL5day3hourXML)
content = BeautifulSoup(r.content)

bigSection = content.findAll('time')
# print(bigSection)
times = []
weathers = []
temperatures = []
for element in bigSection:
    tempElement = str(element)
    timeIndex1 = tempElement.find("from") + 6
    timeIndex2 = tempElement[timeIndex1:].find('"') + timeIndex1
    time = tempElement[timeIndex1:timeIndex2]
    # print(time)
    times.append(time)

    s = str(element.find("symbol"))
    # print(t)
    weatherIndex1 = s.find("name") + 6
    weatherIndex2 = s[weatherIndex1:].find('"') + weatherIndex1
    weather = s[weatherIndex1:weatherIndex2]
    print(weather)
    weathers.append(weather)

    t = str(element.find("temperature"))
    # print(t)
    tempIndex1 = t.find("value") + 7
    tempIndex2 = t[tempIndex1:].find('"') + tempIndex1
    temperature = t[tempIndex1:tempIndex2]
    # print(temperature)
    temperatures.append(float(temperature))
txtMsg = ""
previouslyCold = False
previouslyHot = False
for temp in range(len(temperatures)):
    currentTime = " ".join(times[temp].split("T"))
    if temperatures[temp] < 50 and not previouslyCold:
        txtMsg += f" It's going to start being cold at {currentTime} with temperatures like {temperatures[temp]}ºF"
        previouslyCold = True
    elif temperatures[temp] < 50 and previouslyCold:
        txtMsg += f", {temperatures[temp]}ºF"
    elif previouslyCold and temperatures[temp] >= 50:
        txtMsg += f" and ends being cold at {currentTime}."
        previouslyCold = False
    if temperatures[temp] > 90 and not previouslyHot:
        txtMsg += f" It's going to start being hot at {currentTime} specifically {temperatures[temp]}ºF"
        previouslyHot = True
    elif temperatures[temp] > 90 and previouslyHot:
        txtMsg += f", {temperatures[temp]}ºF"
    elif previouslyHot and temperatures[temp] <= 90:
        txtMsg += f" and ends being hot at {currentTime}."
        previouslyHot = False

previouslyStormy = False
previouslyRainy = False
txtMsg += "\n"
for i in range(len(weathers)):
    currentTime = " ".join(times[i].split("T"))
    if ("rain" in weathers[i]) and not previouslyRainy:
        txtMsg += f" It's going to start {weathers[i]} at {currentTime}"
        previouslyRainy = True
    elif not ("rain" in weathers[i]) and previouslyRainy:
        txtMsg += f" and end at {currentTime}."
        previouslyRainy = False
    if "storm" in weathers[i] and not previouslyStormy:
        txtMsg += f" It's going to start {weathers[i]} at {currentTime}"
        previouslyStormy = True
    elif not ("storm" in weathers[i]) and previouslyStormy:
        txtMsg += f" and end at {currentTime}."
        previouslyStormy = False

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
if txtMsg:
    print(txtMsg)
    account_sid = os.environ['TWILIO_ACCOUNT_SID'] = 'ACbd59276b1fca8fa84dbcf3805586d2d5'
    auth_token = os.environ['TWILIO_AUTH_TOKEN'] = '6b265b1b3becfaa7ccf997821775525c'
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                         body=txtMsg,
                         from_='+18318300211',
                         to='+15129175550'
                     )

    print(message.sid)

'''
bigSection = soup.find('lib-precipitation-graph')
spans = bigSection.findAll('span')
print(spans)

for element in spans:
    print(type(element))
    print(element['class'])
    if "statement-text" in element['class']:
        print("found it!!!!!!!!!!", element.text)
'''
