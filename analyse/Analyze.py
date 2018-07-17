from Helper import *
from argparse import ArgumentParser
import time
import multiprocessing
import thread
import subprocess
import sys
import signal
import inspect
from copy import deepcopy

def Analyze(infile, outfile, topmatchingdir, IdxBegin = 0, IdxEnd = -1, Splitted = False):
    
    if not os.path.isfile(infile):
        print "ERROR: COULD NOT FIND FILE: %s!!!"%infile
        sys.exit(1)
    
    infile_ = TFile(infile)
    intree_ = infile_.Get("tree")
    
    if Splitted: ofile_ = TFile(outfile.replace(".root","_events_"+str(IdxBegin)+"_"+str(IdxEnd)+".root"),"RECREATE")
    else: ofile_ = TFile(outfile,"RECREATE")
    otree_ = intree_.CloneTree(0)
    
    # **************************** add extra branches to output****************************
    dict_variableName_Leaves = {}
    dict_variableName_Leaves.update({"DileptonInvariantMass": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"DileptonDeltaR": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"hadronFlavour_addJet1": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"hadronFlavour_addJet2": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"partonFlavour_addJet1": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"partonFlavour_addJet2": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"CSVv2_addJet1": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"CSVv2_addJet2": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"DeepCSVBDiscr_addJet1": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"DeepCSVBDiscr_addJet2": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"cTagCvsL_addJet1": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"cTagCvsL_addJet2": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"cTagCvsB_addJet1": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"cTagCvsB_addJet2": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"DeepCSVcTagCvsL_addJet1": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"DeepCSVcTagCvsL_addJet2": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"DeepCSVcTagCvsB_addJet1": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"DeepCSVcTagCvsB_addJet2": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"n_CSVv2_L_btagged": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"n_CSVv2_M_btagged": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"n_CSVv2_T_btagged": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"n_cTagger_L_ctagged": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"n_cTagger_M_ctagged": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"n_cTagger_T_ctagged": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"n_cTagger_L_Additional_ctagged": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"n_cTagger_M_Additional_ctagged": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"n_cTagger_T_Additional_ctagged": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"n_DeepCSVBDiscr_L_btagged": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"n_DeepCSVBDiscr_M_btagged": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"n_DeepCSVBDiscr_T_btagged": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"n_DeepCSVcTagger_L_ctagged": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"n_DeepCSVcTagger_M_ctagged": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"n_DeepCSVcTagger_T_ctagged": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"n_DeepCSVcTagger_L_Additional_ctagged": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"n_DeepCSVcTagger_M_Additional_ctagged": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"n_DeepCSVcTagger_T_Additional_ctagged": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"event_Category": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"lepton_Category": [array('i', [0]),"I"]}) # 0 = elel, 1 = mumu, 2 = elmu
    dict_variableName_Leaves.update({"TopMatching_NN_best_value": [array('d', [0]),"D"]})
    #weights
    dict_variableName_Leaves.update({"weight_btag_iterativefit": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_electron_id": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_electron_reco": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_electron_trig": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_muon_id": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_muon_iso": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_muon_trig": [array('d', [1]),"D"]})
    # Gen Level info
    if "TTJets" in infile or "TTTo2L2Nu" in infile:
        dict_variableName_Leaves.update({"Gen_top_pT": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_top_eta": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_top_phi": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_top_E": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_top_M": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_antitop_pT": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_antitop_eta": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_antitop_phi": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_antitop_E": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_antitop_M": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_top_b_pT": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_top_b_eta": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_top_b_phi": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_top_b_E": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_top_b_M": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_antitop_b_pT": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_antitop_b_eta": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_antitop_b_phi": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_antitop_b_E": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_antitop_b_M": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_top_W_pT": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_top_W_eta": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_top_W_phi": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_top_W_E": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_top_W_M": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_antitop_W_pT": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_antitop_W_eta": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_antitop_W_phi": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_antitop_W_E": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_antitop_W_M": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_top_lep_pT": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_top_lep_eta": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_top_lep_phi": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_top_lep_E": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_top_lep_M": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_antitop_lep_pT": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_antitop_lep_eta": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_antitop_lep_phi": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_antitop_lep_E": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_antitop_lep_M": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_top_nu_pT": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_top_nu_eta": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_top_nu_phi": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_top_nu_E": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_top_nu_M": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_antitop_nu_pT": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_antitop_nu_eta": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_antitop_nu_phi": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_antitop_nu_E": [array('d', [1]),"D"]})
        dict_variableName_Leaves.update({"Gen_antitop_nu_M": [array('d', [1]),"D"]})
