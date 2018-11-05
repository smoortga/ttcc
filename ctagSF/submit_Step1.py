import os
from argparse import ArgumentParser
import time

parser = ArgumentParser()
#parser.add_argument('--indir', default="FILL",help='input directory that contains all the samples')
parser.add_argument('--tag', default=time.strftime("%a%d%b%Y_%Hh%Mm%Ss"),help='name of output directory')
args = parser.parse_args()

indir_base = "/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/analyse/SELECTED_ttbarSingleLepton_BTagValueRanking_WithBTagWPSFs/"
nobias_dir = "/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/analyse/SELECTED_ttbarSingleLepton_CorrectPUProfile_NNRanking_0p5/"
#nobias_dir = "/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/analyse/SELECTED_ttbarSingleLepton_CorrectPUProfile_NeurnalNetworkMatching_CorrectTruthLepton_WithoutBTagInfo2/"
#nobias_dir = "/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/analyse/SELECTED_ttbarSingleLepton_CorrectPUProfile_NNRanking_0p95/"

proc_dict = {   # tag, weight string   
    #"central":"weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*mc_weight",
    "central":["weight_btag_DeepCSVTight*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*mc_weight*pu_weight",indir_base],
	"muF0p5":["weight_btag_DeepCSVTight*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*pu_weight*weight_scale_muF0p5",indir_base],
    "muF2":["weight_btag_DeepCSVTight*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*pu_weight*weight_scale_muF2",indir_base],
    "muR0p5":["weight_btag_DeepCSVTight*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*pu_weight*weight_scale_muR0p5",indir_base],
    "muR2":["weight_btag_DeepCSVTight*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*pu_weight*weight_scale_muR2",indir_base],
    "PUUp":["weight_btag_DeepCSVTight*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*mc_weight*pu_weight_up",indir_base],
	"PUDown":["weight_btag_DeepCSVTight*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*mc_weight*pu_weight_down",indir_base],
	"elecIdUp":["weight_btag_DeepCSVTight*weight_electron_id_Up*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*pu_weight*mc_weight",indir_base],
    "elecIdDown":["weight_btag_DeepCSVTight*weight_electron_id_Down*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*pu_weight*mc_weight",indir_base],
	"elecRecoUp":["weight_btag_DeepCSVTight*weight_electron_id*weight_electron_reco_Up*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*pu_weight*mc_weight",indir_base],
	"elecRecoDown":["weight_btag_DeepCSVTight*weight_electron_id*weight_electron_reco_Down*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*pu_weight*mc_weight",indir_base],
	"elecTrigUp":["weight_btag_DeepCSVTight*weight_electron_id*weight_electron_reco*weight_electron_trig_Up*weight_muon_id*weight_muon_iso*weight_muon_trig*pu_weight*mc_weight",indir_base],
	"elecTrigDown":["weight_btag_DeepCSVTight*weight_electron_id*weight_electron_reco*weight_electron_trig_Down*weight_muon_id*weight_muon_iso*weight_muon_trig*pu_weight*mc_weight",indir_base],
	"muonIdUp":["weight_btag_DeepCSVTight*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id_Up*weight_muon_iso*weight_muon_trig*pu_weight*mc_weight",indir_base],
    "muonIdDown":["weight_btag_DeepCSVTight*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id_Down*weight_muon_iso*weight_muon_trig*pu_weight*mc_weight",indir_base],
	"muonIsoUp":["weight_btag_DeepCSVTight*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso_Up*weight_muon_trig*pu_weight*mc_weight",indir_base],
	"muonIsoDown":["weight_btag_DeepCSVTight*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso_Down*weight_muon_trig*pu_weight*mc_weight",indir_base],
	"muonTrigUp":["weight_btag_DeepCSVTight*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig_Up*pu_weight*mc_weight",indir_base],
	"muonTrigDown":["weight_btag_DeepCSVTight*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig_Down*pu_weight*mc_weight",indir_base],
	"btag_Up":["weight_btag_DeepCSVTightUp*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*pu_weight*mc_weight",indir_base],
    "btag_Down":["weight_btag_DeepCSVTightDown*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*pu_weight*mc_weight",indir_base],
	#"btagBias":["weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*mc_weight*pu_weight",nobias_dir],
	# "central":["weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*mc_weight*pu_weight",nobias_dir],
# 	"muF0p5":["weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*pu_weight*weight_scale_muF0p5",nobias_dir],
#     "muF2":["weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*pu_weight*weight_scale_muF2",nobias_dir],
#     "muR0p5":["weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*pu_weight*weight_scale_muR0p5",nobias_dir],
#     "muR2":["weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*pu_weight*weight_scale_muR2",nobias_dir],
#     "PUUp":["weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*mc_weight*pu_weight_up",nobias_dir],
# 	"PUDown":["weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*mc_weight*pu_weight_down",nobias_dir],
# 	"elecIdUp":["weight_electron_id_Up*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*pu_weight*mc_weight",nobias_dir],
#     "elecIdDown":["weight_electron_id_Down*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*pu_weight*mc_weight",nobias_dir],
# 	"elecRecoUp":["weight_electron_id*weight_electron_reco_Up*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*pu_weight*mc_weight",nobias_dir],
# 	"elecRecoDown":["weight_electron_id*weight_electron_reco_Down*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*pu_weight*mc_weight",nobias_dir],
# 	"elecTrigUp":["weight_electron_id*weight_electron_reco*weight_electron_trig_Up*weight_muon_id*weight_muon_iso*weight_muon_trig*pu_weight*mc_weight",nobias_dir],
# 	"elecTrigDown":["weight_electron_id*weight_electron_reco*weight_electron_trig_Down*weight_muon_id*weight_muon_iso*weight_muon_trig*pu_weight*mc_weight",nobias_dir],
# 	"muonIdUp":["weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id_Up*weight_muon_iso*weight_muon_trig*pu_weight*mc_weight",nobias_dir],
#     "muonIdDown":["weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id_Down*weight_muon_iso*weight_muon_trig*pu_weight*mc_weight",nobias_dir],
# 	"muonIsoUp":["weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso_Up*weight_muon_trig*pu_weight*mc_weight",nobias_dir],
# 	"muonIsoDown":["weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso_Down*weight_muon_trig*pu_weight*mc_weight",nobias_dir],
# 	"muonTrigUp":["weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig_Up*pu_weight*mc_weight",nobias_dir],
# 	"muonTrigDown":["weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig_Down*pu_weight*mc_weight",nobias_dir],
# 	"btagBias":["weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*mc_weight*pu_weight",nobias_dir],
	
	
    # "btag_JesUp":["weight_btag_iterativefit_JesUp*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*pu_weight*mc_weight",indir_base],
#     "btag_JesDown":["weight_btag_iterativefit_JesDown*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*pu_weight*mc_weight",indir_base],
#     "btag_LfUp":["weight_btag_iterativefit_LfUp*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*pu_weight*mc_weight",indir_base],
#     "btag_LfDown":["weight_btag_iterativefit_LfDown*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*pu_weight*mc_weight",indir_base],
#     "btag_HfUp":["weight_btag_iterativefit_HfUp*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*pu_weight*mc_weight",indir_base],
#     "btag_HfDown":["weight_btag_iterativefit_HfDown*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*pu_weight*mc_weight",indir_base],
#     "btag_Hfstats1Up":["weight_btag_iterativefit_Hfstats1Up*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*pu_weight*mc_weight",indir_base],
#     "btag_Hfstats1Down":["weight_btag_iterativefit_Hfstats1Down*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*pu_weight*mc_weight",indir_base],
#     "btag_Hfstats2Up":["weight_btag_iterativefit_Hfstats2Up*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*pu_weight*mc_weight",indir_base],
#     "btag_Hfstats2Down":["weight_btag_iterativefit_Hfstats2Down*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*pu_weight*mc_weight",indir_base],
#     "btag_Lfstats1Up":["weight_btag_iterativefit_Lfstats1Up*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*pu_weight*mc_weight",indir_base],
#     "btag_Lfstats1Down":["weight_btag_iterativefit_Lfstats1Down*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*pu_weight*mc_weight",indir_base],
#     "btag_Lfstats2Up":["weight_btag_iterativefit_Lfstats2Up*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*pu_weight*mc_weight",indir_base],
#     "btag_Lfstats2Down":["weight_btag_iterativefit_Lfstats2Down*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*pu_weight*mc_weight",indir_base],
#     "btag_Cferr1Up":["weight_btag_iterativefit_Cferr1Up*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*pu_weight*mc_weight",indir_base],
#     "btag_Cferr1Down":["weight_btag_iterativefit_Cferr1Down*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*pu_weight*mc_weight",indir_base],
#     "btag_Cferr2Up":["weight_btag_iterativefit_Cferr2Up*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*pu_weight*mc_weight",indir_base],
#     "btag_Cferr2Down":["weight_btag_iterativefit_Cferr2Down*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*pu_weight*mc_weight",indir_base],
    }

