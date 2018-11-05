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

def Analyze(infile, outfile, IdxBegin = 0, IdxEnd = -1, Splitted = False):
    
    if not os.path.isfile(infile):
        print "ERROR: COULD NOT FIND FILE: %s!!!"%infile
        sys.exit(1)
    
    infile_ = TFile(infile)
    intree_ = infile_.Get("tree")
    
    if Splitted: ofile_ = TFile(outfile.replace(".root","_events_"+str(IdxBegin)+"_"+str(IdxEnd)+".root"),"RECREATE")
    else: ofile_ = TFile(outfile,"RECREATE")
    #otree_ = intree_.CloneTree(0)
    
    ptbins = [20,50,70,90,120,150,300,1000]
    etabins = [0,0.6,1.5,2.0,2.4]
    hist_DeepCSV_total_bjets            = ROOT.TH2D("hist_DeepCSV_total_bjets",";jet p_{T} (GeV);jet #eta",len(ptbins)-1,array("d",ptbins),len(etabins)-1,array("d",etabins))
    hist_DeepCSV_btagged_loose_bjets    = ROOT.TH2D("hist_DeepCSV_btagged_loose_bjets",";jet p_{T} (GeV);jet #eta",len(ptbins)-1,array("d",ptbins),len(etabins)-1,array("d",etabins))
    hist_DeepCSV_btagged_medium_bjets   = ROOT.TH2D("hist_DeepCSV_btagged_medium_bjets",";jet p_{T} (GeV);jet #eta",len(ptbins)-1,array("d",ptbins),len(etabins)-1,array("d",etabins))
    hist_DeepCSV_btagged_tight_bjets    = ROOT.TH2D("hist_DeepCSV_btagged_tight_bjets",";jet p_{T} (GeV);jet #eta",len(ptbins)-1,array("d",ptbins),len(etabins)-1,array("d",etabins))
    hist_DeepCSV_total_cjets            = ROOT.TH2D("hist_DeepCSV_total_cjets",";jet p_{T} (GeV);jet #eta",len(ptbins)-1,array("d",ptbins),len(etabins)-1,array("d",etabins))
    hist_DeepCSV_btagged_loose_cjets    = ROOT.TH2D("hist_DeepCSV_btagged_loose_cjets",";jet p_{T} (GeV);jet #eta",len(ptbins)-1,array("d",ptbins),len(etabins)-1,array("d",etabins))
    hist_DeepCSV_btagged_medium_cjets   = ROOT.TH2D("hist_DeepCSV_btagged_medium_cjets",";jet p_{T} (GeV);jet #eta",len(ptbins)-1,array("d",ptbins),len(etabins)-1,array("d",etabins))
    hist_DeepCSV_btagged_tight_cjets    = ROOT.TH2D("hist_DeepCSV_btagged_tight_cjets",";jet p_{T} (GeV);jet #eta",len(ptbins)-1,array("d",ptbins),len(etabins)-1,array("d",etabins))
    hist_DeepCSV_total_ljets            = ROOT.TH2D("hist_DeepCSV_total_ljets",";jet p_{T} (GeV);jet #eta",len(ptbins)-1,array("d",ptbins),len(etabins)-1,array("d",etabins))
    hist_DeepCSV_btagged_loose_ljets    = ROOT.TH2D("hist_DeepCSV_btagged_loose_ljets",";jet p_{T} (GeV);jet #eta",len(ptbins)-1,array("d",ptbins),len(etabins)-1,array("d",etabins))
    hist_DeepCSV_btagged_medium_ljets   = ROOT.TH2D("hist_DeepCSV_btagged_medium_ljets",";jet p_{T} (GeV);jet #eta",len(ptbins)-1,array("d",ptbins),len(etabins)-1,array("d",etabins))
    hist_DeepCSV_btagged_tight_ljets    = ROOT.TH2D("hist_DeepCSV_btagged_tight_ljets",";jet p_{T} (GeV);jet #eta",len(ptbins)-1,array("d",ptbins),len(etabins)-1,array("d",etabins))
    
    # Uncomment this if you want to disable saving all the original collections (Drastically reduces size by a factor of ~ 3)
    # otree_.SetBranchStatus("Truth",0)
