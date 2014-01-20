%load('../data/groundtruth/MSR2/seq2/gt_handwaving.mat');
%load('../data/groundtruth/MSR2/seq2/gt_handclapping.mat');
load('../data/groundtruth/MSR2/seq2/gt_boxing.mat');

%a=size(gt_handwaving);
%a=size(gt_handclapping);
a=size(gt_boxing);
%file2save='../data/groundtruth/MSR2/seq2/handwaving/';
%file2save='../data/groundtruth/MSR2/seq2/handclapping/';
file2save='../data/groundtruth/MSR2/seq2/boxing/';
for i=1:a(1),
   %filename=strcat(file2save,int2str(gt_handwaving(i,1)),'.avi.mat');
   %filename=strcat(file2save,int2str(gt_handclapping(i,1)),'.avi.mat');
   filename=strcat(file2save,int2str(gt_boxing(i,1)),'.avi.mat');
   %vidname=strcat(int2str(gt_handwaving(i,1)),'.avi');
   %vidname=strcat(int2str(gt_handclapping(i,1)),'.avi');
   vidname=strcat(int2str(gt_boxing(i,1)),'.avi');
   %bb=gt_handwaving(i,2:5);
   %bb=gt_handclapping(i,2:5);
   bb=gt_boxing(i,2:5);
   %start_frm=gt_handwaving(i,6);
   %start_frm=gt_handclapping(i,6);
   start_frm=gt_boxing(i,6);
   %end_frm=gt_handwaving(i,7);
   %end_frm=gt_handclapping(i,7);
   end_frm=gt_boxing(i,7);
   save(filename,'bb','start_frm','end_frm','vidname');
end