import math
import numpy as np
import cv2
import time

def getTrajectories(filepath,startframe,endframe,x,y,width,height):
    f=open(filepath)
    filepathsplit=str(filepath).split('.')
    filepathsplit[-2]='.dt.'
    newfile='..'
    for part in filepathsplit:
        newfile+=part

    f1=open(newfile,'w')
    xStartLimit=x
    xEndLimit=x+width
    yStartLimit=y
    yEndLimit=y+height
    for line in f:
        linesplit=str(line).split('\t')
        condition=True
        for i in range(11,40,2):
            x=float(linesplit[i])
            y=float(linesplit[i+1])
            if (x<=xEndLimit and x>xStartLimit and y<=yEndLimit and y>yStartLimit):
                condition=condition and True 
            else:
                condition=condition and False
        print condition 
        if condition==True:
            f1.write(line)
    f1.close
    f.close

def displayTrajectories(filepath,trajectorylength,x,y,w,h):
    filesplit=filepath.split('.')
    dirstruct=str(filesplit[2]).split('/')
    moddirstruct="/"+dirstruct[1]+"/results/"+dirstruct[2]+"/"+dirstruct[4]
    dtfilename=".."+moddirstruct+".dt.txt"
    f=open(dtfilename)

    inc=0
    video=cv2.VideoCapture(filepath) 
    cv2.namedWindow("trajectories")
    if video.isOpened():
        line=f.readline()
        rval, frame=video.read()
        print "shape of thhe frame"+str(frame.shape)
        inc+=1
    else:
        rval=False
        print rval
    while rval:
        print inc
        linesplit=str(line).split('\t')
        if(line!='' and int(linesplit[1])==inc):
            trackslist=[]
            while(int(linesplit[1])==inc):
                trackslist.append(linesplit)
                line=f.readline()
                if line == '':
                    break
                linesplit=str(line).split('\t')
            print "tracklist length"+str(len(trackslist))
            for tracks in trackslist:
                start=13
                pointx1=int(math.ceil(float(tracks[11])))
                pointy1=int(math.ceil(float(tracks[12])))
                frame[pointy1,pointx1]=(0,0,255)
                for index in range(0,28,2):
                    pointx2=int(math.ceil(float(tracks[start+index])))
                    pointy2=int(math.ceil(float(tracks[start+index+1])))
                    cv2.line(frame,(pointx1,pointy1),(pointx2,pointy2),(0,255,0),1)
                    pointx1=pointx2
                    pointy1=pointy2

        inc+=1
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0))
        cv2.imshow("trajectories",frame)
        time.sleep(0.1)
        rval,frame=video.read()

        key=cv2.waitKey(20)
        if key in [27,ord('Q'),ord('q')]:
            break
    
if __name__=="__main__":
    #getTrajectories('../data/results/MSR2/10.avi.txt',25,600,70,40,70,75)
    displayTrajectories('../data/MSR2/videos/10.avi',15,70,40,70,75)
