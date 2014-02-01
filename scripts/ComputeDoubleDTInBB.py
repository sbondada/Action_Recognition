import sys
#including the files in the python path so that when we could import the function from a file 
sys.path.insert(0,'/home/kaushal/Documents/projects/dense_trajectory_and_codebook/python/')
import tables
import GetDoubleBoxedTrajectory as gdbt
import scipy.io
import os

'''
this script is to run and get the bounded trajectories for each dataset
it has one functions which are responsible for that
computeFTinBB accept the location of the ground truth and the location where to 
save the file
'''


def computeDTinBB(gt_location,save_location):
    for dirpath, dirnames, filenames in os.walk(gt_location):
        print "dir path"+dirpath
        print "len of the dir"+str(len(dirnames))
        splitstr=str.split(dirpath,"/")
        #print "length of split str"+str(len(splitstr))
        print splitstr
        #checking the directory depth
        if len(splitstr)==9:
            full_dtpath_location=str(save_location)+"/"+splitstr[-3]+"/"
            complete_save_location=str(save_location)+"/"+splitstr[-3]+"/seq2_double/"
        else:
            full_dtpath_location=str(save_location)+"/"+splitstr[-3]+"/"+splitstr[-1]+"/"
            complete_save_location=str(save_location)+"/"+splitstr[-3]+"/"+splitstr[-1]+"/seq2_double/"
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
            x=x1-(0.5*(w))
            y=y1-(0.5*(h))
            w=w+(w)
            h=h+(h)
            startframe=int(f.root.start_frm[0][0])
            endframe=int(f.root.end_frm[0][0])
            gdbt.getTrajectories(full_dtfile_location,startframe,endframe,15,x,y,w,h)
            #print x,y,w,h,startframe,endframe
            
if __name__=='__main__':
    computeDTinBB('/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/groundtruth/MSR2','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results')
