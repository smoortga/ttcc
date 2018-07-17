import os
import time
from argparse import ArgumentParser
import ROOT
import pickle

parser = ArgumentParser()
parser.add_argument('--nevents', type=int, default=-1,help='number of events for each sample')
parser.add_argument('--maxneventsperjob', type=int, default=-1,help='number of events for each sample')
parser.add_argument('--tag', default=time.strftime("%a%d%b%Y_%Hh%Mm%Ss"),help='name of output directory')
args = parser.parse_args()

basedir = "/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/"
workingdir = "/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/selection"
configfile = workingdir+"/config/config.ini"
triggerfile = workingdir+"/config/triggers.txt"
nevents_dict_file = workingdir+"/config/nevents_dict.pkl"

samples = {
    # MC
    # "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC/DYJetsToLL_M-4to50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/180518_204914/0000/":["DYJetsToLL_M-4to50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8.root",args.nevents],
#     "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/180518_204722/0000/":["DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8.root",args.nevents],
#     "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC/ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/180518_205106/0000/":["ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8.root",args.nevents],
#     "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC/ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/180518_205258/0000/":["ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8.root",args.nevents],
#     "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC/ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/180518_205454/0000/":["ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8.root",args.nevents],
#     "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/180518_205643/0000/":["ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8.root",args.nevents],
#     "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC/ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/180518_205840/0000/":["ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8.root",args.nevents],
#     "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/180518_204525/0000/":["TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8.root",args.nevents],
#     "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1_v2_MINIAODSIM/180518_210034/0000/":["WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8.root",args.nevents],
#     "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/180613_091654/0000/":["TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC_WithgenTTXJets/DYJetsToLL_M-4to50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/180704_085500/0000/":["DYJetsToLL_M-4to50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC_WithgenTTXJets/DYJetsToLL_M-4to50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1_v1_MINIAODSIM/180704_085559/0000/":["DYJetsToLL_M-4to50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC_WithgenTTXJets/DYJetsToLL_M-4to50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1_v1_MINIAODSIM/180704_085648/0000/":["DYJetsToLL_M-4to50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC_WithgenTTXJets/DYJetsToLL_M-4to50_HT-600toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/180704_085859/0000/":["DYJetsToLL_M-4to50_HT-600toInf_TuneCP5_13TeV-madgraphMLM-pythia8.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC_WithgenTTXJets/DYJetsToLL_M-4to50_HT-70to100_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1_v1_MINIAODSIM/180704_085408/0000/":["DYJetsToLL_M-4to50_HT-70to100_TuneCP5_13TeV-madgraphMLM-pythia8.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC_WithgenTTXJets/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/180704_085259/0000/":["DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC_WithgenTTXJets/ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/180704_090116/0000/":["ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC_WithgenTTXJets/ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/180704_090222/0000/":["ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC_WithgenTTXJets/ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/180704_090315/0000/":["ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC_WithgenTTXJets/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/180704_090411/0000/":["ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC_WithgenTTXJets/ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/180704_090522/0000/":["ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC_WithgenTTXJets/ttHJetTobb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v1_MINIAODSIM/180704_092041/0000/":["ttHJetTobb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC_WithgenTTXJets/ttHJetToNonbb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v1_MINIAODSIM/180704_091924/0000/":["ttHJetToNonbb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC_WithgenTTXJets/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/180704_085054/0000/":["TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8.root",args.nevents],
    #"/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC_WithgenTTXJets/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/180704_085054/0001/":["EXTENDED_TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8.root",args.nevents]
    #"/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC_WithgenTTXJets/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/180704_085155/0000/":["TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8.root",args.nevents]
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC_WithgenTTXJets/TTWJetsToLNu_TuneCP5_PSweights_13TeV-amcatnloFXFX-madspin-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/180704_091008/0000/":["TTWJetsToLNu_TuneCP5_PSweights_13TeV-amcatnloFXFX-madspin-pythia8.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC_WithgenTTXJets/TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/180704_090905/0000/":["TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC_WithgenTTXJets/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/180704_090754/0000/":["TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC_WithgenTTXJets/TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/180704_090712/0000/":["TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC_WithgenTTXJets/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1_v2_MINIAODSIM/180704_090607/0000/":["WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC_WithgenTTXJets/WW_TuneCP5_13TeV-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/180704_091229/0000/":["WW_TuneCP5_13TeV-pythia8.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC_WithgenTTXJets/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/180704_091724/0000/":["WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC_WithgenTTXJets/WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/180704_091559/0000/":["WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC_WithgenTTXJets/WZ_TuneCP5_13TeV-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/180704_091330/0000/":["WZ_TuneCP5_13TeV-pythia8.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC_WithgenTTXJets/WZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/180704_091436/0000/":["WZZ_TuneCP5_13TeV-amcatnlo-pythia8.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC_WithgenTTXJets/ZZ_TuneCP5_13TeV-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/180704_091104/0000/":["ZZ_TuneCP5_13TeV-pythia8.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC_WithgenTTXJets/ZZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/180704_091809/0000/":["ZZZ_TuneCP5_13TeV-amcatnlo-pythia8.root",args.nevents]
    # Data
    # "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_Data/DoubleEG/Run2017B_31Mar2018_v1_MINIAOD/180522_114603/0000/":["DoubleEG_Run2017B_31Mar2018_v1_MINIAOD.root",args.nevents],
#     "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_Data/DoubleEG/Run2017C_31Mar2018_v1_MINIAOD/180522_114704/0000/":["DoubleEG_Run2017C_31Mar2018_v1_MINIAOD.root",args.nevents],
#     "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_Data/DoubleEG/Run2017D_31Mar2018_v1_MINIAOD/180522_114804/0000/":["DoubleEG_Run2017D_31Mar2018_v1_MINIAOD.root",args.nevents],
#     "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_Data/DoubleEG/Run2017E_31Mar2018_v1_MINIAOD/180522_114901/0000/":["DoubleEG_Run2017E_31Mar2018_v1_MINIAOD.root",args.nevents],
#     "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_Data/DoubleEG/Run2017F_31Mar2018_v1_MINIAOD/180522_114957/0000/":["DoubleEG_Run2017F_31Mar2018_v1_MINIAOD.root",args.nevents],
#     "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_Data/DoubleMuon/Run2017B_31Mar2018_v1_MINIAOD/180522_114016/0000/":["DoubleMuon_Run2017B_31Mar2018_v1_MINIAOD.root",args.nevents],
#     "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_Data/DoubleMuon/Run2017C_31Mar2018_v1_MINIAOD/180522_114131/0000/":["DoubleMuon_Run2017C_31Mar2018_v1_MINIAOD.root",args.nevents],
#     "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_Data/DoubleMuon/Run2017D_31Mar2018_v1_MINIAOD/180522_114303/0000/":["DoubleMuon_Run2017D_31Mar2018_v1_MINIAOD.root",args.nevents],
#     "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_Data/DoubleMuon/Run2017E_31Mar2018_v1_MINIAOD/180522_114408/0000/":["DoubleMuon_Run2017E_31Mar2018_v1_MINIAOD.root",args.nevents],
#     "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_Data/DoubleMuon/Run2017F_31Mar2018_v1_MINIAOD/180522_114507/0000/":["DoubleMuon_Run2017F_31Mar2018_v1_MINIAOD.root",args.nevents],
#     "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_Data/MuonEG/Run2017B_31Mar2018_v1_MINIAOD/180522_115057/0000/":["MuonEG_Run2017B_31Mar2018_v1_MINIAOD.root",args.nevents],
#     "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_Data/MuonEG/Run2017C_31Mar2018_v1_MINIAOD/180522_115153/0000/":["MuonEG_Run2017C_31Mar2018_v1_MINIAOD.root",args.nevents],
#     "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_Data/MuonEG/Run2017D_31Mar2018_v1_MINIAOD/180522_115252/0000/":["MuonEG_Run2017D_31Mar2018_v1_MINIAOD.root",args.nevents],
#     "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_Data/MuonEG/Run2017E_31Mar2018_v1_MINIAOD/180522_115348/0000/":["MuonEG_Run2017E_31Mar2018_v1_MINIAOD.root",args.nevents],
#     "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_Data/MuonEG/Run2017F_31Mar2018_v1_MINIAOD/180522_115453/0000/":["MuonEG_Run2017F_31Mar2018_v1_MINIAOD.root",args.nevents]
}


