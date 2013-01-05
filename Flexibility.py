'''
Created on 2 janv. 2013

@author: Salah Benmoussati, Yassine Zenati
'''

from toolsCalculus import totalFloatEarly, totalFloatLate, addRes, projectDuration
from ResourceLeveling import buildNewResourceList

def analyseActivity(listActivities, act, projectResources):
    
    projectDur = projectDuration(listActivities)
    
    # Build a table of resources per day 
    
    nbResources = len(listActivities[1].resources)
    listResources = [[0] * nbResources] * projectDur
    
    for activitiy in listActivities:
        if (activitiy.ident == -1 or activitiy.ident == -2):
            continue
        for i in range(activitiy.startTime, activitiy.startTime + activitiy.duration):
            listResources[i] = addRes(activitiy.resources, listResources[i])
            
                    
        
    listDelays = []
    print "The activity " + act.name + " is supposed to start the day " + str(act.startTime)
    
    # Processing the total float for each side
    totalRightFloat = totalFloatLate(act, projectDur)
    totalLeftFloat = totalFloatEarly(act)
    print "float on the left = " + str(totalLeftFloat) 
    print "float on the right = " + str(totalRightFloat)
    
    # We ask the user if he wants to move the activity on the right or 
    # on the left
    
    while (True):
        answer = raw_input("Do you want to move the activity on the right or on the left (L/R):")
        if answer == "R" or answer == "L":
            break    
    if answer == "L":
        listSeqLeft = [] # List of possible sequenciation
        
        # For each potentiel position, we build a new list of resources 
        # if the building returns None, it means that this position 
        # overuse the resources of the project resources
        for i in range(act.startTime - totalLeftFloat, act.startTime):
            newResList = buildNewResourceList(listResources, act, i, projectResources)
            if not newResList is None:
                listSeqLeft.append(i)
        if len(listSeqLeft) == 0:
            print "Sorry you can't delay this activity on the left with the actual resources"
            return 
        else: 
            print "These are the delays on the left available"
            for newDate in listSeqLeft:
                print str(act.startTime - newDate) + " days"
                listDelays.append(act.startTime - newDate)
        while True:
            newSeq = input("type the delay that satisfies you (integer) : ")
            if newSeq in listDelays:
                act.startTime = newSeq
                break
    else:            
        listSeqRight = [] # List of posible sequenciation
        for i in range(act.startTime + 1, act.startTime + totalRightFloat + 1):
            newResList = buildNewResourceList(listResources, act, i, projectResources)
            if not newResList is None:
                listSeqRight.append(i)
        if len(listSeqRight) == 0:
            print "Sorry you can't delay this activity on the right with the actual resources"
            return 
        else: 
            print "These are the delays on the right available"
            for newDate in listSeqRight:
                print str(newDate - act.startTime) + " days" 
                listDelays.append(newDate - act.startTime)
        while True:
            newSeq = input("type the delay that satisfies you (integer) : ")
            if newSeq in listDelays:
                act.startTime = newSeq
                break

    