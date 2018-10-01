#!/bin/bash
source /user/smoortga/sklearn_setenv.sh
cd /user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/matching/
python /user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/matching/TrainMatchingNN.py --tag=JetPtAbove30GeV --skipEvery=5 --nepoch=100 --infile=/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/matching/Training_JetPtAbove30GeV/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8.root