'''
Created on 30 dec. 2012

@author: Salah Benmoussati, Yassine Zenati
'''
from toolsCalculus import minStartTime, seqActivity

def earlyOrLateProcess(listActivities, projectresources, late):
    """ Proceso adelanto or retraso, depending if late is True or not
        (late is True <=> proceso de retraso)
    """
    
    # Sort the list of activities by finish date time
    sortedList = sorted(listActivities, key=lambda activity: activity.startTime + activity.duration, reverse=late)
    
    #Initialisation of the tab of resources
    
    maxProjectDuration = sum(act.duration for act in listActivities)
    tabresources = [projectresources] * maxProjectDuration
    
    for act in sortedList:
        # We don't want to process the startActivity nor the end Activity
        if act.ident == -1 or act.ident == -2:
            continue
        
        # If we are processing retraso, the an activity has to be sequenced after its successors
        # Otherwise it's after its predecessors
        minST = 0 # We have to initialize this variable
        if late:
            minST = minStartTime(act.successors)
        else:
            minST = minStartTime(act.predecessors)
        seqActivity(act, minST, tabresources)
    # Update of the startTime field
    
    if late:
        projectDuration = sortedList[-3].seq  + sortedList[-3].duration # project duration = first activity's seq + duration
        for act in listActivities:
            if not act.ident == -1:
                act.startTime = projectDuration - (act.seq + act.duration)
    else:
        projectDuration = sortedList[-1].seq  + sortedList[-1].duration
        for act in listActivities:
            if not act.ident == -1:
                act.startTime = act.seq
                act.seq = 0
        