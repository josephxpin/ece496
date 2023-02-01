import math
import numpy as np
from os import listdir

def findHifiMapName():
    files = listdir()
    for f in files:
        if f.startswith("hifi") and not f.endswith("maps"):
            return f

def findLofiMapName():
    files = listdir()
    for f in files:
        if f.startswith("lofi") and not f.endswith("maps"):
            return f
        
def extractTransmitter(filename):
    fNameList = filename.split('_')
    hester = []

    for i in range(1, len(fNameList)):
        hester.append(float(fNameList[i].replace('x','').replace('y','').replace('z','').replace('n','-').replace('p','.').replace('.csv','')))

    return hester

def p2pDist(p1, p2):
    return math.sqrt(math.pow(p2[0]-p1[0],2) + math.pow(p2[1]-p1[1],2) + math.pow(p2[2]-p1[2],2))

powerMapName = findLofiMapName()
powerMapFile = open(powerMapName, "r")
transLoc = extractTransmitter(powerMapName)
powerMap = powerMapFile.readlines()
powerMapFile.close()

for idx in range(len(powerMap)):
    if idx == 0:
        powerMap[0]=powerMap[0].rstrip("\n")+", Friis, LoS\n"
    else:
        row = powerMap[idx].split(',')
        recLoc = [float(row[0]),float(row[1]),float(row[2])]
        R = p2pDist(recLoc, transLoc)
        friis = 15 + 3 + 2.15 + 20*math.log10(0.1391148297/(4*math.pi*R))

        LoS = 0
        if friis<float(row[3]):
            LoS = 1
        
        powerMap[idx] = powerMap[idx].rstrip("\n")+', '+str(round(friis,3))+", "+str(LoS)+"\n"
        
powerMapFile=open(powerMapName,"w")
powerMapFile.writelines(powerMap)
powerMapFile.close()
