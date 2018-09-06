import matplotlib.pyplot as plt
import numpy as np

#skipLengthList = list(range(15,70))+[100,200,300,500,800,980]
skipLengthList = list(range(15,70))+list(range(70,1000,25))
#skipLengthList = list(range(1,20))+[30,40]
minList = []
maxList = []
avgList = []

buildingHeight = 1000

for skipFloorLength in skipLengthList:
    dropCountList = []
    #print("\nskipFloorLength =",skipFloorLength)
    for breakFloor in range(1,buildingHeight+1):
        firstEggWhole = True
        drops = 0
        lastUnbrokenFloor = 0
        #skipFloorLength = 5
        curFloor = skipFloorLength
        #print()
        while firstEggWhole:
            drops += 1
            #print("drop {}: dropping from floor {}".format(drops,curFloor))
            if curFloor>=breakFloor:
                #print("first egg broken dropping from floor",curFloor)
                firstEggWhole = False
            else:
                lastUnbrokenFloor = curFloor
                curFloor += skipFloorLength

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
    #print("min: {}, max: {}, avgDrops: {}".format(minDrops,maxDrops,avgDrops))
    minList.append(minDrops)
    maxList.append(maxDrops)
    avgList.append(avgDrops)


avgListArgMin = np.argmin(np.array(avgList))
maxListArgMin = np.argmin(np.array(maxList))
print('best skip length in terms of avg case:',skipLengthList[avgListArgMin])
print('best skip length in terms of worst case:',skipLengthList[maxListArgMin])
print('best avg case:',avgList[avgListArgMin])
print('best worst case:',maxList[maxListArgMin])
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
