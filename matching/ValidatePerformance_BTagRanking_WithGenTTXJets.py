from Helper import *
from argparse import ArgumentParser
import time
import multiprocessing
import thread
import subprocess
import sys
import signal
import inspect
from ROOT import TTree
# from keras.models import load_model
# from keras.models import Sequential
# from keras.layers import Dense, Activation, Dropout
# import pickle
# import numpy as np
# from sklearn.preprocessing import StandardScaler


parser = ArgumentParser()
parser.add_argument('--indir', default="/pnfs/iihe/cms/store/user/smoortga/Analysis/Selection/OUTPUT_WithGenTTXJets_DeepCSVReweighting/",help='directory name of input files')
parser.add_argument('--infiles', default="TTJets*",help='name of input files')
parser.add_argument('--tag', default=time.strftime("%a%d%b%Y_%Hh%Mm%Ss"),help='name of output directory')
parser.add_argument('--nevents', type=int, default=-1,help='maximum number of events for each dataset to process')
parser.add_argument('--nmaxevtsperjob', type=int, default=400000,help='maximum number of events per job (otherwise split)')
parser.add_argument('--ncpu', type=int, default=-1,help='number of CPU to use in parallel')
parser.add_argument('--topmatchingdir', default=os.getcwd(),help='name of training directory')
args = parser.parse_args()


def Analyze(infile, outdir=args.topmatchingdir, IdxBegin = 0, IdxEnd = -1, Splitted = False):
    
    if not os.path.isfile(infile):
        print "ERROR: COULD NOT FIND FILE: %s!!!"%infile
        sys.exit(1)
    
    infile_ = TFile(infile)
    intree_ = infile_.Get("tree")
    
    # if Splitted: ofile_ = TFile(outfile.replace(".root","_"+str(IdxBegin)+"_"+str(IdxEnd)+".root"),"RECREATE")
#     else: ofile_ = TFile(outfile,"RECREATE")
#     otree_correct_ = TTree("tree_correct","tree_correct")
#     otree_wrong_ = TTree("tree_wrong","tree_wrong")
    
    # **************************** add extra branches to output****************************
    dict_variableName_Leaves = {}
    # event category
    dict_variableName_Leaves.update({"event_Category": [array('i', [0]),"I"]})
    #kinematics
    dict_variableName_Leaves.update({"pT_topb": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"pT_antitopb": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"pT_addlead": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"pT_addsublead": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"Eta_topb": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"Eta_antitopb": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"Eta_addlead": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"Eta_addsublead": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"Phi_topb": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"Phi_antitopb": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"Phi_addlead": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"Phi_addsublead": [array('d', [0]),"D"]})
    #Discriminators
    dict_variableName_Leaves.update({"CSVv2_topb": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"CSVv2_antitopb": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"CSVv2_addlead": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"CSVv2_addsublead": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"DeepCSVBDiscr_topb": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"DeepCSVBDiscr_antitopb": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"DeepCSVBDiscr_addlead": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"DeepCSVBDiscr_addsublead": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"DeepCSVCvsL_topb": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"DeepCSVCvsL_antitopb": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"DeepCSVCvsL_addlead": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"DeepCSVCvsL_addsublead": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"DeepCSVCvsB_topb": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"DeepCSVCvsB_antitopb": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"DeepCSVCvsB_addlead": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"DeepCSVCvsB_addsublead": [array('d', [0]),"D"]})
    #DeltaR
    dict_variableName_Leaves.update({"DeltaR_topb_leppos": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"DeltaR_antitopb_lepneg": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"DeltaR_adds": [array('d', [0]),"D"]})
    #invariant masses
    dict_variableName_Leaves.update({"minv_topb_leppos": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"minv_antitopb_lepneg": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"minv_adds": [array('d', [0]),"D"]})
    
    # for name,arr in dict_variableName_Leaves.iteritems():
#         otree_correct_.Branch(name,arr[0],name+"/"+arr[1])
#         otree_wrong_.Branch(name,arr[0],name+"/"+arr[1])
    #****************************************************************************************
    # **************************** Top matching training files ****************************
    # model = load_model(args.topmatchingdir+"/model_checkpoint_save.hdf5")
