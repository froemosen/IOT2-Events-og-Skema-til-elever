import time
import os
from datetime import datetime
import requests
import json


def getTime(currentTime): #Daglig send af skema og begivenheder
    global latestTime
    
    if currentTime.tm_hour == 8 and currentTime.tm_hour != latestTime:
        latestTime = currentTime.tm_hour
        return True
    else: 
        latestTime = currentTime.tm_hour
        return False
    
    
def getCalendar(): #Skaffer kalender fra delt outlook-kalender
    #Get new calendar
    url = 'https://outlook.office365.com/owa/calendar/a19df33077b54a79be1081a918a9bb9d@edu.aarhustech.dk/71c83e977f364dbdbceb38dac8215c3417612726230718974412/calendar.ics'
    r = requests.get(url, allow_redirects=True)
    open('calendar.ics', 'wb').write(r.content)
    
    messageFound = False
    planFound = False
    dayPlan = ""
    # read the data from the file    
    with open('calendar.ics', 'rt') as f:
        data = f.readlines()
    
    for line in data:
        if "Lokale:" in line:
            room = ", "+line.removeprefix("DESCRIPTION:").partition("-")[0]
        
        if "SUMMARY" in line: 
            try: #Prøv at tilføje lokale
                message = line.removeprefix("SUMMARY:").replace("\n", "")
                message += room
                if len(room)<15: message += room
                messageFound = True
            except: #Hvis ikke lokale er fastsat 
                message = line.removeprefix("SUMMARY:").replace("\n", "")
                messageFound = True
            
        if "DTSTART" in line and messageFound: 
            date = line.removeprefix("DTSTART;TZID=Romance Standard Time:")
            date = date[:-3]
            #print(message)
            #print(date)
            if date[:-5] == str(datetime.today()).split()[0].replace("-", ""):
                #Format time and day
                oldformatDay = date[:-5]
                datetimeobjectDay = datetime.strptime(oldformatDay,'%Y%m%d')
                newformatDay = datetimeobjectDay.strftime('%d-%m-%Y')
                time = date[9:11] + ":" + date[11:13]          
                date = "**_"+time+"_**"+"᲼-᲼"+newformatDay
                
                #Format final message
                dayPlan += message+"\n"+date+"\n\n"
                
                #End operation
                messageFound = False
                planFound = True
                room = ""
            else: pass
                
    if planFound:
        try: return dayPlan
        except: return dayPlan
        
            
            
def getChanges(currentCalendar, prevCalendar): #Tjekker efter ændringer i kalender
    if currentCalendar != prevCalendar:
        print("Changes have happened")
        newChanges = "Some change"
        
        return True, newChanges
    
    else:
        return False, 0


def sendCalendar(Calendar): #Sender daglig kalender til IFTTT
    print("Sending Calendar...\n")
    print(Calendar)
    toSend = json.dumps({'data':Calendar.replace('"','\'')})
    print("\n\n\n"+toSend+"\n\n\n")
    r = requests.post('https://maker.ifttt.com/trigger/fest/json/with/key/bEOACrKudUx-DNoZ2icG0J', json={' ':"<br>"+Calendar.replace('"','\'').replace("\n", "<br>")}) #date=toSend
    print(f"Response: {r}: {r.text}")


def timeToClear(unix):
    global lastClearTime
    
    if unix > lastClearTime+86400: 
        lastClearTime = unix
        return True
    else: 
        return False
    


if __name__ == '__main__':
    prevCalendar = getCalendar()
    latestTime = 0
    lastClearTime = int(time.time())
        
    
    while True:
        print(f"Current time: {time.ctime(int(time.time()))}")
        currentCalendar = getCalendar() #Ny kalender hentes ind.
               
        #Hvis det er tid til daglige events
        if getTime(time.localtime(int(time.time()))): #Klokken er lige blevet 7 - send besked
            sendCalendar(currentCalendar)
            print("Daily message sent")
        else: #Det er ikke tid til at sende en daglig besked
            print("No daily message sent")
        
        
        #Hvis der er sket ændringer siden sidste tjek
        changeStatus, changes = getChanges(currentCalendar, prevCalendar)
            
        if changeStatus:
            pass
        else:
            print("No changes comitted")    
            
        prevCalendar = currentCalendar
        print("\n")
        if timeToClear(int(time.time())): os.system("cls")
        time.sleep(60) #Opdater ændringer hvert minut