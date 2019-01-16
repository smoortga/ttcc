import os
from argparse import ArgumentParser
import sys
#import ROOT

parser = ArgumentParser()
parser.add_argument('--indir', default="FILLME",help='name of SelectedSamples directory')
args = parser.parse_args()


os.system("voms-proxy-init --voms cms --valid 192:0")
os.system("cp $X509_USER_PROXY /user/$USER/")

if args.indir.endswith("/"): 
    indir = args.indir[:-1]
else:
    indir= args.indir


tag=indir.split("/")[-1].split("OUTPUT_")[1]
print tag
localdir = os.getcwd()+"/OUTPUT_"+tag+"/hadd_localgrid"
print localdir
if not os.path.isdir(localdir): 
    os.mkdir(localdir)
else:
    print "HADD DIR ALREADY EXISTS!!! PLEASE FIRST DELETE IT!!!"
    sys.exit(1)


allfiles = [i for i in os.listdir(indir) if ".root" in i]
unique_files = {}
for f in allfiles:
    if not "_events_" in f: continue
    f_tmp = f.split(".root")[0]
    if "_events_" in f_tmp: f_tmp = f_tmp.split("_events_")[0]
    if f_tmp in unique_files: unique_files[f_tmp].append(f)
    else: unique_files[f_tmp] = [f]


f_bigsub = open(localdir+"/bigsub.txt", 'w')

for sample,files in unique_files.iteritems():
    print sample
    if not os.path.isdir(localdir+"/"+sample): os.mkdir(localdir+"/"+sample)

    ff_ = open(localdir+"/"+sample+"/launch.sh", 'w')
    ff_.write("#!/bin/bash \n")
    ff_.write("pwd=$PWD \n")  
    ff_.write("source $VO_CMS_SW_DIR/cmsset_default.sh \n")                                                                                                                                                           
    ff_.write("cd /storage_mnt/storage/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src \n")                                                                                                                                                          
    ff_.write("eval `scram runtime -sh` \n")                                                                                                                                           
    ff_.write("cd $pwd \n")  
    ff_.write("export X509_USER_PROXY=/user/$USER/x509up_u$(id -u $USER) \n")
    
    if sample+".root" in allfiles:
       print "WARNING: File %s exists already in %s. Skipping this file"%(sample+".root",indir)
       continue
    cmd = "hadd %s.root"%("$TMPDIR/"+sample)
    for ff in files:
       cmd += " %s"%(indir+"/"+ff)
    ff_.write("%s \n"%cmd)
    ff_.write("gfal-copy file://$TMPDIR/"+sample+".root srm://maite.iihe.ac.be:8443"+indir+"/"+sample+".root \n")
    for fff in files:
        ff_.write("gfal-rm srm://maite.iihe.ac.be:8443%s/%s \n"%(indir,fff))
    ff_.close()
    
    f_bigsub.write("qsub -q localgrid -o %s/script.stdout -e %s/script.stderr -l walltime=02:00:00 %s/launch.sh \n"%(localdir+"/"+sample,localdir+"/"+sample,localdir+"/"+sample))

f_bigsub.close()

print "Submit via: '\033[92mbig-submission %s/bigsub.txt\033[0m'"%(localdir)
print "Use '\033[94mqstat -u $USER\033[0m' to monitor samples"
print "use '\033[94mfor j in $(qselect -u $USER);do timeout 3 qdel -a $j;done\033[0m' to delete all your jobs"

text = raw_input("Would you like to submit this now? (y/n): ")
if text == "y" or text == "Y" or text == "yes" or text == "Yes" or text == "YES":
    os.system("big-submission %s/bigsub.txt"%(localdir))
    
else:
    print "Not yet starting any submission... ending..."

#for target,files in unique_files.iteritems():
#    print "***************** %s ********************"%target
#    if target+".root" in allfiles:
#        print "WARNING: File %s exists already in %s. Skipping this file"%(target+".root",indir)
#        continue
#    cmd = "hadd %s.root"%(tmpdir+"/"+target)
#    for ff in files:
#        cmd += " %s"%(indir+"/"+ff)
#    print cmd
#    os.system(cmd)
#    
#    # check if the output file already exists
#    # if target+".root" in [i for i in os.listdir(indir) if ".root" in i]:
##         print "File already exists in output directory! making a backup first"
##         os.system("gfal-copy srm://maite.iihe.ac.be:8443%s/%s.root srm://maite.iihe.ac.be:8443%s/backup_%s.root"%(indir,target,indir,target))
##         os.system("gfal-rm srm://maite.iihe.ac.be:8443%s/%s.root"%(indir,target))
#        
#    
#    cp_cmd = "gfal-copy file:///user/$USER/%s/%s.root srm://maite.iihe.ac.be:8443%s/"%(tmpdir_fromuser,target,indir)
#    print cp_cmd
#    os.system(cp_cmd)
#    
#    if target+".root" in [i for i in os.listdir(indir) if ".root" in i]:
#        print "Copy was succesful! deleting original files"
#        os.system("rm %s.root"%(tmpdir+"/"+target))
#        for ff in files:
#            print "gfal-rm srm://maite.iihe.ac.be:8443%s/%s"%(indir,ff)
#            os.system("gfal-rm srm://maite.iihe.ac.be:8443%s/%s"%(indir,ff))
#    else:
#        print "ERROR: something went wrong during file transfer... moving on!"
#    
#    print "*******************************************"
#    print " "
#
#if len([i for i in os.listdir(tmpdir)]) != 0:
#    print "ERROR: TMPDIR_hadd is not empty! not deleting it"
#else:
#    os.system("rmdir %s"%tmpdir)

    # remove individual files
#     if not target+".root" in os.listdir(indir):
#         print "WARNING: File %s can not be found in %s and the original files will therefore not be deleted!!"%(target+".root",indir)
#         continue
#     rm_cmd = "rm %s_events_*"%(indir+"/"+target)
#     print rm_cmd
#     os.system(rm_cmd)
