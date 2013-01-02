'''
Created on 2 janv. 2013

@author: Salah Benmoussati, Yassine Zenati
'''
from toolsCalculus import addRes, minusRes

def resourceLeveling(listActivities, listNonCriticalAct, projectDuration):
    
    nbResources = len(listActivities[1].resources) 
    
    # Build a table of resources per day 
    
    listResources = [[0] * nbResources] * projectDuration
    
    for act in listActivities:
        for i in range(act.startTime, act.startTime + act.duration):
            listResources[i] = addRes(act.resources, listResources[i])
    
    listSum = [0] * nbResources
    listLen = [projectDuration] * nbResources
    # Process the average of each resource
    for day in listResources:
        for cpt, res in enumerate(day):
            listSum[cpt] = listSum[cpt] + res
    
    listAvg = [(float(x)/ y) for x, y in zip(listSum, listLen)]
    
    # Build a table of var
    for day in listResources:
        for cpt, res in enumerate(day):
    
    # Sort the activities by finishing time
    sortedNCA = sorted(listNonCriticalAct, key=lambda activity: activity.startTime + activity.duration, reverse=True)
    
    for act in sortedNCA:
        endTimeAct = act.startTime + act.duration # Finalisation of the activity
        
        # Process of the total float (holgura libre)
        totalFloat = act.successors[0].startTime - endTimeAct
        for suc in act.successors[1:]:
            if suc.startTime - endTimeAct < totalFloat:
                totalFloat = suc.startTime - endTimeAct
                
        