import os
import time
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('--nevents', type=int, default=-1,help='number of events for each sample')
parser.add_argument('--tag', default=time.strftime("%a%d%b%Y_%Hh%Mm%Ss"),help='name of output directory')
args = parser.parse_args()

basedir = "/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/"
workingdir = "/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/selection"
configfile = workingdir+"/config/config.ini"
triggerfile = workingdir+"/config/triggers.txt"

samples = {
    # MC
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC/DYJetsToLL_M-4to50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/180518_204914/0000/":["./SelectedSamples/DYJetsToLL_M-4to50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/180518_204722/0000/":["./SelectedSamples/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC/ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/180518_205106/0000/":["./SelectedSamples/ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC/ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/180518_205258/0000/":["./SelectedSamples/ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC/ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/180518_205454/0000/":["./SelectedSamples/ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/180518_205643/0000/":["./SelectedSamples/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC/ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/180518_205840/0000/":["./SelectedSamples/ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_v1_MINIAODSIM/180518_204525/0000/":["./SelectedSamples/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2_PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1_v2_MINIAODSIM/180518_210034/0000/":["./SelectedSamples/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8.root",args.nevents],
    # Data
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_Data/DoubleEG/Run2017B_31Mar2018_v1_MINIAOD/180522_114603/0000/":["./SelectedSamples/DoubleEG_Run2017B_31Mar2018_v1_MINIAOD.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_Data/DoubleEG/Run2017C_31Mar2018_v1_MINIAOD/180522_114704/0000/":["./SelectedSamples/DoubleEG_Run2017C_31Mar2018_v1_MINIAOD.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_Data/DoubleEG/Run2017D_31Mar2018_v1_MINIAOD/180522_114804/0000/":["./SelectedSamples/DoubleEG_Run2017D_31Mar2018_v1_MINIAOD.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_Data/DoubleEG/Run2017E_31Mar2018_v1_MINIAOD/180522_114901/0000/":["./SelectedSamples/DoubleEG_Run2017E_31Mar2018_v1_MINIAOD.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_Data/DoubleEG/Run2017F_31Mar2018_v1_MINIAOD/180522_114957/0000/":["./SelectedSamples/DoubleEG_Run2017F_31Mar2018_v1_MINIAOD.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_Data/DoubleMuon/Run2017B_31Mar2018_v1_MINIAOD/180522_114016/0000/":["./SelectedSamples/DoubleMuon_Run2017B_31Mar2018_v1_MINIAOD.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_Data/DoubleMuon/Run2017C_31Mar2018_v1_MINIAOD/180522_114131/0000/":["./SelectedSamples/DoubleMuon_Run2017C_31Mar2018_v1_MINIAOD.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_Data/DoubleMuon/Run2017D_31Mar2018_v1_MINIAOD/180522_114303/0000/":["./SelectedSamples/DoubleMuon_Run2017D_31Mar2018_v1_MINIAOD.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_Data/DoubleMuon/Run2017E_31Mar2018_v1_MINIAOD/180522_114408/0000/":["./SelectedSamples/DoubleMuon_Run2017E_31Mar2018_v1_MINIAOD.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_Data/DoubleMuon/Run2017F_31Mar2018_v1_MINIAOD/180522_114507/0000/":["./SelectedSamples/DoubleMuon_Run2017F_31Mar2018_v1_MINIAOD.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_Data/MuonEG/Run2017B_31Mar2018_v1_MINIAOD/180522_115057/0000/":["./SelectedSamples/MuonEG_Run2017B_31Mar2018_v1_MINIAOD.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_Data/MuonEG/Run2017C_31Mar2018_v1_MINIAOD/180522_115153/0000/":["./SelectedSamples/MuonEG_Run2017C_31Mar2018_v1_MINIAOD.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_Data/MuonEG/Run2017D_31Mar2018_v1_MINIAOD/180522_115252/0000/":["./SelectedSamples/MuonEG_Run2017D_31Mar2018_v1_MINIAOD.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_Data/MuonEG/Run2017E_31Mar2018_v1_MINIAOD/180522_115348/0000/":["./SelectedSamples/MuonEG_Run2017E_31Mar2018_v1_MINIAOD.root",args.nevents],
    "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_Data/MuonEG/Run2017F_31Mar2018_v1_MINIAOD/180522_115453/0000/":["./SelectedSamples/MuonEG_Run2017F_31Mar2018_v1_MINIAOD.root",args.nevents]
}


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
    ff_.write("cd /storage_mnt/storage/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src \n")                                                                                                                                                          
    ff_.write("eval `scram runtime -sh` \n")                                                                                                                                           
    ff_.write("cd $pwd \n")  
    ff_.write("cdir=%s \n"%basedir)
    ff_.write("export LD_LIBRARY_PATH=${cdir}:${cdir}/..:$LD_LIBRARY_PATH \n")
    ff_.write("export X509_USER_PROXY=/user/$USER/x509up_$(id -u $USER) \n")
    ff_.write(workingdir+"/Selection --infiledirectory %s --outfilepath %s --config %s --triggers %s --nevents %i \n"%(indir,workingdir+"/OUTPUT_"+args.tag+"/"+output[0], configfile , triggerfile, output[1]))
    ff_.close()
    

    print "qsub -q localgrid -o %s/script.stdout -e %s/script.stderr  %s/launch.sh"%(dir_tmp,dir_tmp,dir_tmp)
    os.system("qsub -q localgrid -o %s/script.stdout -e %s/script.stderr %s/launch.sh"%(dir_tmp,dir_tmp,dir_tmp))
    
print "Done! use 'qstat -u $USER' to monitor samples"
print "use 'for j in $(qselect -u $USER);do timeout 3 qdel -a $j;done' to delete all your jobs"
