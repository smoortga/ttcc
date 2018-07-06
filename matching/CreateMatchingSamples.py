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

def Analyze(infile, outfile, IdxBegin = 0, IdxEnd = -1, Splitted = False):
    
    if not os.path.isfile(infile):
        print "ERROR: COULD NOT FIND FILE: %s!!!"%infile
        sys.exit(1)
    
    infile_ = TFile(infile)
    intree_ = infile_.Get("tree")
    
    if Splitted: ofile_ = TFile(outfile.replace(".root","_"+str(IdxBegin)+"_"+str(IdxEnd)+".root"),"RECREATE")
    else: ofile_ = TFile(outfile,"RECREATE")
    otree_correct_ = TTree("tree_correct","tree_correct")
    otree_flipped_ = TTree("tree_flipped","tree_flipped")
    otree_wrong_ = TTree("tree_wrong","tree_wrong")
    
    # **************************** add extra branches to output****************************
    dict_variableName_Leaves = {}
    # event category
    dict_variableName_Leaves.update({"event_Category": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"weight": [array('d', [0]),"D"]})
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
    
    for name,arr in dict_variableName_Leaves.iteritems():
        otree_correct_.Branch(name,arr[0],name+"/"+arr[1])
        otree_flipped_.Branch(name,arr[0],name+"/"+arr[1])
        otree_wrong_.Branch(name,arr[0],name+"/"+arr[1])
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
    v_met = ROOT.std.vector( MissingEnergy )()
    v_trig = ROOT.std.vector( Trigger )()
    v_truth = ROOT.std.vector( Truth )()
    
    # ***************** Start event loop ********************
    for evt in range(IdxBegin,IdxEnd):
        if (evt % int(actual_nentries/10.) == 0): print"%s: Processing event %i/%i (%.1f %%)"%(infile.split("/")[-1],evt,IdxEnd,100*float(evt-IdxBegin)/float(actual_nentries))
        intree_.GetEntry(evt)
        
        v_el = intree_.Electrons
        v_mu = intree_.Muons
        v_jet = intree_.Jets
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
        
        if len(bjet_matching_dict) != 2: continue
        if bjet_matching_dict["top_bjet"] == bjet_matching_dict["antitop_bjet"]: continue # can in principle not happen, but just to be sure
        
        
        # now investigate all possible permutations
        perm = [i for i in permutations(range(len(validjets)),2)]
        for p in perm:
            if validjets.at(p[0]).Pt() < 25 or validjets.at(p[1]).Pt() < 25: continue
            if validjets.at(p[0]) == bjet_matching_dict["top_bjet"] and validjets.at(p[1]) == bjet_matching_dict["antitop_bjet"]:
                #print p,"MATCHED"
                perm_top_bjet = validjets.at(p[0])
                perm_antitop_bjet = validjets.at(p[1])
                remaining_indices = range(len(validjets))
                remaining_indices.remove(p[0])
                remaining_indices.remove(p[1])
                remaining_jets = [validjets.at(ij) for ij in remaining_indices]
                ptsorted_remaining_jets = sorted(remaining_jets, key=lambda x: x.DeepCSVCvsL(), reverse=True)
                perm_addjet_lead = ptsorted_remaining_jets[0]
                perm_addjet_sublead = ptsorted_remaining_jets[1]
                #fill variables
                dict_variableName_Leaves["event_Category"][0][0] = cat
                dict_variableName_Leaves["pT_topb"][0][0] = perm_top_bjet.Pt()
                dict_variableName_Leaves["pT_antitopb"][0][0] = perm_antitop_bjet.Pt()
                dict_variableName_Leaves["pT_addlead"][0][0] = perm_addjet_lead.Pt()
                dict_variableName_Leaves["pT_addsublead"][0][0] = perm_addjet_sublead.Pt()
                dict_variableName_Leaves["Eta_topb"][0][0] = perm_top_bjet.Eta()
                dict_variableName_Leaves["Eta_antitopb"][0][0] = perm_antitop_bjet.Eta()
                dict_variableName_Leaves["Eta_addlead"][0][0] = perm_addjet_lead.Eta()
                dict_variableName_Leaves["Eta_addsublead"][0][0] = perm_addjet_sublead.Eta()
                dict_variableName_Leaves["Phi_topb"][0][0] = perm_top_bjet.Phi()
                dict_variableName_Leaves["Phi_antitopb"][0][0] = perm_antitop_bjet.Phi()
                dict_variableName_Leaves["Phi_addlead"][0][0] = perm_addjet_lead.Phi()
                dict_variableName_Leaves["Phi_addsublead"][0][0] = perm_addjet_sublead.Phi()
                dict_variableName_Leaves["CSVv2_topb"][0][0] = perm_top_bjet.CSVv2()
                dict_variableName_Leaves["CSVv2_antitopb"][0][0] = perm_antitop_bjet.CSVv2()
                dict_variableName_Leaves["CSVv2_addlead"][0][0] = perm_addjet_lead.CSVv2()
                dict_variableName_Leaves["CSVv2_addsublead"][0][0] = perm_addjet_sublead.CSVv2()
                dict_variableName_Leaves["DeepCSVBDiscr_topb"][0][0] = perm_top_bjet.DeepCSVBDiscr()
                dict_variableName_Leaves["DeepCSVBDiscr_antitopb"][0][0] = perm_antitop_bjet.DeepCSVBDiscr()
                dict_variableName_Leaves["DeepCSVBDiscr_addlead"][0][0] = perm_addjet_lead.DeepCSVBDiscr()
                dict_variableName_Leaves["DeepCSVBDiscr_addsublead"][0][0] = perm_addjet_sublead.DeepCSVBDiscr()
                dict_variableName_Leaves["DeepCSVCvsL_topb"][0][0] = perm_top_bjet.DeepCSVCvsL()
                dict_variableName_Leaves["DeepCSVCvsL_antitopb"][0][0] = perm_antitop_bjet.DeepCSVCvsL()
                dict_variableName_Leaves["DeepCSVCvsL_addlead"][0][0] = perm_addjet_lead.DeepCSVCvsL()
                dict_variableName_Leaves["DeepCSVCvsL_addsublead"][0][0] =  perm_addjet_sublead.DeepCSVCvsL()
                dict_variableName_Leaves["DeepCSVCvsB_topb"][0][0] = perm_top_bjet.DeepCSVCvsB()
                dict_variableName_Leaves["DeepCSVCvsB_antitopb"][0][0] = perm_antitop_bjet.DeepCSVCvsB()
                dict_variableName_Leaves["DeepCSVCvsB_addlead"][0][0] = perm_addjet_lead.DeepCSVCvsB()
                dict_variableName_Leaves["DeepCSVCvsB_addsublead"][0][0] = perm_addjet_sublead.DeepCSVCvsB()
                dict_variableName_Leaves["DeltaR_topb_leppos"][0][0] = DeltaR(perm_top_bjet,pos_lepton)
                dict_variableName_Leaves["DeltaR_antitopb_lepneg"][0][0] = DeltaR(perm_antitop_bjet,neg_lepton)
                dict_variableName_Leaves["DeltaR_adds"][0][0] = DeltaR(perm_addjet_lead,perm_addjet_sublead)
                dict_variableName_Leaves["minv_topb_leppos"][0][0] = IvariantMass(perm_top_bjet,pos_lepton)
                dict_variableName_Leaves["minv_antitopb_lepneg"][0][0] = IvariantMass(perm_antitop_bjet,neg_lepton)
                dict_variableName_Leaves["minv_adds"][0][0] = IvariantMass(perm_addjet_lead,perm_addjet_sublead)
                if cat == 0 or cat == 2: dict_variableName_Leaves["weight"][0][0] = 20
                elif cat == 1: dict_variableName_Leaves["weight"][0][0] = 10
                elif cat == 3: dict_variableName_Leaves["weight"][0][0] = 5
                else: dict_variableName_Leaves["weight"][0][0] = 1
                if np.isnan([dict_variableName_Leaves[var][0][0] for var in dict_variableName_Leaves.keys()]).any():
                    print "WARNING: nan value encountered in NN inputs. skipping event"
                    continue
                otree_correct_.Fill()
            elif validjets.at(p[1]) == bjet_matching_dict["top_bjet"] and validjets.at(p[0]) == bjet_matching_dict["antitop_bjet"]:
                #print p,"MATCHED"
                perm_top_bjet = validjets.at(p[0])
                perm_antitop_bjet = validjets.at(p[1])
                remaining_indices = range(len(validjets))
                remaining_indices.remove(p[0])
                remaining_indices.remove(p[1])
                remaining_jets = [validjets.at(ij) for ij in remaining_indices]
                ptsorted_remaining_jets = sorted(remaining_jets, key=lambda x: x.DeepCSVCvsL(), reverse=True)
                perm_addjet_lead = ptsorted_remaining_jets[0]
                perm_addjet_sublead = ptsorted_remaining_jets[1]
                #fill variables
                dict_variableName_Leaves["event_Category"][0][0] = cat
                dict_variableName_Leaves["pT_topb"][0][0] = perm_top_bjet.Pt()
                dict_variableName_Leaves["pT_antitopb"][0][0] = perm_antitop_bjet.Pt()
                dict_variableName_Leaves["pT_addlead"][0][0] = perm_addjet_lead.Pt()
                dict_variableName_Leaves["pT_addsublead"][0][0] = perm_addjet_sublead.Pt()
                dict_variableName_Leaves["Eta_topb"][0][0] = perm_top_bjet.Eta()
                dict_variableName_Leaves["Eta_antitopb"][0][0] = perm_antitop_bjet.Eta()
                dict_variableName_Leaves["Eta_addlead"][0][0] = perm_addjet_lead.Eta()
                dict_variableName_Leaves["Eta_addsublead"][0][0] = perm_addjet_sublead.Eta()
                dict_variableName_Leaves["Phi_topb"][0][0] = perm_top_bjet.Phi()
                dict_variableName_Leaves["Phi_antitopb"][0][0] = perm_antitop_bjet.Phi()
                dict_variableName_Leaves["Phi_addlead"][0][0] = perm_addjet_lead.Phi()
                dict_variableName_Leaves["Phi_addsublead"][0][0] = perm_addjet_sublead.Phi()
                dict_variableName_Leaves["CSVv2_topb"][0][0] = perm_top_bjet.CSVv2()
                dict_variableName_Leaves["CSVv2_antitopb"][0][0] = perm_antitop_bjet.CSVv2()
                dict_variableName_Leaves["CSVv2_addlead"][0][0] = perm_addjet_lead.CSVv2()
                dict_variableName_Leaves["CSVv2_addsublead"][0][0] = perm_addjet_sublead.CSVv2()
                dict_variableName_Leaves["DeepCSVBDiscr_topb"][0][0] = perm_top_bjet.DeepCSVBDiscr()
                dict_variableName_Leaves["DeepCSVBDiscr_antitopb"][0][0] = perm_antitop_bjet.DeepCSVBDiscr()
                dict_variableName_Leaves["DeepCSVBDiscr_addlead"][0][0] = perm_addjet_lead.DeepCSVBDiscr()
                dict_variableName_Leaves["DeepCSVBDiscr_addsublead"][0][0] = perm_addjet_sublead.DeepCSVBDiscr()
                dict_variableName_Leaves["DeepCSVCvsL_topb"][0][0] = perm_top_bjet.DeepCSVCvsL()
                dict_variableName_Leaves["DeepCSVCvsL_antitopb"][0][0] = perm_antitop_bjet.DeepCSVCvsL()
                dict_variableName_Leaves["DeepCSVCvsL_addlead"][0][0] = perm_addjet_lead.DeepCSVCvsL()
                dict_variableName_Leaves["DeepCSVCvsL_addsublead"][0][0] =  perm_addjet_sublead.DeepCSVCvsL()
                dict_variableName_Leaves["DeepCSVCvsB_topb"][0][0] = perm_top_bjet.DeepCSVCvsB()
                dict_variableName_Leaves["DeepCSVCvsB_antitopb"][0][0] = perm_antitop_bjet.DeepCSVCvsB()
                dict_variableName_Leaves["DeepCSVCvsB_addlead"][0][0] = perm_addjet_lead.DeepCSVCvsB()
                dict_variableName_Leaves["DeepCSVCvsB_addsublead"][0][0] = perm_addjet_sublead.DeepCSVCvsB()
                dict_variableName_Leaves["DeltaR_topb_leppos"][0][0] = DeltaR(perm_top_bjet,pos_lepton)
                dict_variableName_Leaves["DeltaR_antitopb_lepneg"][0][0] = DeltaR(perm_antitop_bjet,neg_lepton)
                dict_variableName_Leaves["DeltaR_adds"][0][0] = DeltaR(perm_addjet_lead,perm_addjet_sublead)
                dict_variableName_Leaves["minv_topb_leppos"][0][0] = IvariantMass(perm_top_bjet,pos_lepton)
                dict_variableName_Leaves["minv_antitopb_lepneg"][0][0] = IvariantMass(perm_antitop_bjet,neg_lepton)
                dict_variableName_Leaves["minv_adds"][0][0] = IvariantMass(perm_addjet_lead,perm_addjet_sublead)
                if cat == 0 or cat == 2: dict_variableName_Leaves["weight"][0][0] = 20
                elif cat == 1: dict_variableName_Leaves["weight"][0][0] = 10
                elif cat == 3: dict_variableName_Leaves["weight"][0][0] = 5
                else: dict_variableName_Leaves["weight"][0][0] = 1
                if np.isnan([dict_variableName_Leaves[var][0][0] for var in dict_variableName_Leaves.keys()]).any():
                    print "WARNING: nan value encountered in NN inputs. skipping event"
                    continue
                otree_flipped_.Fill()
            else:
                #print p,"not matched"
                perm_top_bjet = validjets.at(p[0])
                perm_antitop_bjet = validjets.at(p[1])
                remaining_indices = range(len(validjets))
                remaining_indices.remove(p[0])
                remaining_indices.remove(p[1])
                remaining_jets = [validjets.at(ij) for ij in remaining_indices]
                ptsorted_remaining_jets = sorted(remaining_jets, key=lambda x: x.DeepCSVCvsL(), reverse=True)
                perm_addjet_lead = ptsorted_remaining_jets[0]
                perm_addjet_sublead = ptsorted_remaining_jets[1]
                #fill variables
                dict_variableName_Leaves["event_Category"][0][0] = cat
                dict_variableName_Leaves["pT_topb"][0][0] = perm_top_bjet.Pt()
                dict_variableName_Leaves["pT_antitopb"][0][0] = perm_antitop_bjet.Pt()
                dict_variableName_Leaves["pT_addlead"][0][0] = perm_addjet_lead.Pt()
                dict_variableName_Leaves["pT_addsublead"][0][0] = perm_addjet_sublead.Pt()
                dict_variableName_Leaves["Eta_topb"][0][0] = perm_top_bjet.Eta()
                dict_variableName_Leaves["Eta_antitopb"][0][0] = perm_antitop_bjet.Eta()
                dict_variableName_Leaves["Eta_addlead"][0][0] = perm_addjet_lead.Eta()
                dict_variableName_Leaves["Eta_addsublead"][0][0] = perm_addjet_sublead.Eta()
                dict_variableName_Leaves["Phi_topb"][0][0] = perm_top_bjet.Phi()
                dict_variableName_Leaves["Phi_antitopb"][0][0] = perm_antitop_bjet.Phi()
                dict_variableName_Leaves["Phi_addlead"][0][0] = perm_addjet_lead.Phi()
                dict_variableName_Leaves["Phi_addsublead"][0][0] = perm_addjet_sublead.Phi()
                dict_variableName_Leaves["CSVv2_topb"][0][0] = perm_top_bjet.CSVv2()
                dict_variableName_Leaves["CSVv2_antitopb"][0][0] = perm_antitop_bjet.CSVv2()
                dict_variableName_Leaves["CSVv2_addlead"][0][0] = perm_addjet_lead.CSVv2()
                dict_variableName_Leaves["CSVv2_addsublead"][0][0] = perm_addjet_sublead.CSVv2()
                dict_variableName_Leaves["DeepCSVBDiscr_topb"][0][0] = perm_top_bjet.DeepCSVBDiscr()
                dict_variableName_Leaves["DeepCSVBDiscr_antitopb"][0][0] = perm_antitop_bjet.DeepCSVBDiscr()
                dict_variableName_Leaves["DeepCSVBDiscr_addlead"][0][0] = perm_addjet_lead.DeepCSVBDiscr()
                dict_variableName_Leaves["DeepCSVBDiscr_addsublead"][0][0] = perm_addjet_sublead.DeepCSVBDiscr()
                dict_variableName_Leaves["DeepCSVCvsL_topb"][0][0] = perm_top_bjet.DeepCSVCvsL()
                dict_variableName_Leaves["DeepCSVCvsL_antitopb"][0][0] = perm_antitop_bjet.DeepCSVCvsL()
                dict_variableName_Leaves["DeepCSVCvsL_addlead"][0][0] = perm_addjet_lead.DeepCSVCvsL()
                dict_variableName_Leaves["DeepCSVCvsL_addsublead"][0][0] =  perm_addjet_sublead.DeepCSVCvsL()
                dict_variableName_Leaves["DeepCSVCvsB_topb"][0][0] = perm_top_bjet.DeepCSVCvsB()
                dict_variableName_Leaves["DeepCSVCvsB_antitopb"][0][0] = perm_antitop_bjet.DeepCSVCvsB()
                dict_variableName_Leaves["DeepCSVCvsB_addlead"][0][0] = perm_addjet_lead.DeepCSVCvsB()
                dict_variableName_Leaves["DeepCSVCvsB_addsublead"][0][0] = perm_addjet_sublead.DeepCSVCvsB()
                dict_variableName_Leaves["DeltaR_topb_leppos"][0][0] = DeltaR(perm_top_bjet,pos_lepton)
                dict_variableName_Leaves["DeltaR_antitopb_lepneg"][0][0] = DeltaR(perm_antitop_bjet,neg_lepton)
                dict_variableName_Leaves["DeltaR_adds"][0][0] = DeltaR(perm_addjet_lead,perm_addjet_sublead)
                dict_variableName_Leaves["minv_topb_leppos"][0][0] = IvariantMass(perm_top_bjet,pos_lepton)
                dict_variableName_Leaves["minv_antitopb_lepneg"][0][0] = IvariantMass(perm_antitop_bjet,neg_lepton)
                dict_variableName_Leaves["minv_adds"][0][0] = IvariantMass(perm_addjet_lead,perm_addjet_sublead)
                if cat == 0 or cat == 2: dict_variableName_Leaves["weight"][0][0] = 20
                elif cat == 1: dict_variableName_Leaves["weight"][0][0] = 10
                elif cat == 3: dict_variableName_Leaves["weight"][0][0] = 5
                else: dict_variableName_Leaves["weight"][0][0] = 1
                if np.isnan([dict_variableName_Leaves[var][0][0] for var in dict_variableName_Leaves.keys()]).any():
                    print "WARNING: nan value encountered in NN inputs. skipping event"
                    continue
                otree_wrong_.Fill()

        #otree_.Fill()

        v_el.clear()
        v_mu.clear()
        v_jet.clear()
        v_truth.clear()
        v_trig.clear()
    # ***************** end of  event loop ********************
    
    #print "%s: Selected %i/%i (%.3f%%) of events"%(infile.split("/")[-1],otree_.GetEntries(),actual_nentries,100*float(otree_.GetEntries())/float(actual_nentries))

    ofile_.cd()
    otree_correct_.Write()
    otree_flipped_.Write()
    otree_wrong_.Write()
    
    ofile_.Close()
    infile_.Close()
    
    
    
    
    



