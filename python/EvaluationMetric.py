import os
from scipy.cluster.vq import kmeans,vq
from sklearn.kernel_approximation import  AdditiveChi2Sampler
from sklearn import svm
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
            #print condition 
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


def checkifPositive(boundSample,groundTruth,threshold):
    return True 

def getScoresForVideo(actionClass,filepath,modelpath,codebookpath,trajectoylength,x,y,w,h,startframe,endframe,stepspace,steptime):
    videowidth=160
    videoheight=120
    boundingVolumeLength=endframe-startframe
    actionPosition=actionClass-1
    groundTruth=[x,y,w,h,startframe,endframe]
    line = subprocess.check_output(['head', '-1', filepath])
    startframe=int(line.split('\t')[1])
    line = subprocess.check_output(['tail', '-1', filepath])
    endframe=int(line.split('\t')[1])
    f=open(codebookpath)
    codebook=pickle.load(f)
    modelfile=open(modelpath)
    clf=pickle.load(modelfile)
    positiveScores=[]
    print startframe,endframe
    for frame in range(startframe,endframe-steptime,steptime):
        for xstep in range(videowidth-(w+stepspace)):
            for ystep in range(videoheight-(h+stepspace)):
                boundSample=[xstep,ystep,w,h,frame,frame+boundingVolumeLength]    
                if checkifPositive(boundSample,groundTruth,0.2):
                        trajectory=getTrajectories(filepath,frame,frame+boundingVolumeLength,trajectoylength,xstep,ystep,w,h) 
                        bow=getBagOfWords(codebook,trajectory)
                        chi2_feature= AdditiveChi2Sampler(sample_steps=3)
                        testData=chi2_feature.fit_transform(bow)
                        score=clf.decision_function(testData)[0][actionPosition]
                        predictData=clf.predict(testData)
                        print predictData                        
                        positiveScores.append([score,predictData])
                        print score
    return positiveScores

def getTPFP(positiveScores,thrseholdList,actionClass):
    TPList=[]
    FPList=[]
    for threshold in thrseholdList:
        tempTP=0
        tempFP=0
        for score,predictdata in positiveScores:
            if score>threshold and predictdata==actionClassa:
               tempTP+=1 
            if score<threshold and predictdata!=actionClass:
                tempFP+=1
        TPList.append(tempTP)
        FPList.append(tempFP)
    return [TPList,FPList]  

def getEvaluations(actionlocationset,save_location):
    TPFP=[]
    for actionlocation in actionlocationset:
        actionClass=0
        for dirpath, dirnames, filenames in os.walk(actionlocation):
            print "dir path"+dirpath
            print "len of the dir"+str(len(dirnames))
            splitstr=str.split(dirpath,"/")
            #print "length of split str"+str(len(splitstr))
            print splitstr
            #checking the directory depth
            full_dtpath_location=str(save_location)+"/"+splitstr[-3]+"/"+splitstr[-1]+"/"
            if len(splitstr)==11:
                actionClass+=1
            positiveScores=[]
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
                thresholdSteps=30
                codebookpath='/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/codebooks/codebook100pickle.txt'
                modelpath='/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/model.pickle.txt'
                positiveScores.extend(getScoresForVideo(actionClass,full_dtfile_location,modelpath,codebookpath,trajectoyLength,x,y,w,h,startframe,endframe,stepspace,steptime))
                #print actionPosition,x,y,w,h,startframe,endframe
            positiveScores.sort(key=lambda x:x[0]) 
            thresholdList=[]
            for i in range(0,len(positiveScores),len(positiveScores)/thresholdSteps):
                thresholdList.append(positiveScores[i][0])
            TPFP.append(getTPFP(positiveScores,thresholdList,actionClass))
    return TPFP    

if __name__=="__main__":
    #datasets=['/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/groundtruth/MSR2','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/groundtruth/KTH']
    testset=['/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/groundtruth/MSR2/seq2/boxing','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/groundtruth/MSR2/seq2/handwaving','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/groundtruth/MSR2/seq2/handclapping']
    results_location='/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results'
    getEvaluations(testset,results_location)


    #testing the code
    '''
    eg_filepath='/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/MSR2/boxing/10.avi.txt'
    stepspace=3
    steptime=5
    trajectoyLength=15
    codebookpath='/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/codebooks/codebook100pickle.txt'
    print getTrajectories(eg_filepath,15,400,trajectoyLength,23,45,70,90) 
    ''' 