#     scaler = pickle.load(open(args.topmatchingdir+"/scaler.pkl","rb"))
#     variables = pickle.load(open(args.topmatchingdir+"/variables.pkl","rb"))

    #****************************************************************************************
    
    
    # **************************** Validation Histograms ****************************
    h_correct = ROOT.TH1D("h_correct",";;Fraction of events",7,-0.5,6.5)
    h_flipped = ROOT.TH1D("h_flipped",";;Fraction of events",7,-0.5,6.5)
    h_only_top_correct = ROOT.TH1D("h_only_top_correct",";;Fraction of events",7,-0.5,6.5)
    h_only_oneoutoftwo = ROOT.TH1D("h_only_oneoutoftwo",";;Fraction of events",7,-0.5,6.5)
    h_wrong = ROOT.TH1D("h_wrong",";;Fraction of events",7,-0.5,6.5)
    h_nomatch = ROOT.TH1D("h_nomatch",";;Fraction of events",7,-0.5,6.5)

    #****************************************************************************************
    
    
    original_nentries = intree_.GetEntries()
    if IdxEnd > IdxBegin:
        actual_nentries = IdxEnd-IdxBegin
    else: actual_nentries = original_nentries
    
    #if nevents > 0 and nevents < nEntries: nEntries = nevents
    #nEntries = 1000
    
    print "Processing File %s, containing %i events (processing %i events from %i to %i)"%(infile,original_nentries,actual_nentries,IdxBegin,IdxEnd)
    
    v_el = ROOT.std.vector( Electron )()
    v_mu = ROOT.std.vector( Muon )()
    v_jet = ROOT.std.vector( Jet )()
    v_GenTTXJets = ROOT.std.vector( GenJet )()
    v_met = ROOT.std.vector( MissingEnergy )()
    v_trig = ROOT.std.vector( Trigger )()
    v_truth = ROOT.std.vector( Truth )()
    
    nselectedevts=0
    # ***************** Start event loop ********************
    for evt in range(IdxBegin,IdxEnd):
        if (evt % int(actual_nentries/10.) == 0): print"%s: Processing event %i/%i (%.1f %%)"%(infile.split("/")[-1],evt,IdxEnd,100*float(evt-IdxBegin)/float(actual_nentries))
        intree_.GetEntry(evt)
        
        v_el = intree_.Electrons
        v_mu = intree_.Muons
        v_jet = intree_.Jets
        v_GenTTXJets = intree_.GenTTXJets
        v_trig = intree_.Trigger
        v_met = intree_.MET
        if "TTJets" in infile or "TTTo2L2Nu" in infile: v_truth = intree_.Truth
        
        
        
        
        
        # ***************** Leading Electrons ********************
        leading_elec = Electron()
        subleading_elec = Electron()
        n_isolated_electrons = 0
        for el in v_el:
            #**********************
            #   LEADING ELECTRON?
            #**********************
            if (el.isMedium() and el.relIso() < 0.077 and abs(el.Eta()) < 1.48 and el.Pt() > leading_elec.Pt()): 
                n_isolated_electrons = n_isolated_electrons + 1
                subleading_elec = leading_elec.Clone() # the previous leading one now becomes subleading
                leading_elec = el
            elif (el.isMedium() and el.relIso() < 0.068 and abs(el.Eta()) >= 1.48 and el.Pt() > leading_elec.Pt()): 
                n_isolated_electrons = n_isolated_electrons + 1
                subleading_elec = leading_elec.Clone()
                leading_elec = el
            #**********************
            #   SUBLEADING ELECTRON?
            #**********************
            elif (el.isMedium() and el.relIso() < 0.077 and abs(el.Eta()) < 1.48 and el.Pt() > subleading_elec.Pt()): 
                n_isolated_electrons = n_isolated_electrons + 1
                subleading_elec = el
            elif (el.isMedium() and el.relIso() < 0.068 and abs(el.Eta()) >= 1.48 and el.Pt() > subleading_elec.Pt()): 
                n_isolated_electrons = n_isolated_electrons + 1
                subleading_elec = el
        # *******************************************************
        
        # ***************** Leading Muon ********************
        leading_muon = Muon()
        subleading_muon = Muon()
        n_isolated_muons = 0
        for mu in v_mu:
             #**********************
             #   LEADING MUON?
             #**********************
             if (mu.isTight() and mu.relIso() < 0.15 and mu.Pt() > leading_muon.Pt()): 
                n_isolated_muons = n_isolated_muons + 1
                subleading_muon = leading_muon.Clone() # the previous leading one now becomes subleading
                leading_muon = mu
            
             #**********************
             #   SUBLEADING MUON?
             #**********************
             elif (mu.isTight() and mu.relIso() < 0.15 and mu.Pt() > subleading_muon.Pt()): 
                n_isolated_muons = n_isolated_muons + 1
                subleading_muon = mu

        # *******************************************************
        
        if ((n_isolated_muons + n_isolated_electrons) != 2): continue
        # ***************** Leading Lepton ********************
        leading_leptons = [leading_elec,subleading_elec,leading_muon,subleading_muon]
        leading_leptons.sort(key=lambda x: x.Pt(), reverse=True) # Pt ordering
        leading_leptons = leading_leptons[0:2]

        #print isinstance(leading_leptons[0],Electron)

        
        
        # define the lepton categories
        lepton_category=-1
        if (isinstance(leading_leptons[0],Electron) and isinstance(leading_leptons[1],Electron)): lepton_category = 0 # elel
        elif (isinstance(leading_leptons[0],Muon) and isinstance(leading_leptons[1],Muon)): lepton_category = 1 # mumu
        elif ( (isinstance(leading_leptons[0],Muon) and isinstance(leading_leptons[1],Electron)) or (isinstance(leading_leptons[0],Electron) and isinstance(leading_leptons[1],Muon)) ): lepton_category = 2 # elmu/muel
        else: 
            print "NO PROPER LEPTON CATEGORY FOUND"
            continue
        
        Zmass = 91.1876
        Zwindow = 15.
        ZmassLow = Zmass-Zwindow
        ZmassHigh = Zmass+Zwindow
        
        # Require OS leptons
        if leading_leptons[0].Charge()*leading_leptons[1].Charge() >= 0: continue
        
        mll = DileptonIvariantMass(leading_leptons[0],leading_leptons[1])
        
        if (lepton_category == 2): # elmu
            if not (mll>12.): continue 
            #dict_variableName_Leaves["lepton_Category"][0][0] = 2 #emu
            
        elif (lepton_category == 0): # elel
            if v_met.at(0).Pt() < 30: continue
            if (mll>ZmassLow and mll<ZmassHigh): continue
            #dict_variableName_Leaves["lepton_Category"][0][0] = 0 #elel  
            
        elif (lepton_category == 1): # mumu
            if v_met.at(0).Pt() < 30: continue
            if (mll>ZmassLow and mll<ZmassHigh): continue
            #dict_variableName_Leaves["lepton_Category"][0][0] = 1 #mumu  
            
        else: continue     
        
              
        
        # *******************************************************
        
        
        # ***************** Jets ********************
        # event category based on jet content
        # https://twiki.cern.ch/twiki/bin/view/CMSPublic/GenHFHadronMatcher
        if (not intree_.is_data):
            cat = -1 # default for anything not ttbar of for ttbar which is not in the following categories
            if intree_.genTTX_id != -999:
                id = int(str(intree_.genTTX_id)[-2:])
                if "TTJets" in infile or "TTTo2L2Nu" in infile:
                    if (id == 53 or id == 54 or id == 55): cat = 0 #ttbb
                    elif (id == 51 or id == 52): cat = 1 #ttbj
                    elif (id == 43 or id == 44 or id == 45): cat = 2 #ttcc
                    elif (id == 41 or id == 42): cat = 3 #ttcj
                    elif (id == 0): cat = 4 #ttjj
        
        
        # start the classification / assignment of the jets
        jclf = JetsClassifier(v_jet)
        jclf.Clean(leading_leptons[0],leading_leptons[1])
        
        
        #if not jclf.IsValid(): continue # at least 4 valid jets found with valid CSVv2 values
        
        validjets = jclf.validJets()
        
        if len(validjets) < 4: continue
        
        
