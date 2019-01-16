import os
import time
from argparse import ArgumentParser
import ROOT
import pickle

parser = ArgumentParser()
parser.add_argument('--nevents', type=int, default=-1,help='number of events for each sample')
parser.add_argument('--maxneventsperjob', type=int, default=1000000,help='number of events for each sample')
parser.add_argument('--tag', default=time.strftime("%a%d%b%Y_%Hh%Mm%Ss"),help='name of output directory')
args = parser.parse_args()

basedir = "/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/"
workingdir = "/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/phasespace"
nevents_dict_file = workingdir+"/nevents_dict.pkl"

samples = { # format "input-directory":["output-name",number-of-events,"JESsyst(central,Up,Down)","JERsyst(central,Up,Down)"]
    # MC
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/181116_105011/0000/":["TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS.root",args.nevents],
    }


resubmit_buffer = []

if os.path.isfile(nevents_dict_file):
    nevents_dict = pickle.load(open(nevents_dict_file,"rb"))
else:
    nevents_dict = {}

if not os.path.isdir(workingdir+"/OUTPUT_"+args.tag): os.mkdir(workingdir+"/OUTPUT_"+args.tag)
if not os.path.isdir(workingdir+"/OUTPUT_"+args.tag+"/localgrid_"+args.tag): os.mkdir(workingdir+"/OUTPUT_"+args.tag+"/localgrid_"+args.tag)
if not os.path.isdir(workingdir+"/OUTPUT_"+args.tag+"/histograms"): os.mkdir(workingdir+"/OUTPUT_"+args.tag+"/histograms")

