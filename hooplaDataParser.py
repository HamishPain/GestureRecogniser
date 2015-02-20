import os

def getSignalList():
    timeList = []
    gyroList = [[],[],[]]
    accelList = [[],[],[]]
    hitList = []

    signalList = []

    print(os.getcwd())
    for fileName in os.listdir(os.getcwd()+"\\hoopData\\"):
        #print(fileName)
        signal = []
        with open(os.getcwd()+"\\hoopData\\"+fileName) as f:
            for line in f:
                a = line.split(',')
                timeList.append(float(a[0]))

                accelList[0].append(signedShort(int(a[1]) + int(a[2])*256))
                accelList[1].append(signedShort(int(a[3]) + int(a[4])*256))
                accelList[2].append(signedShort(int(a[5]) + int(a[6])*256))

                gyroList[0].append(signedShort(int(a[7]) + int(a[8])*256))
                gyroList[1].append(signedShort(int(a[9]) + int(a[10])*256))
                gyroList[2].append(signedShort(int(a[11]) + int(a[12])*256))

                hitList.append(int(a[13]))
                if len(timeList) < 2:
                    deltaTime = 0.01
                else:
                    deltaTime = timeList[-1]-timeList[-2]
                signal.append([deltaTime, accelList[1][-1], accelList[2][-1], gyroList[0][-1], hitList[-1]])
                #print(signal[-1])
        signalList.append(signal)
    return signalList

def signedShort(a):
        a &= 0xFFFF
        if a >= 1 << 15:
            a -= 1 << 16
        return a


