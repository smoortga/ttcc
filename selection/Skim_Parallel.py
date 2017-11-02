from ROOT import *
from argparse import ArgumentParser
import time
import multiprocessing
import thread
import subprocess



def runSelection(inputdir, outputfile, nevts):
    Selection(inputdir, outputfile, nevts)

def main():
    
    gROOT.ProcessLine(".L Converter.C+")
    gROOT.ProcessLine(".L Selection.C+")

    gSystem.Load("LoadVectorDict_C")
    gSystem.Load("../objects/Electron_C")
    gSystem.Load("../objects/Muon_C")
    gSystem.Load("../objects/Jet_C")
    gSystem.Load("../objects/MissingEnergy_C")
    gSystem.Load("../objects/Trigger_C")
    
    time_start = time.time()
    parallelProcesses = multiprocessing.cpu_count()
    p = multiprocessing.Pool(parallelProcesses)
    print "Using %i parallel processes" %parallelProcesses
    
    samples = {
        "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/FirstTests-25102017/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_v1_MINIAODSIM/171025_114734/0000/":["./SelectedSamples/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8.root",100000],
        "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/FirstTests-25102017/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4/RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_v1_MINIAODSIM/171025_114640/0000/":["./SelectedSamples/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4.root",100000]
    }
    
    
    for indir, output in samples.iteritems():
        print indir, output[0], output[1]
        p.apply_async(runSelection, args = (indir, output[0], output[1],))#-1
    p.close()
    p.join()

    print "Total elpased time: %.2f seconds"%(time.time()-time_start)


if __name__ == "__main__":
    main()