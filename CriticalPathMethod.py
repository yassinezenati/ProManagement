'''
Created on 30 dec. 2012

@author: Salah Benmoussati, Yassine Zenati
'''

import datetime

def criticalPathMethod(listActivities):
    """ CPM algorithm
    """
    
    # First step : order the activity
    listOrdenedAct = []
    for act in listActivities:
        if (not act in listOrdenedAct):
            listOrdenedAct.append(act)
        for pred in act.predecessors:
            if (pred in listOrdenedAct):
                if (listOrdenedAct.index(pred) > listOrdenedAct.index(act)):
                    listOrdenedAct.remove(pred)
                    listOrdenedAct.insert( listOrdenedAct.index(act), pred)
            else :
                listOrdenedAct.insert(listOrdenedAct.index(act), pred)
    
    # Second step : for each activity process its early start time 
    
    for act in listOrdenedAct:
        if (not (act.ident == -1)):
            maxDate = act.predecessors[0].duration + act.predecessors[0].EST
            for pred in act.predecessors[1:]: # We skip the first predecessors duration
                if (pred.EST + pred.duration > maxDate):
                    maxDate = pred.EST + pred.duration
            act.EST = maxDate        
    listActivities[-1].LST = listActivities[-1].EST
    
    # Third step : for each activity, process its late start time
    
    startDate = datetime.date.today() 
    currentDate=startDate + datetime.timedelta(days=1)
    
    if (currentDate.isoweekday()==6) : 
        currentDate=startDate + datetime.timedelta(days=2)
    if (currentDate.isoweekday()==7) : 
        currentDate=startDate + datetime.timedelta(days=1)

    listOrdenedAct.reverse() # Reverse the order of the list
    for act in listOrdenedAct:
        if (act.ident==-2) : 
            duration = act.EST
            print "Duration of the project : ", duration , "days"
            count=0
            while count < duration : 
                if (currentDate.isoweekday() == 5):
                    currentDate= currentDate + datetime.timedelta(days=3)
                else :
                    currentDate=currentDate + datetime.timedelta(days=1)
                count=count+1
                    
        if (not (act.ident == -2)):
            minDate = act.successors[0].LST - act.duration
            for suc in act.successors:
                if (suc.LST - act.duration < minDate):
                    minDate = suc.LST - act.duration
            act.LST = minDate
        
    print ("Starting of the project : "),
    print startDate 
    print ("Ending of the project : "), 
    print currentDate 
    
    for act in listActivities : 
        act.LFT = act.LST + act.duration