#     otree_.SetBranchStatus("GenTTXJets",0)
#     otree_.SetBranchStatus("Jets",0)
#     otree_.SetBranchStatus("Muons",0)
#     otree_.SetBranchStatus("Electrons",0)
#     otree_.SetBranchStatus("Trigger",0)
#     otree_.SetBranchStatus("MET",0)
    
    # **************************** add extra branches to output****************************
    # dict_variableName_Leaves = {}
#     dict_variableName_Leaves.update({"Pt_lepton": [array('d', [0]),"D"]})
#     dict_variableName_Leaves.update({"Eta_lepton": [array('d', [0]),"D"]})
#     dict_variableName_Leaves.update({"hadronFlavour_addJet1": [array('i', [0]),"I"]})
#     dict_variableName_Leaves.update({"hadronFlavour_addJet2": [array('i', [0]),"I"]})
#     dict_variableName_Leaves.update({"hadronFlavour_addJet3": [array('i', [0]),"I"]})
#     dict_variableName_Leaves.update({"partonFlavour_addJet1": [array('i', [0]),"I"]})
#     dict_variableName_Leaves.update({"partonFlavour_addJet2": [array('i', [0]),"I"]})
#     dict_variableName_Leaves.update({"partonFlavour_addJet3": [array('i', [0]),"I"]})
#     dict_variableName_Leaves.update({"Pt_addJet1": [array('d', [0]),"D"]})
#     dict_variableName_Leaves.update({"Pt_addJet2": [array('d', [0]),"D"]})
#     dict_variableName_Leaves.update({"Pt_addJet3": [array('d', [0]),"D"]})
#     dict_variableName_Leaves.update({"Eta_addJet1": [array('d', [0]),"D"]})
#     dict_variableName_Leaves.update({"Eta_addJet2": [array('d', [0]),"D"]})
#     dict_variableName_Leaves.update({"Eta_addJet3": [array('d', [0]),"D"]})
#     dict_variableName_Leaves.update({"DeepCSVBDiscr_addJet1": [array('d', [0]),"D"]})
#     dict_variableName_Leaves.update({"DeepCSVBDiscr_addJet2": [array('d', [0]),"D"]})
#     dict_variableName_Leaves.update({"DeepCSVBDiscr_addJet3": [array('d', [0]),"D"]})
#     dict_variableName_Leaves.update({"cTagCvsL_addJet1": [array('d', [0]),"D"]})
#     dict_variableName_Leaves.update({"cTagCvsL_addJet2": [array('d', [0]),"D"]})
#     dict_variableName_Leaves.update({"cTagCvsL_addJet3": [array('d', [0]),"D"]})
#     dict_variableName_Leaves.update({"cTagCvsB_addJet1": [array('d', [0]),"D"]})
#     dict_variableName_Leaves.update({"cTagCvsB_addJet2": [array('d', [0]),"D"]})
#     dict_variableName_Leaves.update({"cTagCvsB_addJet3": [array('d', [0]),"D"]})
#     dict_variableName_Leaves.update({"DeepCSVcTagCvsL_addJet1": [array('d', [0]),"D"]})
#     dict_variableName_Leaves.update({"DeepCSVcTagCvsL_addJet2": [array('d', [0]),"D"]})
#     dict_variableName_Leaves.update({"DeepCSVcTagCvsL_addJet3": [array('d', [0]),"D"]})
#     dict_variableName_Leaves.update({"DeepCSVcTagCvsB_addJet1": [array('d', [0]),"D"]})
#     dict_variableName_Leaves.update({"DeepCSVcTagCvsB_addJet2": [array('d', [0]),"D"]})
#     dict_variableName_Leaves.update({"DeepCSVcTagCvsB_addJet3": [array('d', [0]),"D"]})
#     dict_variableName_Leaves.update({"DeepFlavourcTagCvsL_addJet1": [array('d', [0]),"D"]})
#     dict_variableName_Leaves.update({"DeepFlavourcTagCvsL_addJet2": [array('d', [0]),"D"]})
#     dict_variableName_Leaves.update({"DeepFlavourcTagCvsL_addJet3": [array('d', [0]),"D"]})
#     dict_variableName_Leaves.update({"DeepFlavourcTagCvsB_addJet1": [array('d', [0]),"D"]})
#     dict_variableName_Leaves.update({"DeepFlavourcTagCvsB_addJet2": [array('d', [0]),"D"]})
#     dict_variableName_Leaves.update({"DeepFlavourcTagCvsB_addJet3": [array('d', [0]),"D"]})
#     dict_variableName_Leaves.update({"n_cTagger_L_ctagged": [array('i', [0]),"I"]})
#     dict_variableName_Leaves.update({"n_cTagger_M_ctagged": [array('i', [0]),"I"]})
#     dict_variableName_Leaves.update({"n_cTagger_T_ctagged": [array('i', [0]),"I"]})
# #     dict_variableName_Leaves.update({"n_cTagger_L_Additional_ctagged": [array('i', [0]),"I"]})
# #     dict_variableName_Leaves.update({"n_cTagger_M_Additional_ctagged": [array('i', [0]),"I"]})
# #     dict_variableName_Leaves.update({"n_cTagger_T_Additional_ctagged": [array('i', [0]),"I"]})
#     dict_variableName_Leaves.update({"n_DeepCSVBDiscr_L_btagged": [array('i', [0]),"I"]})
#     dict_variableName_Leaves.update({"n_DeepCSVBDiscr_M_btagged": [array('i', [0]),"I"]})
#     dict_variableName_Leaves.update({"n_DeepCSVBDiscr_T_btagged": [array('i', [0]),"I"]})
#     dict_variableName_Leaves.update({"n_DeepCSVcTagger_L_ctagged": [array('i', [0]),"I"]})
#     dict_variableName_Leaves.update({"n_DeepCSVcTagger_M_ctagged": [array('i', [0]),"I"]})
#     dict_variableName_Leaves.update({"n_DeepCSVcTagger_T_ctagged": [array('i', [0]),"I"]})
# #     dict_variableName_Leaves.update({"n_DeepCSVcTagger_L_Additional_ctagged": [array('i', [0]),"I"]})
# #     dict_variableName_Leaves.update({"n_DeepCSVcTagger_M_Additional_ctagged": [array('i', [0]),"I"]})
# #     dict_variableName_Leaves.update({"n_DeepCSVcTagger_T_Additional_ctagged": [array('i', [0]),"I"]})
#     dict_variableName_Leaves.update({"lepton_Category": [array('i', [0]),"I"]}) # 0 = elel, 1 = mumu, 2 = elmu
#     #weights
#     dict_variableName_Leaves.update({"weight_btag_iterativefit": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_btag_iterativefit_JesUp": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_btag_iterativefit_JesDown": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_btag_iterativefit_LfUp": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_btag_iterativefit_LfDown": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_btag_iterativefit_HfUp": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_btag_iterativefit_HfDown": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_btag_iterativefit_Hfstats1Up": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_btag_iterativefit_Hfstats1Down": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_btag_iterativefit_Hfstats2Up": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_btag_iterativefit_Hfstats2Down": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_btag_iterativefit_Lfstats1Up": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_btag_iterativefit_Lfstats1Down": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_btag_iterativefit_Lfstats2Up": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_btag_iterativefit_Lfstats2Down": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_btag_iterativefit_Cferr1Up": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_btag_iterativefit_Cferr1Down": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_btag_iterativefit_Cferr2Up": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_btag_iterativefit_Cferr2Down": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_btag_DeepCSVLoose": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_btag_DeepCSVLooseUp": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_btag_DeepCSVLooseDown": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_btag_DeepCSVMedium": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_btag_DeepCSVMediumUp": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_btag_DeepCSVMediumDown": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_btag_DeepCSVTight": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_btag_DeepCSVTightUp": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_btag_DeepCSVTightDown": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_electron_id": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_electron_reco": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_electron_trig": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_muon_id": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_muon_iso": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_muon_trig": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_electron_id_Up": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_electron_reco_Up": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_electron_trig_Up": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_muon_id_Up": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_muon_iso_Up": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_muon_trig_Up": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_electron_id_Down": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_electron_reco_Down": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_electron_trig_Down": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_muon_id_Down": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_muon_iso_Down": [array('d', [1]),"D"]})
#     dict_variableName_Leaves.update({"weight_muon_trig_Down": [array('d', [1]),"D"]})

