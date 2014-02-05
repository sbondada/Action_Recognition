import os
import random
from scipy.cluster.vq import kmeans,vq
import time
from numpy import array
import pickle

'''
this file has the implementation for construction of the code book with two functions to do the tasks
randomLineSelection-this file accepts 3 parameters
    noOfFiles-this is the total no files it has to select from all the directory list
    from each its divided by the directories in the list
    noOfLinesperFile-this specifies how many random bounded trajectories has to be selected
    fileLocationList-this is the list of places where different action classes bounded trajectories are present

getBagOfWords-this takes the codebook constructed in the main method from the random bounded trajectories and create
the file based on the binsize provided
'''


def randomLineSelection(noOfFiles,noOfLinesperFile,fileLocationList):
    fileData=[]
    #loop the filelocation list
    for fileLocation in fileLocationList:
        print fileLocation
        for dirpath, dirnames, filenames in os.walk(fileLocation):
            inc=0
            #looping the files names untill the nooffiles and then the loop is breaked
            for files in filenames:
                filepath=os.path.join(dirpath,files)
                print filepath
                f=open(filepath)
                lines=f.read().splitlines()
                if inc<(noOfFiles/len(fileLocationList)) and lines!=[]:
                    for i in range(noOfLinesperFile):
                        myline=random.choice(lines)
                        linesplit=myline.split('\t')
                        #the code book is constructed with the data for the relative trajectories and the 
                        # mixture of other descriptors
                        floatlinesplit=[float(x) for x in linesplit[41:] if x!='']
                        fileData.append(floatlinesplit)
                    inc+=1
                else:
                    f.close()
                    break
    return fileData

def getBagOfWords(codebook,filename,binSize):
    f=open(filename)
    data=[]
    for line in f:
        linesplit=line.split('\t')
        #print linesplit
        floatlinesplit=[float(x) for x in linesplit[41:] if x!='\n']
        data.append(floatlinesplit)
    #here it accepts the codebook and the trajectory to find to which bin this trajectory is close and assign the index
    #of the code book
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


if __name__=="__main__":
    fileLocationList=['/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/MSR2/boxing/seq2','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/MSR2/handwaving/seq2','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/MSR2/handclapping/seq2','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/KTH/boxing/seq2','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/KTH/handwaving/seq2','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/KTH/handclapping/seq2']
   # fileLocationList=['/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/MSR2/boxing/seq2_double','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/MSR2/handwaving/seq2_double','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/MSR2/handclapping/seq2_double','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/KTH/boxing/seq2','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/KTH/handwaving/seq2','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/KTH/handclapping/seq2']
   #fileLocationList=['/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/MSR2/boxing/seq2_double','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/MSR2/handwaving/seq2_double','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/MSR2/handclapping/seq2_double']
    noOfFiles=500
    noOfLinesperFile=400
    binSize=400
    randomLines=randomLineSelection(noOfFiles,noOfLinesperFile,fileLocationList)
    codebook,_ = kmeans(array(randomLines),binSize)
    #bow=getBagOfWords(codebook,'/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/MSR2/boxing/seq2/10.dt.txt',binSize)
    #print bow
    #codefile=open('/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/codebook.pickle.txt','w')
    codefile=open('/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/codebook400pickle.txt','w')
    pickle.dump(codebook,codefile)