#         print "*****"
#         for idx,j in enumerate(validjets):
#             print "jet %i: "%idx, j.Eta(), j.Phi(), j.Pt(), j.HadronFlavour()
#         print "leading lepton: ",leading_leptons[0].Eta(), leading_leptons[0].Phi(), leading_leptons[0].Pt()
#         print "subleading lepton: ",leading_leptons[1].Eta(), leading_leptons[1].Phi(), leading_leptons[1].Pt()
        
        # Gen level info
        toptruth_lep_pt = -999;
        toptruth_lep_eta = -999;
        toptruth_lep_phi = -999;
        toptruth_b_pt = -999;
        toptruth_b_eta = -999;
        toptruth_b_phi = -999;
        antitoptruth_lep_pt = -999;
        antitoptruth_lep_eta = -999;
        antitoptruth_lep_phi = -999;
        antitoptruth_b_pt = -999;
        antitoptruth_b_eta = -999;
        antitoptruth_b_phi = -999;
        if "TTJets" in infile or "TTTo2L2Nu" in infile: 
            for truth in v_truth:
                label_name = truth.LabelName()
                if label_name == "top_lep":
                    toptruth_lep_pt = truth.Pt()
                    toptruth_lep_eta = truth.Eta()
                    toptruth_lep_phi = truth.Phi()
                elif label_name == "antitop_lep":
                    antitoptruth_lep_pt = truth.Pt()
                    antitoptruth_lep_eta = truth.Eta()
                    antitoptruth_lep_phi = truth.Phi()
                elif label_name == "top_b":
                    toptruth_b_pt = truth.Pt()
                    toptruth_b_eta = truth.Eta()
                    toptruth_b_phi = truth.Phi()
                elif label_name == "antitop_b":
                    antitoptruth_b_pt = truth.Pt()
                    antitoptruth_b_eta = truth.Eta()
                    antitoptruth_b_phi = truth.Phi()
                else: continue
        
        #match the gen-level leptons
        #print DeltaPhi(leading_leptons[0].Phi(),toptruth_lep_phi)
        if sqrt(pow(DeltaPhi(leading_leptons[0].Phi(),toptruth_lep_phi),2) + pow(leading_leptons[0].Eta()-toptruth_lep_eta,2)) < 0.1 and sqrt(pow(DeltaPhi(leading_leptons[1].Phi(),antitoptruth_lep_phi),2) + pow(leading_leptons[1].Eta()-antitoptruth_lep_eta,2)) < 0.1:
            top_lepton = leading_leptons[0]
            antitop_lepton = leading_leptons[1]
    
        elif sqrt(pow(DeltaPhi(leading_leptons[1].Phi(),toptruth_lep_phi),2) + pow(leading_leptons[1].Eta()-toptruth_lep_eta,2)) < 0.1 and sqrt(pow(DeltaPhi(leading_leptons[0].Phi(),antitoptruth_lep_phi),2) + pow(leading_leptons[0].Eta()-antitoptruth_lep_eta,2)) < 0.1:
            top_lepton = leading_leptons[1]
            antitop_lepton = leading_leptons[0]
        
        else: continue
        
        # define positively charged lepton and negatively charged lepton
        if leading_leptons[0].Charge() > 0 and leading_leptons[1].Charge() < 0:
            pos_lepton = leading_leptons[0]
            neg_lepton = leading_leptons[1]
        elif leading_leptons[0].Charge() < 0 and leading_leptons[1].Charge() > 0:
            pos_lepton = leading_leptons[1]
            neg_lepton = leading_leptons[0]
        else: continue
        
        #print "top lepton: ",top_lepton.Eta(),toptruth_lep_eta, top_lepton.Phi(), toptruth_lep_phi
        #print "antitop lepton: ",antitop_lepton.Eta(),antitoptruth_lep_eta, antitop_lepton.Phi(), antitoptruth_lep_phi
        
        
        # match gen-level b's
        bjet_matching_dict = {}
        for jdx,jet in enumerate(validjets):
            if sqrt(pow(DeltaPhi(jet.Phi(),toptruth_b_phi),2) + pow(jet.Eta()-toptruth_b_eta,2)) < 0.3: bjet_matching_dict["top_bjet"] = jet
            elif sqrt(pow(DeltaPhi(jet.Phi(),antitoptruth_b_phi),2) + pow(jet.Eta()-antitoptruth_b_eta,2)) < 0.3: bjet_matching_dict["antitop_bjet"] = jet
        
        # if len(bjet_matching_dict) != 2: 
