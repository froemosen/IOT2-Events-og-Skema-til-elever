import time
import os



def getTime(currentTime): #Daglig send af skema og begivenheder
    global latestTime
    
    if currentTime.tm_hour == 7 and currentTime.tm_hour != latestTime:
        latestTime = currentTime.tm_hour
        return True
    else: 
        latestTime = currentTime.tm_hour
        return False
    
    
def getCalendar(): #Skaffer kalender fra delt outlook-kalender
    # read the data from the file
    with open('calendar.ics', 'rt') as f:
        data = f.readlines()
    
    for line in data:
        if "SUMMARY" in line and newTime: 
            print(line)
            newTime = False
        elif "DTSTART" in line: 
            date = line.removeprefix("DTSTART;TZID=Romance Standard Time:")
            date = date[:-3]
            print(date)
            print("\n")
            newTime = True
        
        
        

def getChanges(currentCalendar, prevCalendar): #Tjekker efter ændringer i kalender
    if currentCalendar != prevCalendar:
        print("Changes have happened")
        newChanges = "Some change"
        
        return True, newChanges
    
    else:
        return False, 0


def sendCalendar(Calendar): #Sender daglig kalender til IFTTT
    print(Calendar)

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

