from Helper import *
from argparse import ArgumentParser
import time
import multiprocessing
import thread
import subprocess
import sys
import signal
import inspect

def Analyze(infile, outfile, nevents = -1):
    
    if not os.path.isfile(infile):
        print "ERROR: COULD NOT FIND FILE: %s!!!"%infile
        sys.exit(1)
    
    infile_ = TFile(infile)
    intree_ = infile_.Get("tree")
    
    ofile_ = TFile(outfile,"RECREATE")
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
    dict_variableName_Leaves.update({"n_CSVv2_L_btagged": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"n_CSVv2_M_btagged": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"n_CSVv2_T_btagged": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"n_DeepCSVBDiscr_L_btagged": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"n_DeepCSVBDiscr_M_btagged": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"n_DeepCSVBDiscr_T_btagged": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"event_Category": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"lepton_Category": [array('i', [0]),"I"]}) # 0 = elel, 1 = mumu, 2 = elmu
    #weights
    dict_variableName_Leaves.update({"weight_btag_iterativefit": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_electron_id": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_electron_reco": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_muon_id": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_muon_iso": [array('d', [1]),"D"]})
    # Gen Level info
    if "TT_Tune" in infile:
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
    #****************************************************************************************
    
    original_nentries = intree_.GetEntries()
    nEntries = original_nentries
    if nevents > 0 and nevents < nEntries: nEntries = nevents
    #nEntries = 1000
    
    print "Processing File %s, containing %i events (processing %i events)"%(infile,original_nentries,nEntries)
    
    v_el = ROOT.std.vector( Electron )()
    v_mu = ROOT.std.vector( Muon )()
    v_jet = ROOT.std.vector( Jet )()
    v_met = ROOT.std.vector( MissingEnergy )()
    v_trig = ROOT.std.vector( Trigger )()
    v_truth = ROOT.std.vector( Truth )()
    
    # ***************** Start event loop ********************
    for evt in range(nEntries):
        if (evt % int(nEntries/10.) == 0): print"%s: Processing event %i/%i (%.1f %%)"%(infile.split("/")[-1],evt,nEntries,100*float(evt)/float(nEntries))
        intree_.GetEntry(evt)
        
        v_el = intree_.Electrons
        v_mu = intree_.Muons
        v_jet = intree_.Jets
        v_trig = intree_.Trigger
        v_met = intree_.MET
        if "TT_Tune" in infile: v_truth = intree_.Truth
        
        
        
        
        
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
                dict_variableName_Leaves["weight_muon_id"][0][0] = leading_muon.w_Id()
                dict_variableName_Leaves["weight_muon_iso"][0][0] = leading_muon.w_Iso()
            elif (lepton_category == 0): # elel
                dict_variableName_Leaves["weight_electron_id"][0][0] = leading_elec.w_CBid() * subleading_elec.w_CBid()
                dict_variableName_Leaves["weight_electron_reco"][0][0] = leading_elec.w_Reco() * subleading_elec.w_Reco()
                dict_variableName_Leaves["weight_muon_id"][0][0] = 1
                dict_variableName_Leaves["weight_muon_iso"][0][0] = 1
            elif (lepton_category == 1): # mumu
                dict_variableName_Leaves["weight_electron_id"][0][0] = 1
                dict_variableName_Leaves["weight_electron_reco"][0][0] = 1
                dict_variableName_Leaves["weight_muon_id"][0][0] = leading_muon.w_Id() * subleading_muon.w_Id()
                dict_variableName_Leaves["weight_muon_iso"][0][0] = leading_muon.w_Iso() * subleading_muon.w_Iso()
            
            
            
            
        
        # ***************** Trigger for dilepton cases only! ********************
        passTrigger = False
        #iTrig = Trigger()
        for trig in v_trig:
            if (lepton_category == 2):
                if ("Ele" in trig.Name().Data() and "Mu" in trig.Name().Data() and trig.Pass()): passTrigger = True
            elif (lepton_category == 0):
                if ("Ele" in trig.Name().Data() and not "Mu" in trig.Name().Data() and trig.Pass()): passTrigger = True
            elif (lepton_category == 1):
                if (not "Ele" in trig.Name().Data() and "Mu" in trig.Name().Data() and trig.Pass()): passTrigger = True
        if not passTrigger: continue
        # *******************************************************
        
        
        # ***************** Jets ********************
        # event category based on jet content
        # https://twiki.cern.ch/twiki/bin/view/CMSPublic/GenHFHadronMatcher
        if (not intree_.is_data):
            cat = -1 # default for anything not ttbar of for ttbar which is not in the following categories
            id = int(str(intree_.genTTX_id)[-2:])
            if "TT_Tune" in infile:
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
        for jet in v_jet:
            if isCSVv2L(jet): n_L_CSVv2_btagged_jets += 1
            if isCSVv2M(jet): n_M_CSVv2_btagged_jets += 1
            if isCSVv2T(jet): n_T_CSVv2_btagged_jets += 1
            if isDeepCSVBDiscrL(jet): n_L_DeepCSVBDiscr_btagged_jets += 1
            if isDeepCSVBDiscrM(jet): n_M_DeepCSVBDiscr_btagged_jets += 1
            if isDeepCSVBDiscrT(jet): n_T_DeepCSVBDiscr_btagged_jets += 1
        dict_variableName_Leaves["n_CSVv2_L_btagged"][0][0] = n_L_CSVv2_btagged_jets
        dict_variableName_Leaves["n_CSVv2_M_btagged"][0][0] = n_M_CSVv2_btagged_jets
        dict_variableName_Leaves["n_CSVv2_T_btagged"][0][0] = n_T_CSVv2_btagged_jets
        dict_variableName_Leaves["n_DeepCSVBDiscr_L_btagged"][0][0] = n_L_DeepCSVBDiscr_btagged_jets
        dict_variableName_Leaves["n_DeepCSVBDiscr_M_btagged"][0][0] = n_M_DeepCSVBDiscr_btagged_jets
        dict_variableName_Leaves["n_DeepCSVBDiscr_T_btagged"][0][0] = n_T_DeepCSVBDiscr_btagged_jets
        
        
        # start the classification / assignment of the jets
        jclf = JetsClassifier(v_jet)
        jclf.Clean(leading_leptons[0],leading_leptons[1])
        
        jclf.OrderDeepCSV()
        
        if not jclf.IsValid(): continue # at least 4 valid jets found with valid CSVv2 values
        
        if not (isDeepCSVBDiscrM(jclf.jets_dict_["leading_top_bjet"][0]) and isDeepCSVBDiscrM(jclf.jets_dict_["subleading_top_bjet"][0])): continue
        
        # https://twiki.cern.ch/twiki/bin/view/CMS/BTagSFMethods
        if (not intree_.is_data): dict_variableName_Leaves["weight_btag_iterativefit"][0][0] = jclf.LeadingTopJet().SfIterativeFitCentral()*jclf.SubLeadingTopJet().SfIterativeFitCentral()*jclf.LeadingAddJet().SfIterativeFitCentral()*jclf.SubLeadingAddJet().SfIterativeFitCentral()
        else: dict_variableName_Leaves["weight_btag_iterativefit"][0][0] = 1.
        
        
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
        if "TT_Tune" in infile: 
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
    # ***************** end of  event loop ********************
    
    print "%s: Selected %i/%i (%.3f%%) of events"%(infile.split("/")[-1],otree_.GetEntries(),nEntries,100*float(otree_.GetEntries())/float(nEntries))
    
    hcount = infile_.Get("hcount")
    hweight = infile_.Get("hweight")
    
    
    ofile_.cd()
    hcount.Write()
    hweight.Write()
    otree_.Write()
    
    ofile_.Close()
    infile_.Close()
    
    
    
    
    



