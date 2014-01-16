import math
import numpy as np
import cv2
import time

def getTrajectories(filepath,startframe,endframe,trajectoylength,x,y,width,height):
    f=open(filepath)
    filepathsplit=str(filepath).split('.')
    filepathsplit[-2]='.dt.'
    newfile=''
    for part in filepathsplit:
        newfile+=part
    newfilesplit=str(newfile).split('/')
    newfilesplit.insert(-1,'seq2')
    modfile=''
    for index in range(len(newfilesplit)-1):
        modfile+=newfilesplit[index]+'/'
    modfile+=newfilesplit[-1]
    print 'writing the file to this location :'+str(modfile)

    f1=open(modfile,'w')
    xStartLimit=x
    xEndLimit=x+width
    yStartLimit=y
    yEndLimit=y+height
    for line in f:
        linesplit=str(line).split('\t')
        if int(math.ceil(float(linesplit[1])))>=startframe and int(math.ceil(float(linesplit[1])))<=endframe:
            condition=True
            inc=0
            for i in range(11,40,2):
                x=float(linesplit[i])
                y=float(linesplit[i+1])
                if (x<=xEndLimit and x>xStartLimit and y<=yEndLimit and y>yStartLimit):
                    condition=condition and True 
                    inc+=1;
                else:
                    condition=condition and False
            print condition 
            if inc>=trajectoylength/2 or condition==True:
                f1.write(line)
    f1.close
    f.close

def displayTrajectories(filepath,trajectorylength,x,y,w,h):
    filesplit=filepath.split('.')
    dirstruct=str(filesplit[0]).split('/')
    moddirstruct="/"+dirstruct[1]+'/'+dirstruct[2]+'/'+dirstruct[3]+'/'+dirstruct[4]+'/'+dirstruct[5]+'/'+dirstruct[6]+"/results/"+dirstruct[7]+'/'+dirstruct[9]+"/seq2/"+dirstruct[10]
    dtfilename=moddirstruct+".dt.txt"
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
    
# do not use relative paths any where in the code
if __name__=="__main__":
    #getTrajectories('/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/MSR2/10.avi.txt',25,600,15,70,40,70,75)
    displayTrajectories('/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/KTH/videos/handclapping/person23_handclapping_d4_uncomp.avi',15,27,11,51,104)
