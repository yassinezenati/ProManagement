'''
Created on 11 nov. 2012

@author: yassine
'''
from PMFiles import PMFiles
import sys
import datetime
import copy
from Activity import Activity
from ParallelAct import ParallelAct
from copy import deepcopy


fileName = sys.argv[1]
listActivities = PMFiles.read(fileName)

def buildList(listAct):
    """ Add the start activity and end activity
    """
    listStart = []
    listActWithPred = [] #List of activities having at least predecessor
    start = Activity(-1, "start", listStart, 0, 0, -1, -1, None)
    start.EST = 0
    start.LST = 0
    start.LFT = 0
    end = Activity(-2, "end", None, 0, -1, -1, -1, None)
    for act in listAct:
        if (act.successors is None):
            act.successors = [end]
            end.predecessors.append(act)
        else:
            listActWithPred.extend(act.successors)
            for suc in act.successors: #adding predecessors
                suc.predecessors.append(act)
    for act in listAct:
        if (not act in listActWithPred):
            start.successors.append(act)
            act.predecessors.append(start)
            
    listAct.insert(0, start)
    listAct.append(end)


def criticalPathMethod(listActivities):
    """ CPM algorithm
    """
    
    listCriticalPath = []
    
    # First step : order the activity
    listOrdenedAct = []
    for act in listActivities:
        if (not act in listOrdenedAct):
            listOrdenedAct.append(act)
        for pred in act.predecessors:
            if (pred in listOrdenedAct):
                if (listOrdenedAct.index(pred) > listOrdenedAct.index(act)):
                    listOrdenedAct.remove(pred)
                    listOrdenedAct.insert( listOrdenedAct.index(act), pred)
            else :
                listOrdenedAct.insert(listOrdenedAct.index(act), pred)
    
    # Second step : for each activity process its early start time 
    
    for act in listOrdenedAct:
        if (not (act.ident == -1)):
            maxDate = act.predecessors[0].duration + act.predecessors[0].EST
            for pred in act.predecessors[1:]: # We skip the first predecessors duration
                if (pred.EST + pred.duration > maxDate):
                    maxDate = pred.EST + pred.duration
            act.EST = maxDate        
    listActivities[-1].LST = listActivities[-1].EST
    
    # Third step : for each activity, process its late start time
    
    startDate = datetime.date.today() 
    currentDate=startDate + datetime.timedelta(days=1)
    
    if (currentDate.isoweekday()==6) : 
        currentDate=startDate + datetime.timedelta(days=2)
    if (currentDate.isoweekday()==7) : 
        currentDate=startDate + datetime.timedelta(days=1)

    listOrdenedAct.reverse() # Reverse the order of the list
    for act in listOrdenedAct:
        if (act.ident==-2) : 
            duration = act.EST
            print "Duration of the project : ", duration , "days"
            count=0
            while count < duration : 
                if (currentDate.isoweekday() == 5):
                    currentDate= currentDate + datetime.timedelta(days=3)
                else :
                    currentDate=currentDate + datetime.timedelta(days=1)
                count=count+1
                    
        if (not (act.ident == -2)):
            minDate = act.successors[0].LST - act.duration
            for suc in act.successors:
                if (suc.LST - act.duration < minDate):
                    minDate = suc.LST - act.duration
            act.LST = minDate
        if (act.EST == act.LST):
            listCriticalPath.append(act)
        
    print ("Starting of the project : "),
    print startDate 
    print ("Ending of the project : "), 
    print currentDate 
    
    for act in listActivities : 
        act.LFT = act.LST + act.duration

