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
Visible PS: 
    two (truth) leptons form top and antitop decay found with pT > 30 GeV and abs(Eta) < 2.4
    two b-jets from top decays found (ttXID starts with 2)
    categorization based on additional jets:
        cat = 0: ttbb (ttXID = 53,54,55)
        cat = 1: ttbL (ttXID = 51,52)
        cat = 2: ttcc (ttXID = 43,44,45)
        cat = 3: ttcL (ttXID = 41,42)
        cat = 4: ttLL (ttXID = 0)
        cat = -1: ttOther (ttxID does not start with 2 or leptons not found)
"""


def Analyze(indir, outfile, IdxBegin = 0, IdxEnd = -1, Splitted = False):
    
    nevents = IdxEnd-IdxBegin
    processed_filenames = []
    intree_ = ROOT.TChain("FlatTree/tree")
    files = [f for f in os.listdir(indir) if "output" in f and ".root" in f]
    for f in files:
        print f
        intree_.Add(indir+"/"+f)
        processed_filenames.append(f)
        if (nevents > 0 and intree_.GetEntries() > IdxEnd): break
    
    
    
    if Splitted: ofile_ = ROOT.TFile(outfile.replace(".root","_events_"+str(IdxBegin)+"_"+str(IdxEnd)+".root"),"RECREATE")
    else: ofile_ = TFile(outfile,"RECREATE")
    
    hist_vis = ROOT.TH1D("hist_vis",";;number of MC events",6,-1.5,4.5)
    
    original_nentries = intree_.GetEntries()
    if IdxEnd > IdxBegin:
        actual_nentries = IdxEnd-IdxBegin
    else: actual_nentries = original_nentries
    
    events_this_job = actual_nentries
    
    
    # ***************** Start event loop ********************
    for evt in range(IdxBegin,IdxEnd):
        if (evt % int(actual_nentries/10.) == 0): print"Processing event %i/%i (%.1f %%)"%(evt,IdxEnd,100*float(evt-IdxBegin)/float(actual_nentries))
        intree_.GetEntry(evt)
        
        mcweight = intree_.mc_weight
        genttxid = intree_.genTTX_id
        
        # if not two b jets form decay were found in visible phase space: don't count
        if not int(str(intree_.genTTX_id)[0]) == 2: 
            hist_vis.Fill(-1,mcweight)
            continue
        
        # if not at least 4 genJets were found within acceptance, continue
        ngen = 0
        for iGenJet in range(intree_.genJet_n):
            if intree_.genJet_pt[iGenJet] > 20 and abs(intree_.genJet_eta[iGenJet]) < 2.4: 
                ngen += 1
            if ngen >= 4: break
        
        if ngen < 4:
            hist_vis.Fill(-1,mcweight)
            continue
        
        # loop over gen particles
        foundTop1 = 0 #top
        foundTop2 = 0 #antitop
        foundLep1 = 0
        foundLep2 = 0
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
                
                for j in range(intree_.gen_daughter_n[c]):
                    idx = intree_.gen_daughter_index[c][j]
                    pdgid_c = intree_.gen_id[idx]
                    
                    if( abs(pdgid_c) == 24 ):
                        # find unique particle
                        ppcur = idx
                        nLimit = 1000 # temporary fix
                        iiter = 0
                        while( 1 ):
                            foundDupl = False
                            daug = intree_.gen_daughter_index[ppcur]
                            Ndaug = intree_.gen_daughter_n[ppcur]
                            for ip in range(Ndaug):
                                d = daug[ip]
                                if (intree_.gen_id[d] == intree_.gen_id[ppcur]) and not (ppcur == d):
                                    ppcur = d
                                    foundDupl = True
                                    break
                            if not foundDupl:
                                break
                            if iiter > nLimit:
                                break
                            iiter += 1
                        cc = ppcur
                        ##########################
                        
                        #start loop over W daughters
                        for j2 in range(intree_.gen_daughter_n[cc]):
                            idx2 = intree_.gen_daughter_index[cc][j2]
                            pdgid_cc = intree_.gen_id[idx2]
                            momPdgid_cc = intree_.gen_id[intree_.gen_mother_index[idx2]]
                            if( (abs(pdgid_cc) == 11 or abs(pdgid_cc) == 13 or abs(pdgid_cc) == 15 or abs(pdgid_cc) == 12 or abs(pdgid_cc) == 14 or abs(pdgid_cc) == 16) and not abs(momPdgid_cc) == 15 ):
                                
                                # find unique particle
                                pppcur = idx2
                                nLimit = 1000 # temporary fix
                                iiiter = 0
                                while( 1 ):
                                    foundDupl = False
                                    daug = intree_.gen_daughter_index[pppcur]
                                    Ndaug = intree_.gen_daughter_n[pppcur]
                                    for ip in range(Ndaug):
                                        d = daug[ip]
                                        if (intree_.gen_id[d] == intree_.gen_id[pppcur]) and not (pppcur == d):
                                            pppcur = d
                                            foundDupl = True
                                            break
                                    if not foundDupl:
                                        break
                                    if iiiter > nLimit:
                                        break
                                    iiiter += 1
                                ccc = pppcur
                                ##########################
                                
                                
                                if( (abs(pdgid_cc) == 11 or abs(pdgid_cc) == 13 or abs(pdgid_cc) == 15) and pdgid == 6 ) :
                                    if intree_.gen_pt[ccc] > 25. and abs(intree_.gen_eta[ccc]) < 2.4:
                                        foundLep1 = 1
                                if( (abs(pdgid_cc) == 11 or abs(pdgid_cc) == 13 or abs(pdgid_cc) == 15) and pdgid == -6 ):
                                    if intree_.gen_pt[ccc] > 25. and abs(intree_.gen_eta[ccc]) < 2.4:
                                        foundLep2 = 1
                
        
        # Events with two b-jets from top decay and two leptons within acceptance are now selected        
        if not foundTop1 or not foundTop2 or not foundLep1 or not foundLep2:
            hist_vis.Fill(-1,mcweight)
            continue
        
        id = int(str(intree_.genTTX_id)[-2:])
        #print id, intree_.genTTX_id
        if (id == 53 or id == 54 or id == 55):hist_vis.Fill(0,mcweight) #ttbb
        elif (id == 51 or id == 52): hist_vis.Fill(1,mcweight) #ttbL
        elif (id == 43 or id == 44 or id == 45): hist_vis.Fill(2,mcweight) #ttcc
        elif (id == 41 or id == 42): hist_vis.Fill(3,mcweight) #ttcL
        elif (id == 0): hist_vis.Fill(4,mcweight) #ttLF
        else:
            print "COULD NOT ASSIGN MEANINGFULL CATEGORY!!!! FILLING -1 INSTEAD"
            hist_vis.Fill(-1,mcweight)
    
    
    
    
    # ***************** end of  event loop ********************
    
    hist_vis.GetXaxis().SetBinLabel(1,"t#bar{t}Other")
    hist_vis.GetXaxis().SetBinLabel(2,"t#bar{t}b#bar{b}")
    hist_vis.GetXaxis().SetBinLabel(3,"t#bar{t}bL")
    hist_vis.GetXaxis().SetBinLabel(4,"t#bar{t}c#bar{c}")
    hist_vis.GetXaxis().SetBinLabel(5,"t#bar{t}cL")
    hist_vis.GetXaxis().SetBinLabel(6,"t#bar{t}LF")
    
    ofile_.cd()
    hist_vis.Write()
    
        
        
        

    # Copy the hcount and hweight to save the original amount of simulated events
    hcount = ROOT.TH1D("hcount","hcount",1,0.,1.)
    hweight = ROOT.TH1D("hweight","hweight",1,0.,1.)
    for f in processed_filenames:
        f_ = ROOT.TFile(indir+"/"+f)
        hcount.Add(f_.Get("FlatTree/hcount"))
        hweight.Add(f_.Get("FlatTree/hweight"))
        f_.Close()

    if (events_this_job > 0 and events_this_job < intree_.GetEntries()):
        hcount.SetBinContent(1,events_this_job*hcount.GetBinContent(1)/float(intree_.GetEntries()))
        hweight.SetBinContent(1,events_this_job*hweight.GetBinContent(1)/float(intree_.GetEntries()))

    ofile_.cd()
    hcount.Write()
    hweight.Write()
    
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


