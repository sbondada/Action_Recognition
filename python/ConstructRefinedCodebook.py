import os
import random
from scipy.cluster.vq import kmeans,vq
import time
from numpy import array
import pickle

def randomLineSelection(noOfFiles,noOfLinesperFile,fileLocationList):
    TrajList=[]
    HOGList=[]
    HOFList=[]
    MBHxList=[]
    MBHyList=[] 
    #loop the filelocation list
    for fileLocation in fileLocationList:
        print "file location"+str(fileLocation)
        for dirpath, dirnames, filenames in os.walk(fileLocation):
            inc=0
            #looping the files names untill the nooffiles and then the loop is breaked
            for files in filenames:
                filepath=os.path.join(dirpath,files)
                print "file path"+str(filepath)
                f=open(filepath)
                lines=f.read().splitlines()
                # this is the breaking condition to break if the file has no lines in the code
                if inc<(noOfFiles/len(fileLocationList)) and lines!=[]:
                    for i in range(noOfLinesperFile):
                        myline=random.choice(lines)
                        linesplit=myline.split('\t')
                        #print linesplit
                        #the code book is constructed with the data for the relative trajectories and the 
                        # mixture of other descriptors
                        Trajlinesplit=[float(x) for x in linesplit[41:71] if x!='']
                        #print (Trajlinesplit)
                        HOGlinesplit=[float(x) for x in linesplit[71:167] if x!='']
                        #print (HOGlinesplit)
                        HOFlinesplit=[float(x) for x in linesplit[167:275] if x!='']
                        #print (HOFlinesplit)
                        MBHxlinesplit=[float(x) for x in linesplit[275:371] if x!='']
                        #print (MBHxlinesplit)
                        MBHylinesplit=[float(x) for x in linesplit[371:467] if x!='']
                        #print (MBHylinesplit)
                        TrajList.append(Trajlinesplit)
                        HOGList.append(HOGlinesplit)
                        HOFList.append(HOFlinesplit)
                        MBHxList.append(MBHxlinesplit)
                        MBHyList.append(MBHylinesplit)
                    inc+=1
                else:
                    f.close()
                    break
    return [TrajList,HOGList,HOFList,MBHxList,MBHyList] 

def getBagOfWords(codebookList,filename,binSize):
    TrajList=[]
    HOGList=[]
    HOFList=[]
    MBHxList=[]
    MBHyList=[]
    f=open(filename)
    for line in f:
        linesplit=line.split('\t')
        #print linesplit
        Trajlinesplit=[float(x) for x in linesplit[41:71] if x!='\n']
        HOGlinesplit=[float(x) for x in linesplit[71:167] if x!='\n']
        HOFlinesplit=[float(x) for x in linesplit[167:275] if x!='\n']
        MBHxlinesplit=[float(x) for x in linesplit[275:371] if x!='\n']
        MBHylinesplit=[float(x) for x in linesplit[371:467] if x!='\n']
        TrajList.append(Trajlinesplit)
        HOGList.append(HOGlinesplit)
        HOFList.append(HOFlinesplit)
        MBHxList.append(MBHxlinesplit)
        MBHyList.append(MBHylinesplit)
    featureList=[TrajList,HOGList,HOFList,MBHxList,MBHyList]
    #here it accepts the codebook and the trajectory to find to which bin this trajectory is close and assign the index
    #of the code book
    bagOfWords=[]
    #there is a chance that the file may not have any trajectories which may lead to empty
    #data vector
    for listPos in range(len(featureList)):
        bagOfWordsPerFeature=[0]*binSizeList[listPos]
        if featureList[listPos]!=[]:
            idx,_=vq(array(featureList[listPos]),codebookList[listPos])
            #constructing the dictionary constructing the array of the size of the bins and each having the no of trajectories
            #its closer to
            for indexEle in idx:
                bagOfWordsPerFeature[int(indexEle)]+=1
            #normalizing the individual bow per feature
            bagOfWordsPerFeature=[float(x)/len(idx) for x in bagOfWordsPerFeature]
            print bagOfWordsPerFeature
            print "length"+str(len(bagOfWordsPerFeature))
        bagOfWords.extend(bagOfWordsPerFeature)
    return bagOfWordsPerFeature

if __name__=="__main__":
    '''
    fileLocationList=['/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/MSR2/boxing/seq2','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/MSR2/handwaving/seq2','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/MSR2/handclapping/seq2','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/KTH/boxing/seq2','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/KTH/handwaving/seq2','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/KTH/handclapping/seq2']
    noOfFiles=500
    noOfLinesperFile=400
    binSizeList=[25,25,25,25,25]
    randomFeatureList=randomLineSelection(noOfFiles,noOfLinesperFile,fileLocationList)
    Trajcodebook,_ = kmeans(array(randomFeatureList[0]),binSizeList[0])
    print Trajcodebook
    Trajcodefile=open('/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/codebooks/refined_codebook/100/Trajcodebook100pickle.txt','w')
    pickle.dump(Trajcodebook,Trajcodefile) 
    HOGcodebook,_ = kmeans(array(randomFeatureList[1]),binSizeList[1])
    HOGcodefile=open('/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/codebooks/refined_codebook/100/HOGcodebook100pickle.txt','w')
    pickle.dump(HOGcodebook,HOGcodefile) 
    HOFcodebook,_ = kmeans(array(randomFeatureList[2]),binSizeList[2])
    HOFcodefile=open('/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/codebooks/refined_codebook/100/HOFcodebook100pickle.txt','w')
    pickle.dump(HOFcodebook,HOFcodefile) 
    MBHxcodebook,_ = kmeans(array(randomFeatureList[3]),binSizeList[3])
    MBHxcodefile=open('/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/codebooks/refined_codebook/100/MBHxcodebook100pickle.txt','w')
    pickle.dump(MBHxcodebook,MBHxcodefile) 
    MBHycodebook,_ = kmeans(array(randomFeatureList[4]),binSizeList[4])
    MBHycodefile=open('/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/codebooks/refined_codebook/100/MBHycodebook100pickle.txt','w')
    pickle.dump(MBHycodebook,MBHycodefile) 
    '''
    binSizeList=[25,25,25,25,25]
    codebookLocationList=['/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/codebooks/refined_codebook/100/Trajcodebook100pickle.txt','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/codebooks/refined_codebook/100/HOGcodebook100pickle.txt','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/codebooks/refined_codebook/100/HOFcodebook100pickle.txt','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/codebooks/refined_codebook/100/MBHxcodebook100pickle.txt','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/codebooks/refined_codebook/100/MBHycodebook100pickle.txt']

    codebookList=[]
    for location in codebookLocationList:
        codebookList.append(pickle.load(open(location)))

    bow=getBagOfWords(codebookList,'/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/MSR2/boxing/seq2/54.dt.txt',binSizeList)
    print bow

