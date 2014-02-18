import os
import pickle
import sys
sys.path.append('/home/kaushal/Documents/projects/dense_trajectory_and_codebook/python/')
import ConstructRefinedCodebook as crcb
import scipy.io
'''
this file is a script which runs all the location list to generate the bagofwords at each
location using the function called 
computeBagOfWords-which accepts codebook file name ,location list and bin size
'''


def computeBagOfWords(codebookList,inputLocationList,binsizeList):
    for dt_location in inputLocationList:
        #constructing the directory path to the files to be saved
        dt_locsplit=dt_location.split('/')
        tempsavelocation=''
        for i in range(len(dt_locsplit)-1):
            tempsavelocation+=dt_locsplit[i]+'/'
        tempsavelocation+='seq2_refined_100_bow/'       
        print tempsavelocation
        for dirpath, dirnames, filenames in os.walk(dt_location):  
            for files in filenames:
                filepath=os.path.join(dirpath,files)
                print filepath
                bagofwords=crcb.getBagOfWords(codebookList,filepath,binsizeList)
                #constructing a dict so that the bagofwords can be stored in .mat file
                bowdict={'bagofwords':bagofwords}
                #constructing the file name 
                filenamesplit=files.split('.') 
                filenamesplit[-2]='bow' 
                filenamesplit[-1]='mat'
                bowfilename=''
                for i in range(len(filenamesplit)-1): 
                    bowfilename+=filenamesplit[i]+'.'
                bowfilename+=filenamesplit[-1]
                #merging the directory path and filename
                filesavelocation=tempsavelocation+bowfilename
                #saving the file as a mat file
                scipy.io.savemat(filesavelocation,bowdict)


if __name__=="__main__":

    inputLocationList=['/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/MSR2/boxing/seq2','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/MSR2/handwaving/seq2','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/MSR2/handclapping/seq2','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/KTH/boxing/seq2','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/KTH/handwaving/seq2','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/KTH/handclapping/seq2']

    binSizeList=[25,25,25,25,25]
    codebookLocationList=['/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/codebooks/refined_codebook/100/Trajcodebook100pickle.txt','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/codebooks/refined_codebook/100/HOGcodebook100pickle.txt','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/codebooks/refined_codebook/100/HOFcodebook100pickle.txt','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/codebooks/refined_codebook/100/MBHxcodebook100pickle.txt','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/codebooks/refined_codebook/100/MBHycodebook100pickle.txt']

    codebookList=[]
    for location in codebookLocationList:
        codebookList.append(pickle.load(open(location)))

    computeBagOfWords(codebookList,inputLocationList,binSizeList)
