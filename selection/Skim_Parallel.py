from ROOT import *
from argparse import ArgumentParser
import time
import multiprocessing
import thread
import subprocess

parser = ArgumentParser()
parser.add_argument('--ncpu', type=int, default=-1,help='number of CPU to use in parallel')
parser.add_argument('--nevents', type=int, default=-1,help='number of events for each sample')
parser.add_argument('--tag', default=time.strftime("%a%d%b%Y_%Hh%Mm%Ss"),help='name of output directory')
args = parser.parse_args()

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
    if (args.ncpu < 0 or args.ncpu > multiprocessing.cpu_count()): parallelProcesses = multiprocessing.cpu_count()
    else: parallelProcesses = args.ncpu
    p = multiprocessing.Pool(parallelProcesses)
    print "Using %i parallel processes" %parallelProcesses
    
    #if args.nevents > 0: nEntries = args.nevents
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
    
    
    for indir, output in samples.iteritems():
        p.apply_async(runSelection, args = (indir, "./"+args.tag+"/"+output[0], output[1],))#-1
    p.close()
    p.join()

    print "Total elpased time: %.2f seconds"%(time.time()-time_start)


if __name__ == "__main__":
    main()