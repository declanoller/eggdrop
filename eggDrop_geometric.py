import matplotlib.pyplot as plt
import numpy as np
from math import sqrt,floor,ceil

minList = []
maxList = []
avgList = []

buildingHeight = 100
#buildingHeight = 1000


dropCountList = []

for breakFloor in range(1,buildingHeight+1):
#for breakFloor in [100]:


    firstEggWhole = True
    drops = 0
    lastUnbrokenFloor = 0
    #skipFloorLength = 5
    floorsAboveCur = buildingHeight - 0
    skipFloorLength = ceil(sqrt(floorsAboveCur))
    curFloor = skipFloorLength
    #print()
    while firstEggWhole:
        drops += 1
        print("skipFloorLength =",skipFloorLength)
        print("drop {}: dropping from floor {}".format(drops,curFloor))
        if curFloor>=breakFloor:
            print("first egg broken dropping from floor",curFloor)
            firstEggWhole = False
        else:
            lastUnbrokenFloor = curFloor
            floorsAboveCur = buildingHeight - curFloor
            skipFloorLength = ceil(sqrt(floorsAboveCur))
            curFloor += skipFloorLength


    if curFloor==breakFloor:
        print("have to search {} more floors ({} to {})".format(((breakFloor-1) - lastUnbrokenFloor),lastUnbrokenFloor+1,(breakFloor-1)))
        drops += ((breakFloor-1) - lastUnbrokenFloor)
        print("total drops:",drops)
    else:
        print("have to search {} more floors ({} to {})".format((breakFloor - lastUnbrokenFloor),lastUnbrokenFloor+1,breakFloor))
        drops += (breakFloor - lastUnbrokenFloor)
        print("total drops:",drops)

    dropCountList.append(drops)

minDrops = min(dropCountList)
maxDrops = max(dropCountList)
avgDrops = sum(dropCountList)/len(dropCountList)
print("min: {}, max: {}, avgDrops: {}".format(minDrops,maxDrops,avgDrops))

exit(0)

minList.append(minDrops)
maxList.append(maxDrops)
avgList.append(avgDrops)


maxListArgMin = np.argmin(np.array(maxList))
avgListArgMin = np.argmin(np.array(avgList))
print('best skip length in terms of avg case:',skipLengthList[avgListArgMin])
print('best skip length in terms of worst case:',skipLengthList[maxListArgMin])
avgLine = plt.plot(skipLengthList,avgList,'bo-',label='avg')
maxLine = plt.plot(skipLengthList,maxList,'ro-',label='worst')
plt.axvline(skipLengthList[avgListArgMin], color='b', linestyle='dashed', linewidth=1)
plt.axvline(skipLengthList[maxListArgMin], color='r', linestyle='dashed', linewidth=1)
plt.xlabel('skip floors length')
plt.ylabel('# of drops')
plt.title('building height = '+str(buildingHeight))
plt.legend()
plt.show()







#
