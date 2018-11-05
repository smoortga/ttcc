from Helper_ttbarSingleLepton import *
import time
import multiprocessing
import thread
import subprocess
import sys
import signal
import inspect
import random
from copy import deepcopy

def Analyze(infile, outfile, topmatchingdir, ttHFSelectordir, reweightingdir, IdxBegin = 0, IdxEnd = -1, Splitted = False):
    
    if not os.path.isfile(infile):
        print "ERROR: COULD NOT FIND FILE: %s!!!"%infile
        sys.exit(1)
    
    infile_ = TFile(infile)
    intree_ = infile_.Get("tree")
    
    if Splitted: ofile_ = TFile(outfile.replace(".root","_events_"+str(IdxBegin)+"_"+str(IdxEnd)+".root"),"RECREATE")
    else: ofile_ = TFile(outfile,"RECREATE")
    otree_ = intree_.CloneTree(0)
    
    # Uncomment this if you want to disable saving all the original collections (Drastically reduces size by a factor of ~ 3)
    otree_.SetBranchStatus("Truth",0)
    otree_.SetBranchStatus("GenTTXJets",0)
    otree_.SetBranchStatus("Jets",0)
    otree_.SetBranchStatus("Muons",0)
    otree_.SetBranchStatus("Electrons",0)
    otree_.SetBranchStatus("Trigger",0)
    otree_.SetBranchStatus("MET",0)
    
    # **************************** add extra branches to output****************************
    dict_variableName_Leaves = {}
    dict_variableName_Leaves.update({"Pt_lepton": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"Eta_lepton": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"hadronFlavour_addJet1": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"hadronFlavour_addJet2": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"hadronFlavour_addJet3": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"partonFlavour_addJet1": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"partonFlavour_addJet2": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"partonFlavour_addJet3": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"Pt_addJet1": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"Pt_addJet2": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"Pt_addJet3": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"Eta_addJet1": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"Eta_addJet2": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"Eta_addJet3": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"DeepCSVBDiscr_addJet1": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"DeepCSVBDiscr_addJet2": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"DeepCSVBDiscr_addJet3": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"cTagCvsL_addJet1": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"cTagCvsL_addJet2": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"cTagCvsL_addJet3": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"cTagCvsB_addJet1": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"cTagCvsB_addJet2": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"cTagCvsB_addJet3": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"DeepCSVcTagCvsL_addJet1": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"DeepCSVcTagCvsL_addJet2": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"DeepCSVcTagCvsL_addJet3": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"DeepCSVcTagCvsB_addJet1": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"DeepCSVcTagCvsB_addJet2": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"DeepCSVcTagCvsB_addJet3": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"DeepFlavourcTagCvsL_addJet1": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"DeepFlavourcTagCvsL_addJet2": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"DeepFlavourcTagCvsL_addJet3": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"DeepFlavourcTagCvsB_addJet1": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"DeepFlavourcTagCvsB_addJet2": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"DeepFlavourcTagCvsB_addJet3": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"n_cTagger_L_ctagged": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"n_cTagger_M_ctagged": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"n_cTagger_T_ctagged": [array('i', [0]),"I"]})
#     dict_variableName_Leaves.update({"n_cTagger_L_Additional_ctagged": [array('i', [0]),"I"]})
#     dict_variableName_Leaves.update({"n_cTagger_M_Additional_ctagged": [array('i', [0]),"I"]})
#     dict_variableName_Leaves.update({"n_cTagger_T_Additional_ctagged": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"n_DeepCSVBDiscr_L_btagged": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"n_DeepCSVBDiscr_M_btagged": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"n_DeepCSVBDiscr_T_btagged": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"n_DeepCSVcTagger_L_ctagged": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"n_DeepCSVcTagger_M_ctagged": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"n_DeepCSVcTagger_T_ctagged": [array('i', [0]),"I"]})
#     dict_variableName_Leaves.update({"n_DeepCSVcTagger_L_Additional_ctagged": [array('i', [0]),"I"]})
#     dict_variableName_Leaves.update({"n_DeepCSVcTagger_M_Additional_ctagged": [array('i', [0]),"I"]})
#     dict_variableName_Leaves.update({"n_DeepCSVcTagger_T_Additional_ctagged": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"lepton_Category": [array('i', [0]),"I"]}) # 0 = elel, 1 = mumu, 2 = elmu
    #weights
    dict_variableName_Leaves.update({"weight_btag_iterativefit": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_btag_iterativefit_JesUp": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_btag_iterativefit_JesDown": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_btag_iterativefit_LfUp": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_btag_iterativefit_LfDown": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_btag_iterativefit_HfUp": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_btag_iterativefit_HfDown": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_btag_iterativefit_Hfstats1Up": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_btag_iterativefit_Hfstats1Down": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_btag_iterativefit_Hfstats2Up": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_btag_iterativefit_Hfstats2Down": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_btag_iterativefit_Lfstats1Up": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_btag_iterativefit_Lfstats1Down": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_btag_iterativefit_Lfstats2Up": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_btag_iterativefit_Lfstats2Down": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_btag_iterativefit_Cferr1Up": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_btag_iterativefit_Cferr1Down": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_btag_iterativefit_Cferr2Up": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_btag_iterativefit_Cferr2Down": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_btag_DeepCSVLoose": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_btag_DeepCSVLooseUp": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_btag_DeepCSVLooseDown": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_btag_DeepCSVMedium": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_btag_DeepCSVMediumUp": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_btag_DeepCSVMediumDown": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_btag_DeepCSVTight": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_btag_DeepCSVTightUp": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_btag_DeepCSVTightDown": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_electron_id": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_electron_reco": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_electron_trig": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_muon_id": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_muon_iso": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_muon_trig": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_electron_id_Up": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_electron_reco_Up": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_electron_trig_Up": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_muon_id_Up": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_muon_iso_Up": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_muon_trig_Up": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_electron_id_Down": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_electron_reco_Down": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_electron_trig_Down": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_muon_id_Down": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_muon_iso_Down": [array('d', [1]),"D"]})
    dict_variableName_Leaves.update({"weight_muon_trig_Down": [array('d', [1]),"D"]})

