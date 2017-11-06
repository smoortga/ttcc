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
        "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/FirstTests-02112017/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_v1_MINIAODSIM/171102_140923/0000/":["ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1.root",args.nevents],
        "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/FirstTests-02112017/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_v1_MINIAODSIM/171102_141157/0000/":["WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root",args.nevents],
        "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/FirstTests-02112017/ST_t-channel_top_4f_inclusiveDecays_TuneCUETP8M2T4_13TeV-powhegV2-madspin/RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_v1_MINIAODSIM/171102_141015/0000/":["ST_t-channel_top_4f_inclusiveDecays_TuneCUETP8M2T4_13TeV-powhegV2-madspin.root",args.nevents],
        "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/FirstTests-02112017/ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_v1_MINIAODSIM/171102_141250/0000/":["ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8.root",args.nevents],
        "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/FirstTests-02112017/ttZJets_13TeV_madgraphMLM/RunIISummer16MiniAODv2_80X_mcRun2_asymptotic_2016_TrancheIV_v6_v1_MINIAODSIM/171102_141317/0000/":["ttZJets_13TeV_madgraphMLM.root",args.nevents],
        "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/FirstTests-02112017/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4/RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_v1_MINIAODSIM/171102_141045/0000/":["ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4.root",args.nevents],
        "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/FirstTests-02112017/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_v1_MINIAODSIM/171102_140828/0000/":["DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8.root",args.nevents],
        "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/FirstTests-02112017/ttWJets_13TeV_madgraphMLM/RunIISummer16MiniAODv2_80X_mcRun2_asymptotic_2016_TrancheIV_v6_v1_MINIAODSIM/171102_141355/0000/":["ttWJets_13TeV_madgraphMLM.root",args.nevents],
        "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/FirstTests-02112017/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2_PUMoriond17_HCALDebug_80X_mcRun2_asymptotic_2016_TrancheIV_v6_v1_MINIAODSIM/171102_140856/0000/":["DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8.root",args.nevents],
        "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/FirstTests-02112017/ttHToNonbb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_v1_MINIAODSIM/171102_141222/0000/":["ttHToNonbb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8.root",args.nevents],
        "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/FirstTests-02112017/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4/RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_v1_MINIAODSIM/171102_141109/0000/":["ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4.root",args.nevents],
        "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/FirstTests-02112017/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_v1_MINIAODSIM/171102_141133/0000/":["TT_TuneCUETP8M2T4_13TeV-powheg-pythia8.root",args.nevents],
        "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/FirstTests-02112017/ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_v1_MINIAODSIM/171102_140949/0000/":["ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1.root",args.nevents]
    }

if not os.path.isdir(workingdir+"/OUTPUT_"+args.tag): os.mkdir(workingdir+"/OUTPUT_"+args.tag)
if not os.path.isdir(workingdir+"/OUTPUT_"+args.tag+"/localgrid_"+args.tag): os.mkdir(workingdir+"/OUTPUT_"+args.tag+"/localgrid_"+args.tag)
for indir, output in samples.iteritems():
    dir_tmp = workingdir+"/OUTPUT_"+args.tag+"/localgrid_"+args.tag+"/"+output[0].split(".")[0]
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