#     
    
    for name,arr in dict_variableName_Leaves.iteritems():
        otree_.Branch(name,arr[0],name+"/"+arr[1])
    
    # v_validjets_ = ROOT.std.vector( Jet )()
#     otree_.Branch("ValidJets",v_validjets_);
    #****************************************************************************************
    
    # **************************** Load the top matching training ****************************
    model = load_model(topmatchingdir+"/model_checkpoint_save.hdf5")
    scaler = pickle.load(open(topmatchingdir+"/scaler.pkl","rb"))
    input_variables = pickle.load(open(topmatchingdir+"/variables.pkl","rb"))
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
        #if leading_leptons[0].Charge()*leading_leptons[1].Charge() >= 0: continue
        
        if leading_leptons[0].Charge() > 0 and leading_leptons[1].Charge() < 0:
            pos_lepton = leading_leptons[0]
            neg_lepton = leading_leptons[1]
        elif leading_leptons[0].Charge() < 0 and leading_leptons[1].Charge() > 0:
            pos_lepton = leading_leptons[1]
            neg_lepton = leading_leptons[0]
        else: continue
        
        mll = DileptonIvariantMass(leading_leptons[0],leading_leptons[1])
        
        if (lepton_category == 2): # elmu
            if not (mll>12.): continue 
            dict_variableName_Leaves["lepton_Category"][0][0] = 2 #emu
            
        elif (lepton_category == 0): # elel
            if v_met.at(0).Pt() < 30: continue
            if (mll>ZmassLow and mll<ZmassHigh): continue
            dict_variableName_Leaves["lepton_Category"][0][0] = 0 #elel  
            
        elif (lepton_category == 1): # mumu
            if v_met.at(0).Pt() < 30: continue
            if (mll>ZmassLow and mll<ZmassHigh): continue
            dict_variableName_Leaves["lepton_Category"][0][0] = 1 #mumu  
            
        else: continue     
        
        dict_variableName_Leaves["DileptonInvariantMass"][0][0] = mll
        dict_variableName_Leaves["DileptonDeltaR"][0][0] = DileptonDeltaR(leading_leptons[0],leading_leptons[1])
        
        
        
        # add lepton weights 
        if (not intree_.is_data):
            if (lepton_category == 2): #elmu
                dict_variableName_Leaves["weight_electron_id"][0][0] = leading_elec.w_CBid()
                dict_variableName_Leaves["weight_electron_reco"][0][0] = leading_elec.w_Reco()
                dict_variableName_Leaves["weight_electron_trig"][0][0] = leading_elec.w_Trig()
                dict_variableName_Leaves["weight_muon_id"][0][0] = leading_muon.w_Id()
                dict_variableName_Leaves["weight_muon_iso"][0][0] = leading_muon.w_Iso()
                dict_variableName_Leaves["weight_muon_trig"][0][0] = leading_muon.w_Trig()
            elif (lepton_category == 0): # elel
                dict_variableName_Leaves["weight_electron_id"][0][0] = leading_elec.w_CBid() * subleading_elec.w_CBid()
                dict_variableName_Leaves["weight_electron_reco"][0][0] = leading_elec.w_Reco() * subleading_elec.w_Reco()
                dict_variableName_Leaves["weight_electron_trig"][0][0] = leading_elec.w_Trig() * subleading_elec.w_Trig()
                dict_variableName_Leaves["weight_muon_id"][0][0] = 1
                dict_variableName_Leaves["weight_muon_iso"][0][0] = 1
                dict_variableName_Leaves["weight_muon_trig"][0][0] = 1
            elif (lepton_category == 1): # mumu
                dict_variableName_Leaves["weight_electron_id"][0][0] = 1
                dict_variableName_Leaves["weight_electron_reco"][0][0] = 1
                dict_variableName_Leaves["weight_electron_trig"][0][0] = 1
                dict_variableName_Leaves["weight_muon_id"][0][0] = leading_muon.w_Id() * subleading_muon.w_Id()
                dict_variableName_Leaves["weight_muon_iso"][0][0] = leading_muon.w_Iso() * subleading_muon.w_Iso()
                dict_variableName_Leaves["weight_muon_trig"][0][0] = leading_muon.w_Trig() * subleading_muon.w_Trig()
            
            
            
            
        #
        # 
        #
        # ***************** Trigger for dilepton cases only! ********************

        passAnyTrigger = False
        passDoubleEGTrigger = False
        passDoubleMuonTrigger_B=False
        passDoubleMuonTrigger_CDEF=False
        passMuonEGTrigger = False
        #iTrig = Trigger()
        for trig in v_trig:
        
            # MC --> logic or of all triggers
            if ((not intree_.is_data) and trig.Pass()):
                passAnyTrigger = True
            
            # Data: depending on the data stream
            elif intree_.is_data:
                if "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL" in trig.Name().Data() and trig.Pass():
                    passDoubleEGTrigger = True
                elif "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8" in trig.Name().Data() and trig.Pass():
                    passDoubleMuonTrigger_CDEF = True
                elif "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ" in trig.Name().Data() and not "Mass3p8" in trig.Name().Data() and trig.Pass():
                    passDoubleMuonTrigger_B = True
                elif "Mu" in trig.Name().Data() and "Ele" in trig.Name().Data() and trig.Pass():
                    passMuonEGTrigger = True
        
        passTriggerLogic = passAnyTrigger or ("DoubleEG" in infile and passDoubleEGTrigger) or ("DoubleMuon" in infile and "Run2017B" in infile and passDoubleMuonTrigger_B and not passDoubleEGTrigger) or ("DoubleMuon" in infile and (not "Run2017B" in infile) and passDoubleMuonTrigger_CDEF and not passDoubleEGTrigger) or ("MuonEG" in infile and passMuonEGTrigger and not passDoubleEGTrigger and not passDoubleMuonTrigger_B and not passDoubleMuonTrigger_CDEF)
        if not passTriggerLogic: continue        
        
        # *******************************************************
        
        
        # ***************** Jets ********************
        # event category based on jet content
        # https://twiki.cern.ch/twiki/bin/view/CMSPublic/GenHFHadronMatcher
        if (not intree_.is_data):
            cat = -1 # default for anything not ttbar of for ttbar which is not in the following categories
            if intree_.genTTX_id != -999:
                id = int(str(intree_.genTTX_id)[-2:])
                #print "genTTXid = ",intree_.genTTX_id
                if "TTJets" in infile or "TTTo2L2Nu" in infile:
                    if (id == 53 or id == 54 or id == 55): cat = 0 #ttbb
                    elif (id == 51 or id == 52): cat = 1 #ttbj
                    elif (id == 43 or id == 44 or id == 45): cat = 2 #ttcc
                    elif (id == 41 or id == 42): cat = 3 #ttcj
                    elif (id == 0): cat = 4 #ttjj
        
        
        # count number of b-tagged jets
        n_L_CSVv2_btagged_jets = 0
        n_M_CSVv2_btagged_jets = 0
        n_T_CSVv2_btagged_jets = 0
        n_L_DeepCSVBDiscr_btagged_jets = 0
        n_M_DeepCSVBDiscr_btagged_jets = 0
        n_T_DeepCSVBDiscr_btagged_jets = 0
        n_L_cTagger_ctagged_jets = 0
        n_M_cTagger_ctagged_jets = 0
        n_T_cTagger_ctagged_jets = 0
        n_L_DeepCSVcTagger_ctagged_jets = 0
        n_M_DeepCSVcTagger_ctagged_jets = 0
        n_T_DeepCSVcTagger_ctagged_jets = 0
        for jet in v_jet:
            if isCSVv2L(jet): n_L_CSVv2_btagged_jets += 1
            if isCSVv2M(jet): n_M_CSVv2_btagged_jets += 1
            if isCSVv2T(jet): n_T_CSVv2_btagged_jets += 1
            if isDeepCSVBDiscrL(jet): n_L_DeepCSVBDiscr_btagged_jets += 1
            if isDeepCSVBDiscrM(jet): n_M_DeepCSVBDiscr_btagged_jets += 1
            if isDeepCSVBDiscrT(jet): n_T_DeepCSVBDiscr_btagged_jets += 1
            if iscTaggerL(jet): n_L_cTagger_ctagged_jets += 1
            if iscTaggerM(jet): n_M_cTagger_ctagged_jets += 1
            if iscTaggerT(jet): n_T_cTagger_ctagged_jets += 1
            if isDeepCSVcTaggerL(jet): n_L_DeepCSVcTagger_ctagged_jets += 1
            if isDeepCSVcTaggerM(jet): n_M_DeepCSVcTagger_ctagged_jets += 1
            if isDeepCSVcTaggerT(jet): n_T_DeepCSVcTagger_ctagged_jets += 1
        dict_variableName_Leaves["n_CSVv2_L_btagged"][0][0] = n_L_CSVv2_btagged_jets
        dict_variableName_Leaves["n_CSVv2_M_btagged"][0][0] = n_M_CSVv2_btagged_jets
        dict_variableName_Leaves["n_CSVv2_T_btagged"][0][0] = n_T_CSVv2_btagged_jets
        dict_variableName_Leaves["n_DeepCSVBDiscr_L_btagged"][0][0] = n_L_DeepCSVBDiscr_btagged_jets
        dict_variableName_Leaves["n_DeepCSVBDiscr_M_btagged"][0][0] = n_M_DeepCSVBDiscr_btagged_jets
        dict_variableName_Leaves["n_DeepCSVBDiscr_T_btagged"][0][0] = n_T_DeepCSVBDiscr_btagged_jets
        dict_variableName_Leaves["n_cTagger_L_ctagged"][0][0] = n_L_cTagger_ctagged_jets
        dict_variableName_Leaves["n_cTagger_M_ctagged"][0][0] = n_M_cTagger_ctagged_jets
        dict_variableName_Leaves["n_cTagger_T_ctagged"][0][0] = n_T_cTagger_ctagged_jets
        dict_variableName_Leaves["n_DeepCSVcTagger_L_ctagged"][0][0] = n_L_DeepCSVcTagger_ctagged_jets
        dict_variableName_Leaves["n_DeepCSVcTagger_M_ctagged"][0][0] = n_M_DeepCSVcTagger_ctagged_jets
        dict_variableName_Leaves["n_DeepCSVcTagger_T_ctagged"][0][0] = n_T_DeepCSVcTagger_ctagged_jets
        
        
        # start the classification / assignment of the jets
        jclf = JetsClassifier(v_jet)
        jclf.Clean(leading_leptons[0],leading_leptons[1])
        
        if len(jclf.validJets()) < 4: continue
        
        #rint "CATEGORY: ", cat
        #print "n jets: ", len(v_jet)
        #print "all jets hadronflavour: ", [jj.HadronFlavour() for jj in v_jet]
        matchingvalue = jclf.OrderTopMatchingNN(model,scaler,input_variables,pos_lepton,neg_lepton)
        #jclf.OrderDeepCSV()
        if matchingvalue == -999: 
            print "Event information: run: %i, id: %i, lumi: %i"%(intree_.ev_run, intree_.ev_id, intree_.ev_lumi)
            print "Not using this event"
            continue
        
        #if matchingvalue < 0.95: continue
        
        if not jclf.IsValid(): continue # at least 4 valid jets found with valid CSVv2 values
        
        if not (isDeepCSVBDiscrM(jclf.jets_dict_["leading_top_bjet"][0]) and isDeepCSVBDiscrM(jclf.jets_dict_["subleading_top_bjet"][0])): continue
        if not (jclf.jets_dict_["leading_top_bjet"][0].Pt() > 30 and jclf.jets_dict_["subleading_top_bjet"][0].Pt() > 30): continue
        
        # Fill best matching value
        dict_variableName_Leaves["TopMatching_NN_best_value"][0][0] = matchingvalue
        
        
        # Additional jets c-tagged?
        n_L_cTagger_additional_ctagged_jets = 0
        n_M_cTagger_additional_ctagged_jets = 0
        n_T_cTagger_additional_ctagged_jets = 0
        n_L_DeepCSVcTagger_additional_ctagged_jets = 0
        n_M_DeepCSVcTagger_additional_ctagged_jets = 0
        n_T_DeepCSVcTagger_additional_ctagged_jets = 0
        if iscTaggerL(jclf.LeadingAddJet()): n_L_cTagger_additional_ctagged_jets += 1
        if iscTaggerL(jclf.SubLeadingAddJet()): n_L_cTagger_additional_ctagged_jets += 1
        if iscTaggerM(jclf.LeadingAddJet()): n_M_cTagger_additional_ctagged_jets += 1
        if iscTaggerM(jclf.SubLeadingAddJet()): n_M_cTagger_additional_ctagged_jets += 1
        if iscTaggerT(jclf.LeadingAddJet()): n_T_cTagger_additional_ctagged_jets += 1
        if iscTaggerT(jclf.SubLeadingAddJet()): n_T_cTagger_additional_ctagged_jets += 1
        if isDeepCSVcTaggerL(jclf.LeadingAddJet()): n_L_DeepCSVcTagger_additional_ctagged_jets += 1
        if isDeepCSVcTaggerL(jclf.SubLeadingAddJet()): n_L_DeepCSVcTagger_additional_ctagged_jets += 1
        if isDeepCSVcTaggerM(jclf.LeadingAddJet()): n_M_DeepCSVcTagger_additional_ctagged_jets += 1
        if isDeepCSVcTaggerM(jclf.SubLeadingAddJet()): n_M_DeepCSVcTagger_additional_ctagged_jets += 1
        if isDeepCSVcTaggerT(jclf.LeadingAddJet()): n_T_DeepCSVcTagger_additional_ctagged_jets += 1
        if isDeepCSVcTaggerT(jclf.SubLeadingAddJet()): n_T_DeepCSVcTagger_additional_ctagged_jets += 1
        dict_variableName_Leaves["n_cTagger_L_Additional_ctagged"][0][0] = n_L_cTagger_additional_ctagged_jets
        dict_variableName_Leaves["n_cTagger_M_Additional_ctagged"][0][0] = n_M_cTagger_additional_ctagged_jets
        dict_variableName_Leaves["n_cTagger_T_Additional_ctagged"][0][0] = n_T_cTagger_additional_ctagged_jets
        dict_variableName_Leaves["n_DeepCSVcTagger_L_Additional_ctagged"][0][0] = n_L_DeepCSVcTagger_additional_ctagged_jets
        dict_variableName_Leaves["n_DeepCSVcTagger_M_Additional_ctagged"][0][0] = n_M_DeepCSVcTagger_additional_ctagged_jets
        dict_variableName_Leaves["n_DeepCSVcTagger_T_Additional_ctagged"][0][0] = n_T_DeepCSVcTagger_additional_ctagged_jets
        
        # https://twiki.cern.ch/twiki/bin/view/CMS/BTagSFMethods
        if (not intree_.is_data): 
            dict_variableName_Leaves["weight_btag_iterativefit"][0][0] = 1
            for jet_tmp in jclf.validJets():
                dict_variableName_Leaves["weight_btag_iterativefit"][0][0] *= jet_tmp.SfIterativeFitCentral()
        else: dict_variableName_Leaves["weight_btag_iterativefit"][0][0] = 1.
        
        # https://twiki.cern.ch/twiki/bin/view/CMS/BTagSFMethods
        # if (not intree_.is_data):