#     
    
    for name,arr in dict_variableName_Leaves.iteritems():
        otree_.Branch(name,arr[0],name+"/"+arr[1])
    
    
    # for amcatnlo I need to normalize the scale variations to inital weight!
    intree_.GetEntry(1)
    if (not intree_.is_data):
        buffer_weight_scale_muF0p5 = array('f', [1])
        buffer_weight_scale_muF2 = array('f', [1])
        buffer_weight_scale_muR0p5 = array('f', [1])
        buffer_weight_scale_muR2 = array('f', [1])

        otree_.SetBranchAddress("weight_scale_muF0p5",buffer_weight_scale_muF0p5)
        otree_.SetBranchAddress("weight_scale_muF2",buffer_weight_scale_muF2)
        otree_.SetBranchAddress("weight_scale_muR0p5",buffer_weight_scale_muR0p5)
        otree_.SetBranchAddress("weight_scale_muR2",buffer_weight_scale_muR2)
    
    # v_validjets_ = ROOT.std.vector( Jet )()
#     otree_.Branch("ValidJets",v_validjets_);
    #****************************************************************************************
    
    #****************************efficiency histograms:****************************
    eff_histo_file = ROOT.TFile("/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/analyse/BTaggingEfficiencyHistograms/SELECTED_ttbarSingleLepton_histos/btagEffHisto.root")
    #****************************************************************************************   
    
    
    #**************************** Load the top matching training ****************************
    model = load_model(topmatchingdir+"/model_checkpoint_save.hdf5")
    scaler = pickle.load(open(topmatchingdir+"/scaler.pkl","rb"))
    input_variables = pickle.load(open(topmatchingdir+"/variables.pkl","rb"))
    #****************************************************************************************
