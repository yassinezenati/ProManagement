'''
Created on 11 nov. 2012

@author: yassine
'''
from PMFiles import PMFiles
import sys
from Activity import Activity


fileName = sys.argv[1]
listActivities = PMFiles.read(fileName)

def buildList(listAct):
    """ Add the start activity and end activity
    """
    listStart = []
    listActWithPred = [] #List of activities having at least predecessor
    start = Activity(-1, "start", listStart, 0, 0, -1, -1, None)
    start.EST = 0
    start.LST = 0
    end = Activity(-2, "end", None, 0, -1, -1, -1, None)
    for act in listAct:
        if (act.successors is None):
            act.successors = [end]
            end.predecessors.append(act)
        else:
            listActWithPred.extend(act.successors)
            for suc in act.successors: #adding predecessors
                suc.predecessors.append(act)
    for act in listAct:
        if (not act in listActWithPred):
            start.successors.append(act)
            act.predecessors.append(start)
            
    listAct.insert(0, start)
    listAct.append(end)


def criticalPathMethod(listActivities):
    """ CPM algorithm
    """
    
    listCriticalPath = []
    
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
    
    listOrdenedAct.reverse() # Reverse the order of the list
    for act in listOrdenedAct:
        if (not (act.ident == -2)):
            minDate = act.successors[0].LST - act.duration
            for suc in act.successors:
                if (suc.LST - act.duration < minDate):
                    minDate = suc.LST - act.duration
            act.LST = minDate
        if (act.EST == act.LST):
            listCriticalPath.append(act)
        
        
buildList(listActivities)
criticalPathMethod(listActivities)

print("########################################")
for act in listActivities:
    act.display()
