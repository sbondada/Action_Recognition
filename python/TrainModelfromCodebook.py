import os
import numpy as np
import scipy.io
from sklearn import svm 
import pickle

'''
the file basically constructs the data abropriate for training and testing using svm
has 5 functions
constructTrainInputData-accepts directory location list and classlabel list to construct a 
ndarray of bagofwords and ndarrray of classlabels
ConstructModel-accepts the ndarray of bagofwords and classlabel and return the trained model
of svm
constructTestInputData-accepts the test directory list to construct a ndarray of bagofwords
calculateAccuracy-accepts groundtruth class labels and predicted class labels and returns the 
acccuracy of the system
'''


def constructTrainInputdata(fileLocationList,classLabelList):
    inc=-1
    inputData=[]
    inputClassLabel=[]
    #looping the file location
    for fileLocation in fileLocationList:
        inc+=1
        for dirpath, dirnames, filenames in os.walk(fileLocation):
            for files in filenames:
                #reading a matfile of v7
                bow=scipy.io.loadmat(os.path.join(dirpath,files))
                #constructing a list return value is of type [[],[]] 
                tempList=np.ndarray.tolist(bow['bagofwords'])
                #make list of list to list ,returns [ , ]
                bowList=[x[0] for x in tempList] 
                inputData.append(bowList) 
                inputClassLabel.append(classLabelList[inc])
    return (inputData,inputClassLabel)

def constructModel(inputData,inputClassLabel):
    #clf=svm.LinearSVC()
    clf=svm.SVC()
    clf.fit(inputData,inputClassLabel)
    return clf

def constructTestInputdata(fileLocationList):
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

def calculateAccuracy(groundtruth,predictedValue):
    inc=0
    #checking where the groundtruth is similar to predicted value and keeping the 
    #count of similar values to find accuracy
    for i,j in zip(groundtruth,predictedValue):
        if i==j:
            inc+=1
    accuracy=(float(inc)/len(groundtruth))*100
    return accuracy

if __name__=="__main__":
    trainFileLocationList=['/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/KTH/boxing/seq2_bow','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/KTH/handwaving/seq2_bow','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/KTH/handclapping/seq2_bow']
    classLabelList=[1,2,3]
    testInfo=constructTrainInputdata(trainFileLocationList,classLabelList)
    clf=constructModel(testInfo[0],testInfo[1])
    print clf 
    testFileLocationList=['/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/MSR2/boxing/seq2_bow','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/MSR2/handwaving/seq2_bow','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/MSR2/handclapping/seq2_bow']
    testData=constructTestInputdata(testFileLocationList)
    predictInfo=clf.predict(testData)
    print testInfo[1]
    print predictInfo
    print calculateAccuracy(testInfo[1],predictInfo)
    #f=open('/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/model.pickle.txt','w')
    #pickle.dump(clf,f)