if not os.path.isdir(os.getcwd()+"/"+args.tag): os.mkdir(os.getcwd()+"/"+args.tag)
bigsub_script = open(os.getcwd()+"/"+args.tag+"/big_sub.txt","wb")

for proc,properties in proc_dict.iteritems():
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
    flaunch_.write("python MakeHistograms_Step1.py --indir=%s --outdir=%s --weightstring=%s \n"%(properties[1],outdir,properties[0]))
    flaunch_.close()
    
    bigsub_script.write("qsub -q localgrid -o %s/script.stdout -e %s/script.stderr -l walltime=01:00:00 %s/launch.sh \n"%(outdir,outdir,outdir))

bigsub_script.close()

print "Submit via: '\033[92mbig-submission %s/big_sub.txt\033[0m'"%(os.getcwd()+"/"+args.tag)
print "Use '\033[94mqstat -u $USER\033[0m' to monitor samples"
print "use '\033[94mfor j in $(qselect -u $USER);do timeout 3 qdel -a $j;done\033[0m' to delete all your jobs"

text = raw_input("Would you like to submit this now? (y/n): ")
if text == "y" or text == "Y" or text == "yes" or text == "Yes" or text == "YES":
    os.system("big-submission %s/big_sub.txt"%(os.getcwd()+"/"+args.tag))
    
else:
    print "Not yet starting any submission... ending..."

os.system("qstat -u $USER")
