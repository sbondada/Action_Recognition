import os
import numpy as np
import scipy.io
from sklearn import svm 
import pickle

def constructInputdata(fileLocationList,classLabelList):
    inc=-1
    inputData=[]
    inputClassLabel=[]
    for fileLocation in fileLocationList:
        inc+=1
        for dirpath, dirnames, filenames in os.walk(fileLocation):
            for files in filenames:
                bow=scipy.io.loadmat(os.path.join(dirpath,files))
                tempList=np.ndarray.tolist(bow['bagofwords'])
                bowList=[x[0] for x in tempList] 
                inputData.append(bowList) 
                inputClassLabel.append(classLabelList[inc])
    return (inputData,inputClassLabel)

def constructModel(inputData,inputClassLabel):
    clf=svm.SVC()
    clf.fit(inputData,inputClassLabel)
    return clf

if __name__=="__main__":
    fileLocationList=['/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/KTH/boxing/seq2_bow','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/KTH/handwaving/seq2_bow','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/KTH/handclapping/seq2_bow']
    classLabelList=[1,2,3]
    inputInfo=constructInputdata(fileLocationList,classLabelList)
    clf=constructModel(inputInfo[0],inputInfo[1])
    print clf
    f=open('/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/KTH/model.pickle.txt','w')
    pickle.dump(clf,f)
