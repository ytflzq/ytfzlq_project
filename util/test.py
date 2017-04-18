import datetime
import time
import os
if __name__ == '__main__':
    # timeArry = []
    # now = datetime.datetime.now()
    # timeArry.append(now)
    # for x in xrange(1,7):
    #     timeArry.append((datetime.datetime.now() - datetime.timedelta(days = x)))
    # print timeArry[0].year
    # print getdayth(timeArry[0])
    # temp = [];
    # temp.append({"aa":"ddd"})
    # print temp[0]['aa']
    # num = 0
    # num = "222"
    # print num
    devHashs = "444"
    devHashsPath = os.path.normpath(os.path.dirname(os.path.abspath(__file__)) + "/devHashs.txt")
    accountId = "1"
    fileObject = open(devHashsPath)
    try:
        allTheText = fileObject.read()
    finally:
        fileObject.close()
    strArr = allTheText.split('{-}')
    newAllTheText = ""
    cur = 0 
    for x in strArr:
        oneData = x.split('{*}')
        if len(oneData)==2:
            if oneData[0]==accountId:
                cur = 1
                newAllTheText +=accountId+"{*}"+devHashs+"{-}"
            else:
                newAllTheText +=oneData[0]+"{*}"+oneData[1]+"{-}"
    if newAllTheText=="":
        newAllTheText = accountId+"{*}"+devHashs+"{-}"
    elif cur==0:
        newAllTheText += accountId+"{*}"+devHashs+"{-}"
    read = open(devHashsPath,'w+')
    read.write(newAllTheText)
    read.close()
