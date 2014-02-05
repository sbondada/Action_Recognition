import math
import numpy as np
import cv2
import time

'''
this file is resposible for calculating the dense trajectory in the bounding box given as a parameter from the ground truth
file has two functions
Note--the directoryt structure has to be already constructed as the code donot create the directories, only the files
-getTrajectories-this file takes the complete dense trajectory file calculated by the script file "ComputesDenseTrajectory"
and the ground truth information and writes the bounded trajectory of the file to results/"dataset"/"action class"/seq2/
-displayTrajectory-this file accepts the video file as an input and it creates the path to the bouned trajectory file based on its
video file input and displays the trajectories 
'''


def getTrajectories(filepath,startframe,endframe,trajectoylength,x,y,width,height):
    f=open(filepath)
    #splitting the filepath and replacing the avi part of the file name to dt
    filepathsplit=str(filepath).split('.')
    filepathsplit[-2]='.dt.'
    #reconstructing the path with dt
    newfile=''
    for part in filepathsplit:
        newfile+=part
    #splitting the path so that the directory structure could be modified to the 
    #location to save
    newfilesplit=str(newfile).split('/')
    newfilesplit.insert(-1,'seq2')
    modfile=''
    for index in range(len(newfilesplit)-1):
        modfile+=newfilesplit[index]+'/'
    modfile+=newfilesplit[-1]
    print 'writing the file to this location :'+str(modfile)
    #the files are saved at projdir/data/"dataset"/"action class"/seq2/
    f1=open(modfile,'w')
    xStartLimit=x
    xEndLimit=x+width
    yStartLimit=y
    yEndLimit=y+height

    '''
    the condition which is used to select the bounded trajectories from the dataset is 
    we select those trajectories where atleast half of trajectory path is inside the bounding volume
    '''

    for line in f:
        linesplit=str(line).split('\t')
        #condition to check if the trajectory is in the given start and end frame or not
        if int(math.ceil(float(linesplit[1])))>=startframe and int(math.ceil(float(linesplit[1])))<=endframe:
            condition=True
            inc=0
            #looping the trajectory path
            for i in range(11,40,2):
                x=float(linesplit[i])
                y=float(linesplit[i+1])
                #checking if the the trajectory at some frame in the track length is in the boundingbox
                if (x<=xEndLimit and x>xStartLimit and y<=yEndLimit and y>yStartLimit):
                    condition=condition and True 
                    inc+=1;
                else:
                    condition=condition and False
            print condition 
            #adding the trajectory completelyto the file
            if inc>=trajectoylength/2 or condition==True:
                f1.write(line)
    f1.close
    f.close

def displayTrajectories(filepath,trajectorylength,x,y,w,h):
    filesplit=filepath.split('.')
    dirstruct=str(filesplit[0]).split('/')
    moddirstruct="/"+dirstruct[1]+'/'+dirstruct[2]+'/'+dirstruct[3]+'/'+dirstruct[4]+'/'+dirstruct[5]+'/'+dirstruct[6]+"/results/"+dirstruct[7]+'/'+dirstruct[9]+"/seq2/"+dirstruct[10]
    dtfilename=moddirstruct+".dt.txt"
    #opening the bounded trajectory file
    f=open(dtfilename)

    inc=0
    #using open cv to open the video file
    video=cv2.VideoCapture(filepath) 
    cv2.namedWindow("trajectories")
    #checking if the video is opened so that it can read the first frame of the video
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
        #checking if the frame has any trajectory
        if(line!='' and int(linesplit[1])==inc):
            trackslist=[]
            #if true than constructing the trajectory path for displaying
            while(int(linesplit[1])==inc):
                trackslist.append(linesplit)
                line=f.readline()
                if line == '':
                    break
                linesplit=str(line).split('\t')
            print "tracklist length"+str(len(trackslist))
            #looping the trajectory and constructing x and y cordinates to construct a line to show how the point has 
            #traveled in the last 15 frames(as 15 is the track length)
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
        #reducing the spped in which it displays the output
        time.sleep(0.1)
        rval,frame=video.read()

        #this allows to break the displaying process by pressing escape
        key=cv2.waitKey(20)
        if key in [27,ord('Q'),ord('q')]:
            break
    
# do not use relative paths any where in the code
if __name__=="__main__":
    #getTrajectories('/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/MSR2/seq2/boxing/10.avi.txt',25,600,15,70,40,70,75)
    displayTrajectories('/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/MSR2/videos/handclapping/12.avi',15,32,64,98,32)