#             dict_variableName_Leaves["weight_btag_iterativefit"][0][0] = jclf.LeadingTopJet().SfIterativeFitCentral()*jclf.SubLeadingTopJet().SfIterativeFitCentral()*jclf.LeadingAddJet().SfIterativeFitCentral()*jclf.SubLeadingAddJet().SfIterativeFitCentral()
#         else: dict_variableName_Leaves["weight_btag_iterativefit"][0][0] = 1.

        # if (jclf.LeadingTopJet().SfIterativeFitCentral()*jclf.SubLeadingTopJet().SfIterativeFitCentral()*jclf.LeadingAddJet().SfIterativeFitCentral()*jclf.SubLeadingAddJet().SfIterativeFitCentral() == 0):
#             print jclf.LeadingTopJet().SfIterativeFitCentral(),jclf.SubLeadingTopJet().SfIterativeFitCentral(),jclf.LeadingAddJet().SfIterativeFitCentral(),jclf.SubLeadingAddJet().SfIterativeFitCentral()
#             print jclf.LeadingTopJet().CSVv2(),jclf.SubLeadingTopJet().CSVv2(),jclf.LeadingAddJet().CSVv2(),jclf.SubLeadingAddJet().CSVv2()
#             print ""
        #print jclf.LeadingTopJet().GenJetID(), jclf.SubLeadingTopJet().GenJetID(), jclf.LeadingAddJet().GenJetID(), jclf.SubLeadingAddJet().GenJetID()
        
        dict_variableName_Leaves["CSVv2_addJet1"][0][0] = jclf.jets_dict_["leading_add_jet"][0].CSVv2()
        dict_variableName_Leaves["CSVv2_addJet2"][0][0] = jclf.jets_dict_["subleading_add_jet"][0].CSVv2()
        dict_variableName_Leaves["DeepCSVBDiscr_addJet1"][0][0] = jclf.jets_dict_["leading_add_jet"][0].DeepCSVBDiscr()
        dict_variableName_Leaves["DeepCSVBDiscr_addJet2"][0][0] = jclf.jets_dict_["subleading_add_jet"][0].DeepCSVBDiscr()
        dict_variableName_Leaves["cTagCvsL_addJet1"][0][0] = jclf.jets_dict_["leading_add_jet"][0].CTagCvsL()
        dict_variableName_Leaves["cTagCvsL_addJet2"][0][0] = jclf.jets_dict_["subleading_add_jet"][0].CTagCvsL()
        dict_variableName_Leaves["cTagCvsB_addJet1"][0][0] = jclf.jets_dict_["leading_add_jet"][0].CTagCvsB()
        dict_variableName_Leaves["cTagCvsB_addJet2"][0][0] = jclf.jets_dict_["subleading_add_jet"][0].CTagCvsB()
        dict_variableName_Leaves["DeepCSVcTagCvsL_addJet1"][0][0] = jclf.jets_dict_["leading_add_jet"][0].DeepCSVCvsL()
        dict_variableName_Leaves["DeepCSVcTagCvsL_addJet2"][0][0] = jclf.jets_dict_["subleading_add_jet"][0].DeepCSVCvsL()
        dict_variableName_Leaves["DeepCSVcTagCvsB_addJet1"][0][0] = jclf.jets_dict_["leading_add_jet"][0].DeepCSVCvsB()
        dict_variableName_Leaves["DeepCSVcTagCvsB_addJet2"][0][0] = jclf.jets_dict_["subleading_add_jet"][0].DeepCSVCvsB()
        
        if (not intree_.is_data):
            dict_variableName_Leaves["hadronFlavour_addJet1"][0][0] = jclf.jets_dict_["leading_add_jet"][0].HadronFlavour()
            dict_variableName_Leaves["hadronFlavour_addJet2"][0][0] = jclf.jets_dict_["subleading_add_jet"][0].HadronFlavour()
            dict_variableName_Leaves["partonFlavour_addJet1"][0][0] = jclf.jets_dict_["leading_add_jet"][0].PartonFlavour()
            dict_variableName_Leaves["partonFlavour_addJet2"][0][0] = jclf.jets_dict_["subleading_add_jet"][0].PartonFlavour()
            dict_variableName_Leaves["event_Category"][0][0] = cat
        else:
            dict_variableName_Leaves["hadronFlavour_addJet1"][0][0] = -999
            dict_variableName_Leaves["hadronFlavour_addJet2"][0][0] = -999
            dict_variableName_Leaves["partonFlavour_addJet1"][0][0] = -999
            dict_variableName_Leaves["partonFlavour_addJet2"][0][0] = -999
            dict_variableName_Leaves["event_Category"][0][0] = -999
        
        
        # Gen level info
        if "TTJets" in infile or "TTTo2L2Nu" in infile: 
            for truth in v_truth:
                label_name = truth.LabelName()
                # if the label name is not included in one of the branches, skip this truth particle
                if not any([label_name.Data() in i for i in dict_variableName_Leaves.keys()]): continue
                dict_variableName_Leaves["Gen_%s_pT"%label_name][0][0] = truth.Pt()
                dict_variableName_Leaves["Gen_%s_eta"%label_name][0][0] = truth.Eta()
                dict_variableName_Leaves["Gen_%s_phi"%label_name][0][0] = truth.Phi()
                dict_variableName_Leaves["Gen_%s_E"%label_name][0][0] = truth.E()
                dict_variableName_Leaves["Gen_%s_M"%label_name][0][0] = truth.M()

    



        otree_.Fill()

        v_el.clear()
        v_mu.clear()
        v_jet.clear()
        v_truth.clear()
        v_trig.clear()
        
        #v_validjets_.clear()
        
    # ***************** end of  event loop ********************
    
    print "%s: Selected %i/%i (%.3f%%) of events"%(infile.split("/")[-1],otree_.GetEntries(),actual_nentries,100*float(otree_.GetEntries())/float(actual_nentries))
    
    hcount = infile_.Get("hcount")
    hweight = infile_.Get("hweight")
    
    if (actual_nentries < original_nentries):
        hcount.SetBinContent(1,actual_nentries*hcount.GetBinContent(1)/(float(original_nentries)))
        hweight.SetBinContent(1,actual_nentries*hweight.GetBinContent(1)/(float(original_nentries)))
    
    
    ofile_.cd()
    hcount.Write()
    hweight.Write()
    otree_.Write()
    
    ofile_.Close()
    infile_.Close()
    
    
    
    
    



def main():

    parser = ArgumentParser()
    parser.add_argument('--infile', default="FILLMEPLEASE",help='path and name of input file')
    parser.add_argument('--outfile', default="*",help='path and name of output file')
    parser.add_argument('--topmatchingdir', default="FILLME",help='name of training directory')
    parser.add_argument('--firstEvt', type=int, default=0,help='first event')
    parser.add_argument('--lastEvt', type=int, default=-1,help='last event')
    parser.add_argument('--splitted', type=int, default=0,help='bool for splitted or not')
    args = parser.parse_args()
    
    Analyze(args.infile, args.outfile, args.topmatchingdir, args.firstEvt, args.lastEvt, bool(args.splitted))
    
    

if __name__ == "__main__":
	main()


