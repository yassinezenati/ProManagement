'''
Created on 17 nov. 2012

@author: yassine

This class defines an Activity, which is a set of properties of one activity (name, duration, cost...)
'''

class Activity:
    def __init__(self, ident,  name, successors, duration, normalCost, topCost, reductionCost, ressources):
        self.ident = ident
        self.name = name
        self.successors = successors  #list of Activity
        self.predecessors = [] #list of Activity
        self.duration = duration
        self.dateStart = -1
        self.dateEnd = -1
        self.normalCost = normalCost
        self.topCost = topCost
        self.reductionCost = reductionCost
        self.ressources = ressources #List of ressources
        
    def display(self):
        print str(self.ident) + " " + str(self.name) + " " + str(self.duration) +  " "  + str(self.normalCost) + " " + str(self.topCost) + " " + str(self.reductionCost) + " "
        if (not self.successors is None):
            for suc in self.successors: 
                print suc.ident
        print self.ressources 
        