def main():

    parser = ArgumentParser()
    parser.add_argument('--indir', default="../selection/OUTPUT_Full2017DataMC_UnPrescaledTriggers/SelectedSamples/",help='directory name of input files')
    parser.add_argument('--infiles', default="TTTo*",help='name of input files')
    parser.add_argument('--tag', default=time.strftime("%a%d%b%Y_%Hh%Mm%Ss"),help='name of output directory')
    parser.add_argument('--nevents', type=int, default=-1,help='maximum number of events for each dataset to process')
    parser.add_argument('--nmaxevtsperjob', type=int, default=1050000,help='maximum number of events per job (otherwise split)')
    parser.add_argument('--ncpu', type=int, default=-1,help='number of CPU to use in parallel')
    args = parser.parse_args()

    workingdir = os.getcwd()

    if not os.path.isdir(workingdir+"/"+args.tag): os.mkdir(workingdir+"/"+args.tag)
    
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
        tfile = TFile(indir+f)
        tree_ = tfile.Get("tree")
        nevts = tree_.GetEntries()
        if nevts > args.nevents and args.nevents > 0: nevts=args.nevents
        nevts_dict[f]=nevts
    
    for _f,_n in nevts_dict.iteritems():
        print "**** %s: %i events ****"%(_f,_n)

    #sys.exit(1)
        
        
    
    if (args.ncpu < 0 or args.ncpu > multiprocessing.cpu_count()): parallelProcesses = multiprocessing.cpu_count()
    else: parallelProcesses = args.ncpu
    p = multiprocessing.Pool(parallelProcesses)
    print "Using %i parallel processes (%i in total)" %(parallelProcesses,len(filelist))
    
    try:
        split_jobs_dict={}
        for f in filelist:
            split_jobs_dict[f] = False
            # See if jobs need to be split
            if args.nmaxevtsperjob > 0 and nevts_dict[f] > args.nmaxevtsperjob:
                split_jobs_dict[f] = True
                eventsList = []
                startEvent = 0
                while (startEvent < nevts_dict[f]):
                    eventsList.append(startEvent)
                    startEvent += args.nmaxevtsperjob
                eventsList.append(nevts_dict[f])
                print "Dataset %s was splitted in %i jobs" %(f,len(eventsList)-1)
                for i in range(len(eventsList)-1):
                    res = p.apply_async(Analyze, args = (indir+f,workingdir+"/"+args.tag+"/"+f,eventsList[i], eventsList[i+1],True,))
            
            else:
                res = p.apply_async(Analyze, args = (indir+f,workingdir+"/"+args.tag+"/"+f,0,nevts_dict[f],False,))   
                
        res.get(99999)
        p.close()
        p.join()
    except KeyboardInterrupt:
        print "Caught KeyboardInterrupt, terminating workers"
        pool.terminate()
        pool.join()
    
    # Do the hadd in case of splitting
    for _f,splitted in split_jobs_dict.iteritems():
        if splitted:
            fullpath=workingdir+"/"+args.tag+"/"+_f
            #print "hadd %s %s"%(fullpath,fullpath.replace(".root","_*"))
            #print "rm %s"%(fullpath.replace(".root","_*"))
            os.system("hadd %s %s"%(fullpath,fullpath.replace(".root","_*")))
            os.system("rm %s"%(fullpath.replace(".root","_*")))

    #Analyze(args.indir+"/DoubleMuon_Run2017E_31Mar2018_v1_MINIAOD.root",workingdir+"/SELECTED_"+args.tag+"/DoubleMuon_Run2017E_31Mar2018_v1_MINIAOD.root",0,1000,True)
    #Analyze(args.indir+"/DoubleMuon_Run2017B_31Mar2018_v1_MINIAOD.root",workingdir+"/SELECTED_"+args.tag+"/DoubleMuon_Run2017B_31Mar2018_v1_MINIAOD.root",0,1000,True)
#     Analyze(args.indir+"/MuonEG_Run2017F_31Mar2018_v1_MINIAOD.root",workingdir+"/SELECTED_"+args.tag+"/MuonEG_Run2017F_31Mar2018_v1_MINIAOD.root",0,1000,True)
    #Analyze(args.indir+"/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8.root",workingdir+"/SELECTED_"+args.tag+"/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8.root",0,10000,True)

if __name__ == "__main__":
	main()


