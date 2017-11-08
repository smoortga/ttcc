from Helper import *
import os
import time
from argparse import ArgumentParser
import ROOT
from ROOT import gSystem, TFile
gSystem.Load('../objects/Electron_C')
gSystem.Load('../objects/Muon_C')
gSystem.Load('../objects/Jet_C')
gSystem.Load('../objects/MissingEnergy_C')
gSystem.Load('../objects/Trigger_C')
from ROOT import Electron, Muon, Jet, MissingEnergy, Trigger
from array import array

def Analyze(infile, outfile):

    infile_ = TFile(infile)
    intree_ = infile_.Get("tree")
    
    ofile_ = TFile(outfile,"RECREATE")
    otree_ = intree_.CloneTree(0)
    
    # **************************** add extra branches to output****************************
    dict_variableName_Leaves = {}
    dict_variableName_Leaves.update({"DileptonInvariantMass": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"DileptonDeltaR": [array('d', [0]),"D"]})
    
    for name,arr in dict_variableName_Leaves.iteritems():
        otree_.Branch(name,arr[0],name+"/"+arr[1])
    #****************************************************************************************
    
    nEntries = intree_.GetEntries()
    #nEntries = 1000
    
    print "Processing File %s, containing %i events"%(infile,nEntries)
    
    v_el = ROOT.std.vector( Electron )()
    v_mu = ROOT.std.vector( Muon )()
    v_jet = ROOT.std.vector( Jet )()
    
    # ***************** Start event loop ********************
    for evt in range(nEntries):
        if (evt % int(nEntries/10.) == 0): print"%s: Processing event %i/%i (%.1f %%)"%(infile.split("/")[-1],evt,nEntries,100*float(evt)/float(nEntries))
        intree_.GetEntry(evt)
        
        v_el = intree_.Electrons
        v_mu = intree_.Muons
        v_jet = intree_.Jets
        
        
        # ***************** Leading Electron ********************
        leading_elec = Electron()
        found_leading_elec = False
        for el in v_el:
             if (el.isTight() and el.relIso() < 0.15 and el.Pt() > leading_elec.Pt()): 
                found_leading_elec = True
                leading_elec = el
        # *******************************************************
        
        # ***************** Leading Muon ********************
        leading_muon = Muon()
        found_leading_muon = False
        for mu in v_mu:
             if (mu.isTight() and mu.relIso() < 0.15 and mu.Pt() > leading_muon.Pt()): 
                found_leading_muon = True
                leading_muon = mu
        # *******************************************************
        
        if (found_leading_elec and found_leading_muon):
            dict_variableName_Leaves["DileptonInvariantMass"][0][0] = DileptonIvariantMass(leading_elec,leading_muon)#DiLeptonIvariantMass(leading_elec.p4(),leading_muon.p4())
            dict_variableName_Leaves["DileptonDeltaR"][0][0] = DileptonDeltaR(leading_elec,leading_muon)
        else: continue
        
        
        otree_.Fill()
        
        v_el.clear()
        v_mu.clear()
    # ***************** end of  event loop ********************
    
    ofile_.cd()
    otree_.Write()
    
    ofile_.Close()
    infile_.Close()
    
    



def main():

    parser = ArgumentParser()
    #parser.add_argument('--nevents', type=int, default=-1,help='number of events for each sample')
    parser.add_argument('--tag', default=time.strftime("%a%d%b%Y_%Hh%Mm%Ss"),help='name of output directory')
    args = parser.parse_args()

    workingdir = os.getcwd()

    if not os.path.isdir(workingdir+"/SELECTED_"+args.tag): os.mkdir(workingdir+"/SELECTED_"+args.tag)
    Analyze("../selection/OUTPUT_Tue07Nov2017_15h51m33s/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8.root",workingdir+"/SELECTED_"+args.tag+"/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8.root")

if __name__ == "__main__":
	main()





# v = ROOT.std.vector( Electron )()
# v.push_back(object)
# v.push_back(object)
# 
# f = TFile("test.root", "recreate")
# mytree = TTree("mytree", "testing tree appending")
# mytree.Branch("electron", v) 
# mytree.Fill()  
# 
# f.WriteTObject(mytree)
# f.Close()
# 
# f = TFile("test.root")
# t = f.Get("mytree")
# nEntries = t.GetEntries()
# print nEntries
# for i in range(nEntries):
#     t.GetEntry(i)
#     el_collection = t.electron
#     print el_collection.size()
#     for el in el_collection:
#         print el.Pt()
#         el.setp4()
# 