resubmit_buffer = []

os.system("voms-proxy-init --voms cms --valid 192:0")
os.system("cp $X509_USER_PROXY /user/$USER/")
os.system("gfal-mkdir srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/$USER/Analysis/Selection")
os.system("gfal-mkdir srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/$USER/Analysis/Selection/OUTPUT_"+args.tag)


if os.path.isfile(nevents_dict_file):
    nevents_dict = pickle.load(open(nevents_dict_file,"rb"))
else:
    nevents_dict = {}

if not os.path.isdir(workingdir+"/OUTPUT_"+args.tag): os.mkdir(workingdir+"/OUTPUT_"+args.tag)
if not os.path.isdir(workingdir+"/OUTPUT_"+args.tag+"/localgrid_"+args.tag): os.mkdir(workingdir+"/OUTPUT_"+args.tag+"/localgrid_"+args.tag)
for indir, output in samples.iteritems():
    print output[0].split("/")[-1]
    
    
    # splitting of the jobs
    if not os.path.isfile(nevents_dict_file) or args.nevents != -1:
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
        nevents_dict[output[0].split("/")[-1].split(".root")[0]] = nevts_to_process
    
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
            dir_tmp = "$TMPDIR/OUTPUT_"+args.tag+"/localgrid_"+args.tag+"/"+output[0].split("/")[-1].split(".")[0]+"_events_"+str(eventsList[i])+"_"+str(eventsList[i+1]-1)
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
            ff_.write(workingdir+"/Selection --infiledirectory %s --outfilepath %s --config %s --triggers %s --nevents %i --firstevt %i --lastevt %i \n"%(indir,"$TMPDIR/"+output[0].split(".root")[0]+"_events_"+str(eventsList[i])+"_"+str(eventsList[i+1]-1)+".root", configfile , triggerfile, output[1],eventsList[i], eventsList[i+1]))
            #ff_.write("gfal-mkdir srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/$USER/Analysis/Selection \n")
            #ff_.write("gfal-mkdir srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/$USER/Analysis/Selection/OUTPUT_"+args.tag+" \n") 
            ff_.write("gfal-copy file://$TMPDIR/"+output[0].split(".root")[0]+"_events_"+str(eventsList[i])+"_"+str(eventsList[i+1]-1)+".root"+" srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/$USER/Analysis/Selection/OUTPUT_"+args.tag+"/"+output[0].split(".root")[0]+"_events_"+str(eventsList[i])+"_"+str(eventsList[i+1]-1)+".root \n")
            ff_.close()
            print "qsub -q localgrid -o %s/script.stdout -e %s/script.stderr  %s/launch.sh"%(local_dir_tmp,local_dir_tmp,local_dir_tmp)
            stdout = os.popen("qsub -q localgrid -o %s/script.stdout -e %s/script.stderr %s/launch.sh"%(local_dir_tmp,local_dir_tmp,local_dir_tmp)).read()
            print "SUBMISSION OUTPUT: " + stdout
            print stdout == ""
            if stdout=="":
                print "Adding to resubmitting pipeline"
                resubmit_buffer.append("qsub -q localgrid -o %s/script.stdout -e %s/script.stderr  %s/launch.sh"%(local_dir_tmp,local_dir_tmp,local_dir_tmp))
                
    
    else:
        local_dir_tmp = workingdir+"/OUTPUT_"+args.tag+"/localgrid_"+args.tag+"/"+output[0].split("/")[-1].split(".")[0]
        dir_tmp = "$TMPDIR/OUTPUT_"+args.tag+"/localgrid_"+args.tag+"/"+output[0].split("/")[-1].split(".")[0]
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
        ff_.write(workingdir+"/Selection --infiledirectory %s --outfilepath %s --config %s --triggers %s --nevents %i --firstevt %i --lastevt %i \n"%(indir,"$TMPDIR/"+output[0], configfile , triggerfile, output[1],0,output[1]))
        #ff_.write("gfal-mkdir srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/$USER/Analysis/Selection \n")
        #ff_.write("gfal-mkdir srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/$USER/Analysis/Selection/OUTPUT_"+args.tag+" \n")
        ff_.write("gfal-copy file://$TMPDIR/"+output[0]+" srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/$USER/Analysis/Selection/OUTPUT_"+args.tag+"/"+output[0]+" \n")
        ff_.close()
        print "qsub -q localgrid -o %s/script.stdout -e %s/script.stderr  %s/launch.sh"%(local_dir_tmp,local_dir_tmp,local_dir_tmp)
        stdout = os.popen("qsub -q localgrid -o %s/script.stdout -e %s/script.stderr %s/launch.sh"%(local_dir_tmp,local_dir_tmp,local_dir_tmp)).read()
        print "SUBMISSION OUTPUT: " + stdout
        print stdout == ""
        if stdout=="":
            print "Adding to resubmitting pipeline"
            resubmit_buffer.append("qsub -q localgrid -o %s/script.stdout -e %s/script.stderr  %s/launch.sh"%(local_dir_tmp,local_dir_tmp,local_dir_tmp))

print resubmit_buffer                
if (len(resubmit_buffer) != 0):
    print "RESUBMITTING FAILED ATTEMPTS"
    while (len(resubmit_buffer) != 0):
        for cmd in resubmit_buffer:
            stdout = os.popen(cmd).read()
            print stdout
            if not (stdout==""): resubmit_buffer.remove(cmd)
        
if not os.path.isfile(nevents_dict_file) and args.nevents == -1:
    pickle.dump(nevents_dict,open(nevents_dict_file,"wb"))

print "Done! use 'qstat -u $USER' to monitor samples"
print "use 'for j in $(qselect -u $USER);do timeout 3 qdel -a $j;done' to delete all your jobs"
