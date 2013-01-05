'''
Created on 30 dec. 2012

@author: Salah Benmoussati, Yassine Zenati
'''

from Activity import Activity
from toolsCalculus import addRes, minusRes, predComplete, isSeq, activitySearch

def parallelSequencing(listActivities) : 

    #initialization
    available = [7,6]
    chosenAct = []
    copy=[]
    sequencing = []
    complete = []
    instant = 0
    finish=False
   
    #initialization with successors of START
    chosenAct.extend(listActivities[0].successors)
                
    while (finish==False) : 
        
        sequencing = sorted(sequencing, key=lambda ac: ac.seq)  
        copy= sorted(copy, key=lambda activity: activity.LFT) #activities arranged in LFT order
        
            
        if(len(listActivities)==(len(complete)+len(sequencing))): #if all the activities are handled : 
            instant=complete[len(complete)-1].seq
            for seq  in sequencing : 
                complete.append(seq)
                sequencing.remove(seq)
            finish = True 
            
        else : 
            chosenAct=sorted(chosenAct, key=lambda activity: activity.LFT) # Order LFT
            sequencing=sorted(sequencing, key=lambda activity: activity.seq) # Order LFT
         
            for pa in sequencing :  
                    if (pa.seq<=instant):
                        
                        available = addRes(available, pa.resources) #update of resources
                        complete.append(pa)
                        sequencing.remove(pa)
                        for succ in pa.successors :  #verify if the activity is already in the chosen activities list or not to avoid repetition when adding 
                            found=False
                            if succ.ident != -2: 
                                for find in chosenAct :
                                    if succ.name == find.name:
                                        found = True  
                                
                                if predComplete(succ, complete) == True and found == False : 
                                    chosenAct.append(succ)
                                            
             
            copy=list(chosenAct)
            copy= sorted(copy, key=lambda activity: activity.LFT)  
            for act in copy :    #Next step : sequencing the selected activity if not already sequenced thanks to an other predecessor
                if (isSeq(act,available) == True) :
                    parAct = Activity(act.ident,act.name,act.successors,act.duration,act.resources)
                    parAct.seq = instant+act.duration
                    parAct.predecessors = act.predecessors
                    done = False
                    
                    if activitySearch(sequencing,act) == True or activitySearch(complete,act) == True  : 
                        done = True
                        chosenAct.remove(act)
             
                    if (done == False) :  # if the activity is not already sequenced by an other predecessor : 
                        sequencing.append(parAct)
                        available = minusRes(available, act.resources) #update of resources
                        chosenAct.remove(act)
            sequencing = sorted(sequencing, key=lambda activity: activity.seq)
            if (len(complete)+2)<len(listActivities):
                instant = sequencing[0].seq 
            else:
                finish = True  
                        
    print "============================================================================"
    for act in complete : 
        print "--------------------------activity : ", act.name , " finish day ", act.seq
    print "============================================================================"
    print available 