#     
#     # **************************** Load the ttHF Selector training ****************************
#     model_ttHFSelector = load_model(ttHFSelectordir+"/model_checkpoint_save.hdf5")
#     scaler_ttHFSelector = pickle.load(open(ttHFSelectordir+"/scaler.pkl","rb"))
#     input_variables_ttHFSelector = pickle.load(open(ttHFSelectordir+"/variables.pkl","rb"))
#     #****************************************************************************************
#     
#     
#     # **************************** Load the reweighting training ****************************
#     model_reweighting = load_model(reweightingdir+"/final_reconstructor_save.hdf5", custom_objects={'loss_D': make_loss_D(c=1.)})
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
        if "TTJets" in infile or "TTTo" in infile: v_truth = intree_.Truth
        
        
        # ***************** MC scale variations for amcatnlo need to be normalized to initial weights ********************
        if (not intree_.is_data):
            if abs(intree_.mc_weight_originalValue) > 1: 
                buffer_weight_scale_muF0p5[0] = intree_.weight_scale_muF0p5/abs(intree_.mc_weight_originalValue)
                buffer_weight_scale_muF2[0] = intree_.weight_scale_muF2/abs(intree_.mc_weight_originalValue)
                buffer_weight_scale_muR0p5[0] = intree_.weight_scale_muR0p5/abs(intree_.mc_weight_originalValue)
                buffer_weight_scale_muR2[0] = intree_.weight_scale_muR2/abs(intree_.mc_weight_originalValue)
        # ****************************************************************************************************************
        
        
        # ***************** Leading Electrons ********************
        leading_elec = Electron()
        #subleading_elec = Electron()
        n_isolated_electrons = 0
        for el in v_el:
            #**********************
            #   LEADING ELECTRON?
            #**********************
            if (el.isTight() and el.relIso() < 0.077 and abs(el.Eta()) < 1.48 and el.Pt() > leading_elec.Pt()): 
                n_isolated_electrons = n_isolated_electrons + 1
                leading_elec = el
            elif (el.isTight() and el.relIso() < 0.068 and abs(el.Eta()) >= 1.48 and el.Pt() > leading_elec.Pt()): 
                n_isolated_electrons = n_isolated_electrons + 1
                leading_elec = el

        
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
                leading_muon = mu

        # *******************************************************
        
        if ((n_isolated_muons + n_isolated_electrons) != 1): continue
        # ***************** Leading Lepton ********************
        leading_leptons = [leading_elec,leading_muon]
        leading_leptons.sort(key=lambda x: x.Pt(), reverse=True) # Pt ordering
        leading_lepton = leading_leptons[0:1]
        
        dict_variableName_Leaves["Pt_lepton"][0][0] = leading_lepton[0].Pt()
        dict_variableName_Leaves["Eta_lepton"][0][0] = leading_lepton[0].Eta()

        #print isinstance(leading_leptons[0],Electron)

        
        
        # define the lepton categories
        lepton_category=-1
        if (isinstance(leading_lepton[0],Electron)): lepton_category = 0 # el
        elif (isinstance(leading_lepton[0],Muon)): lepton_category = 1 # mumu
        else: 
            print "NO PROPER LEPTON CATEGORY FOUND"
            continue
        
        dict_variableName_Leaves["lepton_Category"][0][0] = lepton_category
        
        
        
        
        # add lepton weights 
        if (not intree_.is_data):
            if (lepton_category == 0): # el
                dict_variableName_Leaves["weight_electron_id"][0][0] = leading_elec.w_CBid()
                dict_variableName_Leaves["weight_electron_reco"][0][0] = leading_elec.w_Reco()
                dict_variableName_Leaves["weight_electron_trig"][0][0] = leading_elec.w_Trig()
                dict_variableName_Leaves["weight_electron_id_Up"][0][0] = leading_elec.w_CBidUp()
                dict_variableName_Leaves["weight_electron_reco_Up"][0][0] = leading_elec.w_RecoUp()
                dict_variableName_Leaves["weight_electron_trig_Up"][0][0] = leading_elec.w_TrigUp()
                dict_variableName_Leaves["weight_electron_id_Down"][0][0] = leading_elec.w_CBidDown()
                dict_variableName_Leaves["weight_electron_reco_Down"][0][0] = leading_elec.w_RecoDown()
                dict_variableName_Leaves["weight_electron_trig_Down"][0][0] = leading_elec.w_TrigDown()
                dict_variableName_Leaves["weight_muon_id"][0][0] = 1
                dict_variableName_Leaves["weight_muon_iso"][0][0] = 1
                dict_variableName_Leaves["weight_muon_trig"][0][0] = 1
                dict_variableName_Leaves["weight_muon_id_Up"][0][0] = 1
                dict_variableName_Leaves["weight_muon_iso_Up"][0][0] = 1
                dict_variableName_Leaves["weight_muon_trig_Up"][0][0] = 1
                dict_variableName_Leaves["weight_muon_id_Down"][0][0] = 1
                dict_variableName_Leaves["weight_muon_iso_Down"][0][0] = 1
                dict_variableName_Leaves["weight_muon_trig_Down"][0][0] = 1
            elif (lepton_category == 1): # mumu
                dict_variableName_Leaves["weight_electron_id"][0][0] = 1
                dict_variableName_Leaves["weight_electron_reco"][0][0] = 1
                dict_variableName_Leaves["weight_electron_trig"][0][0] = 1
                dict_variableName_Leaves["weight_electron_id_Up"][0][0] = 1
                dict_variableName_Leaves["weight_electron_reco_Up"][0][0] = 1
                dict_variableName_Leaves["weight_electron_trig_Up"][0][0] = 1
                dict_variableName_Leaves["weight_electron_id_Down"][0][0] = 1
                dict_variableName_Leaves["weight_electron_reco_Down"][0][0] = 1
                dict_variableName_Leaves["weight_electron_trig_Down"][0][0] = 1
                dict_variableName_Leaves["weight_muon_id"][0][0] = leading_muon.w_Id()
                dict_variableName_Leaves["weight_muon_iso"][0][0] = leading_muon.w_Iso()
                dict_variableName_Leaves["weight_muon_trig"][0][0] = leading_muon.w_Trig()
                dict_variableName_Leaves["weight_muon_id_Up"][0][0] = leading_muon.w_IdUp()
                dict_variableName_Leaves["weight_muon_iso_Up"][0][0] = leading_muon.w_IsoUp()
                dict_variableName_Leaves["weight_muon_trig_Up"][0][0] = leading_muon.w_TrigUp()
                dict_variableName_Leaves["weight_muon_id_Down"][0][0] = leading_muon.w_IdDown()
                dict_variableName_Leaves["weight_muon_iso_Down"][0][0] = leading_muon.w_IsoDown()
                dict_variableName_Leaves["weight_muon_trig_Down"][0][0] = leading_muon.w_TrigDown()
            
            
            
            
            
        #
        # 
        #
        # ***************** Trigger for dilepton cases only! ********************

        passAnyTrigger = False
        passSingleElectronTrigger = False
        passSingleMuonTrigger=False
        for trig in v_trig:
        
            # MC --> logic or of all triggers
            if ((not intree_.is_data) and trig.Pass()):
                passAnyTrigger = True
            
            # Data: depending on the data stream
            elif intree_.is_data:
                if "HLT_Ele35_WPTight_Gsf" in trig.Name().Data() and trig.Pass():
                    passSingleElectronTrigger = True
                elif "HLT_IsoMu27" in trig.Name().Data() and trig.Pass():
                    passSingleMuonTrigger = True
               
        passTriggerLogic = passAnyTrigger or ("SingleMuon" in infile and passSingleMuonTrigger) or ("SingleElectron" in infile and passSingleElectronTrigger and not passSingleMuonTrigger)
        if not passTriggerLogic: continue        
        
        # *******************************************************
        
        
        # ***************** Jets ********************

        
        # count number of b-tagged jets
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
            if isDeepCSVBDiscrL(jet): n_L_DeepCSVBDiscr_btagged_jets += 1
            if isDeepCSVBDiscrM(jet): n_M_DeepCSVBDiscr_btagged_jets += 1
            if isDeepCSVBDiscrT(jet): n_T_DeepCSVBDiscr_btagged_jets += 1
            if iscTaggerL(jet): n_L_cTagger_ctagged_jets += 1
            if iscTaggerM(jet): n_M_cTagger_ctagged_jets += 1
            if iscTaggerT(jet): n_T_cTagger_ctagged_jets += 1
            if isDeepCSVcTaggerL(jet): n_L_DeepCSVcTagger_ctagged_jets += 1
            if isDeepCSVcTaggerM(jet): n_M_DeepCSVcTagger_ctagged_jets += 1
            if isDeepCSVcTaggerT(jet): n_T_DeepCSVcTagger_ctagged_jets += 1
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
        jclf.Clean(leading_lepton[0],leading_lepton[0])
        
        if len(jclf.validJets()) < 4: continue
        validjets = jclf.validJets()
        
        # order and save DeepCSV value and index
        DeepCSV_values = [(idx,jet.DeepCSVBDiscr()) for idx, jet in enumerate(validjets)]
        sorted_values = sorted(DeepCSV_values, key=lambda x: x[1], reverse=True)
		# at least one tight b-tagged jet!
        if not isDeepCSVBDiscrT(validjets.at(sorted_values[0][0])): continue 
        validjets.erase( validjets.begin() + sorted_values[0][0]) #removing this jet from the list
       
        btag_values = [(idx,jet.DeepCSVBDiscr()) for idx, jet in enumerate(validjets)]
        sorted_values_btag = sorted(btag_values, key=lambda x: x[1], reverse=True)
        #print sorted_values_btag
        addJet1 = validjets[sorted_values_btag[0][0]]
        addJet2 = validjets[sorted_values_btag[1][0]]
        addJet3 = validjets[sorted_values_btag[2][0]]

        
        # matchingvalue = jclf.OrderTopMatchingNN(model,scaler,input_variables,leading_lepton[0])
