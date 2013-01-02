'''
Created on 11 nov. 2012

@author: Salah Benmoussati, Yassine Zenati
'''

from PMFiles import PMFiles
import sys
from CriticalPathMethod import criticalPathMethod
from Sequencing import parallelSequencing
from toolsCalculus import find_all_paths, buildList

fileName = sys.argv[1]
listActivities = PMFiles.read(fileName)
            
buildList(listActivities)

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

listCriticalAct = sum(listCriticalPaths, [])
for act in listCriticalAct:
    print act.name

"""
criticalPathMethod(listActivities)

print("########################################")
for act in listActivities:
    act.display()
print("########################################")

parallelSequencing(listActivities)

"""