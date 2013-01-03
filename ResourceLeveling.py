'''
Created on 2 janv. 2013

@author: Salah Benmoussati, Yassine Zenati
'''
from toolsCalculus import addRes, minusRes, overUseRes

def resourceLeveling(listActivities, listNonCriticalAct, projectDuration, projectResources):
    
    nbResources = len(listActivities[1].resources) 
    
    # Build a table of resources per day 
    
    listResources = [[0] * nbResources] * projectDuration
    
    for act in listActivities:
        for i in range(act.startTime, act.startTime + act.duration + 1):
            listResources[i] = addRes(act.resources, listResources[i])
    
    # Sort the activities by finishing time
    sortedNCA = sorted(listNonCriticalAct, key=lambda activity: activity.startTime + activity.duration, reverse=True)
    
    #Initialisation with the current list of resources 
    minimizedList = listResources
    
    for act in sortedNCA:
        endTimeAct = act.startTime + act.duration # Finalisation of the activity
        
        # Process of the total float (holgura total)
        totalFloat = act.successors[0].startTime - endTimeAct
        for suc in act.successors[1:]:
            if suc.startTime - endTimeAct < totalFloat:
                totalFloat = suc.startTime - endTimeAct
                
        # Try every position (sequenciation) available until we reach the end of
        # the total float (holgura total)
        
        
       
        oldListRSD = evaluateResourceList(minimizedList)
        
        for seq in range(act.startTime + 1, act.startTime + totalFloat + 1):
            
            # Build the list with the new resources
            newList = buildNewResourceList(minimizedList, act, seq, projectResources)
            
            if not newList is None: 
            # If newList is None, it means sequencing the activity at this day
            # overuse the resources of the project 
                
                # Evaluate the new list of resources
                newListRSD = evaluateResourceList(newList)
                
                # If the new sequenciation is better
                # The activity startTime and the oldListRSD and minimizedList are updated
                if sum(newListRSD) < sum(oldListRSD):
                    minimizedList = newList
                    oldListRSD = newListRSD
                    act.startTime = seq
                    
                
def buildNewResourceList(listRes, act, newSeq, maxRes):
    """
    Build a new list of resources to be tested, considering:
        => The initial list of resources
        => an activity
        => The new sequenciation of the activity we want to test, 
        => The amount of resources of the project (maxRes)
    If the new sequenciation results in an overuse of the resources, it returns None!
    Returns the new list
    """
    
    newList = list(listRes)
    # Delete the resources taken by the activity at its previous sequenciation
    for day in range(act.startTime,act.startTime+act.duration + 1):
        newList[day] = minusRes(listRes[day],act.resources)
        
    # Add the resources taken by the activity at its new sequenciation
    # If overuse of the resources => return None
    for day in range(newSeq, newSeq+act.duration + 1):
        newRes = addRes(newList[day], act.resources)
        if overUseRes(newRes, maxRes):
            return None
        newList[day] = newRes
    
    return newList

def evaluateResourceList(newList):
    """
    Process the coefficient of variation of each resource and returns it.
    It returns a tuple of these coefs.
    """
    
    
    #Transform the list in order to have a list of values per resources
    # instead of a list of resources per day
    
    listValuesPerResources = zip(*newList)
        
    # Process the relative standard deviation (absolute value of the coef of variation)
    
    listRSD = []
    for res in listValuesPerResources:
        rsd = abs(float(stdDev(res)) / avg(res)) 
        listRSD.append(rsd)
    
    return listRSD

            
def avg(listValues):
    """ Process the average of a list of values
    """
    return sum(listValues, 0.0) / len(listValues)

def variance(listValues):
    """ Process the variance of a list of values
    """
    m=avg(listValues)
    return avg([(x-m)**2 for x in listValues])

def stdDev(listValues):
    """ Process the standard deviation of a list of values
    """
    return variance(listValues)**0.5

    