import os
from argparse import ArgumentParser
import time

parser = ArgumentParser()
parser.add_argument('--indir', default="FILL",help='input directory that contains all the samples')
parser.add_argument('--tag', default=time.strftime("%a%d%b%Y_%Hh%Mm%Ss"),help='name of output directory')
args = parser.parse_args()

proc_dict = {   # tag, weight string   
    "central":"weight_btag_iterativefit*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*mc_weight",
    "btag_JesUp":"weight_btag_iterativefit_JesUp*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*mc_weight",
    "btag_JesDown":"weight_btag_iterativefit_JesDown*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*mc_weight",
    "btag_LfUp": "weight_btag_iterativefit_LfUp*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*mc_weight",
    "btag_LfDown": "weight_btag_iterativefit_LfDown*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*mc_weight",
    "btag_HfUp": "weight_btag_iterativefit_HfUp*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*mc_weight",
    "btag_HfDown": "weight_btag_iterativefit_HfDown*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*mc_weight",
    "btag_Hfstats1Up": "weight_btag_iterativefit_Hfstats1Up*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*mc_weight",
    "btag_Hfstats1Down": "weight_btag_iterativefit_Hfstats1Down*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*mc_weight",
    "btag_Hfstats2Up": "weight_btag_iterativefit_Hfstats2Up*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*mc_weight",
    "btag_Hfstats2Down": "weight_btag_iterativefit_Hfstats2Down*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*mc_weight",
    "btag_Lfstats1Up": "weight_btag_iterativefit_Lfstats1Up*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*mc_weight",
    "btag_Lfstats1Down": "weight_btag_iterativefit_Lfstats1Down*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*mc_weight",
    "btag_Lfstats2Up": "weight_btag_iterativefit_Lfstats2Up*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*mc_weight",
    "btag_Lfstats2Down": "weight_btag_iterativefit_Lfstats2Down*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*mc_weight",
    "btag_Cferr1Up": "weight_btag_iterativefit_Cferr1Up*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*mc_weight",
    "btag_Cferr1Down": "weight_btag_iterativefit_Cferr1Down*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*mc_weight",
    "btag_Cferr2Up": "weight_btag_iterativefit_Cferr2Up*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*mc_weight",
    "btag_Cferr2Down": "weight_btag_iterativefit_Cferr2Down*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*mc_weight",
}

if not os.path.isdir(os.getcwd()+"/"+args.tag): os.mkdir(os.getcwd()+"/"+args.tag)
bigsub_script = open(os.getcwd()+"/"+args.tag+"/big_sub.txt","wb")

for proc,weightstring in proc_dict.iteritems():
    if not os.path.isdir(os.getcwd()+"/"+args.tag+"/"+proc): os.mkdir(os.getcwd()+"/"+args.tag+"/"+proc)
    outdir = os.getcwd()+"/"+args.tag+"/"+proc
    flaunch_ = open(outdir+"/launch.sh","wb")
    flaunch_.write("#!/bin/bash \n")
    flaunch_.write("source /user/smoortga/sklearn_setenv.sh \n")
    flaunch_.write("cdir=/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/ \n")
    flaunch_.write("export LD_LIBRARY_PATH=${cdir}:${cdir}/selection:$LD_LIBRARY_PATH \n")
    flaunch_.write("cd /user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/setup \n")
    flaunch_.write("root -l setup.C \n")
    flaunch_.write("cd /user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/ctagSF \n")
    flaunch_.write("python MakeHistograms_Step1.py --indir=%s --outdir=%s --weightstring=%s \n"%(args.indir,outdir,weightstring))
    flaunch_.close()
    
    bigsub_script.write("qsub -q localgrid -o %s/script.stdout -e %s/script.stderr -l walltime=01:00:00 %s/launch.sh \n"%(outdir,outdir,outdir))

print "done"
