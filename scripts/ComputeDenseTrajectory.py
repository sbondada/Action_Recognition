import os
import subprocess

def computeDenseTrajectory(location2save):
    for dirpath, dirnames, filenames in os.walk(location2save):
        print "dir path"+dirpath
        print "len of the dir"+str(len(dirnames))
        splitstr=str.split(dirpath,"/")
        #print "length of split str"+str(len(splitstr))
        print splitstr
        for files in filenames :
            print files
            if len(splitstr):
                print "splitstr > 3 block"
                p=subprocess.Popen(['./../release/DenseTrack',os.path.join(dirpath,files)],stdout=subprocess.PIPE)
                (output,error)=p.communicate()
                #print output
                f=open('../data/results/'+splitstr[2]+'/'+splitstr[4]+'/'+files+'.txt','w');
                f.write(output);
                f.close
            else:
                print "else block"
                p=subprocess.Popen(['./../release/DenseTrack',os.path.join(dirpath,files)],stdout=subprocess.PIPE)
                (output,error)=p.communicate()
                #print output
                f=open('../data/results/'+splitstr[2]+'/'+files+'.txt','w');
                f.write(output);
                f.close
            #print files

if __name__=='__main__':
    computeDenseTrajectory('../data/MSR2/videos') 