for indir, output in samples.iteritems():
    print output[0].split("/")[-1]
    
    
    # splitting of the jobs
    if not os.path.isfile(nevents_dict_file) or args.nevents != -1 or output[0].split("/")[-1].split(".root")[0] not in nevents_dict.keys():
        files = [i for i in os.listdir(indir) if "output_" in i]
        nevts_to_process = output[1]
        chain = ROOT.TChain("FlatTree/tree")
        for f in files:
            chain.Add(indir+"/"+f)
            if (output[1] > 0 and chain.GetEntries() > output[1]): break
        events_in_chain = chain.GetEntries()
        if (output[1]<0): nevts_to_process = events_in_chain
        elif (output[1] < events_in_chain): nevts_to_process = output[1]
        else: nevts_to_process = events_in_chain
        print "number of events: %i"%nevts_to_process
        if args.nevents == -1: nevents_dict[output[0].split("/")[-1].split(".root")[0]] = nevts_to_process
    
    else:
        nevts_to_process = nevents_dict[output[0].split("/")[-1].split(".root")[0]]
        print "number of events: %i"%nevts_to_process
    
    if (args.maxneventsperjob > 0 and nevts_to_process > args.maxneventsperjob):
        eventsList = []
        startEvent = 0
        while (startEvent < nevts_to_process):
            eventsList.append(startEvent)
            startEvent += args.maxneventsperjob
        eventsList.append(nevts_to_process)
        print "Dataset %s was splitted in %i jobs" %(output[0].split("/")[-1],len(eventsList)-1)
        for i in range(len(eventsList)-1):
            local_dir_tmp = workingdir+"/OUTPUT_"+args.tag+"/localgrid_"+args.tag+"/"+output[0].split("/")[-1].split(".")[0]+"_events_"+str(eventsList[i])+"_"+str(eventsList[i+1]-1)
            #dir_tmp = "$TMPDIR/OUTPUT_"+args.tag+"/localgrid_"+args.tag+"/"+output[0].split("/")[-1].split(".")[0]+"_events_"+str(eventsList[i])+"_"+str(eventsList[i+1]-1)
            if not os.path.isdir(local_dir_tmp): os.mkdir(local_dir_tmp)
            ff_ = open(local_dir_tmp+"/launch.sh", 'w')
            ff_.write("#!/bin/bash \n")
            ff_.write("pwd=$PWD \n")  
            ff_.write("source $VO_CMS_SW_DIR/cmsset_default.sh \n")                                                                                                                                                           
            ff_.write("cd /storage_mnt/storage/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src \n")                                                                                                                                                          
            ff_.write("eval `scram runtime -sh` \n")                                                                                                                                           
            ff_.write("cd $pwd \n")  
            ff_.write("cdir=%s \n"%basedir)
            ff_.write("export LD_LIBRARY_PATH=${cdir}:${cdir}/..:$LD_LIBRARY_PATH \n")
            ff_.write("export X509_USER_PROXY=/user/$USER/x509up_u$(id -u $USER) \n")
            ff_.write("cd /storage_mnt/storage/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/phasespace \n")  
            ff_.write("python VisiblePhaseSpace.py --indir=%s --outfile=%s --firstEvt=%i --lastEvt=%i --splitted=1 \n"%(indir,workingdir+"/OUTPUT_"+args.tag+"/histograms/"+output[0].split(".root")[0]+"_events_"+str(eventsList[i])+"_"+str(eventsList[i+1]-1)+".root",eventsList[i], eventsList[i+1]))
            #ff_.write("gfal-mkdir srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/$USER/Analysis/Selection \n")
            #ff_.write("gfal-mkdir srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/$USER/Analysis/Selection/OUTPUT_"+args.tag+" \n") 
            #ff_.write("gfal-copy file://$TMPDIR/"+output[0].split(".root")[0]+"_events_"+str(eventsList[i])+"_"+str(eventsList[i+1]-1)+".root"+" srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/$USER/Analysis/Selection/OUTPUT_"+args.tag+"/"+output[0].split(".root")[0]+"_events_"+str(eventsList[i])+"_"+str(eventsList[i+1]-1)+".root \n")
            ff_.close()
            print "qsub -q localgrid -o %s/script.stdout -e %s/script.stderr -l walltime=04:59:59 %s/launch.sh"%(local_dir_tmp,local_dir_tmp,local_dir_tmp)
            stdout = os.popen("qsub -q localgrid -o %s/script.stdout -e %s/script.stderr -l walltime=04:59:59 %s/launch.sh"%(local_dir_tmp,local_dir_tmp,local_dir_tmp)).read()
            print "SUBMISSION OUTPUT: " + stdout
            print stdout == ""
            if stdout=="":
                print "Adding to resubmitting pipeline"
                resubmit_buffer.append("qsub -q localgrid -o %s/script.stdout -e %s/script.stderr -l walltime=04:59:59 %s/launch.sh"%(local_dir_tmp,local_dir_tmp,local_dir_tmp))
                
    
    else:
        local_dir_tmp = workingdir+"/OUTPUT_"+args.tag+"/localgrid_"+args.tag+"/"+output[0].split("/")[-1].split(".")[0]
        #dir_tmp = "$TMPDIR/OUTPUT_"+args.tag+"/localgrid_"+args.tag+"/"+output[0].split("/")[-1].split(".")[0]
        if not os.path.isdir(local_dir_tmp): os.mkdir(local_dir_tmp)
        ff_ = open(local_dir_tmp+"/launch.sh", 'w')
        ff_.write("#!/bin/bash \n")
        ff_.write("pwd=$PWD \n")  
        ff_.write("source $VO_CMS_SW_DIR/cmsset_default.sh \n")                                                                                                                                                           
        ff_.write("cd /storage_mnt/storage/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src \n")                                                                                                                                                          
        ff_.write("eval `scram runtime -sh` \n")                                                                                                                                           
        ff_.write("cd $pwd \n")  
        ff_.write("cdir=%s \n"%basedir)
        ff_.write("export LD_LIBRARY_PATH=${cdir}:${cdir}/..:$LD_LIBRARY_PATH \n")
        ff_.write("export X509_USER_PROXY=/user/$USER/x509up_u$(id -u $USER) \n")
        ff_.write(workingdir+"/Selection --infiledirectory %s --outfilepath %s --config %s --triggers %s --nevents %i --firstevt %i --lastevt %i --JESsyst %s --JERsyst %s \n"%(indir,"$TMPDIR/"+output[0], configfile , triggerfile, output[1],0,output[1], output[2], output[3]))
        #ff_.write("gfal-mkdir srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/$USER/Analysis/Selection \n")
        #ff_.write("gfal-mkdir srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/$USER/Analysis/Selection/OUTPUT_"+args.tag+" \n")
        #ff_.write("gfal-copy file://$TMPDIR/"+output[0]+" srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/$USER/Analysis/Selection/OUTPUT_"+args.tag+"/"+output[0]+" \n")
        ff_.close()
        print "qsub -q localgrid -o %s/script.stdout -e %s/script.stderr -l walltime=04:59:59 %s/launch.sh"%(workingdir+"/OUTPUT_"+args.tag+"/localgrid_"+args.tag,workingdir+"/OUTPUT_"+args.tag+"/localgrid_"+args.tag,workingdir+"/OUTPUT_"+args.tag+"/localgrid_"+args.tag)
        stdout = os.popen("qsub -q localgrid -o %s/script.stdout -e %s/script.stderr -l walltime=04:59:59 %s/launch.sh"%(workingdir+"/OUTPUT_"+args.tag+"/localgrid_"+args.tag,workingdir+"/OUTPUT_"+args.tag+"/localgrid_"+args.tag,workingdir+"/OUTPUT_"+args.tag+"/localgrid_"+args.tag)).read()
        print "SUBMISSION OUTPUT: " + stdout
        print stdout == ""
        if stdout=="":
            print "Adding to resubmitting pipeline"
            resubmit_buffer.append("qsub -q localgrid -o %s/script.stdout -e %s/script.stderr -l walltime=04:59:59 %s/launch.sh"%(local_dir_tmp,local_dir_tmp,local_dir_tmp))

print resubmit_buffer                
if (len(resubmit_buffer) != 0):
    print "RESUBMITTING FAILED ATTEMPTS"
    while (len(resubmit_buffer) != 0):
        for cmd in resubmit_buffer:
            stdout = os.popen(cmd).read()
            print stdout
            if not (stdout==""): resubmit_buffer.remove(cmd)
        
#if not os.path.isfile(nevents_dict_file) and args.nevents == -1:
pickle.dump(nevents_dict,open(nevents_dict_file,"wb"))

print "Done! use 'qstat -u $USER' to monitor samples"
print "use 'for j in $(qselect -u $USER);do timeout 3 qdel -a $j;done' to delete all your jobs"