#         #jclf.OrderDeepCSV()
#         if matchingvalue == -999: 
#             #print "Event information: run: %i, id: %i, lumi: %i"%(intree_.ev_run, intree_.ev_id, intree_.ev_lumi)
#             #print "Not using this event"
#             continue
# 
#         if matchingvalue < 0.5: continue
#         
#         # for truth in v_truth:
# #                 label_name = truth.LabelName()
# #                 #print label_name
# #                 if label_name == "top_b":
# #                     print "top b found! ",truth.Pt(),truth.Eta(),truth.Phi()
# #                 elif label_name == "antitop_b":
# #                     print "antitop b found! ",truth.Pt(),truth.Eta(),truth.Phi()
# 
#         
#         addJet1 = jclf.SubLeadingTopJet()
#         if jclf.LeadingAddJet().DeepCSVBDiscr() >= jclf.SubLeadingAddJet().DeepCSVBDiscr():
#             addJet2 = jclf.LeadingAddJet()
#             addJet3 = jclf.SubLeadingAddJet()
#         else:
#             addJet2 = jclf.SubLeadingAddJet()
#             addJet3 = jclf.LeadingAddJet()
        
        # if isDeepCSVBDiscrT(jclf.LeadingTopJet()):
#             addJet0 = jclf.LeadingTopJet()
#             addJet1 = jclf.SubLeadingTopJet()
#             if jclf.LeadingAddJet().DeepCSVBDiscr() >= jclf.SubLeadingAddJet().DeepCSVBDiscr():
#                 addJet2 = jclf.LeadingAddJet()
#                 addJet3 = jclf.SubLeadingAddJet()
#             else:
#                 addJet2 = jclf.SubLeadingAddJet()
#                 addJet3 = jclf.LeadingAddJet()
#         elif isDeepCSVBDiscrT(jclf.SubLeadingTopJet()):
#             addJet0 = jclf.SubLeadingTopJet()
#             addJet1 = jclf.LeadingTopJet()
#             if jclf.LeadingAddJet().DeepCSVBDiscr() >= jclf.SubLeadingAddJet().DeepCSVBDiscr():
#                 addJet2 = jclf.LeadingAddJet()
#                 addJet3 = jclf.SubLeadingAddJet()
#             else:
#                 addJet2 = jclf.SubLeadingAddJet()
#                 addJet3 = jclf.LeadingAddJet()
#         else: continue
        
        # for idx,j in enumerate(jclf.validJets()):
#             print idx, j.HadronFlavour(), j.DeepCSVBDiscr(), j.Pt(), j.Eta(), j.Phi()
#             print "xxxxxxxxxxx"
            
        # print matchingvalue, addJet0.HadronFlavour(), addJet0.DeepCSVBDiscr(), addJet0.Pt(), addJet0.Eta(), addJet0.Phi()