#             h_nomatch.Fill(0)
#             if cat == 4: h_nomatch.Fill(5) #ttjj
#             elif cat == 0: h_nomatch.Fill(1) #ttbb
#             elif cat == 1: h_nomatch.Fill(2) #ttbj
#             elif cat == 2: h_nomatch.Fill(3) #ttcc
#             elif cat == 3: h_nomatch.Fill(4) #ttcj
#             elif cat == -1: h_nomatch.Fill(6) #ttcj
#             continue
        if len(bjet_matching_dict) == 2 and bjet_matching_dict["top_bjet"] == bjet_matching_dict["antitop_bjet"]: continue # can in principle not happen, but just to be sure
        
        
        add_matching_dict = {}
        if len(v_GenTTXJets) == 2:
            add1_gen_pt = v_GenTTXJets.at(0).Pt()
            add1_gen_eta = v_GenTTXJets.at(0).Eta()
            add1_gen_phi = v_GenTTXJets.at(0).Phi()
            add2_gen_pt = v_GenTTXJets.at(1).Pt()
            add2_gen_eta = v_GenTTXJets.at(1).Eta()
            add2_gen_phi = v_GenTTXJets.at(1).Phi()
            #print "ADD1 GenJet: ", add1_gen_pt, add1_gen_eta, add1_gen_phi
            #print "ADD2 GenJet: ", add2_gen_pt, add2_gen_eta, add2_gen_phi
            for jdx,jet in enumerate(validjets):
                if sqrt(pow(DeltaPhi(jet.GenJetPhi(),add1_gen_phi),2) + pow(jet.GenJetEta()-add1_gen_eta,2)) < 0.001 and not "add1_jet" in add_matching_dict.keys(): add_matching_dict["add1_jet"] = jet
                elif sqrt(pow(DeltaPhi(jet.GenJetPhi(),add1_gen_phi),2) + pow(jet.GenJetEta()-add1_gen_eta,2)) < 0.001 and "add1_jet" in add_matching_dict.keys(): add_matching_dict["add2_jet"] = jet
                elif sqrt(pow(DeltaPhi(jet.GenJetPhi(),add2_gen_phi),2) + pow(jet.GenJetEta()-add2_gen_eta,2)) < 0.001 and not "add1_jet" in add_matching_dict.keys(): add_matching_dict["add1_jet"] = jet
                elif sqrt(pow(DeltaPhi(jet.GenJetPhi(),add2_gen_phi),2) + pow(jet.GenJetEta()-add2_gen_eta,2)) < 0.001 and "add1_jet" in add_matching_dict.keys(): add_matching_dict["add2_jet"] = jet
        
        
        elif len(v_GenTTXJets) == 1:
            add1_gen_pt = v_GenTTXJets.at(0).Pt()
            add1_gen_eta = v_GenTTXJets.at(0).Eta()
            add1_gen_phi = v_GenTTXJets.at(0).Phi()
            #print "ADD1 GenJet: ", add1_gen_pt, add1_gen_eta, add1_gen_phi
            for jdx,jet in enumerate(validjets):
                if sqrt(pow(DeltaPhi(jet.GenJetPhi(),add1_gen_phi),2) + pow(jet.GenJetEta()-add1_gen_eta,2)) < 0.001: add_matching_dict["add1_jet"] = jet
        
        
        # now investigate all possible permutations
        #best_perm_val = -999
        best_perm = (-1,-1,-1,-1)
        #correct_perm_val=-999
        correct_perm = (-1,-1,-1,-1)
        perm = [i for i in permutations(range(len(validjets)),4)]
        for p in perm:
        
            if len(bjet_matching_dict) != 2: break
            
            perm_top_bjet = validjets.at(p[0])
            perm_antitop_bjet = validjets.at(p[1])
            if perm_top_bjet.Pt() < 30 or perm_antitop_bjet.Pt() < 30: continue
            remaining_indices = range(len(validjets))
            remaining_indices.remove(p[0])
            remaining_indices.remove(p[1])
            remaining_jets = [validjets.at(ij) for ij in remaining_indices]
            ptsorted_remaining_jets = sorted(remaining_jets, key=lambda x: x.DeepCSVBDiscr(), reverse=True)
            perm_addjet_lead = ptsorted_remaining_jets[0]
            perm_addjet_sublead = ptsorted_remaining_jets[1]
            
            if len( add_matching_dict ) == 2:
                if validjets.at(p[0]) == bjet_matching_dict["top_bjet"] and validjets.at(p[1]) == bjet_matching_dict["antitop_bjet"] and  ((perm_addjet_lead == add_matching_dict["add1_jet"] and perm_addjet_sublead == add_matching_dict["add2_jet"]) or (perm_addjet_lead == add_matching_dict["add2_jet"] and perm_addjet_sublead == add_matching_dict["add1_jet"])):
                    correct_perm=p
                    #correct_perm_val=discr
            elif len( add_matching_dict ) == 1:
                if validjets.at(p[0]) == bjet_matching_dict["top_bjet"] and validjets.at(p[1]) == bjet_matching_dict["antitop_bjet"] and  (perm_addjet_lead == add_matching_dict["add1_jet"]):
                    correct_perm=p
            else:
                if validjets.at(p[0]) == bjet_matching_dict["top_bjet"] and validjets.at(p[1]) == bjet_matching_dict["antitop_bjet"]:
                    correct_perm=p
                
        
        btagvalues = [i.DeepCSVBDiscr() for i in validjets]
        ranking = [0] * len(btagvalues)
        for i, x in enumerate(sorted(range(len(btagvalues)), key=lambda y: btagvalues[y])):
            ranking[x] = i
        best_perm = (ranking.index(len(ranking)-1),ranking.index(len(ranking)-2),ranking.index(len(ranking)-3),ranking.index(len(ranking)-4))
        
        #if validjets.at(best_perm[0])
        if not isDeepCSVBDiscrM(validjets.at(best_perm[0])) or not isDeepCSVBDiscrM(validjets.at(best_perm[1])): continue
        if validjets.at(best_perm[0]).Pt()<30 or validjets.at(best_perm[1]).Pt()<30: continue
        #best_perm[1] = ranking.index(len(ranking)-2)
        
        #print btagvalues,best_perm
        
        if len( add_matching_dict ) != 0 and cat == 4:
            print "ERROR: Fournt ttLF event with add jets!!"
            print id, cat
            sys.exit(1)
        
        
        if best_perm[0] == -1 or best_perm[1] == -1 or best_perm[2] == -1 or best_perm[3] == -1:
            print "ERROR: did not find right permutations"
            sys.exit(1)
        
        if len(bjet_matching_dict) != 2: 
            h_nomatch.Fill(0)
            if cat == 4: h_nomatch.Fill(5) #ttjj
            elif cat == 0: h_nomatch.Fill(1) #ttbb
            elif cat == 1: h_nomatch.Fill(2) #ttbj
            elif cat == 2: h_nomatch.Fill(3) #ttcc
            elif cat == 3: h_nomatch.Fill(4) #ttcj
            elif cat == -1: h_nomatch.Fill(6) #ttcj
        
        elif (len( add_matching_dict ) == 2) and (correct_perm[0] == best_perm[0]) and (correct_perm[1] == best_perm[1]) and ( ((correct_perm[2] == best_perm[2]) and (correct_perm[3] == best_perm[3])) or ((correct_perm[3] == best_perm[2]) and (correct_perm[2] == best_perm[3])) ):
            h_correct.Fill(0)
            if cat == 4: h_correct.Fill(5) #ttjj
            elif cat == 0: h_correct.Fill(1) #ttbb
            elif cat == 1: h_correct.Fill(2) #ttbj
            elif cat == 2: h_correct.Fill(3) #ttcc
            elif cat == 3: h_correct.Fill(4) #ttcj
            elif cat == -1: h_correct.Fill(6) #ttcj
        #elif (len( add_matching_dict ) == 2) and (correct_perm[0] == best_perm[0]) and (correct_perm[1] == best_perm[1]) and not ( ((correct_perm[2] == best_perm[2]) and (correct_perm[3] == best_perm[3])) or ((correct_perm[3] == best_perm[2]) and (correct_perm[2] == best_perm[3])) ):
           #  h_only_top_correct.Fill(0)
