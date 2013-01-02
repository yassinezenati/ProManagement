'''
Created on 11 nov. 2012

@author: Salah Benmoussati, Yassine Zenati
'''
from PMFiles import PMFiles
import sys
from Activity import Activity
from CriticalPathMethod import criticalPathMethod
from Sequencing import parallelSequencing


fileName = sys.argv[1]
listActivities = PMFiles.read(fileName)

def buildList(listAct):
    """ Add the start activity and end activity
    """
    listStart = []
    listActWithPred = [] #List of activities having at least predecessor
    start = Activity(-1, "start", listStart, 0, 0, -1, -1, None)
    start.EST = 0
    start.LST = 0
    start.LFT = 0
    end = Activity(-2, "end", None, 0, -1, -1, -1, None)
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
            
buildList(listActivities)
criticalPathMethod(listActivities)

print("########################################")
for act in listActivities:
    act.display()
print("########################################")

parallelSequencing(listActivities)

