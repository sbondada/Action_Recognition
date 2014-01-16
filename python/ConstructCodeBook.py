import os
import random
from scipy.cluster.vq import kmeans,vq
import time
from numpy import array
import pickle

def randomLineSelection(noOfFiles,noOfLinesperFile,fileLocationList):
    fileData=[]
    for fileLocation in fileLocationList:
        print fileLocation
        for dirpath, dirnames, filenames in os.walk(fileLocation):
            inc=0
            for files in filenames:
                f=open(os.path.join(dirpath,files))
                lines=f.read().splitlines()
                if inc<(noOfFiles/len(fileLocationList)):
                    for i in range(noOfLinesperFile):
                        myline=random.choice(lines)
                        linesplit=myline.split('\t')
                        floatlinesplit=[float(x) for x in linesplit[41:] if x!='']
                        fileData.append(floatlinesplit)
                    inc+=1
                else:
                    f.close()
                    break
    return fileData


if __name__=="__main__":
    fileLocationList=['/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/KTH/boxing/seq2','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/KTH/handwaving/seq2','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/KTH/handclapping/seq2']
    noOfFiles=10
    noOfLinesperFile=200
    binSize=10
    randomLines=randomLineSelection(noOfFiles,noOfLinesperFile,fileLocationList)
    codebook,_ = kmeans(array(randomLines),binSize)
    codefile=open('/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/KTH/codebook.pickle.txt','w')
    pickle.dump(codebook,codefile)