#             if cat == 4: h_only_top_correct.Fill(5) #ttjj
#             elif cat == 0: h_only_top_correct.Fill(1) #ttbb
#             elif cat == 1: h_only_top_correct.Fill(2) #ttbj
#             elif cat == 2: h_only_top_correct.Fill(3) #ttcc
#             elif cat == 3: h_only_top_correct.Fill(4) #ttcj
#             elif cat == -1: h_only_top_correct.Fill(6) #ttcj 
        elif (len( add_matching_dict ) == 2) and (correct_perm[0] == best_perm[0]) and (correct_perm[1] == best_perm[1]) and ( len(list(set([best_perm[2],best_perm[3]])&set([correct_perm[2],correct_perm[3]]))) == 1 ):
            h_only_oneoutoftwo.Fill(0)
            if cat == 4: h_only_oneoutoftwo.Fill(5) #ttjj
            elif cat == 0: h_only_oneoutoftwo.Fill(1) #ttbb
            elif cat == 1: h_only_oneoutoftwo.Fill(2) #ttbj
            elif cat == 2: h_only_oneoutoftwo.Fill(3) #ttcc
            elif cat == 3: h_only_oneoutoftwo.Fill(4) #ttcj
            elif cat == -1: h_only_oneoutoftwo.Fill(6) #ttcj 
        elif (len( add_matching_dict ) == 2) and (correct_perm[0] == best_perm[0]) and (correct_perm[1] == best_perm[1]) and ( len(list(set([best_perm[2],best_perm[3]])&set([correct_perm[2],correct_perm[3]]))) == 0 ):
            h_only_top_correct.Fill(0)
            if cat == 4: h_only_top_correct.Fill(5) #ttjj
            elif cat == 0: h_only_top_correct.Fill(1) #ttbb
            elif cat == 1: h_only_top_correct.Fill(2) #ttbj
            elif cat == 2: h_only_top_correct.Fill(3) #ttcc
            elif cat == 3: h_only_top_correct.Fill(4) #ttcj
            elif cat == -1: h_only_top_correct.Fill(6) #ttcj    
        
        elif (len( add_matching_dict ) == 1) and (correct_perm[0] == best_perm[0]) and (correct_perm[1] == best_perm[1]) and ( ((correct_perm[2] == best_perm[2])) or ((correct_perm[2] == best_perm[3])) ):
            h_correct.Fill(0)
            if cat == 4: h_correct.Fill(5) #ttjj
            elif cat == 0: h_correct.Fill(1) #ttbb
            elif cat == 1: h_correct.Fill(2) #ttbj
            elif cat == 2: h_correct.Fill(3) #ttcc
            elif cat == 3: h_correct.Fill(4) #ttcj
            elif cat == -1: h_correct.Fill(6) #ttcj
        
        elif (len( add_matching_dict ) == 1) and (correct_perm[0] == best_perm[0]) and (correct_perm[1] == best_perm[1]) and not ( ((correct_perm[2] == best_perm[2])) or ((correct_perm[2] == best_perm[3])) ):
            h_only_top_correct.Fill(0)
            if cat == 4: h_only_top_correct.Fill(5) #ttjj
            elif cat == 0: h_only_top_correct.Fill(1) #ttbb
            elif cat == 1: h_only_top_correct.Fill(2) #ttbj
            elif cat == 2: h_only_top_correct.Fill(3) #ttcc
            elif cat == 3: h_only_top_correct.Fill(4) #ttcj
            elif cat == -1: h_only_top_correct.Fill(6) #ttcj
        
        elif (len( add_matching_dict ) == 0) and (correct_perm[0] == best_perm[0]) and (correct_perm[1] == best_perm[1]):
            h_correct.Fill(0)
            if cat == 4: h_correct.Fill(5) #ttjj
            elif cat == 0: h_correct.Fill(1) #ttbb
            elif cat == 1: h_correct.Fill(2) #ttbj
            elif cat == 2: h_correct.Fill(3) #ttcc
            elif cat == 3: h_correct.Fill(4) #ttcj
            elif cat == -1: h_correct.Fill(6) #ttcj
            
        elif (len( add_matching_dict ) == 2) and (correct_perm[0] == best_perm[1]) and (correct_perm[1] == best_perm[0]) and ( ((correct_perm[2] == best_perm[2]) and (correct_perm[3] == best_perm[3])) or ((correct_perm[3] == best_perm[2]) and (correct_perm[2] == best_perm[3])) ):
            h_flipped.Fill(0)
            if cat == 4: h_flipped.Fill(5) #ttjj
            elif cat == 0: h_flipped.Fill(1) #ttbb
            elif cat == 1: h_flipped.Fill(2) #ttbj
            elif cat == 2: h_flipped.Fill(3) #ttcc
            elif cat == 3: h_flipped.Fill(4) #ttcj
            elif cat == -1: h_flipped.Fill(6) #ttcj
        
        # elif (len( add_matching_dict ) == 2) and (correct_perm[0] == best_perm[1]) and (correct_perm[1] == best_perm[0]) and not ( ((correct_perm[2] == best_perm[2]) and (correct_perm[3] == best_perm[3])) or ((correct_perm[3] == best_perm[2]) and (correct_perm[2] == best_perm[3])) ):
