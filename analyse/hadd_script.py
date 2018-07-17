import os
from argparse import ArgumentParser
#import ROOT

parser = ArgumentParser()
parser.add_argument('--indir', default="FILLME",help='name of SelectedSamples directory')
args = parser.parse_args()


allfiles = [i for i in os.listdir(args.indir) if ".root" in i]
unique_files = {}
for f in allfiles:
    if not "_events_" in f: continue
    f_tmp = f.split(".root")[0]
    if "_events_" in f_tmp: f_tmp = f_tmp.split("_events_")[0]
    if f_tmp in unique_files: unique_files[f_tmp].append(f)
    else: unique_files[f_tmp] = [f]

for target,files in unique_files.iteritems():
    if target+".root" in allfiles:
        print "WARNING: File %s exists already in %s. Skipping this file"%(target+".root",args.indir)
        continue
    cmd = "hadd %s.root"%(args.indir+"/"+target)
    for ff in files:
        cmd += " %s"%(args.indir+"/"+ff)
    print cmd
    os.system(cmd)
    
    # remove individual files
    if not target+".root" in os.listdir(args.indir):
        print "WARNING: File %s can not be found in %s and the original files will therefore not be deleted!!"%(target+".root",args.indir)
        continue
    rm_cmd = "rm %s_events_*"%(args.indir+"/"+target)
    print rm_cmd
    os.system(rm_cmd)