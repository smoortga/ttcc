import os
import sys
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('--indir', default="FILLME",help='name of BATCH_* directory')
args = parser.parse_args()



if not os.path.isdir(args.indir): 
    print "ERROR: Could not find directory %s"%(args.indir)
    sys.exit(1)
    
indir = os.path.abspath(args.indir)

proc_dict_done = {}
proc_dict_tofinish = {}
proc_dict_failed = {}
proc_list = [indir+"/"+i for i in os.listdir(indir) if os.path.isdir(indir+"/"+i)]
for p in proc_list:
    p_ = p.split("/")[-1].split("_events_")[0]
    proc_dict_done[p_] = 0
    proc_dict_tofinish[p_] = 0
    proc_dict_failed[p_] = 0



for p in proc_list:
    p_ = p.split("/")[-1].split("_events_")[0]
    if not os.path.isfile(p+"/script.stderr"):
        proc_dict_tofinish[p_] += 1
    else:
        file = open(p+"/script.stderr","r") 
        lines = file.readlines()
        failed = False
        for l in lines: 
            if "job killed" in l: failed = True
        if failed:
            proc_dict_failed[p_] += 1
            n1 = p.split("/")[-1].split("_events_")[1].split("_")[0]
            n2 = str(int(p.split("/")[-1].split("_events_")[1].split("_")[1])+1)
            #print "ls ./SELECTED_ttbarSingleLepton_CorrectPUProfile_NeurnalNetworkMatching_WithoutBTagInfo/" + p_+"_events_"+n1+"_"+n2+".root"
            #os.system("ls ./SELECTED_ttbarSingleLepton_CorrectPUProfile_NeurnalNetworkMatching_WithoutBTagInfo/" + p_+"_events_"+n1+"_"+n2+".root")
            
            
        else:
            proc_dict_done[p_] += 1
        file.close()

print "****************"
for proc_name in proc_dict_done.keys():
    print "%s: "%proc_name
    if proc_dict_done[proc_name] > 0: print "\033[92m   DONE : %i\033[0m"%proc_dict_done[proc_name]
    if proc_dict_tofinish[proc_name] > 0:print "\033[93m   TODO : %i\033[0m"%proc_dict_tofinish[proc_name]
    if proc_dict_failed[proc_name] > 0:print "\033[91m   FAIL : %i\033[0m"%proc_dict_failed[proc_name]
    print "****************"
