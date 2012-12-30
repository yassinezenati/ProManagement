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
        self.EST = -1 # EST = Early Start Time 
        self.LST = -1 # LST = Late Start Time
        self.LFT = -1
        self.normalCost = normalCost
        self.topCost = topCost
        self.reductionCost = reductionCost
        self.ressources = ressources #List of ressources
        
    def display(self):
        print ("                       ==>" + str(self.name)+ "<==")
        print str(self.ident) + " " + str(self.name) + " " + str(self.duration) +  " "  + str(self.normalCost) + " " + str(self.topCost) + " " + str(self.reductionCost) + " "
        print ("suc :"),
        if (not self.successors is None):
            for suc in self.successors: 
                print suc.name,
        print ""
        print ("pred: "),
        if (not self.predecessors is None):
            for pred in self.predecessors: 
                print pred.name,
        print ""
        print ("res: ")
        print ("EST = " + str(self.EST))
        print ("LST = " + str(self.LST))
        print ("LFT = " + str(self.LFT))
        print self.ressources 
        