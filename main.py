import time

def getChanges():
    pass

def getTime(): #Daglig send af skema og begivenheder
    pass

def getCalendar():
    pass


if __name__ == '__main__':
    while True:
        getCalendar() #Ny kalender hentes ind.
        
        changeStatus, changes = getChanges()
        
        if getTime():
            pass
        
        
        
        time.sleep(60) #Opdater ændringer ~hvert minut

