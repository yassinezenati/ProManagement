'''
Created on 31 déc. 2012

@author: Salah Benmoussati, Yassine Zenati

This file provides functions useful for the algorithms 
'''

def minStartTime(listAct):
    """ This function processes the minimum date an activity can start given the sequencing 
        of its predecessors or successors (depending if we are doing "adelanto" or "retraso")
        The param listAct is the list of the activity's pred or succ..
    """
    return max(listAct, key=lambda activity: activity.seq + activity.duration).seq

def isSeq(act, ressources):
    """ return true if the activity's ressources are less or equal than the ressources given in parameter  
    """
    ok = True 
    count = 0
    while (count < len(ressources) and ok):
        ok = act.ressources[count] <= ressources[count]
        count += 1
    return ok
        
def minusRes(res1, res2):
    """ Process the the operation res1 = res1 - res2
        res1 and res2 being two lists of ressources
    """
    
    for i in range(len(res1)):
        res1[i] = res1[i] - res2[i]
        

def seqActivity(act, minStartTime, tabRessources):
    """ This function sequences the activity :
            1. finds the first day with enough resources so that we can sequence the activity 
            2. Update the seq field of the Activity
            3. Update the list of resources
    """
    
    count = minStartTime
    for listRes in tabRessources[minStartTime:]: 
        if isSeq(act, listRes):
            act.seq = count # Update of the startTime
            for res in tabRessources[count:count+act.duration]:
                minusRes(res, act.ressources)
            break 
        count += 1

