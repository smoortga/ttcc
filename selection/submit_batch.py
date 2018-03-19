import os
import time
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('--nevents', type=int, default=-1,help='number of events for each sample')
parser.add_argument('--tag', default=time.strftime("%a%d%b%Y_%Hh%Mm%Ss"),help='name of output directory')
args = parser.parse_args()

basedir = "/user/smoortga/Analysis/NTupler/CMSSW_8_0_25/src/FlatTree/FlatTreeAnalyzer/ttcc/"
workingdir = "/user/smoortga/Analysis/NTupler/CMSSW_8_0_25/src/FlatTree/FlatTreeAnalyzer/ttcc/selection"
configfile = workingdir+"/config/config.ini"

samples = {
    # MC
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Full2016Analysis/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_v1_MINIAODSIM/180312_114246/0000/":["./SelectedSamples/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Full2016Analysis/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2_PUMoriond17_HCALDebug_80X_mcRun2_asymptotic_2016_TrancheIV_v6_v1_MINIAODSIM/180312_110008/0000/":["./SelectedSamples/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Full2016Analysis/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_v1_MINIAODSIM/180312_110112/0000/":["./SelectedSamples/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Full2016Analysis/ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_v1_MINIAODSIM/180312_110214/0000/":["./SelectedSamples/ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Full2016Analysis/ST_t-channel_top_4f_inclusiveDecays_TuneCUETP8M2T4_13TeV-powhegV2-madspin/RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_v1_MINIAODSIM/180312_110320/0000/":["./SelectedSamples/ST_t-channel_top_4f_inclusiveDecays_TuneCUETP8M2T4_13TeV-powhegV2-madspin.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Full2016Analysis/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4/RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_v1_MINIAODSIM/180312_110426/0000/":["./SelectedSamples/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Full2016Analysis/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4/RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_v1_MINIAODSIM/180312_110534/0000/":["./SelectedSamples/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Full2016Analysis/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_v1_MINIAODSIM/180312_110955/0000/":["./SelectedSamples/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Full2016Analysis/ttHToNonbb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_v1_MINIAODSIM/180312_110851/0000/":["./SelectedSamples/ttHToNonbb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Full2016Analysis/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_v1_MINIAODSIM/180312_110639/0000/":["./SelectedSamples/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Full2016Analysis/ttWJets_13TeV_madgraphMLM/RunIISummer16MiniAODv2_80X_mcRun2_asymptotic_2016_TrancheIV_v6_v1_MINIAODSIM/180312_111204/0000/":["./SelectedSamples/ttWJets_13TeV_madgraphMLM.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Full2016Analysis/ttZJets_13TeV_madgraphMLM/RunIISummer16MiniAODv2_80X_mcRun2_asymptotic_2016_TrancheIV_v6_v1_MINIAODSIM/180312_111100/0000/":["./SelectedSamples/ttZJets_13TeV_madgraphMLM.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Full2016Analysis/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_v1_MINIAODSIM/180312_110744/0000/":["./SelectedSamples/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root",args.nevents],
    # Data
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Full2016Analysis_Data/DoubleEG/Run2016B_23Sep2016_v3_MINIAOD/180312_115353/0000/":["./SelectedSamples/DoubleEG_Run2016B_23Sep2016_v3_MINIAOD.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Full2016Analysis_Data/DoubleEG/Run2016C_23Sep2016_v1_MINIAOD/180312_115436/0000/":["./SelectedSamples/DoubleEG_Run2016C_23Sep2016_v1_MINIAOD.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Full2016Analysis_Data/DoubleEG/Run2016D_23Sep2016_v1_MINIAOD/180312_115535/0000/":["./SelectedSamples/DoubleEG_Run2016D_23Sep2016_v1_MINIAOD.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Full2016Analysis_Data/DoubleEG/Run2016E_23Sep2016_v1_MINIAOD/180312_115618/0000/":["./SelectedSamples/DoubleEG_Run2016E_23Sep2016_v1_MINIAOD.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Full2016Analysis_Data/DoubleEG/Run2016F_23Sep2016_v1_MINIAOD/180312_115717/0000/":["./SelectedSamples/DoubleEG_Run2016F_23Sep2016_v1_MINIAOD.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Full2016Analysis_Data/DoubleEG/Run2016G_23Sep2016_v1_MINIAOD/180312_115802/0000/":["./SelectedSamples/DoubleEG_Run2016G_23Sep2016_v1_MINIAOD.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Full2016Analysis_Data/DoubleMuon/Run2016B_23Sep2016_v3_MINIAOD/180312_114741/0000/":["./SelectedSamples/DoubleMuon_Run2016B_23Sep2016_v3_MINIAOD.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Full2016Analysis_Data/DoubleMuon/Run2016C_23Sep2016_v1_MINIAOD/180312_114841/0000/":["./SelectedSamples/DoubleMuon_Run2016C_23Sep2016_v1_MINIAOD.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Full2016Analysis_Data/DoubleMuon/Run2016D_23Sep2016_v1_MINIAOD/180312_114925/0000/":["./SelectedSamples/DoubleMuon_Run2016D_23Sep2016_v1_MINIAOD.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Full2016Analysis_Data/DoubleMuon/Run2016E_23Sep2016_v1_MINIAOD/180312_115024/0000/":["./SelectedSamples/DoubleMuon_Run2016E_23Sep2016_v1_MINIAOD.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Full2016Analysis_Data/DoubleMuon/Run2016F_23Sep2016_v1_MINIAOD/180312_115107/0000/":["./SelectedSamples/DoubleMuon_Run2016F_23Sep2016_v1_MINIAOD.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Full2016Analysis_Data/DoubleMuon/Run2016G_23Sep2016_v1_MINIAOD/180312_115206/0000/":["./SelectedSamples/DoubleMuon_Run2016G_23Sep2016_v1_MINIAOD.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Full2016Analysis_Data/MuonEG/Run2016B_23Sep2016_v3_MINIAOD/180312_115947/0000/":["./SelectedSamples/MuonEG_Run2016B_23Sep2016_v3_MINIAOD.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Full2016Analysis_Data/MuonEG/Run2016C_23Sep2016_v1_MINIAOD/180312_120043/0000/":["./SelectedSamples/MuonEG_Run2016C_23Sep2016_v1_MINIAOD.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Full2016Analysis_Data/MuonEG/Run2016D_23Sep2016_v1_MINIAOD/180312_120125/0000/":["./SelectedSamples/MuonEG_Run2016D_23Sep2016_v1_MINIAOD.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Full2016Analysis_Data/MuonEG/Run2016E_23Sep2016_v1_MINIAOD/180312_120225/0000/":["./SelectedSamples/MuonEG_Run2016E_23Sep2016_v1_MINIAOD.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Full2016Analysis_Data/MuonEG/Run2016F_23Sep2016_v1_MINIAOD/180312_120308/0000/":["./SelectedSamples/MuonEG_Run2016F_23Sep2016_v1_MINIAOD.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Full2016Analysis_Data/MuonEG/Run2016G_23Sep2016_v1_MINIAOD/180312_120406/0000/":["./SelectedSamples/MuonEG_Run2016G_23Sep2016_v1_MINIAOD.root",args.nevents]
}
# samples = {
#         "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/TestTriggers_ttbbAnalysis_25012018/ST_t-channel_top_4f_inclusiveDecays_TuneCUETP8M2T4_13TeV-powhegV2-madspin/RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_v1_MINIAODSIM/180125_113214/0000/":["./SelectedSamples/ST_t-channel_top_4f_inclusiveDecays_TuneCUETP8M2T4_13TeV-powhegV2-madspin.root",args.nevents],
#         "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/TestTriggers_ttbbAnalysis_25012018/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_v1_MINIAODSIM/180125_113353/0000/":["./SelectedSamples/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root",args.nevents],
#         "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/TestTriggers_ttbbAnalysis_25012018/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_v1_MINIAODSIM/180125_113444/0000/":["./SelectedSamples/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8.root",args.nevents],
#         "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/TestTriggers_ttbbAnalysis_25012018/ttWJets_13TeV_madgraphMLM/RunIISummer16MiniAODv2_80X_mcRun2_asymptotic_2016_TrancheIV_v6_v1_MINIAODSIM/180125_113534/0000/":["./SelectedSamples/ttWJets_13TeV_madgraphMLM.root",args.nevents],
#         "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/TestTriggers_ttbbAnalysis_25012018/ttHToNonbb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_v1_MINIAODSIM/180125_113420/0000/":["./SelectedSamples/ttHToNonbb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8.root",args.nevents],
#         "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/TestTriggers_ttbbAnalysis_25012018/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_v1_MINIAODSIM/180125_113120/0000/":["./SelectedSamples/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1.root",args.nevents],
#         "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/TestTriggers_ttbbAnalysis_25012018/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4/RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_v1_MINIAODSIM/180125_113237/0000/":["./SelectedSamples/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4.root",args.nevents],
#         "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/TestTriggers_ttbbAnalysis_25012018/ttZJets_13TeV_madgraphMLM/RunIISummer16MiniAODv2_80X_mcRun2_asymptotic_2016_TrancheIV_v6_v1_MINIAODSIM/180125_113507/0000/":["./SelectedSamples/ttZJets_13TeV_madgraphMLM.root",args.nevents],
#         "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/TestTriggers_ttbbAnalysis_25012018/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4/RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_v1_MINIAODSIM/180125_113305/0000/":["./SelectedSamples/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4.root",args.nevents],
#         "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/TestTriggers_ttbbAnalysis_25012018/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_v1_MINIAODSIM/180125_113032/0000/":["./SelectedSamples/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8.root",args.nevents],
#         "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/TestTriggers_ttbbAnalysis_25012018/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2_PUMoriond17_HCALDebug_80X_mcRun2_asymptotic_2016_TrancheIV_v6_v1_MINIAODSIM/180125_113056/0000/":["./SelectedSamples/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8.root",args.nevents],
#         "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/TestTriggers_ttbbAnalysis_25012018/ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_v1_MINIAODSIM/180125_113149/0000/":["./SelectedSamples/ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1.root",args.nevents],
#         "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/TestTriggers_ttbbAnalysis_25012018/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_v1_MINIAODSIM/180125_113328/0000/":["./SelectedSamples/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8.root",args.nevents],
#         "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/TestTriggers_ttbbAnalysis_data_05022018/MuonEG/Run2016B_23Sep2016_v3_MINIAOD/180205_093500/0000/":["./SelectedSamples/MuonEG_Run2016B_23Sep2016_v3_MINIAOD.root",args.nevents],
#         "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/TestTriggers_ttbbAnalysis_data_05022018/MuonEG/Run2016C_23Sep2016_v1_MINIAOD/180205_093610/0000/":["./SelectedSamples/MuonEG_Run2016C_23Sep2016_v1_MINIAOD.root",args.nevents],
#         "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/TestTriggers_ttbbAnalysis_data_05022018/MuonEG/Run2016D_23Sep2016_v1_MINIAOD/180205_093726/0000/":["./SelectedSamples/MuonEG_Run2016D_23Sep2016_v1_MINIAOD.root",args.nevents],
#         "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/TestTriggers_ttbbAnalysis_data_05022018/MuonEG/Run2016E_23Sep2016_v1_MINIAOD/180205_093833/0000/":["./SelectedSamples/MuonEG_Run2016E_23Sep2016_v1_MINIAOD.root",args.nevents],
#         "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/TestTriggers_ttbbAnalysis_data_05022018/MuonEG/Run2016F_23Sep2016_v1_MINIAOD/180205_093951/0000/":["./SelectedSamples/MuonEG_Run2016F_23Sep2016_v1_MINIAOD.root",args.nevents],
#         "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/TestTriggers_ttbbAnalysis_data_05022018/MuonEG/Run2016G_23Sep2016_v1_MINIAOD/180205_094103/0000/":["./SelectedSamples/MuonEG_Run2016G_23Sep2016_v1_MINIAOD.root",args.nevents]
# }