#         print matchingvalue, addJet1.HadronFlavour(), addJet1.DeepCSVBDiscr(), addJet1.Pt(), addJet1.Eta(), addJet1.Phi()
#         print matchingvalue, addJet2.HadronFlavour(), addJet2.DeepCSVBDiscr(), addJet2.Pt(), addJet2.Eta(), addJet2.Phi()
#         print matchingvalue, addJet3.HadronFlavour(), addJet3.DeepCSVBDiscr(), addJet3.Pt(), addJet3.Eta(), addJet3.Phi()
#         print "XXXXX"
        
        
        
        if (not intree_.is_data): 
            dict_variableName_Leaves["weight_btag_iterativefit"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_iterativefit_JesUp"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_iterativefit_JesDown"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_iterativefit_LfUp"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_iterativefit_LfDown"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_iterativefit_HfUp"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_iterativefit_HfDown"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_iterativefit_Hfstats1Up"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_iterativefit_Hfstats1Down"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_iterativefit_Hfstats2Up"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_iterativefit_Hfstats2Down"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_iterativefit_Lfstats1Up"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_iterativefit_Lfstats1Down"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_iterativefit_Lfstats2Up"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_iterativefit_Lfstats2Down"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_iterativefit_Cferr1Up"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_iterativefit_Cferr1Down"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_iterativefit_Cferr2Up"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_iterativefit_Cferr2Down"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_DeepCSVLoose"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_DeepCSVLooseUp"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_DeepCSVLooseDown"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_DeepCSVMedium"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_DeepCSVMediumUp"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_DeepCSVMediumDown"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_DeepCSVTight"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_DeepCSVTightUp"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_DeepCSVTightDown"][0][0] = 1.
            # see https://twiki.cern.ch/twiki/bin/viewauth/CMS/BTagSFMethods#1a_Event_reweighting_using_scale
            prob_MC_L = 1.
            prob_Data_L = 1.
            prob_Data_L_Up = 1.
            prob_Data_L_Down = 1.
            prob_MC_M = 1.
            prob_Data_M = 1.
            prob_Data_M_Up = 1.
            prob_Data_M_Down = 1.
            prob_MC_T = 1.
            prob_Data_T = 1.
            prob_Data_T_Up = 1.
            prob_Data_T_Down = 1.
            for jet_tmp in jclf.validJets():
                # NOTE: some uncertainties only need to be applied to specific jet flavours!
                # see --> https://twiki.cern.ch/twiki/bin/view/CMS/BTagShapeCalibration
                # However, this should be taken care of already in the SELECTION step)
                dict_variableName_Leaves["weight_btag_iterativefit"][0][0]      *= jet_tmp.SfIterativeFitCentral()
                
                eff_L_ = GetBTagEff(jet_tmp,eff_histo_file,"loose")
                eff_M_ = GetBTagEff(jet_tmp,eff_histo_file,"medium")
                eff_T_ = GetBTagEff(jet_tmp,eff_histo_file,"tight")
                
                #print jet_tmp.HadronFlavour(),eff_L_, eff_M_, eff_T_
                
                if isDeepCSVBDiscrL(jet_tmp): 
                    prob_MC_L *= eff_L_
                    prob_Data_L *= (jet_tmp.SfDeepCSVLCentral()*eff_L_)
                    prob_Data_L_Up *= (jet_tmp.SfDeepCSVLUp()*eff_L_)
                    prob_Data_L_Down *= (jet_tmp.SfDeepCSVLDown()*eff_L_)
                else: 
                    prob_MC_L *= (1.-eff_L_)
                    prob_Data_L *= (1.- jet_tmp.SfDeepCSVLCentral()*eff_L_)
                    prob_Data_L_Up *= (1.- jet_tmp.SfDeepCSVLUp()*eff_L_)
                    prob_Data_L_Down *= (1.- jet_tmp.SfDeepCSVLDown()*eff_L_)
                    
                if isDeepCSVBDiscrM(jet_tmp): 
                    prob_MC_M *= eff_M_
                    prob_Data_M *= (jet_tmp.SfDeepCSVMCentral()*eff_M_)
                    prob_Data_M_Up *= (jet_tmp.SfDeepCSVMUp()*eff_M_)
                    prob_Data_M_Down *= (jet_tmp.SfDeepCSVMDown()*eff_M_)
                else: 
                    prob_MC_M *= (1.-eff_M_)
                    prob_Data_M *= (1.- jet_tmp.SfDeepCSVMCentral()*eff_M_)
                    prob_Data_M_Up *= (1.- jet_tmp.SfDeepCSVMUp()*eff_M_)
                    prob_Data_M_Down *= (1.- jet_tmp.SfDeepCSVMDown()*eff_M_)
                
                if isDeepCSVBDiscrT(jet_tmp): 
                    prob_MC_T *= eff_T_
                    prob_Data_T *= (jet_tmp.SfDeepCSVTCentral()*eff_T_)
                    prob_Data_T_Up *= (jet_tmp.SfDeepCSVTUp()*eff_T_)
                    prob_Data_T_Down *= (jet_tmp.SfDeepCSVTDown()*eff_T_)
                else: 
                    prob_MC_T *= (1.-eff_T_)
                    prob_Data_T *= (1.- jet_tmp.SfDeepCSVTCentral()*eff_T_)
                    prob_Data_T_Up *= (1.- jet_tmp.SfDeepCSVTUp()*eff_T_)
                    prob_Data_T_Down *= (1.- jet_tmp.SfDeepCSVTDown()*eff_T_)


                if jet_tmp.HadronFlavour() == 0:
                    #print jet_tmp.SfIterativeFitLfstats1Up(),jet_tmp.SfIterativeFitHfstats1Up(), jet_tmp.SfIterativeFitCentral()
                    dict_variableName_Leaves["weight_btag_iterativefit_JesUp"][0][0] *= jet_tmp.SfIterativeFitJesUp()
                    dict_variableName_Leaves["weight_btag_iterativefit_JesDown"][0][0] *= jet_tmp.SfIterativeFitJesDown()
                    dict_variableName_Leaves["weight_btag_iterativefit_LfUp"][0][0] *= jet_tmp.SfIterativeFitCentral()
                    dict_variableName_Leaves["weight_btag_iterativefit_LfDown"][0][0] *= jet_tmp.SfIterativeFitCentral()
                    dict_variableName_Leaves["weight_btag_iterativefit_HfUp"][0][0] *= jet_tmp.SfIterativeFitHfUp()
                    dict_variableName_Leaves["weight_btag_iterativefit_HfDown"][0][0] *= jet_tmp.SfIterativeFitHfDown()
                    dict_variableName_Leaves["weight_btag_iterativefit_Hfstats1Up"][0][0] *= jet_tmp.SfIterativeFitCentral()
                    dict_variableName_Leaves["weight_btag_iterativefit_Hfstats1Down"][0][0] *= jet_tmp.SfIterativeFitCentral()
                    dict_variableName_Leaves["weight_btag_iterativefit_Hfstats2Up"][0][0] *= jet_tmp.SfIterativeFitCentral()
                    dict_variableName_Leaves["weight_btag_iterativefit_Hfstats2Down"][0][0] *= jet_tmp.SfIterativeFitCentral()
                    dict_variableName_Leaves["weight_btag_iterativefit_Lfstats1Up"][0][0] *= jet_tmp.SfIterativeFitLfstats1Up()
                    dict_variableName_Leaves["weight_btag_iterativefit_Lfstats1Down"][0][0] *= jet_tmp.SfIterativeFitLfstats1Down()
                    dict_variableName_Leaves["weight_btag_iterativefit_Lfstats2Up"][0][0] *= jet_tmp.SfIterativeFitLfstats2Up()
                    dict_variableName_Leaves["weight_btag_iterativefit_Lfstats2Down"][0][0] *= jet_tmp.SfIterativeFitLfstats2Down()
                    dict_variableName_Leaves["weight_btag_iterativefit_Cferr1Up"][0][0] *= jet_tmp.SfIterativeFitCentral()
                    dict_variableName_Leaves["weight_btag_iterativefit_Cferr1Down"][0][0] *= jet_tmp.SfIterativeFitCentral()
                    dict_variableName_Leaves["weight_btag_iterativefit_Cferr2Up"][0][0] *= jet_tmp.SfIterativeFitCentral() 
                    dict_variableName_Leaves["weight_btag_iterativefit_Cferr2Down"][0][0] *= jet_tmp.SfIterativeFitCentral()
                    
                elif jet_tmp.HadronFlavour() == 4:
                    dict_variableName_Leaves["weight_btag_iterativefit_JesUp"][0][0] *= jet_tmp.SfIterativeFitCentral()
                    dict_variableName_Leaves["weight_btag_iterativefit_JesDown"][0][0] *= jet_tmp.SfIterativeFitCentral()
                    dict_variableName_Leaves["weight_btag_iterativefit_LfUp"][0][0] *= jet_tmp.SfIterativeFitCentral()
                    dict_variableName_Leaves["weight_btag_iterativefit_LfDown"][0][0] *= jet_tmp.SfIterativeFitCentral()
                    dict_variableName_Leaves["weight_btag_iterativefit_HfUp"][0][0] *= jet_tmp.SfIterativeFitCentral()
                    dict_variableName_Leaves["weight_btag_iterativefit_HfDown"][0][0] *= jet_tmp.SfIterativeFitCentral()
                    dict_variableName_Leaves["weight_btag_iterativefit_Hfstats1Up"][0][0] *= jet_tmp.SfIterativeFitCentral()
                    dict_variableName_Leaves["weight_btag_iterativefit_Hfstats1Down"][0][0] *= jet_tmp.SfIterativeFitCentral()
                    dict_variableName_Leaves["weight_btag_iterativefit_Hfstats2Up"][0][0] *= jet_tmp.SfIterativeFitCentral()
                    dict_variableName_Leaves["weight_btag_iterativefit_Hfstats2Down"][0][0] *= jet_tmp.SfIterativeFitCentral()
                    dict_variableName_Leaves["weight_btag_iterativefit_Lfstats1Up"][0][0] *= jet_tmp.SfIterativeFitCentral()
                    dict_variableName_Leaves["weight_btag_iterativefit_Lfstats1Down"][0][0] *= jet_tmp.SfIterativeFitCentral()
                    dict_variableName_Leaves["weight_btag_iterativefit_Lfstats2Up"][0][0] *= jet_tmp.SfIterativeFitCentral()
                    dict_variableName_Leaves["weight_btag_iterativefit_Lfstats2Down"][0][0] *= jet_tmp.SfIterativeFitCentral()
                    dict_variableName_Leaves["weight_btag_iterativefit_Cferr1Up"][0][0] *= jet_tmp.SfIterativeFitCferr1Up() 
                    dict_variableName_Leaves["weight_btag_iterativefit_Cferr1Down"][0][0] *= jet_tmp.SfIterativeFitCferr1Down() 
                    dict_variableName_Leaves["weight_btag_iterativefit_Cferr2Up"][0][0] *= jet_tmp.SfIterativeFitCferr2Up() 
                    dict_variableName_Leaves["weight_btag_iterativefit_Cferr2Down"][0][0] *= jet_tmp.SfIterativeFitCferr2Down() 
                elif jet_tmp.HadronFlavour() == 5:
                    dict_variableName_Leaves["weight_btag_iterativefit_JesUp"][0][0] *= jet_tmp.SfIterativeFitJesUp()
                    dict_variableName_Leaves["weight_btag_iterativefit_JesDown"][0][0] *= jet_tmp.SfIterativeFitJesDown()
                    dict_variableName_Leaves["weight_btag_iterativefit_LfUp"][0][0] *= jet_tmp.SfIterativeFitLfUp()
                    dict_variableName_Leaves["weight_btag_iterativefit_LfDown"][0][0] *= jet_tmp.SfIterativeFitLfDown()
                    dict_variableName_Leaves["weight_btag_iterativefit_HfUp"][0][0] *= jet_tmp.SfIterativeFitCentral()
                    dict_variableName_Leaves["weight_btag_iterativefit_HfDown"][0][0] *= jet_tmp.SfIterativeFitCentral()
                    dict_variableName_Leaves["weight_btag_iterativefit_Hfstats1Up"][0][0] *= jet_tmp.SfIterativeFitHfstats1Up()
                    dict_variableName_Leaves["weight_btag_iterativefit_Hfstats1Down"][0][0] *= jet_tmp.SfIterativeFitHfstats1Down()
                    dict_variableName_Leaves["weight_btag_iterativefit_Hfstats2Up"][0][0] *= jet_tmp.SfIterativeFitHfstats2Up()
                    dict_variableName_Leaves["weight_btag_iterativefit_Hfstats2Down"][0][0] *= jet_tmp.SfIterativeFitHfstats2Down()
                    dict_variableName_Leaves["weight_btag_iterativefit_Lfstats1Up"][0][0] *= jet_tmp.SfIterativeFitCentral()
                    dict_variableName_Leaves["weight_btag_iterativefit_Lfstats1Down"][0][0] *= jet_tmp.SfIterativeFitCentral()
                    dict_variableName_Leaves["weight_btag_iterativefit_Lfstats2Up"][0][0] *= jet_tmp.SfIterativeFitCentral()
                    dict_variableName_Leaves["weight_btag_iterativefit_Lfstats2Down"][0][0] *= jet_tmp.SfIterativeFitCentral()
                    dict_variableName_Leaves["weight_btag_iterativefit_Cferr1Up"][0][0] *= jet_tmp.SfIterativeFitCentral()
                    dict_variableName_Leaves["weight_btag_iterativefit_Cferr1Down"][0][0] *= jet_tmp.SfIterativeFitCentral()
                    dict_variableName_Leaves["weight_btag_iterativefit_Cferr2Up"][0][0] *= jet_tmp.SfIterativeFitCentral()
                    dict_variableName_Leaves["weight_btag_iterativefit_Cferr2Down"][0][0] *= jet_tmp.SfIterativeFitCentral()
            
            
            dict_variableName_Leaves["weight_btag_DeepCSVLoose"][0][0]      = prob_Data_L / prob_MC_L
            dict_variableName_Leaves["weight_btag_DeepCSVLooseUp"][0][0]    = prob_Data_L_Up / prob_MC_L
            dict_variableName_Leaves["weight_btag_DeepCSVLooseDown"][0][0]  = prob_Data_L_Down / prob_MC_L
            dict_variableName_Leaves["weight_btag_DeepCSVMedium"][0][0]     = prob_Data_M / prob_MC_M
            dict_variableName_Leaves["weight_btag_DeepCSVMediumUp"][0][0]   = prob_Data_M_Up / prob_MC_M
            dict_variableName_Leaves["weight_btag_DeepCSVMediumDown"][0][0] = prob_Data_M_Down / prob_MC_M
            dict_variableName_Leaves["weight_btag_DeepCSVTight"][0][0]      = prob_Data_T / prob_MC_T
            dict_variableName_Leaves["weight_btag_DeepCSVTightUp"][0][0]    = prob_Data_T_Up / prob_MC_T
            dict_variableName_Leaves["weight_btag_DeepCSVTightDown"][0][0]  = prob_Data_T_Down / prob_MC_T

        else: 
            dict_variableName_Leaves["weight_btag_iterativefit"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_iterativefit_JesUp"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_iterativefit_JesDown"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_iterativefit_LfUp"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_iterativefit_LfDown"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_iterativefit_HfUp"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_iterativefit_HfDown"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_iterativefit_Hfstats1Up"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_iterativefit_Hfstats1Down"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_iterativefit_Hfstats2Up"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_iterativefit_Hfstats2Down"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_iterativefit_Lfstats1Up"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_iterativefit_Lfstats1Down"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_iterativefit_Lfstats2Up"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_iterativefit_Lfstats2Down"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_iterativefit_Cferr1Up"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_iterativefit_Cferr1Down"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_iterativefit_Cferr2Up"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_iterativefit_Cferr2Down"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_DeepCSVLoose"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_DeepCSVLooseUp"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_DeepCSVLooseDown"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_DeepCSVMedium"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_DeepCSVMediumUp"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_DeepCSVMediumDown"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_DeepCSVTight"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_DeepCSVTightUp"][0][0] = 1.
            dict_variableName_Leaves["weight_btag_DeepCSVTightDown"][0][0] = 1.
        
        

        
       
        
        
        dict_variableName_Leaves["DeepCSVBDiscr_addJet1"][0][0] = addJet1.DeepCSVBDiscr()
        dict_variableName_Leaves["DeepCSVBDiscr_addJet2"][0][0] = addJet2.DeepCSVBDiscr()
        dict_variableName_Leaves["DeepCSVBDiscr_addJet3"][0][0] = addJet3.DeepCSVBDiscr()
        dict_variableName_Leaves["cTagCvsL_addJet1"][0][0] = addJet1.CTagCvsL()
        dict_variableName_Leaves["cTagCvsL_addJet2"][0][0] = addJet2.CTagCvsL()
        dict_variableName_Leaves["cTagCvsL_addJet3"][0][0] = addJet3.CTagCvsL()
        dict_variableName_Leaves["cTagCvsB_addJet1"][0][0] = addJet1.CTagCvsB()
        dict_variableName_Leaves["cTagCvsB_addJet2"][0][0] = addJet2.CTagCvsB()
        dict_variableName_Leaves["cTagCvsB_addJet3"][0][0] = addJet3.CTagCvsB()
        dict_variableName_Leaves["DeepCSVcTagCvsL_addJet1"][0][0] = addJet1.DeepCSVCvsL()
        dict_variableName_Leaves["DeepCSVcTagCvsL_addJet2"][0][0] = addJet2.DeepCSVCvsL()
        dict_variableName_Leaves["DeepCSVcTagCvsL_addJet3"][0][0] = addJet3.DeepCSVCvsL()
        dict_variableName_Leaves["DeepCSVcTagCvsB_addJet1"][0][0] = addJet1.DeepCSVCvsB()
        dict_variableName_Leaves["DeepCSVcTagCvsB_addJet2"][0][0] = addJet2.DeepCSVCvsB()
        dict_variableName_Leaves["DeepCSVcTagCvsB_addJet3"][0][0] = addJet3.DeepCSVCvsB()
        dict_variableName_Leaves["DeepFlavourcTagCvsL_addJet1"][0][0] = addJet1.DeepFlavourCvsL()
        dict_variableName_Leaves["DeepFlavourcTagCvsL_addJet2"][0][0] = addJet2.DeepFlavourCvsL()
        dict_variableName_Leaves["DeepFlavourcTagCvsL_addJet3"][0][0] = addJet3.DeepFlavourCvsL()
        dict_variableName_Leaves["DeepFlavourcTagCvsB_addJet1"][0][0] = addJet1.DeepFlavourCvsB()
        dict_variableName_Leaves["DeepFlavourcTagCvsB_addJet2"][0][0] = addJet2.DeepFlavourCvsB()
        dict_variableName_Leaves["DeepFlavourcTagCvsB_addJet3"][0][0] = addJet3.DeepFlavourCvsB()
        

        
        dict_variableName_Leaves["Pt_addJet1"][0][0] = addJet1.Pt()
        dict_variableName_Leaves["Pt_addJet2"][0][0] = addJet2.Pt()
        dict_variableName_Leaves["Pt_addJet3"][0][0] = addJet3.Pt()
        dict_variableName_Leaves["Eta_addJet1"][0][0] = addJet1.Eta()
        dict_variableName_Leaves["Eta_addJet2"][0][0] = addJet2.Eta()
        dict_variableName_Leaves["Eta_addJet3"][0][0] = addJet3.Eta()
        if (not intree_.is_data):
            dict_variableName_Leaves["hadronFlavour_addJet1"][0][0] = addJet1.HadronFlavour()
            dict_variableName_Leaves["hadronFlavour_addJet2"][0][0] = addJet2.HadronFlavour()
            dict_variableName_Leaves["hadronFlavour_addJet3"][0][0] = addJet3.HadronFlavour()
            dict_variableName_Leaves["partonFlavour_addJet1"][0][0] = addJet1.PartonFlavour()
            dict_variableName_Leaves["partonFlavour_addJet2"][0][0] = addJet2.PartonFlavour()
            dict_variableName_Leaves["partonFlavour_addJet3"][0][0] = addJet3.PartonFlavour()
            #dict_variableName_Leaves["event_Category"][0][0] = cat
        else:
            dict_variableName_Leaves["hadronFlavour_addJet1"][0][0] = -999
            dict_variableName_Leaves["hadronFlavour_addJet2"][0][0] = -999
            dict_variableName_Leaves["hadronFlavour_addJet3"][0][0] = -999
            dict_variableName_Leaves["partonFlavour_addJet1"][0][0] = -999
            dict_variableName_Leaves["partonFlavour_addJet2"][0][0] = -999
            dict_variableName_Leaves["partonFlavour_addJet3"][0][0] = -999
            #dict_variableName_Leaves["event_Category"][0][0] = -999
        
        
        
        
        # c-tagger reweighting
        # if (not intree_.is_data):
#             variables_reweighting_addJet1 = [
#                 "DeepCSVcTagCvsL_addJet1",
#                 "DeepCSVcTagCvsB_addJet1",
#                 "Pt_addJet1",
#                 "hadronFlavour_addJet1",
#                 "Eta_addJet1",
#             ]
#             X_reweighting_addJet1 = np.ndarray(shape=(1,len(variables_reweighting_addJet1)), dtype=float, order='F')
#             for idx,var in enumerate(variables_reweighting_addJet1):
#                 if not "Pt_" in var: X_reweighting_addJet1[0,idx] = dict_variableName_Leaves[var][0][0]
#                 else: X_reweighting_addJet1[0,idx] = dict_variableName_Leaves[var][0][0]/1000. # Pt must be in TeV because of better range for NN
#             pred_reweighting_addJet1 = model_reweighting.predict(np.asarray(X_reweighting_addJet1))
#             dict_variableName_Leaves["DeepCSVcTagCvsL_reweight_addJet1"][0][0] = pred_reweighting_addJet1[:,0]
#             dict_variableName_Leaves["DeepCSVcTagCvsB_reweight_addJet1"][0][0] = pred_reweighting_addJet1[:,1]
#             
#             variables_reweighting_addJet2 = [
#                 "DeepCSVcTagCvsL_addJet2",
#                 "DeepCSVcTagCvsB_addJet2",
#                 "Pt_addJet2",
#                 "hadronFlavour_addJet2",
#                 "Eta_addJet2",
#             ]
#             X_reweighting_addJet2 = np.ndarray(shape=(1,len(variables_reweighting_addJet2)), dtype=float, order='F')
#             for idx,var in enumerate(variables_reweighting_addJet2):
#                 if not "Pt_" in var: X_reweighting_addJet2[0,idx] = dict_variableName_Leaves[var][0][0]
#                 else: X_reweighting_addJet2[0,idx] = dict_variableName_Leaves[var][0][0]/1000. # Pt must be in TeV because of better range for NN
#         
#             pred_reweighting_addJet2 = model_reweighting.predict(np.asarray(X_reweighting_addJet2))
#             dict_variableName_Leaves["DeepCSVcTagCvsL_reweight_addJet2"][0][0] = pred_reweighting_addJet2[:,0]
#             dict_variableName_Leaves["DeepCSVcTagCvsB_reweight_addJet2"][0][0] = pred_reweighting_addJet2[:,1]
#             
#         # for data just copy the original value 
#         else: 
#             dict_variableName_Leaves["DeepCSVcTagCvsL_reweight_addJet1"][0][0] = jclf.jets_dict_["leading_add_jet"][0].DeepCSVCvsL()
#             dict_variableName_Leaves["DeepCSVcTagCvsL_reweight_addJet2"][0][0] = jclf.jets_dict_["subleading_add_jet"][0].DeepCSVCvsL()
#             dict_variableName_Leaves["DeepCSVcTagCvsB_reweight_addJet1"][0][0] = jclf.jets_dict_["leading_add_jet"][0].DeepCSVCvsB()
#             dict_variableName_Leaves["DeepCSVcTagCvsB_reweight_addJet2"][0][0] = jclf.jets_dict_["subleading_add_jet"][0].DeepCSVCvsB()
# 
#         
        
        
        
        
        
       

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
    
    eff_histo_file.Close()
    
    
    



def main():

    parser = ArgumentParser()
    parser.add_argument('--infile', default="FILLMEPLEASE",help='path and name of input file')
    parser.add_argument('--outfile', default="*",help='path and name of output file')
    parser.add_argument('--topmatchingdir', default="FILLME",help='name of training directory')
    parser.add_argument('--tthfselectordir', default="FILLME",help='name of training directory')
    parser.add_argument('--reweightingdir', default="FILLME",help='name of training directory')
    parser.add_argument('--firstEvt', type=int, default=0,help='first event')
    parser.add_argument('--lastEvt', type=int, default=-1,help='last event')
    parser.add_argument('--splitted', type=int, default=0,help='bool for splitted or not')
    args = parser.parse_args()
    
    Analyze(args.infile, args.outfile, args.topmatchingdir, args.tthfselectordir, args.reweightingdir, args.firstEvt, args.lastEvt, bool(args.splitted))
    
    

if __name__ == "__main__":
	main()


