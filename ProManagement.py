'''
Created on 11 nov. 2012

@author: yassine
'''
from PMFiles import PMFiles
import sys


fileName = sys.argv[1]
listActivities = PMFiles.read(fileName)
for act in listActivities: 
    act.display()
    