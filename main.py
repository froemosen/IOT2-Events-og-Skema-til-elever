import time
import os
from datetime import datetime
import requests
import json


def getTime(currentTime): #Daglig send af skema og begivenheder
    global latestTime
    
    if currentTime.tm_hour == 7 and currentTime.tm_hour != latestTime: #Tal i første del er klokkeslæt hvor skema sendes
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
        try:
            if "Lokale:" in line:
                room = ", "+line.removeprefix("DESCRIPTION:").partition("-")[0]
        except: pass
        
        if "SUMMARY" in line: 
            try: #Prøv at tilføje lokale
                message = line.removeprefix("SUMMARY:").replace("\n", "")
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
        return True
    else:
        return False


def sendCalendar(Calendar): #Sender daglig kalender til IFTTT
    print("Sending Calendar...\n")
    print(Calendar) #Normalt format
    print("\n\n\n"+"{"+' '+":"+"<br>"+Calendar.replace('"','\'').replace("\n", "<br>")+"}"+"\n\n\n") #JSON-format
    r = requests.post('https://maker.ifttt.com/trigger/fest/json/with/key/bEOACrKudUx-DNoZ2icG0J', json={' ':"<br>"+Calendar.replace('"','\'').replace("\n", "<br>")}) #besked sendes til ifttt
    print(f"Response: {r}: {r.text}") #200 hvis modtaget
    

def timeToClear(unix):
    global lastClearTime
    if unix > lastClearTime+86400: #24 timer 
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
        try: currentCalendar = getCalendar() #Ny kalender hentes ind.
        except: print("NETWORK CONNECTION FAILED - Waiting another minute")
               
        #Hvis det er tid til daglige events
        if getTime(time.localtime(int(time.time()))): #Klokken er lige blevet 7 - send besked
            sendCalendar(currentCalendar)
            print("Daily message sent")
        else: #Det er ikke tid til at sende en daglig besked
            print("No daily message sent")
        
        
        #Hvis der er sket ændringer siden sidste tjek
        changeStatus = getChanges(currentCalendar, prevCalendar)
            
        if changeStatus:
            print("Sending new changes...")
            sendCalendar("**!!!CHANGES HAVE OCCURED IN TODAY'S PROGRAM!!!** \n"+currentCalendar)
        else:
            print("No changes comitted")   
            
        prevCalendar = currentCalendar
        print("\n")
        if timeToClear(int(time.time())): os.system("cls") #Der cleares én gang per døgn for at undgå spildt RAM.
        time.sleep(60) #Opdater ændringer hvert minut