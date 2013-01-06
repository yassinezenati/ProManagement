'''
Created on 11 nov. 2012

@author: Salah Benmoussati, Yassine Zenati
'''

from PMFiles import PMFiles
import sys
from CriticalPathMethod import criticalPathMethod
from Sequencing import parallelSequencing
from toolsCalculus import find_all_paths, buildList, findNonCriticalAct, projectDuration, buildResources
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


buildList(listActivities)

#earlyOrLateProcess(listActivities, resources, True)

#earlyOrLateProcess(listActivities, resources, False)

#newRes = resourceLeveling(listActivities, resources)

#print buildResources(listActivities, projectDuration(listActivities))

for act in listActivities:
    print act.name + "startTime = " + str(act.startTime)

# SALAH, tu dois remplacer le sys.argv[3] par un entier que l'utilisateur aura saisi s'il choisit 
# de faire de la flexibilite (en vrai tu lui demande si il veut deplacer une activitite
# ce sera un truc du genre numAct = input("type the number of the activity you want to move (number
# written in the CSV file")
analyseActivity(listActivities, listActivities[int(sys.argv[3])], resources)

"""
criticalPathMethod(listActivities)

print("########################################")
for act in listActivities:
    act.display()
print("########################################")

parallelSequencing(listActivities)

"""