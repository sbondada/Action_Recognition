import sys
sys.path.insert(0,'/home/kaushal/Documents/projects/dense_trajectory_and_codebook/python/')
import tables
import GetBoxedTrajectory as gbt
import scipy.io
import os

def computeDTinBB(gt_location,save_location):
    for dirpath, dirnames, filenames in os.walk(gt_location):
        print "dir path"+dirpath
        print "len of the dir"+str(len(dirnames))
        splitstr=str.split(dirpath,"/")
        #print "length of split str"+str(len(splitstr))
        print splitstr
        if len(splitstr)==9:
            full_dtpath_location=str(save_location)+"/"+splitstr[-3]+"/"
            complete_save_location=str(save_location)+"/"+splitstr[-3]+"/seq2/"
        else:
            full_dtpath_location=str(save_location)+"/"+splitstr[-3]+"/"+splitstr[-1]+"/"
            complete_save_location=str(save_location)+"/"+splitstr[-3]+"/"+splitstr[-1]+"/seq2/"
        for files in filenames:
            dtfilesplit=str(files).split('.')
            dtfile=''
            for index in range(len(dtfilesplit)-1):
                dtfile+=dtfilesplit[index]+'.'
            dtfile+='txt'
            full_dtfile_location=full_dtpath_location+dtfile
            print full_dtfile_location
            gt_file=os.path.join(dirpath,files)
            f=tables.openFile(gt_file)
            x1=int(f.root.bb[0][0])
            y1=int(f.root.bb[1][0])
            x2=int(f.root.bb[2][0])
            y2=int(f.root.bb[3][0])
            if x1>x2 and y1<y2:
                x=x2
                y=y2
                w=x1-x2
                h=y2-y1
            else:
                x=x1
                y=y1
                w=x2-x1
                h=y1-y2
            startframe=int(f.root.start_frm[0][0])
            endframe=int(f.root.end_frm[0][0])
            gbt.getTrajectories(full_dtfile_location,startframe,endframe,15,x,y,w,h)
            
if __name__=='__main__':
    computeDTinBB('/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/groundtruth','/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results')
