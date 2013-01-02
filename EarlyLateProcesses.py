'''
Created on 30 déc. 2012

@author: Salah Benmoussati, Yassine Zenati
'''
from toolsCalculus import minStartTime, seqActivity

def earlyOrLateProcess(listActivities, projectRessources, late):
    """ Proceso adelanto or retraso, depending if late is True or not
        (late is True <=> proceso de retraso)
    """
    
    # Sort the list of activities by finish date time
    sortedList = sorted(listActivities, key=lambda activity: activity.startTime + activity.duration, reverse=late)
    
    #Initialisation of the tab of ressources
    
    maxProjectDuration = sum(act.duration for act in listActivities)
    tabRessources = [projectRessources] * maxProjectDuration
    
    for act in sortedList:
        # If we are processing retraso, the an activity has to be sequenced after its successors
        # Otherwise it's after its predecessors
        if late:
            minStartTime = minStartTime(act.successors)
        else:
            minStartTime = minStartTime(act.predecessors)
        seqActivity(act, minStartTime, tabRessources, late)
        
    # Update of the startTime field
    
    projectDuration = sortedList[-1].seq  + sortedList[-1].duration # project duration = last activity's end date
    
    if late:
        for act in listActivities:
            act.startTime = projectDuration - (act.seq + act.duration)
    else:
        for act in listActivities:
            act.startTime = act.seq
            