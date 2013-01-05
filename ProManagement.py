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
listActivities = PMFiles.readAct(fileName)
conf = PMFiles.readConfProject(sys.argv[2])

projectName = conf["projectName"]
resources = conf["resources"]
beginDate = conf["beginningDate"]
daysOffs = conf["daysOff"]

print daysOffs

buildList(listActivities)

#earlyOrLateProcess(listActivities, [5,8,7,6], True)

#earlyOrLateProcess(listActivities, [5,8,7,6], False)

"""
print projectDuration
resourceLeveling(listActivities, [30,20])
"""
for act in listActivities:
    print act.name + "startTime = " + str(act.startTime)

#analyseActivity(listActivities, listActivities[10], [5,8,7,6])

"""
criticalPathMethod(listActivities)

print("########################################")
for act in listActivities:
    act.display()
print("########################################")

parallelSequencing(listActivities)

"""