#             h_only_top_correct.Fill(0)
#             if cat == 4: h_only_top_correct.Fill(5) #ttjj
#             elif cat == 0: h_only_top_correct.Fill(1) #ttbb
#             elif cat == 1: h_only_top_correct.Fill(2) #ttbj
#             elif cat == 2: h_only_top_correct.Fill(3) #ttcc
#             elif cat == 3: h_only_top_correct.Fill(4) #ttcj
#             elif cat == -1: h_only_top_correct.Fill(6) #ttcj
        
        elif (len( add_matching_dict ) == 2) and (correct_perm[0] == best_perm[1]) and (correct_perm[1] == best_perm[0]) and ( len(list(set([best_perm[2],best_perm[3]])&set([correct_perm[2],correct_perm[3]]))) == 1 ):
            h_only_oneoutoftwo.Fill(0)
            if cat == 4: h_only_oneoutoftwo.Fill(5) #ttjj
            elif cat == 0: h_only_oneoutoftwo.Fill(1) #ttbb
            elif cat == 1: h_only_oneoutoftwo.Fill(2) #ttbj
            elif cat == 2: h_only_oneoutoftwo.Fill(3) #ttcc
            elif cat == 3: h_only_oneoutoftwo.Fill(4) #ttcj
            elif cat == -1: h_only_oneoutoftwo.Fill(6) #ttcj 
        elif (len( add_matching_dict ) == 2) and (correct_perm[0] == best_perm[1]) and (correct_perm[1] == best_perm[0]) and ( len(list(set([best_perm[2],best_perm[3]])&set([correct_perm[2],correct_perm[3]]))) == 0 ):
            h_only_top_correct.Fill(0)            
            if cat == 4: h_only_top_correct.Fill(5) #ttjj
            elif cat == 0: h_only_top_correct.Fill(1) #ttbb
            elif cat == 1: h_only_top_correct.Fill(2) #ttbj
            elif cat == 2: h_only_top_correct.Fill(3) #ttcc
            elif cat == 3: h_only_top_correct.Fill(4) #ttcj
            elif cat == -1: h_only_top_correct.Fill(6) #ttcj 
            
        elif (len( add_matching_dict ) == 1) and (correct_perm[0] == best_perm[1]) and (correct_perm[1] == best_perm[0]) and ( ((correct_perm[2] == best_perm[2])) or ((correct_perm[2] == best_perm[3])) ):
            h_flipped.Fill(0)
            if cat == 4: h_flipped.Fill(5) #ttjj
            elif cat == 0: h_flipped.Fill(1) #ttbb
            elif cat == 1: h_flipped.Fill(2) #ttbj
            elif cat == 2: h_flipped.Fill(3) #ttcc
            elif cat == 3: h_flipped.Fill(4) #ttcj
            elif cat == -1: h_flipped.Fill(6) #ttcj
            
        elif (len( add_matching_dict ) == 1) and (correct_perm[0] == best_perm[1]) and (correct_perm[1] == best_perm[0]) and not ( ((correct_perm[2] == best_perm[2])) or ((correct_perm[2] == best_perm[3])) ):
            h_only_top_correct.Fill(0)
            if cat == 4: h_only_top_correct.Fill(5) #ttjj
            elif cat == 0: h_only_top_correct.Fill(1) #ttbb
            elif cat == 1: h_only_top_correct.Fill(2) #ttbj
            elif cat == 2: h_only_top_correct.Fill(3) #ttcc
            elif cat == 3: h_only_top_correct.Fill(4) #ttcj
            elif cat == -1: h_only_top_correct.Fill(6) #ttcj
            
        elif (len( add_matching_dict ) == 0) and (correct_perm[0] == best_perm[1]) and (correct_perm[1] == best_perm[0]):
            h_flipped.Fill(0)
            if cat == 4: h_flipped.Fill(5) #ttjj
            elif cat == 0: h_flipped.Fill(1) #ttbb
            elif cat == 1: h_flipped.Fill(2) #ttbj
            elif cat == 2: h_flipped.Fill(3) #ttcc
            elif cat == 3: h_flipped.Fill(4) #ttcj
            elif cat == -1: h_flipped.Fill(6) #ttcj    

        else:
            h_wrong.Fill(0)
            if cat == 4: h_wrong.Fill(5) #ttjj
            elif cat == 0: h_wrong.Fill(1) #ttbb
            elif cat == 1: h_wrong.Fill(2) #ttbj
            elif cat == 2: h_wrong.Fill(3) #ttcc
            elif cat == 3: h_wrong.Fill(4) #ttcj
            elif cat == -1: h_wrong.Fill(6) #ttcj

        nselectedevts += 1
        
        v_el.clear()
        v_mu.clear()
        v_jet.clear()
        v_GenTTXJets.clear()
        v_truth.clear()
        v_trig.clear()
        
    # ***************** end of  event loop ********************
    
    print "selected %i out of %i events (%.2f%%)"%(nselectedevts,len(range(IdxBegin,IdxEnd)),100*float(nselectedevts)/float(len(range(IdxBegin,IdxEnd))))
    
    
    ROOT.gROOT.SetBatch(1)
    
    for iBin in range(h_correct.GetNbinsX()):
        summed = h_correct.GetBinContent(iBin+1)+h_only_oneoutoftwo.GetBinContent(iBin+1)+h_only_top_correct.GetBinContent(iBin+1)+h_flipped.GetBinContent(iBin+1)+h_wrong.GetBinContent(iBin+1) #+ h_nomatch.GetBinContent(iBin+1)
        if summed != 0:
            h_correct.SetBinContent(iBin+1,h_correct.GetBinContent(iBin+1)/float(summed))
            h_only_top_correct.SetBinContent(iBin+1,h_only_top_correct.GetBinContent(iBin+1)/float(summed))
            h_only_oneoutoftwo.SetBinContent(iBin+1,h_only_oneoutoftwo.GetBinContent(iBin+1)/float(summed))
            h_flipped.SetBinContent(iBin+1,h_flipped.GetBinContent(iBin+1)/float(summed))
            h_wrong.SetBinContent(iBin+1,h_wrong.GetBinContent(iBin+1)/float(summed))
            h_nomatch.SetBinContent(iBin+1,h_nomatch.GetBinContent(iBin+1)/float(summed))
    
    h_correct.SetLineWidth(0)
    h_correct.SetFillColor(ROOT.kGreen + 3)
    h_only_top_correct.SetLineWidth(0)
    h_only_top_correct.SetFillColor(ROOT.kOrange+1)
    h_only_oneoutoftwo.SetLineWidth(0)
    h_only_oneoutoftwo.SetFillColor(ROOT.kYellow+1)
    h_flipped.SetLineWidth(0)
    h_flipped.SetFillColor(30)
    h_wrong.SetLineWidth(0)
    h_wrong.SetFillColor(2)
    h_nomatch.SetLineWidth(0)
    h_nomatch.SetFillColor(45)
    
    hs = ROOT.THStack("hs",";;Fraction of events")
    hs.Add(h_correct)
    hs.Add(h_flipped)
    hs.Add(h_only_oneoutoftwo)
    hs.Add(h_only_top_correct)
    hs.Add(h_wrong)
    #hs.Add(h_nomatch)
    
    
    
    
    
    c = ROOT.TCanvas("c","c",800,700)
    c.cd()
    ROOT.gPad.SetMargin(0.12,0.05,0.1,0.165)
    ROOT.gPad.SetTicky(2)
    ROOT.gPad.SetTickx(0)
    
    hs.Draw()
    hs.SetMinimum(0.)
    hs.SetMaximum(1.1)
    hs.GetXaxis().SetBinLabel(1,"incl")
    hs.GetXaxis().SetBinLabel(2,"ttbb")
    hs.GetXaxis().SetBinLabel(3,"ttbL")
    hs.GetXaxis().SetBinLabel(4,"ttcc")
    hs.GetXaxis().SetBinLabel(5,"ttcL")
    hs.GetXaxis().SetBinLabel(6,"ttLL")
    hs.GetXaxis().SetBinLabel(7,"other")
    hs.GetYaxis().SetTitleSize(0.05)
    hs.GetYaxis().SetTitleOffset(1.1)
    hs.GetXaxis().SetLabelSize(0.07)
    hs.GetXaxis().SetRangeUser(-0.5,5.5)
    hs.GetXaxis().SetTickLength(0)
    
    #Legend
    l = ROOT.TLegend(0.12,0.82,0.95,0.9)
    l.SetNColumns(5)
    l.SetTextSize(0.045)
    l.AddEntry(h_correct,"correct","f")
    l.AddEntry(h_flipped,"flipped","f")
    l.AddEntry(h_only_oneoutoftwo,"one/two","f")
    l.AddEntry(h_only_top_correct,"only top","f")
    l.AddEntry(h_wrong,"wrong","f")
    #l.AddEntry(h_nomatch,"no match","f")
    l.Draw("same")
    
    line = ROOT.TLine()
    line.SetLineColor(1)
    line.SetLineStyle(1)
    line.SetLineWidth(2)
    line.DrawLine(-0.5, 1, 5.5, 1)
    
    #horizontal
    grids = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
    line_dict={}
    for g in grids:
        line_dict[g] = ROOT.TLine()
        line_dict[g].SetLineColor(12)
        line_dict[g].SetLineStyle(2)
        line_dict[g].DrawLine(-0.5, g, 5.5, g)
    
    #vertical
    grids = [0.5,1.5,2.5,3.5,4.5]
    line_dict={}
    for g in grids:
        line_dict[g] = ROOT.TLine()
        line_dict[g].SetLineColor(1)
        line_dict[g].SetLineStyle(1)
        line_dict[g].DrawLine(g, 0, g, 1)
    
    
    # TEXT
    year = "2017"
    latex = ROOT.TLatex()
    latex.SetTextFont(42)
    latex.SetTextSize(0.05)
    latex.SetTextAlign(32)
    latex.DrawLatexNDC(0.94,0.94,year + ", 94X")
    
    latex_sample = ROOT.TLatex()
    latex_sample.SetTextFont(42)
    latex_sample.SetTextSize(0.045)
    latex_sample.SetTextAlign(31)
    latex_sample.DrawLatexNDC(0.93,0.77,"b-tag ranked top matching")
    
    latex_cms = ROOT.TLatex()
    latex_cms.SetTextFont(42)
    latex_cms.SetTextSize(0.045)
    latex_cms.SetTextAlign(11)
    latex_cms.DrawLatexNDC(0.16,0.77,"#bf{CMS} #it{Simulation}")
    
    c.SaveAs(os.getcwd()+"/Performance_BTagRanking_TopMatching.pdf")
    c.SaveAs(os.getcwd()+"/Performance_BTagRanking_TopMatching.C")
    
    
    
    infile_.Close()
    
    
    
    
    



