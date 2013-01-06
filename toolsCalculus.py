'''
Created on 31 dec. 2012

@author: Salah Benmoussati, Yassine Zenati

This file provides functions useful for the algorithms 
'''
from Activity import Activity

def buildList(listAct):
    """ Add the start activity and end activity
    """
    listStart = []
    listActWithPred = [] #List of activities having at least predecessor
    start = Activity(-1, "start", listStart, 0, None)
    start.EST = 0
    start.LST = 0
    start.LFT = 0
    end = Activity(-2, "end", None, 0, None)
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

def minStartTime(listAct):
    """ This function processes the minimum date an activity can start given the sequencing 
        of its predecessors or successors (depending if we are doing "adelanto" or "retraso")
        The param listAct is the list of the activity's pred or succ..
    """
    maxAct = max(listAct, key=lambda activity: activity.seq + activity.duration)
    return maxAct.seq + maxAct.duration 

def isSeq(act, resources):
    """ return true if the activity's resources are less or equal than the resources given in parameter  
    """
    ok = True 
    count = 0
    while (count < len(resources) and ok):
        ok = act.resources[count] <= resources[count]
        count += 1
    return ok
        
def minusRes(res1, res2):
    """ Process the the operation res = res1 - res2
        res, res1 and res2 being lists of resources
    """
    return [(x - y) for x, y in zip(res1, res2)]

def addRes(res1, res2):
    """ Process the the operation res = res1 +  res2
        res, res1 and res2 being lists of resources
    """
    return [(x + y) for x, y in zip(res1, res2)]
            
def overUseRes(res1, res2):
    """ Evaluate if at least one resource of res1 exceed 
        its equivalent in res2
    """
    
    for i in range(len(res1)):
        if res1[i] > res2[i]:
            return True
    return False
    
def seqActivity(act, minStartTime, tabresources):
    """ This function sequences the activity :
            1. finds the first day with enough resources so that we can sequence the activity 
            2. Update the seq field of the Activity
            3. Update the list of resources
    """
    
    count = minStartTime
    for listRes in tabresources[minStartTime:]: 
        if isSeq(act, listRes):
            act.seq = count # Update of the startTime
            for cpt, res in enumerate(tabresources[count:count+act.duration]):
                res = minusRes(res, act.resources)
                tabresources[count + cpt] = res
            break
        count += 1
        
def find_all_paths(act, path=[]):
        path = path + [act]
        if act.ident == -2:
            return [path]
        paths = []
        for suc in act.successors:
            if suc not in path:
                newpaths = find_all_paths(suc, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths
    
def projectDuration(listActivities):
    """ Process the duration of the project
    """
    lastAct = max(listActivities, key=lambda activity: activity.startTime)
    return lastAct.startTime + lastAct.duration
    
def findNonCriticalAct(listActivities):
    """ Returns non critical activities and write in projectDuration the duration of the project
    """    
    # Find all paths and critical paths
    
    listPaths = find_all_paths(listActivities[0])
    listDurations = []
    for cpt, path in enumerate(listPaths):
        listDurations.append(sum(act.duration for act in path))
    projectDuration = max(listDurations)
    listCriticalPaths = []
    for cpt, path in enumerate(listPaths):
        if listDurations[cpt] == projectDuration:
            listCriticalPaths.append(path)
    listNonCritActs = []
    for act in listActivities:
        if act not in sum(listCriticalPaths, []):
            listNonCritActs.append(act)
    return listNonCritActs

def totalFloatLate(act, projectDuration):
    """ Process the late total float (holgura total de retraso) of an activity
    """
    endTimeAct = act.startTime + act.duration

    if act.successors[0].ident == -2:
        totalFloat = projectDuration - endTimeAct
    else:  
        totalFloat = act.successors[0].startTime - endTimeAct
        for suc in act.successors[1:]:
            if suc.startTime - endTimeAct < totalFloat:
                totalFloat = suc.startTime - endTimeAct
            
    return totalFloat

def totalFloatEarly(act):
    """ Process the early total float (holgura total de adelanto) of an activity
    """
    
    if act.predecessors[0].ident == -1:
        totalFloat = act.startTime
    else:
        totalFloat = act.startTime - (act.predecessors[0].startTime + act.predecessors[0].duration)
        for pred in act.predecessors[1:]:
            if act.startTime - (pred.startTime + pred.duration) < totalFloat:
                totalFloat = act.startTime - (pred.startTime + pred.duration)
    return totalFloat

def activitySearch (listAct,activity):
    """
    this function return true if an activity is found in a given list
    """
    
    for act in listAct:
        if (act.name == activity.name): 
            return True
        
def predComplete (activity, completeList):
    """
    this function return true if all the predecessors of an activity are already completed
    """
    prednb=len(activity.predecessors) 
    predcount=0
    
    for pred in activity.predecessors : 
        if pred.name=="start" : 
            prednb-=1
        else : 
            for acc in completeList:
                if acc.name==pred.name:
                    predcount+=1
        if predcount==prednb :
            return True
        
def buildResources(listActivities, projectDur):
    nbResources = len(listActivities[1].resources)
    listResources = [[0] * nbResources] * projectDur
    
    for activitiy in listActivities:
        if (activitiy.ident == -1 or activitiy.ident == -2):
            continue
        for i in range(activitiy.startTime, activitiy.startTime + activitiy.duration):
            listResources[i] = addRes(activitiy.resources, listResources[i])
    return listResources


    