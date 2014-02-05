import math 
import numpy as np
import scipy.io
import os

def chiSquare(observed,expected):
    sumchi=0
    for i in range(len(observed)):
        sumchi+=float(math.pow(observed[i]-expected[i],2))/(observed[i]+expected[i]+np.finfo(float).eps)
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
    #KTHFileLocationList=['/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/KTH/boxing/seq2_bow','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/KTH/handwaving/seq2_bow','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/KTH/handclapping/seq2_bow']
    #MSRFileLocationList=['/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/MSR2/boxing/seq2_bow','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/MSR2/handwaving/seq2_bow','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/MSR2/handclapping/seq2_bow']
    MSRDoubleFileLocationList=['/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/MSR2/boxing/seq2_400_bow','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/MSR2/handwaving/seq2_400_bow','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/MSR2/handclapping/seq2_400_bow']
    #KTHMatchList=constructData(KTHFileLocationList)
    #MSRMatchList=constructData(MSRFileLocationList)
    MSRDoubleMatchList=constructData(MSRDoubleFileLocationList)
    #MSRKTHmachingList=performSimilarityMatching(MSRMatchList,KTHMatchList)
    #MSRMSRmatchingList=performSimilarityMatching(MSRMatchList,MSRMatchList)
    MSRDMSRDmatchingList=performSimilarityMatching(MSRDoubleMatchList,MSRDoubleMatchList)
    #KTHKTHmatchingList=performSimilarityMatching(KTHMatchList,KTHMatchList) 
    #matchDict={"MSR_KTH":MSRKTHmachingList,"MSR_MSR":MSRMSRmatchingList,"KTH_KTH":KTHKTHmatchingList}
    matchDict={"MSRD_MSRD":MSRDMSRDmatchingList}
    #bowDict={"KTH":KTHMatchList,"MSR": MSRMatchList,"MSR_Double":MSRDoubleMatchList}
    bowDict={"MSR_400":MSRDoubleMatchList}
    scipy.io.savemat("../data/results/400matchinglist.mat",matchDict)
    scipy.io.savemat("../data/results/bow400List.mat",bowDict)
