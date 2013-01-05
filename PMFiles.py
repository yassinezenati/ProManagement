'''
Created on 11 nov. 2012

@author: Salah Benmoussati, Yassine Zenati

This class provides methods to read the input file and to produce output files

'''

import csv
from Activity import Activity

class PMFiles:
    @staticmethod
    def readAct(fileActivities):
        """Reads the input file 
        
        The file must be a CSV file
        The attributes of each activities must follow this order :
            1. ID
            2. Name
            3. Successors : set of activities' id delimited by the symbol ";"
            4. Duration
            5. Normal Cost 
            8. resources : set of integer delimited by the symbol ";"
                (First integer is the amount of the first ressource and so on)
        
        """
        
        listActivities = {}
        f = csv.reader(open(fileActivities,"rb"))
        for line in f:
            # cast each value as an int
            ident = int(line[0])
            name = line[1]
            successors = ""
            if (line[2] != ""):
                successors = map(int, line[2].split(";"))
            else:
                successors = None
            duration = int(line[3])
            resources = ""
            if (line[4] != ""):
                resources = map(int, line[4].split(";"))
            if (line[5] != ""):
                startTime = int(line[5])
            else:
                startTime = -1
            act = Activity(ident, name, successors, duration, resources, startTime)
            listActivities[act.ident] = act
            
        for act in listActivities.values(): # replace activities id by activities in successors
            if (not act.successors is None):
                count = 0
                while (count < len(act.successors)):
                    sucId = act.successors.pop(0)
                    act.successors.append(listActivities[sucId])
                    count = count + 1
        return listActivities.values()
    
    @staticmethod
    def readConfProject(fileConf):
        f = open(fileConf,"rb")
        conf = {}
        cpt = 0
        listDaysOff = []
        for line in f:
            if cpt == 0:
                conf["projectName"] = line
            elif cpt == 1:
                conf["resources"] = map(int, line.split(";"))
            elif cpt == 2:
                conf["beginningDate"] = map(int, line.split("/"))
            else:
                listDaysOff.append(map(int, line.split("/")))
            cpt += 1
        conf["daysOff"] = listDaysOff
        f.close()
        return conf
    