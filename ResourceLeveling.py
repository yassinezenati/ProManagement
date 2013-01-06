'''
Created on 2 janv. 2013

@author: Salah Benmoussati, Yassine Zenati
'''
from toolsCalculus import addRes, minusRes, overUseRes, totalFloatLate, findNonCriticalAct, projectDuration

def resourceLeveling(listActivities, projectResources):
    
    projectDur = projectDuration(listActivities)
    listNonCriticalAct = findNonCriticalAct(listActivities)
    
    nbResources = len(listActivities[1].resources) 
    
    # Build a table of resources per day 
    
    listResources = [[0] * nbResources] * projectDur
        
    for act in listActivities:
        if (act.ident == -1 or act.ident == -2):
            continue
        for i in range(act.startTime, act.startTime + act.duration):
            listResources[i] = addRes(act.resources, listResources[i])
    
    # Calculate totalFloat of each activity and sort by totalFloat
    for activity in listNonCriticalAct:
        activity.totalFloat = totalFloatLate(activity, projectDur)
    
    firstSortNCA =  sorted(listNonCriticalAct, key=lambda activity: activity.totalFloat, reverse=True)
    # Sort the activities by finishing time
    sortedNCA = sorted(firstSortNCA, key=lambda activity: activity.startTime + activity.duration, reverse=True)
    
    #Initialisation with the current list of resources 
    minimizedList = listResources
    
    for act in sortedNCA:
        if (act.ident == -1 or act.ident == -2):
            continue
        
        totalFloat = totalFloatLate(act, projectDur)        
                
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
     
    # return list of actual resources                
    return minimizedList
    
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
    for day in range(act.startTime,act.startTime+act.duration):
        newList[day] = minusRes(listRes[day],act.resources)
        
    # Add the resources taken by the activity at its new sequenciation
    # If overuser of the project resources => return None
        
    for day in range(newSeq, newSeq+act.duration):
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

    