def main():

    

    workingdir = os.getcwd()

    #if not os.path.isdir(workingdir+"/SELECTED_"+args.tag): os.mkdir(workingdir+"/SELECTED_"+args.tag)
    
    # Search for the input directory
    indir = os.path.abspath(args.indir)+"/"
    if not os.path.isdir(indir):
        print "Error: could not find directory '%s'"%indir
        sys.exit(1)
    
    # Take only files defined by args.infiles
    if not args.infiles == "*": 
        filelist = []
        tags = args.infiles.split("*")
        for f in [f for f in os.listdir(indir)]:
            for t in tags:
                if t == "": continue
                if t in f: filelist.append(f)
    else: 
        filelist = [f for f in os.listdir(indir)]
    
    # Count number of events in each file
    nevts_dict = {}
    print "Counting number of events in each file"
    for f in filelist:
        tfile = TFile(indir+f,workingdir+"/SELECTED_"+args.tag+"/"+f)
        tree_ = tfile.Get("tree")
        nevts = tree_.GetEntries()
        if nevts > args.nevents and args.nevents > 0: nevts=args.nevents
        nevts_dict[f]=nevts
    
    for _f,_n in nevts_dict.iteritems():
        print "**** %s: %i events ****"%(_f,_n)

    #sys.exit(1)
        
        
    
    # if (args.ncpu < 0 or args.ncpu > multiprocessing.cpu_count()): parallelProcesses = multiprocessing.cpu_count()