#     
    
    # for name,arr in dict_variableName_Leaves.iteritems():
#         otree_.Branch(name,arr[0],name+"/"+arr[1])
    
    
    # for amcatnlo I need to normalize the scale variations to inital weight!
    # intree_.GetEntry(1)
#     if (not intree_.is_data):
#         buffer_weight_scale_muF0p5 = array('f', [1])
#         buffer_weight_scale_muF2 = array('f', [1])
#         buffer_weight_scale_muR0p5 = array('f', [1])
#         buffer_weight_scale_muR2 = array('f', [1])
# 
#         otree_.SetBranchAddress("weight_scale_muF0p5",buffer_weight_scale_muF0p5)
#         otree_.SetBranchAddress("weight_scale_muF2",buffer_weight_scale_muF2)
#         otree_.SetBranchAddress("weight_scale_muR0p5",buffer_weight_scale_muR0p5)
#         otree_.SetBranchAddress("weight_scale_muR2",buffer_weight_scale_muR2)
    
    # v_validjets_ = ROOT.std.vector( Jet )()
#     otree_.Branch("ValidJets",v_validjets_);
    #****************************************************************************************
    
    #**************************** Load the top matching training ****************************
   #  model = load_model(topmatchingdir+"/model_checkpoint_save.hdf5")
