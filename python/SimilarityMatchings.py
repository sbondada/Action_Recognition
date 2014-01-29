import math
import numpy as np
import scipy.io
import os

def chiSquare(observed,expected):
    sumchi=0
    for i in range(len(observed)):
        if expected[i]!=0:
            sumchi+=float(math.pow(observed[i]-expected[i],2))/expected[i]
    return sumchi

def constructData(fileLocationList):
    #Test construction is exactly similar to constructTrainInputdata
    inputData=[]
    for fileLocation in fileLocationList:
        for dirpath, dirnames, filenames in os.walk(fileLocation):
            for files in filenames:
                bow=scipy.io.loadmat(os.path.join(dirpath,files))
                tempList=np.ndarray.tolist(bow['bagofwords'])
                bowList=[x[0] for x in tempList] 
                inputData.append(bowList) 
    return inputData


def performSimilarityMatching(sourceMatchList,destMatchList): 
    matchingList=[]
    for i in range(len(sourceMatchList)):
        similarityList=[]       
        for j in range(len(destMatchList)):
            chi2sim=chiSquare(sourceMatchList[i],destMatchList[j])
            similarityList.append(chi2sim)
        matchingList.append(similarityList)
    return matchingList 

def printResults(matchingList):
    for itemList in matchingList:
        print itemList
        print "\n" 

if __name__=='__main__':
    sourceFileLocationList=['/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/KTH/boxing/seq2_bow','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/KTH/handwaving/seq2_bow','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/KTH/handclapping/seq2_bow']
    destFileLocationList=['/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/MSR2/boxing/seq2_bow','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/MSR2/handwaving/seq2_bow','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/MSR2/handclapping/seq2_bow']
    sourceMatchList=constructData(sourceFileLocationList)
    destMatchList=constructData(destFileLocationList)
    matchingList=performSimilarityMatching(sourceMatchList,destMatchList)
    printResults(matchingList)
