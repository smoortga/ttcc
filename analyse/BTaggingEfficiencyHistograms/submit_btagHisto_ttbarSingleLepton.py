from argparse import ArgumentParser
import sys
import os
import time
from ROOT import gSystem, TFile

def main():

    parser = ArgumentParser()
    parser.add_argument('--indir', default="FILLMEPLEASE",help='directory name of input files')
    parser.add_argument('--infiles', default="*",help='name of input files')
    parser.add_argument('--tag', default=time.strftime("%a%d%b%Y_%Hh%Mm%Ss"),help='name of output directory')
    parser.add_argument('--nevents', type=int, default=-1,help='maximum number of events for each dataset to process')
    parser.add_argument('--nmaxevtsperjob', type=int, default=100000,help='maximum number of events per job (otherwise split)')
    parser.add_argument('--ncpu', type=int, default=-1,help='number of CPU to use in parallel')
#     parser.add_argument('--topmatchingdir', default="FILLME",help='name of training directory')
#     parser.add_argument('--tthfselectordir', default="FILLME",help='name of training directory')
#     parser.add_argument('--reweightingdir', default="FILLME",help='name of training directory')
    args = parser.parse_args()

    workingdir = os.getcwd()

    if not os.path.isdir(workingdir+"/SELECTED_"+args.tag): os.mkdir(workingdir+"/SELECTED_"+args.tag)
    
    # Search for the input directory
    indir = os.path.abspath(args.indir)+"/"
    if not os.path.isdir(indir):
        print "Error: could not find directory '%s'"%indir
        sys.exit(1)
    
    # Take only files defined by args.infiles
    if not args.infiles == "*": 
        filelist = []
        tags = args.infiles.split("*")
        for f in [f for f in os.listdir(indir)]:
            for t in tags:
                if t == "": continue
                if t in f: filelist.append(f)
    else: 
        filelist = [f for f in os.listdir(indir) if not "TTTo" in f and not "ttH" in f and not "TTZ" in f and not "TTW" in f]
    
    # Count number of events in each file
    nevts_dict = {}
    print "Counting number of events in each file"
    for f in filelist:
        tfile = TFile(indir+f,workingdir+"/SELECTED_"+args.tag+"/"+f)
        tree_ = tfile.Get("tree")
        nevts = tree_.GetEntries()
        if nevts > args.nevents and args.nevents > 0: nevts=args.nevents
        nevts_dict[f]=nevts
    
    for _f,_n in nevts_dict.iteritems():
        print "**** %s: %i events ****"%(_f,_n)

    #sys.exit(1)
        
    # Create batch temp
    tmpdirname="BATCH_TMP_"+args.tag
    if not os.path.isdir(workingdir+"/"+tmpdirname): os.mkdir(workingdir+"/"+tmpdirname)
    ff_ = open(workingdir+"/"+tmpdirname+"/bigsub.txt", 'w')
   

    split_jobs_dict={}
    for f in filelist:
        split_jobs_dict[f] = False
        # See if jobs need to be split
        if args.nmaxevtsperjob > 0 and nevts_dict[f] > args.nmaxevtsperjob:
            split_jobs_dict[f] = True
            eventsList = []
            startEvent = 0
            while (startEvent < nevts_dict[f]):
                eventsList.append(startEvent)
                startEvent += args.nmaxevtsperjob
            eventsList.append(nevts_dict[f])
            print "Dataset %s was splitted in %i jobs" %(f,len(eventsList)-1)
            for i in range(len(eventsList)-1):
                if not os.path.isdir(workingdir+"/"+tmpdirname+"/"+f.split(".root")[0]+"_events_"+str(eventsList[i])+"_"+str(eventsList[i+1]-1)): os.mkdir(workingdir+"/"+tmpdirname+"/"+f.split(".root")[0]+"_events_"+str(eventsList[i])+"_"+str(eventsList[i+1]-1))
                flaunch_ = open(workingdir+"/"+tmpdirname+"/"+f.split(".root")[0]+"_events_"+str(eventsList[i])+"_"+str(eventsList[i+1]-1)+"/launch.sh", 'w')
                flaunch_.write("#!/bin/bash \n")
                flaunch_.write("source /user/smoortga/sklearn_setenv.sh \n")
                flaunch_.write("cdir=/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/ \n")
                flaunch_.write("export LD_LIBRARY_PATH=${cdir}:${cdir}/selection:$LD_LIBRARY_PATH \n")
                flaunch_.write("cd /user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/setup \n")
                flaunch_.write("root -l setup.C \n")
                flaunch_.write("cd /user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/analyse/BTaggingEfficiencyHistograms \n")
                flaunch_.write("python CreateBTagEffHistograms_ttbarSingleLepton.py --infile=%s --outfile=%s --firstEvt=%i --lastEvt=%i --splitted=1 \n"%(indir+f,workingdir+"/SELECTED_"+args.tag+"/"+f, eventsList[i], eventsList[i+1]))
                flaunch_.close()
                ff_.write("qsub -q localgrid -o %s/script.stdout -e %s/script.stderr -l walltime=05:00:00 %s/launch.sh \n"%(workingdir+"/"+tmpdirname+"/"+f.split(".root")[0]+"_events_"+str(eventsList[i])+"_"+str(eventsList[i+1]-1),workingdir+"/"+tmpdirname+"/"+f.split(".root")[0]+"_events_"+str(eventsList[i])+"_"+str(eventsList[i+1]-1),workingdir+"/"+tmpdirname+"/"+f.split(".root")[0]+"_events_"+str(eventsList[i])+"_"+str(eventsList[i+1]-1)))
                #res = p.apply_async(Analyze, args = (indir+f,workingdir+"/SELECTED_"+args.tag+"/"+f, args.topmatchingdir,eventsList[i], eventsList[i+1],True,))
        
        else:
            if not os.path.isdir(workingdir+"/"+tmpdirname+"/"+f.split(".root")[0]): os.mkdir(workingdir+"/"+tmpdirname+"/"+f.split(".root")[0])
            flaunch_ = open(workingdir+"/"+tmpdirname+"/"+f.split(".root")[0]+"/launch.sh", 'w')
            flaunch_.write("#!/bin/bash \n")
            flaunch_.write("source /user/smoortga/sklearn_setenv.sh \n")
            flaunch_.write("cdir=/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/ \n")
            flaunch_.write("export LD_LIBRARY_PATH=${cdir}:${cdir}/selection:$LD_LIBRARY_PATH \n")
            flaunch_.write("cd /user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/setup \n")
            flaunch_.write("root -l setup.C \n")
            flaunch_.write("cd /user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/analyse/BTaggingEfficiencyHistograms \n")
            flaunch_.write("python CreateBTagEffHistograms_ttbarSingleLepton.py --infile=%s --outfile=%s --firstEvt=0 --lastEvt=%i --splitted=0 \n"%(indir+f,workingdir+"/SELECTED_"+args.tag+"/"+f, nevts_dict[f]))
            flaunch_.close()  
            ff_.write("qsub -q localgrid -o %s/script.stdout -e %s/script.stderr -l walltime=05:00:00 %s/launch.sh \n"%(workingdir+"/"+tmpdirname+"/"+f.split(".root")[0],workingdir+"/"+tmpdirname+"/"+f.split(".root")[0],workingdir+"/"+tmpdirname+"/"+f.split(".root")[0]))
            #res = p.apply_async(Analyze, args = (indir+f,workingdir+"/SELECTED_"+args.tag+"/"+f, args.topmatchingdir,0,nevts_dict[f],False,))   
            
    ff_.close()
    
    
if __name__ == "__main__":
	main()