#     scaler = pickle.load(open(topmatchingdir+"/scaler.pkl","rb"))
#     input_variables = pickle.load(open(topmatchingdir+"/variables.pkl","rb"))
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
     #    if (not intree_.is_data):
#             if abs(intree_.mc_weight_originalValue) > 1: 
#                 buffer_weight_scale_muF0p5[0] = intree_.weight_scale_muF0p5/abs(intree_.mc_weight_originalValue)
#                 buffer_weight_scale_muF2[0] = intree_.weight_scale_muF2/abs(intree_.mc_weight_originalValue)
#                 buffer_weight_scale_muR0p5[0] = intree_.weight_scale_muR0p5/abs(intree_.mc_weight_originalValue)
#                 buffer_weight_scale_muR2[0] = intree_.weight_scale_muR2/abs(intree_.mc_weight_originalValue)
#         # ****************************************************************************************************************
#         
        
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

  
        
        
        # start the classification / assignment of the jets
        jclf = JetsClassifier(v_jet)
        jclf.Clean(leading_lepton[0],leading_lepton[0])
        
        if len(jclf.validJets()) < 4: continue
        validjets = jclf.validJets()
        
        if (not intree_.is_data):
            for jet_tmp in jclf.validJets():
                flav = jet_tmp.HadronFlavour()
                pt = jet_tmp.Pt()
                abseta = abs(jet_tmp.Eta())
                if flav == 5:
                    hist_DeepCSV_total_bjets.Fill(pt,abseta)
                    if isDeepCSVBDiscrL(jet_tmp): hist_DeepCSV_btagged_loose_bjets.Fill(pt,abseta)
                    if isDeepCSVBDiscrM(jet_tmp): hist_DeepCSV_btagged_medium_bjets.Fill(pt,abseta)
                    if isDeepCSVBDiscrT(jet_tmp): hist_DeepCSV_btagged_tight_bjets.Fill(pt,abseta)
                elif flav == 4:
                    hist_DeepCSV_total_cjets.Fill(pt,abseta)
                    if isDeepCSVBDiscrL(jet_tmp): hist_DeepCSV_btagged_loose_cjets.Fill(pt,abseta)
                    if isDeepCSVBDiscrM(jet_tmp): hist_DeepCSV_btagged_medium_cjets.Fill(pt,abseta)
                    if isDeepCSVBDiscrT(jet_tmp): hist_DeepCSV_btagged_tight_cjets.Fill(pt,abseta)
                elif flav == 0:
                    hist_DeepCSV_total_ljets.Fill(pt,abseta)
                    if isDeepCSVBDiscrL(jet_tmp): hist_DeepCSV_btagged_loose_ljets.Fill(pt,abseta)
                    if isDeepCSVBDiscrM(jet_tmp): hist_DeepCSV_btagged_medium_ljets.Fill(pt,abseta)
                    if isDeepCSVBDiscrT(jet_tmp): hist_DeepCSV_btagged_tight_ljets.Fill(pt,abseta)


        
        
        
       

        #otree_.Fill()

        v_el.clear()
        v_mu.clear()
        v_jet.clear()
        v_truth.clear()
        v_trig.clear()
        
        #v_validjets_.clear()
        
    # ***************** end of  event loop ********************
    
    #print "%s: Selected %i/%i (%.3f%%) of events"%(infile.split("/")[-1],otree_.GetEntries(),actual_nentries,100*float(otree_.GetEntries())/float(actual_nentries))
    
   #  hcount = infile_.Get("hcount")
