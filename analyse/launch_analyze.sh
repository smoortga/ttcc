#!/bin/bash
source /user/smoortga/sklearn_setenv.sh
cdir=/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/
export LD_LIBRARY_PATH=${cdir}:${cdir}/selection:$LD_LIBRARY_PATH

cd /user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/setup
root -l setup.C

cd /user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/analyse
#python Analyze.py --indir=/pnfs/iihe/cms/store/user/smoortga/Analysis/Selection/OUTPUT_WithGenTTXJets_DeepCSVReweighting/ --topmatchingdir=/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/matching/FullTrainingWithGenTTXJets/ --tag=CorrectBTagShapeReweighting_AllJetsUsedForSF_newMatchingTraining_WithoutCTagInfo --ncpu=16 --nmaxevtsperjob=100000
#python Analyze.py --indir=/pnfs/iihe/cms/store/user/smoortga/Analysis/Selection/OUTPUT_WithGenTTXJets_DeepCSVReweighting/ --topmatchingdir=/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/matching/FullTrainingWithGenTTXJets_WithCTagInfo/ --tag=CorrectBTagShapeReweighting_AllJetsUsedForSF_newMatchingTraining --ncpu=-1
#python Analyze_ttbarControl.py --indir=/pnfs/iihe/cms/store/user/smoortga/Analysis/Selection/OUTPUT_ttbarControlRegion/ --topmatchingdir=/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/matching/FullTrainingWithGenTTXJets_WithCTagInfo/ --tag=ttbar_controlRegion --ncpu=8 
python Analyze_Z_ControlRegion.py --indir=/pnfs/iihe/cms/store/user/smoortga/Analysis/Selection/OUTPUT_WithGenTTXJets_DeepCSVReweighting/ --topmatchingdir=/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/matching/FullTrainingWithGenTTXJets_WithCTagInfo/ --tag=ZControlRegion --ncpu=8 --nmaxevtsperjob=50000