def parallelSequencing(listActivities) : 
   
    #initialization
    dispo = [20,30]
    chosenAct = []
    copy=[]
    sequencing = []
    complete = []
    instant = 0
    count=0
    finish="false"
    for act in listActivities :       #initialization 
        for pred in act.predecessors :
            if (pred.ident == -1):
                chosenAct.append(act)
                
    for act in listActivities :
        for pred in act.predecessors :
            if (pred.ident == -2):
                count+=1
    while (finish=="false") : 
        
        sequencing = sorted(sequencing, key=lambda ac: ac.seq)
        copy= sorted(copy, key=lambda activity: activity.LFT)
        
            
        if(len(listActivities)==(len(complete)+len(sequencing))):
            instant=complete[len(complete)-1].seq
            for seq  in sequencing : 
                complete.append(seq)
                sequencing.remove(seq)
                  
            sequencing = sorted(sequencing, key=lambda activity: activity.seq)
            finish="true"
        else : 
            print"-------------------------- dispo debut : ",dispo 
    
            print "-----------tournee   ",count, "instant      ",instant
            
            chosenAct=sorted(chosenAct, key=lambda activity: activity.LFT) # Order LFT
            sequencing=sorted(sequencing, key=lambda activity: activity.seq) # Order LFT
            copy=sorted(copy, key=lambda activity: activity.LFT)
            copy=list(chosenAct)
            for pa in sequencing : 
                    print "voici les sequences : ",pa.name, "temps : ", pa.seq
                    if (pa.seq<=instant):
                        j=0
                        while (j<len(dispo)) :
                            print "                ressources a voir :         ",pa.ressources[j]
                            dispo[j]=dispo[j] + pa.ressources[j]
                            j=j+1
                        complete.append(pa)
                        sequencing.remove(pa)
                        prednb=0
                        for succ in pa.succ : 
                            if succ.name!="end":
                                found="no"
                                 #trouver condition pour verifier avec les pred s'ils sont finis ou non
                                for find in chosenAct :
                                    if succ.name==find.name:
                                        found="yes"
                                
                                
                                prednb=len(succ.predecessors)
                                predcount=0
                                for pred in succ.predecessors : 
                                    if pred.name=="start" : 
                                        prednb-=1
                                    else : 
                                        for acc in complete:
                                            if acc.name==pred.name:
                                                predcount+=1
                                    if predcount==prednb:
                                        print " nombre de predecesseurs : ",prednb
                                        if found=="no":
                                            chosenAct.append(succ)
                                            print found
                                            print "succ : ",succ.name
            print " dispoooo ", dispo           
            print "longueur : ",len(copy) 
            copy=list(chosenAct)
            copy= sorted(copy, key=lambda activity: activity.LFT)  
            for act in copy :
                i=0
                positif="true"
                print "activite  parcourues : ",act.name
                
                
                for acta in chosenAct : 
                    print "aaaaaa- ",acta.name
                
                while (i<len(dispo)) and (positif =="true"): 
                    if ((dispo[i]-act.ressources[i])<0):
                        positif="false"
                    i=i+1
                if (positif == "true") :
                    
                    print "activite valide :", act.name , "duree : ", act.duration
                    parAct = ParallelAct(act.name,instant+act.duration,act.ressources,act.successors,act.predecessors)
                    
                    done="false"
                    for seq in sequencing:
                        
                        if (seq.name == act.name): 
                            done ="true"
                            chosenAct.remove(act)
                    for comp in complete:
                        
                        if (comp.name == act.name): 
                            done ="true"
                            chosenAct.remove(act)
                    if (done=="false") : 
                        sequencing.append(parAct)
                        count+=1
                        
                        
                        j=0
                        while (j<len(dispo)) :
                            print "                                  soustraction faite"
                            dispo[j]=dispo[j] - act.ressources[j]
                            j=j+1
                        chosenAct.remove(act)
               
            sequencing = sorted(sequencing, key=lambda activity: activity.seq)
                             
            print("============================================================================")
            for act in complete : 
                print "--------------------------activite : ", act.name , " finie  l instant ", act.seq 
            print("============================================================================")
            for act in listActivities : 
                print "--------------------------activite : ", act.name , " duree ", act.duration

            if (len(complete)+2)<len(listActivities):
                instant = sequencing[0].seq 
            else:
                finish="true"  
                        
                        
            print dispo 
            
buildList(listActivities)
criticalPathMethod(listActivities)

print("########################################")
for act in listActivities:
    act.display()
print("########################################")

parallelSequencing(listActivities)

