#!/bin/bash
source /user/smoortga/sklearn_setenv.sh
cdir=/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/
export LD_LIBRARY_PATH=${cdir}:${cdir}/selection:$LD_LIBRARY_PATH

cd /user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/analyse
python Analyze.py --indir=/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/selection/OUTPUT_Full2017DataMC_UnPrescaledTriggers/SelectedSamples/ --topmatchingdir=/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/matching/FullTrainingWithFlippedAndWeightsDeepScaledInputs/ --tag=CorrectBTagShapeReweighting --ncpu=8


