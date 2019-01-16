import os
import time
from argparse import ArgumentParser
import ROOT
import pickle

parser = ArgumentParser()
parser.add_argument('--nevents', type=int, default=-1,help='number of events for each sample')
parser.add_argument('--maxneventsperjob', type=int, default=3000000,help='number of events for each sample')
parser.add_argument('--tag', default=time.strftime("%a%d%b%Y_%Hh%Mm%Ss"),help='name of output directory')
args = parser.parse_args()

basedir = "/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/"
workingdir = "/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/selection"
configfile = workingdir+"/config/config.ini"
triggerfile = workingdir+"/config/triggers.txt"
nevents_dict_file = workingdir+"/config/nevents_dict.pkl"

samples = { # format "input-directory":["output-name",number-of-events,"JESsyst(central,Up,Down)","JERsyst(central,Up,Down)"]
    # MC
    #"/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v1_MINIAODSIM/181108_083113/0000/":["TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8.root",args.nevents,"central","central"],
    #"/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v1_MINIAODSIM/181108_083113/0000/ JESUp":["TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8_JESUp.root",args.nevents,"Up","central"],
    #"/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v1_MINIAODSIM/181108_083113/0000/ JESDown":["TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8_JESDown.root",args.nevents,"Down","central"],
    #"/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v1_MINIAODSIM/181108_083113/0000/ JERUp":["TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8_JERUp.root",args.nevents,"central","Up"],
    #"/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v1_MINIAODSIM/181108_083113/0000/ JERDown":["TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8_JERDown.root",args.nevents,"central","Down"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v1_MINIAODSIM/181111_185926/0000/":["TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8_VisiblePS.root",args.nevents,"central","central"],
    #"/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v1_MINIAODSIM/181111_185926/0000/ JESUp":["TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8_VisiblePS_JESUp.root",args.nevents,"Up","central"],
    #"/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v1_MINIAODSIM/181111_185926/0000/ JESDown":["TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8_VisiblePS_JESDown.root",args.nevents,"Down","central"],
    #"/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v1_MINIAODSIM/181111_185926/0000/ JERUp":["TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8_VisiblePS_JERUp.root",args.nevents,"central","Up"],
    #"/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v1_MINIAODSIM/181111_185926/0000/ JERDown":["TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8_VisiblePS_JERDown.root",args.nevents,"central","Down"],

    #"/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v1_MINIAODSIM/181107_164712/0000/":["TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8.root",args.nevents,"central","central"],
    #"/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v1_MINIAODSIM/181107_164712/0000/ JESUp":["TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8_JESUp.root",args.nevents,"Up","central"],
    #"/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v1_MINIAODSIM/181107_164712/0000/ JESDown":["TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8_JESDown.root",args.nevents,"Down","central"],
    #"/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v1_MINIAODSIM/181107_164712/0000/ JERUp":["TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8_JERUp.root",args.nevents,"central","Up"],
    #"/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v1_MINIAODSIM/181107_164712/0000/ JERDown":["TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8_JERDown.root",args.nevents,"central","Down"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v2_MINIAODSIM/181226_102657/0000/":["TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS.root",args.nevents,"central","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v2_MINIAODSIM/181226_102657/0000/ JESUp":["TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS_JESUp.root",args.nevents,"Up","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v2_MINIAODSIM/181226_102657/0000/ JESDown":["TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS_JESDown.root",args.nevents,"Down","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v2_MINIAODSIM/181226_102657/0000/ JERUp":["TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS_JERUp.root",args.nevents,"central","Up"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v2_MINIAODSIM/181226_102657/0000/ JERDown":["TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS_JERDown.root",args.nevents,"central","Down"],
    #*********************************************************
    #"/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTTo2L2Nu_TuneCP5up_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v1_MINIAODSIM/181107_165228/0000/":["TTTo2L2Nu_TuneCP5up_PSweights_13TeV-powheg-pythia8.root",args.nevents,"central","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTTo2L2Nu_TuneCP5up_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v1_MINIAODSIM/181111_190155/0000/":["TTTo2L2Nu_TuneCP5up_PSweights_13TeV-powheg-pythia8_VisiblePS.root",args.nevents,"central","central"],
    #"/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTTo2L2Nu_TuneCP5down_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v1_MINIAODSIM/181107_165006/0000/":["TTTo2L2Nu_TuneCP5down_PSweights_13TeV-powheg-pythia8.root",args.nevents,"central","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTTo2L2Nu_TuneCP5down_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v1_MINIAODSIM/181111_190030/0000/":["TTTo2L2Nu_TuneCP5down_PSweights_13TeV-powheg-pythia8_VisiblePS.root",args.nevents,"central","central"],
    #"/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTTo2L2Nu_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/181107_165736/0000/":["TTTo2L2Nu_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8.root",args.nevents,"central","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTTo2L2Nu_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/181111_190441/0000/":["TTTo2L2Nu_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS.root",args.nevents,"central","central"],
    #"/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTTo2L2Nu_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v1_MINIAODSIM/181108_083228/0000/":["TTTo2L2Nu_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8.root",args.nevents,"central","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTTo2L2Nu_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v1_MINIAODSIM/181111_190313/0000/":["TTTo2L2Nu_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS.root",args.nevents,"central","central"],

    #"/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v2_MINIAODSIM/181107_165945/0000/":["TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8.root",args.nevents,"central","central"],
    #"/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v2_MINIAODSIM/181107_165945/0000/ JESUp":["TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_JESUp.root",args.nevents,"Up","central"],
    #"/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v2_MINIAODSIM/181107_165945/0000/ JESDown":["TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_JESDown.root",args.nevents,"Down","central"],
    #"/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v2_MINIAODSIM/181107_165945/0000/ JERUp":["TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_JERUp.root",args.nevents,"central","Up"],
    #"/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v2_MINIAODSIM/181107_165945/0000/ JERDown":["TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_JERDown.root",args.nevents,"central","Down"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v2_MINIAODSIM/181111_190544/0000/":["TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS.root",args.nevents,"central","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v2_MINIAODSIM/181111_190544/0000/ JESUp":["TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS_JESUp.root",args.nevents,"Up","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v2_MINIAODSIM/181111_190544/0000/ JESDown":["TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS_JESDown.root",args.nevents,"Down","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v2_MINIAODSIM/181111_190544/0000/ JERUp":["TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS_JERUp.root",args.nevents,"central","Up"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v2_MINIAODSIM/181111_190544/0000/ JERDown":["TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS_JERDown.root",args.nevents,"central","Down"],
    #"/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTToSemiLeptonic_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/181107_170739/0000/":["TTToSemiLeptonic_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8.root",args.nevents,"central","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTToSemiLeptonic_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/181111_191100/0000/":["TTToSemiLeptonic_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS.root",args.nevents,"central","central"],
    #"/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTToSemiLeptonic_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v2_MINIAODSIM/181107_170556/0000/":["TTToSemiLeptonic_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8.root",args.nevents,"central","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTToSemiLeptonic_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v2_MINIAODSIM/181111_190937/0000/":["TTToSemiLeptonic_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS.root",args.nevents,"central","central"],
    #"/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTToSemiLeptonic_TuneCP5up_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v2_MINIAODSIM/181107_170253/0000/":["TTToSemiLeptonic_TuneCP5up_PSweights_13TeV-powheg-pythia8.root",args.nevents,"central","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTToSemiLeptonic_TuneCP5up_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v2_MINIAODSIM/181111_190648/0000/":["TTToSemiLeptonic_TuneCP5up_PSweights_13TeV-powheg-pythia8_VisiblePS.root",args.nevents,"central","central"],
    #"/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTToSemiLeptonic_TuneCP5down_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/181107_170424/0000/":["TTToSemiLeptonic_TuneCP5down_PSweights_13TeV-powheg-pythia8.root",args.nevents,"central","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTToSemiLeptonic_TuneCP5down_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/181111_190808/0000/":["TTToSemiLeptonic_TuneCP5down_PSweights_13TeV-powheg-pythia8_VisiblePS.root",args.nevents,"central","central"],

    #"/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v1_MINIAODSIM/181107_171001/0000/":["TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8.root",args.nevents,"central","central"],
    #"/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v1_MINIAODSIM/181107_171001/0000/ JESUp":["TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_JESUp.root",args.nevents,"Up","central"],
    #"/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v1_MINIAODSIM/181107_171001/0000/ JESDown":["TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_JESDown.root",args.nevents,"Down","central"],
    #"/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v1_MINIAODSIM/181107_171001/0000/ JERUp":["TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_JERUp.root",args.nevents,"central","Up"],
    #"/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v1_MINIAODSIM/181107_171001/0000/ JERDown":["TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_JERDown.root",args.nevents,"central","Down"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v1_MINIAODSIM/181111_191247/0000/":["TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS.root",args.nevents,"central","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v1_MINIAODSIM/181111_191247/0000/ JESUp":["TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS_JESUp.root",args.nevents,"Up","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v1_MINIAODSIM/181111_191247/0000/ JESDown":["TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS_JESDown.root",args.nevents,"Down","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v1_MINIAODSIM/181111_191247/0000/ JERUp":["TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS_JERUp.root",args.nevents,"central","Up"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v1_MINIAODSIM/181111_191247/0000/ JERDown":["TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS_JERDown.root",args.nevents,"central","Down"],
    #"/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTToHadronic_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v2_MINIAODSIM/181107_171920/0000/":["TTToHadronic_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8.root",args.nevents,"central","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTToHadronic_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v2_MINIAODSIM/181111_191931/0000/":["TTToHadronic_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS.root",args.nevents,"central","central"],
    #"/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTToHadronic_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/181108_170509/0000/":["TTToHadronic_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8.root",args.nevents,"central","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTToHadronic_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/181111_191718/0000/":["TTToHadronic_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS.root",args.nevents,"central","central"],
    #"/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTToHadronic_TuneCP5down_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v2_MINIAODSIM/181107_171156/0000/":["TTToHadronic_TuneCP5down_PSweights_13TeV-powheg-pythia8.root",args.nevents,"central","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTToHadronic_TuneCP5down_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v2_MINIAODSIM/181111_191400/0000/":["TTToHadronic_TuneCP5down_PSweights_13TeV-powheg-pythia8_VisiblePS.root",args.nevents,"central","central"],
    #"/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTToHadronic_TuneCP5up_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v1_MINIAODSIM/181107_171559/0000/":["TTToHadronic_TuneCP5up_PSweights_13TeV-powheg-pythia8.root",args.nevents,"central","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTToHadronic_TuneCP5up_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v1_MINIAODSIM/181111_191525/0000/":["TTToHadronic_TuneCP5up_PSweights_13TeV-powheg-pythia8_VisiblePS.root",args.nevents,"central","central"],

    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v2_MINIAODSIM/181107_173139/0000/":["ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8.root",args.nevents,"central","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v2_MINIAODSIM/181108_170145/0000/":["ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8.root",args.nevents,"central","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v1_MINIAODSIM/181107_172828/0000/":["ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8.root",args.nevents,"central","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v1_MINIAODSIM/181107_173330/0000/":["ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8.root",args.nevents,"central","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v2_MINIAODSIM/181108_170326/0000/":["ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8.root",args.nevents,"central","central"],

    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/181107_172036/0000/":["DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8.root",args.nevents,"central","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/181107_172337/0000/":["DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8.root",args.nevents,"central","central"],

    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v2_MINIAODSIM/181107_173627/0000/":["WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8.root",args.nevents,"central","central"],

    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/181107_181325/0000/":["WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8.root",args.nevents,"central","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/181107_180954/0000/":["WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8.root",args.nevents,"central","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/ZZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/181107_181710/0000/":["ZZZ_TuneCP5_13TeV-amcatnlo-pythia8.root",args.nevents,"central","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/WZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/181107_180513/0000/":["WZZ_TuneCP5_13TeV-amcatnlo-pythia8.root",args.nevents,"central","central"],

    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/WZ_TuneCP5_13TeV-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/181107_180124/0000/":["WZ_TuneCP5_13TeV-pythia8.root",args.nevents,"central","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/WW_TuneCP5_13TeV-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/181107_175723/0000/":["WW_TuneCP5_13TeV-pythia8.root",args.nevents,"central","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/ZZ_TuneCP5_13TeV-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/181107_175427/0000/":["ZZ_TuneCP5_13TeV-pythia8.root",args.nevents,"central","central"],

    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v1_MINIAODSIM/181107_182623/0000/":["ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8.root",args.nevents,"central","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v1_MINIAODSIM/181107_182157/0000/":["ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8.root",args.nevents,"central","central"],

    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTWJetsToLNu_TuneCP5_PSweights_13TeV-amcatnloFXFX-madspin-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14_v1_MINIAODSIM/181107_175120/0000/":["TTWJetsToLNu_TuneCP5_PSweights_13TeV-amcatnloFXFX-madspin-pythia8.root",args.nevents,"central","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v2_MINIAODSIM/181107_174811/0000/":["TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8.root",args.nevents,"central","central"],

    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTZToLLNuNu_M-10_TuneCP5_PSweights_13TeV-amcatnlo-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/181107_174432/0000/":["TTZToLLNuNu_M-10_TuneCP5_PSweights_13TeV-amcatnlo-pythia8.root",args.nevents,"central","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_MC_NewElectronIDv2/TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v2_MINIAODSIM/181107_174158/0000/":["TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8.root",args.nevents,"central","central"],
     
    # Data
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_Data_NewElectronIDv2/DoubleEG/Run2017C_31Mar2018_v1_MINIAOD/181107_154639/0000/":["DoubleEG_Run2017C_31Mar2018_v1_MINIAOD.root",args.nevents,"central","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_Data_NewElectronIDv2/DoubleEG/Run2017E_31Mar2018_v1_MINIAOD/181107_155124/0000/":["DoubleEG_Run2017E_31Mar2018_v1_MINIAOD.root",args.nevents,"central","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_Data_NewElectronIDv2/DoubleEG/Run2017B_31Mar2018_v1_MINIAOD/181107_154343/0000/":["DoubleEG_Run2017B_31Mar2018_v1_MINIAOD.root",args.nevents,"central","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_Data_NewElectronIDv2/DoubleEG/Run2017D_31Mar2018_v1_MINIAOD/181107_154859/0000/":["DoubleEG_Run2017D_31Mar2018_v1_MINIAOD.root",args.nevents,"central","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_Data_NewElectronIDv2/DoubleEG/Run2017F_31Mar2018_v1_MINIAOD/181107_155308/0000/":["DoubleEG_Run2017F_31Mar2018_v1_MINIAOD.root",args.nevents,"central","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_Data_NewElectronIDv2/MuonEG/Run2017C_31Mar2018_v1_MINIAOD/181107_155719/0000/":["MuonEG_Run2017C_31Mar2018_v1_MINIAOD.root",args.nevents,"central","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_Data_NewElectronIDv2/MuonEG/Run2017E_31Mar2018_v1_MINIAOD/181107_160219/0000/":["MuonEG_Run2017E_31Mar2018_v1_MINIAOD.root",args.nevents,"central","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_Data_NewElectronIDv2/MuonEG/Run2017B_31Mar2018_v1_MINIAOD/181107_155523/0000/":["MuonEG_Run2017B_31Mar2018_v1_MINIAOD.root",args.nevents,"central","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_Data_NewElectronIDv2/MuonEG/Run2017D_31Mar2018_v1_MINIAOD/181107_155857/0000/":["MuonEG_Run2017D_31Mar2018_v1_MINIAOD.root",args.nevents,"central","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_Data_NewElectronIDv2/MuonEG/Run2017F_31Mar2018_v1_MINIAOD/181107_160438/0000/":["MuonEG_Run2017F_31Mar2018_v1_MINIAOD.root",args.nevents,"central","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_Data_NewElectronIDv2/DoubleMuon/Run2017C_31Mar2018_v1_MINIAOD/181107_153456/0000/":["DoubleMuon_Run2017C_31Mar2018_v1_MINIAOD.root",args.nevents,"central","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_Data_NewElectronIDv2/DoubleMuon/Run2017E_31Mar2018_v1_MINIAOD/181107_153910/0000/":["DoubleMuon_Run2017E_31Mar2018_v1_MINIAOD.root",args.nevents,"central","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_Data_NewElectronIDv2/DoubleMuon/Run2017B_31Mar2018_v1_MINIAOD/181107_153133/0000/":["DoubleMuon_Run2017B_31Mar2018_v1_MINIAOD.root",args.nevents,"central","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_Data_NewElectronIDv2/DoubleMuon/Run2017D_31Mar2018_v1_MINIAOD/181107_153652/0000/":["DoubleMuon_Run2017D_31Mar2018_v1_MINIAOD.root",args.nevents,"central","central"],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/2017Analysis_Data_NewElectronIDv2/DoubleMuon/Run2017F_31Mar2018_v1_MINIAOD/181107_154139/0000/":["DoubleMuon_Run2017F_31Mar2018_v1_MINIAOD.root",args.nevents,"central","central"],
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
    if " " in indir: indir=indir.split(" ")[0] # This is just a trick to process also JES(R)Up(Down) without overwriting the dictionary
    print output[0].split("/")[-1]
    
    
    # splitting of the jobs
    if not os.path.isfile(nevents_dict_file) or args.nevents != -1 or indir not in nevents_dict.keys():
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
        if args.nevents == -1: nevents_dict[indir] = nevts_to_process
    
    else:
        nevts_to_process = nevents_dict[indir]
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
            ff_.write(workingdir+"/Selection --infiledirectory %s --outfilepath %s --config %s --triggers %s --nevents %i --firstevt %i --lastevt %i --JESsyst %s --JERsyst %s \n"%(indir,"$TMPDIR/"+output[0].split(".root")[0]+"_events_"+str(eventsList[i])+"_"+str(eventsList[i+1]-1)+".root", configfile , triggerfile, output[1],eventsList[i], eventsList[i+1], output[2], output[3]))
            #ff_.write("gfal-mkdir srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/$USER/Analysis/Selection \n")
            #ff_.write("gfal-mkdir srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/$USER/Analysis/Selection/OUTPUT_"+args.tag+" \n") 
            ff_.write("gfal-copy file://$TMPDIR/"+output[0].split(".root")[0]+"_events_"+str(eventsList[i])+"_"+str(eventsList[i+1]-1)+".root"+" srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/$USER/Analysis/Selection/OUTPUT_"+args.tag+"/"+output[0].split(".root")[0]+"_events_"+str(eventsList[i])+"_"+str(eventsList[i+1]-1)+".root \n")
            ff_.close()
            print "qsub -q localgrid -o %s/script.stdout -e %s/script.stderr -l walltime=06:00:00 %s/launch.sh"%(local_dir_tmp,local_dir_tmp,local_dir_tmp)
            stdout = os.popen("qsub -q localgrid -o %s/script.stdout -e %s/script.stderr -l walltime=06:00:00 %s/launch.sh"%(local_dir_tmp,local_dir_tmp,local_dir_tmp)).read()
            print "SUBMISSION OUTPUT: " + stdout
            print stdout == ""
            if stdout=="":
                print "Adding to resubmitting pipeline"
                resubmit_buffer.append("qsub -q localgrid -o %s/script.stdout -e %s/script.stderr -l walltime=06:00:00 %s/launch.sh"%(local_dir_tmp,local_dir_tmp,local_dir_tmp))
                
    
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
        ff_.write(workingdir+"/Selection --infiledirectory %s --outfilepath %s --config %s --triggers %s --nevents %i --firstevt %i --lastevt %i --JESsyst %s --JERsyst %s \n"%(indir,"$TMPDIR/"+output[0], configfile , triggerfile, output[1],0,output[1], output[2], output[3]))
        #ff_.write("gfal-mkdir srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/$USER/Analysis/Selection \n")
        #ff_.write("gfal-mkdir srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/$USER/Analysis/Selection/OUTPUT_"+args.tag+" \n")
        ff_.write("gfal-copy file://$TMPDIR/"+output[0]+" srm://maite.iihe.ac.be:8443/pnfs/iihe/cms/store/user/$USER/Analysis/Selection/OUTPUT_"+args.tag+"/"+output[0]+" \n")
        ff_.close()
        print "qsub -q localgrid -o %s/script.stdout -e %s/script.stderr -l walltime=06:00:00 %s/launch.sh"%(local_dir_tmp,local_dir_tmp,local_dir_tmp)
        stdout = os.popen("qsub -q localgrid -o %s/script.stdout -e %s/script.stderr -l walltime=06:00:00 %s/launch.sh"%(local_dir_tmp,local_dir_tmp,local_dir_tmp)).read()
        print "SUBMISSION OUTPUT: " + stdout
        print stdout == ""
        if stdout=="":
            print "Adding to resubmitting pipeline"
            resubmit_buffer.append("qsub -q localgrid -o %s/script.stdout -e %s/script.stderr -l walltime=06:00:00 %s/launch.sh"%(local_dir_tmp,local_dir_tmp,local_dir_tmp))

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