#     else: parallelProcesses = args.ncpu
#     p = multiprocessing.Pool(parallelProcesses)
#     print "Using %i parallel processes (%i in total)" %(parallelProcesses,len(filelist))
#     
#     try:
#         split_jobs_dict={}
#         for f in filelist:
#             split_jobs_dict[f] = False
#             # See if jobs need to be split
#             if args.nmaxevtsperjob > 0 and nevts_dict[f] > args.nmaxevtsperjob:
#                 split_jobs_dict[f] = True
#                 eventsList = []
#                 startEvent = 0
#                 while (startEvent < nevts_dict[f]):
#                     eventsList.append(startEvent)
#                     startEvent += args.nmaxevtsperjob
#                 eventsList.append(nevts_dict[f])
#                 print "Dataset %s was splitted in %i jobs" %(f,len(eventsList)-1)
#                 for i in range(len(eventsList)-1):
#                     res = p.apply_async(Analyze, args = (indir+f,workingdir+"/SELECTED_"+args.tag+"/"+f,eventsList[i], eventsList[i+1],True,))
#             
#             else:
#                 res = p.apply_async(Analyze, args = (indir+f,workingdir+"/SELECTED_"+args.tag+"/"+f,0,nevts_dict[f],False,))   
#                 
#         res.get(99999)
#         p.close()
#         p.join()
#     except KeyboardInterrupt:
#         print "Caught KeyboardInterrupt, terminating workers"
#         pool.terminate()
#         pool.join()
#     
#     # Do the hadd in case of splitting
#     for _f,splitted in split_jobs_dict.iteritems():
#         if splitted:
#             fullpath=workingdir+"/SELECTED_"+args.tag+"/"+_f
#             #print "hadd %s %s"%(fullpath,fullpath.replace(".root","_*"))
#             #print "rm %s"%(fullpath.replace(".root","_*"))
#             os.system("hadd %s %s"%(fullpath,fullpath.replace(".root","_*")))
#             os.system("rm %s"%(fullpath.replace(".root","_*")))

    #Analyze(args.indir+"/DoubleMuon_Run2017E_31Mar2018_v1_MINIAOD.root",workingdir+"/SELECTED_"+args.tag+"/DoubleMuon_Run2017E_31Mar2018_v1_MINIAOD.root",0,1000,True)
    #Analyze(args.indir+"/DoubleMuon_Run2017B_31Mar2018_v1_MINIAOD.root",workingdir+"/SELECTED_"+args.tag+"/DoubleMuon_Run2017B_31Mar2018_v1_MINIAOD.root",0,1000,True)
#     Analyze(args.indir+"/MuonEG_Run2017F_31Mar2018_v1_MINIAOD.root",workingdir+"/SELECTED_"+args.tag+"/MuonEG_Run2017F_31Mar2018_v1_MINIAOD.root",0,1000,True)
    Analyze(args.indir+"/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8.root",args.topmatchingdir,0,args.nevents,True)

if __name__ == "__main__":
	main()


