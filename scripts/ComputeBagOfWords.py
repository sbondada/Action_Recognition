import os
import pickle
import sys
sys.path.append('/home/kaushal/Documents/projects/dense_trajectory_and_codebook/python/')
import ConstructCodeBook as ccb
import scipy.io

def computeBagOfWords(codefile,inputLocationList,binSize):
    f=open(codefile)
    codebook=pickle.load(f)
    for dt_location in inputLocationList:
        dt_locsplit=dt_location.split('/')
        tempsavelocation=''
        for i in range(len(dt_locsplit)-1):
            tempsavelocation+=dt_locsplit[i]+'/'
        tempsavelocation+='seq2_bow/'       
        print tempsavelocation
        for dirpath, dirnames, filenames in os.walk(dt_location):  
            for files in filenames:
                bagofwords=ccb.getBagOfWords(codebook,os.path.join(dirpath,files),binSize)
                bowdict={'bagofwords':bagofwords}
                filenamesplit=files.split('.') 
                filenamesplit[-2]='bow' 
                filenamesplit[-1]='mat'
                bowfilename=''
                for i in range(len(filenamesplit)-1): 
                    bowfilename+=filenamesplit[i]+'.'
                bowfilename+=filenamesplit[-1]
                filesavelocation=tempsavelocation+bowfilename
                scipy.io.savemat(filesavelocation,bowdict)


if __name__=="__main__":
    inputLocationList=['/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/KTH/boxing/seq2','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/KTH/handwaving/seq2','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/KTH/handclapping/seq2']
    computeBagOfWords('/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/KTH/codebook.pickle.txt',inputLocationList,10)
