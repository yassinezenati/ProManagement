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
    start = Activity(-1, "start", listStart, -1, -1, -1, -1, None)
    end = Activity(-2, "end", None, -1, -1, -1, -1, None)
    for act in listAct:
        if (act.successors is None):
            act.successors = [end]
        else:
            listActWithPred.extend(act.successors)
            for suc in act.successors: #adding predecessors
                suc.predecessors.append(act)
    for act in listAct:
        if (not act in listActWithPred):
            start.successors.append(act)
            
    listAct.insert(0, start)
    listAct.append(end)


buildList(listActivities)
for act in listActivities:
    act.display()
    
      
    

    