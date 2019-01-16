import ROOT
import os
#from Helper import *
from argparse import ArgumentParser
import time
import multiprocessing
import thread
import subprocess
import sys
import signal
import inspect
from copy import deepcopy


"""
Full PS: 
    top and anti-top found
    categorization based on additional jets:
        cat = 0: ttbb (ttXID = 53,54,55)
        cat = 1: ttbL (ttXID = 51,52)
        cat = 2: ttcc (ttXID = 43,44,45)
        cat = 3: ttcL (ttXID = 41,42)
        cat = 4: ttLL (ttXID = 0)
        cat = -1: ttOther (top and anti-top were not found in truth info (should never happen really...))
"""


def Analyze(indir, outfile, IdxBegin = 0, IdxEnd = -1, Splitted = False):
    
    intree_ = ROOT.TChain("FlatTree/tree")
    files = [f for f in os.listdir(indir) if "output" in f and ".root" in f]
    for f in files:
        print f
        intree_.Add(indir+"/"+f)
    
    
    if Splitted: ofile_ = ROOT.TFile(outfile.replace(".root","_events_"+str(IdxBegin)+"_"+str(IdxEnd)+".root"),"RECREATE")
    else: ofile_ = TFile(outfile,"RECREATE")
    
    hist_full = ROOT.TH1D("hist_full",";;number of MC events",6,-1.5,4.5)
    
    original_nentries = intree_.GetEntries()
    if IdxEnd > IdxBegin:
        actual_nentries = IdxEnd-IdxBegin
    else: actual_nentries = original_nentries
    
    # ***************** Start event loop ********************
    for evt in range(IdxBegin,IdxEnd):
        if (evt % int(actual_nentries/10.) == 0): print"Processing event %i/%i (%.1f %%)"%(evt,IdxEnd,100*float(evt-IdxBegin)/float(actual_nentries))
        intree_.GetEntry(evt)
        
        mcweight = intree_.mc_weight
        genttxid = intree_.genTTX_id
        
        # if not at least 4 genJets were found within acceptance, continue
        ngen = 0
        for iGenJet in range(intree_.genJet_n):
            if intree_.genJet_pt[iGenJet] > 20: 
                ngen += 1
            if ngen >= 4: break
        
        if ngen < 4:
            hist_vis.Fill(-1,mcweight)
            continue
        
        # loop over gen particles
        foundTop1 = 0 #top
        foundTop2 = 0 #antitop
        for iGen in range(intree_.gen_n):
            if ( abs(intree_.gen_id[iGen]) != 6 ): continue
            
            # find unique particle
            pcur = iGen
            nLimit = 1000 # temporary fix
            iter = 0
            while( 1 ):
                foundDupl = False
                daug = intree_.gen_daughter_index[pcur]
                Ndaug = intree_.gen_daughter_n[pcur]
                for ip in range(Ndaug):
                    d = daug[ip]
                    if (intree_.gen_id[d] == intree_.gen_id[pcur]) and not (pcur == d):
                        pcur = d
                        foundDupl = True
                        break
                if not foundDupl:
                    break
                if iter > nLimit:
                    break
                iter += 1
            c = pcur
            ##########################
            
            pdgid = intree_.gen_id[c]
            status = intree_.gen_status[c]
            
            if ( status == 62 and ((pdgid == 6 and not foundTop1) or (pdgid == -6 and not foundTop2)) ):
                if( pdgid == 6 ): foundTop1 = 1
                if( pdgid == -6 ): foundTop2 = 1

        # Events with two b-jets from top decay and two leptons within acceptance are now selected        
        if not foundTop1 or not foundTop2:
            hist_full.Fill(-1,mcweight)
            continue
        
        id = int(str(intree_.genTTX_id)[-2:])
        print id, intree_.genTTX_id
        if (id == 53 or id == 54 or id == 55):hist_full.Fill(0,mcweight) #ttbb
        elif (id == 51 or id == 52): hist_full.Fill(1,mcweight) #ttbL
        elif (id == 43 or id == 44 or id == 45): hist_full.Fill(2,mcweight) #ttcc
        elif (id == 41 or id == 42): hist_full.Fill(3,mcweight) #ttcL
        elif (id == 0): hist_full.Fill(4,mcweight) #ttLF
        else:
            print "COULD NOT ASSIGN MEANINGFULL CATEGORY!!!! FILLING -1 INSTEAD"
            hist_full.Fill(-1,mcweight)
    
    
    
    
    # ***************** end of  event loop ********************
    
    hist_full.GetXaxis().SetBinLabel(1,"t#bar{t}Other")
    hist_full.GetXaxis().SetBinLabel(2,"t#bar{t}b#bar{b}")
    hist_full.GetXaxis().SetBinLabel(3,"t#bar{t}bL")
    hist_full.GetXaxis().SetBinLabel(4,"t#bar{t}c#bar{c}")
    hist_full.GetXaxis().SetBinLabel(5,"t#bar{t}cL")
    hist_full.GetXaxis().SetBinLabel(6,"t#bar{t}LF")
    
    ofile_.cd()
    hist_full.Write()
    ofile_.Close()
        
           



def main():

    parser = ArgumentParser()
    parser.add_argument('--indir', default="FILLMEPLEASE",help='path to input files output_n.root')
    parser.add_argument('--outfile', default="*",help='path and name of output file')
    parser.add_argument('--firstEvt', type=int, default=0,help='first event')
    parser.add_argument('--lastEvt', type=int, default=-1,help='last event')
    parser.add_argument('--splitted', type=int, default=0,help='bool for splitted or not')
    args = parser.parse_args()
    
    Analyze(args.indir, args.outfile, args.firstEvt, args.lastEvt, bool(args.splitted))
    
    

if __name__ == "__main__":
	main()


