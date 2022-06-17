import glob
import os
import time


mystat = os.stat('/Users/anil/Desktop/fwdmotioncamerasetupandpermissions/camera2.conf')
print(mystat)
for eachVideoUrl in glob.glob('/Users/anil/Desktop/fwdmotioncamerasetupandpermissions/*'):
    print(eachVideoUrl)
    stat = os.stat(eachVideoUrl)
    fileCreationTime = stat.st_birthtime;
    currentTime = time.time()*1000.0 - 10000

    print("last modified: %s" % time.ctime(os.path.getmtime(eachVideoUrl)))
    # print(time.time())
