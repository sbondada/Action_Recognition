import os
import subprocess

''' 
this file is a script which based on the video locations creates the dense trajectory features
'''

def computeDenseTrajectory(location2save):
    '''
    here we recursively traverse the folders from the given location and store the required parameters like
    dirpath- directory path     
    dirnames-includes a list of directory name alone not the path
    filenames-includes the list of the name of the files, not the paths
    '''

    for dirpath, dirnames, filenames in os.walk(location2save):
        print "dir path"+dirpath
        print "len of the dir"+str(len(dirnames))
        splitstr=str.split(dirpath,"/")
        #print "length of split str"+str(len(splitstr))
        print splitstr
        #iterate the file list
        for files in filenames :
            print files
            #based on the no of directories depth a particular part of the if is executed
            # 9 is till the videos folder starting from "" to videos 10th folder is action folder
            if len(splitstr)>9:
                p=subprocess.Popen(['/home/kaushal/Documents/projects/dense_trajectory_and_codebook/release/DenseTrack',os.path.join(dirpath,files)],stdout=subprocess.PIPE)
                (output,error)=p.communicate()
                #print output
                f=open('/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/'+splitstr[7]+'/'+splitstr[9]+'/'+files+'.txt','w');
                f.write(output);
                f.close
            else:
                p=subprocess.Popen(['/home/kaushal/Documents/projects/dense_trajectory_and_codebook/release/DenseTrack',os.path.join(dirpath,files)],stdout=subprocess.PIPE)
                (output,error)=p.communicate()
                #print output
                f=open('/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/results/'+splitstr[7]+'/'+files+'.txt','w');
                f.write(output);
                f.close
            #print files

if __name__=='__main__':
    computeDenseTrajectory('/home/kaushal/Documents/projects/dense_trajectory_and_codebook/data/KTH/videos') 
