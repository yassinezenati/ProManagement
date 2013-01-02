'''
Created on 30 déc. 2012

@author: Salah Benmoussati, Yassine Zenati
'''

from ParallelAct import ParallelAct

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
            