'''
Created on 6 dec. 2012

@author: SALAH
'''
class ParallelAct :
    def __init__(self, name,seq,ressources,succ,pred) :
        self.name = name
        self.seq = seq
        self.ressources= ressources
        self.succ=succ
        self.pred=pred
