import os
from argparse import ArgumentParser
import sys
#import ROOT

parser = ArgumentParser()
parser.add_argument('--indir', default="FILLME",help='name of SelectedSamples directory')
args = parser.parse_args()


if args.indir.endswith("/"): 
    indir = args.indir[:-1]
else:
    indir= args.indir



#
# Create tempdir to hadd here
#

if not os.path.isdir("%s/TMPDIR_hadd"%os.getcwd()): 
    os.system("mkdir %s/TMPDIR_hadd"%os.getcwd())
    print "Created %s/TMPDIR_hadd for temporary storage"%os.getcwd()
    
tmpdir="%s/TMPDIR_hadd"%os.getcwd()
tmpdir_fromuser = tmpdir.split("/smoortga/")[1]


allfiles = [i for i in os.listdir(indir) if ".root" in i]
unique_files = {}
for f in allfiles:
    if not "_events_" in f: continue
    f_tmp = f.split(".root")[0]
    if "_events_" in f_tmp: f_tmp = f_tmp.split("_events_")[0]
    if f_tmp in unique_files: unique_files[f_tmp].append(f)
    else: unique_files[f_tmp] = [f]
 

for target,files in unique_files.iteritems():
    print "***************** %s ********************"%target
    if target+".root" in allfiles:
        print "WARNING: File %s exists already in %s. Skipping this file"%(target+".root",indir)
        continue
    cmd = "hadd %s.root"%(tmpdir+"/"+target)
    for ff in files:
        cmd += " %s"%(indir+"/"+ff)
    print cmd
    os.system(cmd)
    
    # check if the output file already exists
    # if target+".root" in [i for i in os.listdir(indir) if ".root" in i]:
#         print "File already exists in output directory! making a backup first"
#         os.system("gfal-copy srm://maite.iihe.ac.be:8443%s/%s.root srm://maite.iihe.ac.be:8443%s/backup_%s.root"%(indir,target,indir,target))
#         os.system("gfal-rm srm://maite.iihe.ac.be:8443%s/%s.root"%(indir,target))
        
    
    cp_cmd = "gfal-copy file:///user/$USER/%s/%s.root srm://maite.iihe.ac.be:8443%s/"%(tmpdir_fromuser,target,indir)
    print cp_cmd
    os.system(cp_cmd)
    
    if target+".root" in [i for i in os.listdir(indir) if ".root" in i]:
        print "Copy was succesful! deleting original files"
        os.system("rm %s.root"%(tmpdir+"/"+target))
        for ff in files:
            print "gfal-rm srm://maite.iihe.ac.be:8443%s/%s"%(indir,ff)
            os.system("gfal-rm srm://maite.iihe.ac.be:8443%s/%s"%(indir,ff))
    else:
        print "ERROR: something went wrong during file transfer... moving on!"
    
    print "*******************************************"
    print " "

if len([i for i in os.listdir(tmpdir)]) != 0:
    print "ERROR: TMPDIR_hadd is not empty! not deleting it"
else:
    os.system("rmdir %s"%tmpdir)

    # remove individual files
#     if not target+".root" in os.listdir(indir):
#         print "WARNING: File %s can not be found in %s and the original files will therefore not be deleted!!"%(target+".root",indir)
#         continue
#     rm_cmd = "rm %s_events_*"%(indir+"/"+target)
#     print rm_cmd
#     os.system(rm_cmd)