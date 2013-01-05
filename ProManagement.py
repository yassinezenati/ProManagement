'''
Created on 11 nov. 2012

@author: Salah Benmoussati, Yassine Zenati
'''

from PMFiles import PMFiles
import sys
from CriticalPathMethod import criticalPathMethod
from Sequencing import parallelSequencing
from toolsCalculus import find_all_paths, buildList, findNonCriticalAct, projectDuration
from EarlyLateProcesses import earlyOrLateProcess
from ResourceLeveling import resourceLeveling
from Flexibility import analyseActivity

fileName = sys.argv[1]
listActivities = PMFiles.read(fileName)
            
buildList(listActivities)

#earlyOrLateProcess(listActivities, [5,8,7,6], True)

#earlyOrLateProcess(listActivities, [5,8,7,6], False)

"""
print projectDuration
resourceLeveling(listActivities, [30,20])
"""
for act in listActivities:
    print act.name + "startTime = " + str(act.startTime)

projectDur = projectDuration(listActivities)
analyseActivity(listActivities, listActivities[10], projectDur, [5,8,7,6])

"""
criticalPathMethod(listActivities)

print("########################################")
for act in listActivities:
    act.display()
print("########################################")

parallelSequencing(listActivities)

"""