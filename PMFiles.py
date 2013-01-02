'''
Created on 11 nov. 2012

@author: Salah Benmoussati, Yassine Zenati

This class provides methods to read the input file and to produce output files

'''

import csv
from Activity import Activity

class PMFiles:
    @staticmethod
    def read(fileActivities):
        """Reads the input file 
        
        The file must be a CSV file
        The attributes of each activities must follow this order :
            1. ID
            2. Name
            3. Successors : set of activities' id delimited by the symbol ";"
            4. Duration
            5. Normal Cost 
            6. Top Cost
            7. Reduction Cost
            8. Ressources : set of integer delimited by the symbol ";"
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
            normalCost = int(line[4])
            topCost = int(line[5])
            reductionCost = int(line[6])
            ressources = ""
            if (line[3] != ""):
                ressources = map(int, line[7].split(";"))
            act = Activity(ident, name, successors, duration, normalCost, topCost, reductionCost, ressources)
            listActivities[act.ident] = act
            
        for act in listActivities.values(): # replace activities id by activities in successors
            if (not act.successors is None):
                count = 0
                while (count < len(act.successors)):
                    sucId = act.successors.pop(0)
                    act.successors.append(listActivities[sucId])
                    count = count + 1
        return listActivities.values()
    