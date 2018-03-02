import os

"""
Make sure you did "cmsenv" before running this script!
"""


path_to_analysis_JSON = "~/Analysis/NTupler/CMSSW_8_0_25/src/FlatTree/FlatTreeProducer/test/PROD/GRL/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt"
#/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/PileUp/pileup_latest.txt
path_to_pileup_JSON = "~/Analysis/NTupler/CMSSW_8_0_25/src/FlatTree/FlatTreeAnalyzer/ttcc/selection/config/pileupJSON_2016.txt"
max_PU = 75
minbias_xsec = 69200
minbias_xsec_up = 72383
minbias_xsec_down = 66017

# 4.6% systematics
# https://twiki.cern.ch/twiki/bin/view/CMS/PileupJSONFileforData
# https://twiki.cern.ch/twiki/bin/view/CMS/PileupSystematicErrors

print "***************************************************"
print "Make sure you did 'cmsenv' before running this script!"
print "***************************************************"

print "Calculating PU nominal histograms"
print "pileupCalc.py -i %s --inputLumiJSON %s --calcMode true --minBiasXsec %i --maxPileupBin %i --numPileupBins %i Pileup.root"%(path_to_analysis_JSON,path_to_pileup_JSON,minbias_xsec,max_PU,max_PU)
os.system("pileupCalc.py -i %s --inputLumiJSON %s --calcMode true --minBiasXsec %i --maxPileupBin %i --numPileupBins %i Pileup.root"%(path_to_analysis_JSON,path_to_pileup_JSON,minbias_xsec,max_PU,max_PU))

print "Calculating PU Up-variation histograms"
print "pileupCalc.py -i %s --inputLumiJSON %s --calcMode true --minBiasXsec %i --maxPileupBin %i --numPileupBins %i Pileup.root"%(path_to_analysis_JSON,path_to_pileup_JSON,minbias_xsec_up,max_PU,max_PU)
os.system("pileupCalc.py -i %s --inputLumiJSON %s --calcMode true --minBiasXsec %i --maxPileupBin %i --numPileupBins %i Pileup_Up.root"%(path_to_analysis_JSON,path_to_pileup_JSON,minbias_xsec_up,max_PU,max_PU))

print "Calculating PU Down-variation histograms"
print "pileupCalc.py -i %s --inputLumiJSON %s --calcMode true --minBiasXsec %i --maxPileupBin %i --numPileupBins %i Pileup.root"%(path_to_analysis_JSON,path_to_pileup_JSON,minbias_xsec_down,max_PU,max_PU)
os.system("pileupCalc.py -i %s --inputLumiJSON %s --calcMode true --minBiasXsec %i --maxPileupBin %i --numPileupBins %i Pileup_Down.root"%(path_to_analysis_JSON,path_to_pileup_JSON,minbias_xsec_down,max_PU,max_PU))
