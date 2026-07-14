#BSUB -q short -R rusage[mem=16384] -R affinity[thread*8]
ml awscli
aws s3 sync /home/projects/yonina/data/OpenH-RF/thyroid_full/subjects_info_new s3://openh-rf-submissions/weizmann-sampl/