def main():

    parser = ArgumentParser()
    parser.add_argument('--indir', default="FILLMEPLEASE",help='directory name of input files')
    parser.add_argument('--infiles', default="*",help='name of input files')
    parser.add_argument('--tag', default=time.strftime("%a%d%b%Y_%Hh%Mm%Ss"),help='name of output directory')
    parser.add_argument('--nevents', type=int, default=-1,help='number of CPU to use in parallel')
    parser.add_argument('--ncpu', type=int, default=-1,help='number of CPU to use in parallel')
    args = parser.parse_args()

    workingdir = os.getcwd()

    if not os.path.isdir(workingdir+"/SELECTED_"+args.tag): os.mkdir(workingdir+"/SELECTED_"+args.tag)
    
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

    
    
    if (args.ncpu < 0 or args.ncpu > multiprocessing.cpu_count()): parallelProcesses = multiprocessing.cpu_count()
    else: parallelProcesses = args.ncpu
    p = multiprocessing.Pool(parallelProcesses)
    print "Using %i parallel processes (%i in total)" %(parallelProcesses,len(filelist))
    
    try:
        for f in filelist:
            #Analyze(indir+f,workingdir+"/SELECTED_"+args.tag+"/"+f)
            res = p.apply_async(Analyze, args = (indir+f,workingdir+"/SELECTED_"+args.tag+"/"+f,args.nevents,))
            #res.get(99999) # timout when this number of seconds is reached
        res.get(99999)
        p.close()
        p.join()
    except KeyboardInterrupt:
        print "Caught KeyboardInterrupt, terminating workers"
        pool.terminate()
        pool.join()
    
    #Analyze(args.indir+"/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8.root",workingdir+"/SELECTED_"+args.tag+"/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8.root",nevents=10000)

if __name__ == "__main__":
	main()


