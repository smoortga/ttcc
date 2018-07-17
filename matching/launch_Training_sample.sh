#!/bin/bash
pwd=$PWD
source $VO_CMS_SW_DIR/cmsset_default.sh                                                    
cd /storage_mnt/storage/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src         
eval `scram runtime -sh`                                                                   
cd $pwd
cdir=/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/
export LD_LIBRARY_PATH=${cdir}:${cdir}/selection:$LD_LIBRARY_PATH

cd /user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/setup
root -l setup.C

cd /user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/matching
python CreateMatchingSamples.py --indir=/pnfs/iihe/cms/store/user/smoortga/Analysis/Selection/OUTPUT_WithGenTTXJets_DeepCSVReweighting/ --tag=FullTrainingWithGenTTXJets --nmaxevtsperjob=250000 --ncpu=8


