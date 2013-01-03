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
    return max(listAct, key=lambda activity: activity.seq + activity.duration).seq

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
    res = []
    for i in range(len(res1)):
        res.insert(i, res1[i] - res2[i])
    return res
    
def addRes(res1, res2):
    """ Process the the operation res = res1 +  res2
        res, res1 and res2 being lists of resources
    """
    res = []
    for i in range(len(res1)):
        res.insert(i, res1[i] + res2[i])
    return res
            
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
            for res in tabresources[count:count+act.duration]:
                res = minusRes(res, act.resources)
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
    