#     hweight = infile_.Get("hweight")
#     
    # if (actual_nentries < original_nentries):
#         hcount.SetBinContent(1,actual_nentries*hcount.GetBinContent(1)/(float(original_nentries)))
#         hweight.SetBinContent(1,actual_nentries*hweight.GetBinContent(1)/(float(original_nentries)))
#     
    
    # ofile_.cd()
#     hcount.Write()
#     hweight.Write()
#     otree_.Write()
    
    hist_DeepCSV_total_bjets.Write()       
    hist_DeepCSV_btagged_loose_bjets.Write()     
    hist_DeepCSV_btagged_medium_bjets.Write()    
    hist_DeepCSV_btagged_tight_bjets.Write()     
    hist_DeepCSV_total_cjets.Write()             
    hist_DeepCSV_btagged_loose_cjets.Write()     
    hist_DeepCSV_btagged_medium_cjets.Write()    
    hist_DeepCSV_btagged_tight_cjets.Write()     
    hist_DeepCSV_total_ljets.Write()             
    hist_DeepCSV_btagged_loose_ljets.Write()     
    hist_DeepCSV_btagged_medium_ljets.Write()    
    hist_DeepCSV_btagged_tight_ljets.Write()     

    
    ofile_.Close()
    infile_.Close()
    
    
    
    
    



def main():

    parser = ArgumentParser()
    parser.add_argument('--infile', default="FILLMEPLEASE",help='path and name of input file')
    parser.add_argument('--outfile', default="*",help='path and name of output file')
    parser.add_argument('--firstEvt', type=int, default=0,help='first event')
    parser.add_argument('--lastEvt', type=int, default=-1,help='last event')
    parser.add_argument('--splitted', type=int, default=0,help='bool for splitted or not')
    args = parser.parse_args()
    
    Analyze(args.infile, args.outfile, args.firstEvt, args.lastEvt, bool(args.splitted))
    
    

if __name__ == "__main__":
	main()


