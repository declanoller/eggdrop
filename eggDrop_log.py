import matplotlib.pyplot as plt
import numpy as np
from math import log,ceil,floor

minList = []
maxList = []
avgList = []

buildingHeight = 100

dropCountList = []

for breakFloor in range(1,buildingHeight+1):

    firstEggWhole = True
    drops = 0
    lastUnbrokenFloor = 0
    curFloor = floor(buildingHeight/2)
    #print()
    while firstEggWhole:
        drops += 1
        #print("drop {}: dropping from floor {}".format(drops,curFloor))
        if curFloor>=breakFloor:
            #print("first egg broken dropping from floor",curFloor)
            firstEggWhole = False
        else:
            lastUnbrokenFloor = curFloor
            curFloor = ceil((buildingHeight + curFloor)/2)

    if curFloor==breakFloor:
        #print("have to search {} more floors ({} to {})".format(((breakFloor-1) - lastUnbrokenFloor),lastUnbrokenFloor+1,(breakFloor-1)))
        drops += ((breakFloor-1) - lastUnbrokenFloor)
        #print("total drops:",drops)
    else:
        #print("have to search {} more floors ({} to {})".format((breakFloor - lastUnbrokenFloor),lastUnbrokenFloor+1,breakFloor))
        drops += (breakFloor - lastUnbrokenFloor)
        #print("total drops:",drops)

    dropCountList.append(drops)

minDrops = min(dropCountList)
maxDrops = max(dropCountList)
avgDrops = sum(dropCountList)/len(dropCountList)
print("min: {}, max: {}, avgDrops: {}".format(minDrops,maxDrops,avgDrops))
