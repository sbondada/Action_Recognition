import os
from scipy.cluster.vq import kmeans,vq
from numpy import array
import pickle
import tables
import subprocess
import sys
import math
sys.path.insert(0,'/home/kaushal/Documents/projects/dense_trajectory_and_codebook/python/')

def getTrajectories(filepath,startframe,endframe,trajectoylength,x,y,width,height):
    f=open(filepath)
    xStartLimit=x
    xEndLimit=x+width
    yStartLimit=y
    yEndLimit=y+height

    '''
    the condition which is used to select the bounded trajectories from the dataset is 
    we select those trajectories where atleast half of trajectory path is inside the bounding volume
    '''
    trajectoryList=[]
    for line in f:
        linesplit=str(line).split('\t')
        linesplit=[float(x) for x in linesplit[:] if x!='\n']

        #condition to check if the trajectory is in the given start and end frame or not
        if int(math.ceil(linesplit[1]))>=startframe and int(math.ceil(linesplit[1]))<=endframe:
            condition=True
            inc=0
            #looping the trajectory path
            for i in range(11,40,2):
                x=linesplit[i]
                y=linesplit[i+1]
                #checking if the the trajectory at some frame in the track length is in the boundingbox
                if (x<=xEndLimit and x>xStartLimit and y<=yEndLimit and y>yStartLimit):
                    condition=condition and True 
                    inc+=1;
                else:
                    condition=condition and False
            print condition 
            #adding the trajectory completelyto the file
            if inc>=trajectoylength/2 or condition==True:
                trajectoryList.append(linesplit[41:])
    f.close
    return trajectoryList

def getBagOfWords(codebook,data):
    #here it accepts the codebook and the trajectory to find to which bin this trajectory is close and assign the index
    #of the code book
    binSize=len(codebook)
    print "binsize"+str(binSize)
    bagofwords=[0]*binSize 
    #there is a chance that the file may not have any trajectories which may lead to empty
    #data vector
    if data!=[]:
        idx,_=vq(array(data),codebook)
        #constructing the dictionary constructing the array of the size of the bins and each having the no of trajectories
        #its closer to
        for indexEle in idx:
            bagofwords[int(indexEle)]+=1
        bagofwords=[float(x)/len(idx) for x in bagofwords]
    return bagofwords

def getScoresForVideo(filepath,codebookpath,trajectoylength,x,y,w,h,boundingVolumeLength,stepspace,steptime):
    line = subprocess.check_output(['head', '-1', filepath])
    startframe=int(line.split('\t')[1])
    line = subprocess.check_output(['tail', '-1', filepath])
    endframe=int(line.split('\t')[1])
    print startframe,endframe
    for frame in range(startframe,endframe-steptime,steptime):
        trajectory=getTrajectories(filepath,frame,frame+boundingVolumeLength,trajectoylength,x,y,w,h) 
        print trajectory
        f=open(codebookpath)
        codebook=pickle.load(f)
        bow=getBagOfWords(codebook,trajectory)
        print "bow"+str(bow)


def getEvaluations(datasets,save_location):
    for dataset in datasets:
        for dirpath, dirnames, filenames in os.walk(dataset):
            print "dir path"+dirpath
            print "len of the dir"+str(len(dirnames))
            splitstr=str.split(dirpath,"/")
            #print "length of split str"+str(len(splitstr))
            print splitstr
            #checking the directory depth
            full_dtpath_location=str(save_location)+"/"+splitstr[-3]+"/"+splitstr[-1]+"/"
            #looping the file
            for files in filenames:
                dtfilesplit=str(files).split('.')
                dtfile=''
                #constructing the name of the file which would be like "videoname".dt.txt
                for index in range(len(dtfilesplit)-1):
                    dtfile+=dtfilesplit[index]+'.'
                dtfile+='txt'
                full_dtfile_location=full_dtpath_location+dtfile
                print full_dtfile_location
                #reading the matfile so that we can pass the ground truths to find bounded trajectories
                gt_file=os.path.join(dirpath,files)
                print "reading file "+str(gt_file)
                f=tables.openFile(gt_file)
                x1=int(f.root.bb[0][0])
                y1=int(f.root.bb[1][0])
                x2=int(f.root.bb[2][0])
                y2=int(f.root.bb[3][0])
                x=x1
                y=y1
                #since our function accept width and height instead of x2,y2 ,constructing
                #width and height from the cordinates
                w=x2-x1
                h=y2-y1
                startframe=int(f.root.start_frm[0][0])
                endframe=int(f.root.end_frm[0][0])
                stepspace=3
                steptime=5
                trajectoyLength=15
                boundingVolumeLength=endframe-startframe
                codebookpath='/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/codebooks/codebook100pickle.txt'
                getScoresForVideo(full_dtfile_location,codebookpath,trajectoyLength,x,y,w,h,boundingVolumeLength,stepspace,steptime)
                print x,y,w,h,startframe,endframe
       

if __name__=="__main__":
    datasets=('/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/groundtruth/MSR2','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/groundtruth/KTH')
    results_location='/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results'
    #getEvaluations(datasets,results_location)
    eg_filepath='/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/MSR2/boxing/10.avi.txt'
    stepspace=3
    steptime=5
    trajectoyLength=15
    codebookpath='/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/codebooks/codebook100pickle.txt'
    print getTrajectories(eg_filepath,15,400,trajectoyLength,23,45,70,90) 
        