if not os.path.isdir(workingdir+"/OUTPUT_"+args.tag): os.mkdir(workingdir+"/OUTPUT_"+args.tag)
if not os.path.isdir(workingdir+"/OUTPUT_"+args.tag+"/localgrid_"+args.tag): os.mkdir(workingdir+"/OUTPUT_"+args.tag+"/localgrid_"+args.tag)
for indir, output in samples.iteritems():
    print output[0].split("/")[-1]
    dir_tmp = workingdir+"/OUTPUT_"+args.tag+"/localgrid_"+args.tag+"/"+output[0].split("/")[-1].split(".")[0]
    if not os.path.isdir(dir_tmp): os.mkdir(dir_tmp)
    ff_ = open(dir_tmp+"/launch.sh", 'w')
    ff_.write("#!/bin/bash \n")
    ff_.write("pwd=$PWD \n")  
    ff_.write("source $VO_CMS_SW_DIR/cmsset_default.sh \n")                                                                                                                                                           
    ff_.write("cd /storage_mnt/storage/user/smoortga/Analysis/NTupler/CMSSW_8_0_25/src \n")                                                                                                                                                          
    ff_.write("eval `scram runtime -sh` \n")                                                                                                                                           
    ff_.write("cd $pwd \n")  
    ff_.write("cdir=%s \n"%basedir)
    ff_.write("export LD_LIBRARY_PATH=${cdir}:${cdir}/..:$LD_LIBRARY_PATH \n")
    ff_.write("export X509_USER_PROXY=/user/$USER/x509up_$(id -u $USER) \n")
    ff_.write(workingdir+"/Selection --infiledirectory %s --outfilepath %s --config %s --nevents %i \n"%(indir,workingdir+"/OUTPUT_"+args.tag+"/"+output[0], configfile , output[1]))
    ff_.close()
    

    print "qsub -q localgrid -o %s/script.stdout -e %s/script.stderr  %s/launch.sh"%(dir_tmp,dir_tmp,dir_tmp)
    os.system("qsub -q localgrid -o %s/script.stdout -e %s/script.stderr %s/launch.sh"%(dir_tmp,dir_tmp,dir_tmp))
    
print "Done! use 'qstat -u $USER' to monitor samples"
print "use 'for j in $(qselect -u $USER);do timeout 3 qdel -a $j;done' to delete all your jobs"
