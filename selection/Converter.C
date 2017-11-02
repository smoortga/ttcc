#include "Converter.h"
//
// This converter assumes a FlatTree
// as produced by https://github.com/smoortga/FlatTree
//

Converter::Converter(TTree* intree, TTree* outtree, bool saveElectrons, bool saveMuons, bool saveJets, bool saveMET, int nen)
{
    assert(intree);
    assert(outtree);
    itree_ = intree;
    otree_ = outtree;
    
    saveElectrons_ = saveElectrons;
    saveMuons_ = saveMuons;
    saveJets_ = saveJets;
    saveMET_ = saveMET;
    
    if (nen<0 || nen>itree_->GetEntries()){nen_ = itree_->GetEntries();}
    else{nen_ = nen;}
    
    // initialize a vector with all the available branch names in the input tree
    branchnames_.clear();
    TObjArray* branchlist = (TObjArray*)itree_->GetListOfBranches();
    for (Int_t i = 0; i < branchlist->GetEntries(); i++){
        branchnames_.push_back(branchlist->At(i)->GetName());
    }
}

Converter::~Converter()
{
}

bool Converter::EXISTS(TString br)
{
    if (std::find(branchnames_.begin(),branchnames_.end(), br) != branchnames_.end()) return true;
    else return false;
}

void Converter::Convert()
{

    std::cout << "Converting " << nen_ << " events from FlatTree To ObjectOriented Tree" << std::endl;
    
    
    // **************************************************************
    // ******************* Initialize Event-based *******************
    // **************************************************************
    if ( EXISTS("ev_run") )                         itree_->SetBranchAddress("ev_run",&ev_run_); 
    if ( EXISTS("ev_id") )                          itree_->SetBranchAddress("ev_id",&ev_id_);
    if ( EXISTS("ev_lumi") )                        itree_->SetBranchAddress("ev_lumi",&ev_lumi_);
    if ( EXISTS("mc_weight") )                      itree_->SetBranchAddress("mc_weight",&mc_weight_);
    if ( EXISTS("nvertex") )                        itree_->SetBranchAddress("nvertex",&nvertex_);
    if ( EXISTS("pv_x") )                           itree_->SetBranchAddress("pv_x",&pv_x_);
    if ( EXISTS("pv_y") )                           itree_->SetBranchAddress("pv_y",&pv_y_);
    if ( EXISTS("pv_z") )                           itree_->SetBranchAddress("pv_z",&pv_z_);
    if ( EXISTS("pv_xError") )                      itree_->SetBranchAddress("pv_xError",&pv_xError_);
    if ( EXISTS("pv_yError") )                      itree_->SetBranchAddress("pv_yError",&pv_yError_);
    if ( EXISTS("pv_zError") )                      itree_->SetBranchAddress("pv_zError",&pv_zError_);
    if ( EXISTS("pv_ndof") )                        itree_->SetBranchAddress("pv_ndof",&pv_ndof_);
    if ( EXISTS("pv_chi2") )                        itree_->SetBranchAddress("pv_chi2",&pv_chi2_);
    if ( EXISTS("pv_rho") )                         itree_->SetBranchAddress("pv_rho",&pv_rho_);
    if ( EXISTS("pv_isFake") )                      itree_->SetBranchAddress("pv_isFake",&pv_isFake_);
    otree_->Branch("ev_run",&ev_run_); 
    otree_->Branch("ev_id",&ev_id_);
    otree_->Branch("ev_lumi",&ev_lumi_);
    otree_->Branch("mc_weight",&mc_weight_);
    otree_->Branch("nvertex",&nvertex_);
    otree_->Branch("pv_x",&pv_x_);
    otree_->Branch("pv_y",&pv_y_);
    otree_->Branch("pv_z",&pv_z_);
    otree_->Branch("pv_xError",&pv_xError_);
    otree_->Branch("pv_yError",&pv_yError_);
    otree_->Branch("pv_zError",&pv_zError_);
    otree_->Branch("pv_ndof",&pv_ndof_);
    otree_->Branch("pv_chi2",&pv_chi2_);
    otree_->Branch("pv_rho",&pv_rho_);
    otree_->Branch("pv_isFake",&pv_isFake_);

    // **************************************************************
    
    // **************************************************************
    // ******************* Initialize Trigger ***********************
    // **************************************************************
    v_trig_ = std::vector<Trigger*>();
    otree_->Branch("Trigger",&v_trig_);
    
    if ( EXISTS("trigger_n") )                      itree_->SetBranchAddress("trigger_n",&trigger_n_); 
    if ( EXISTS("trigger") )                        itree_->SetBranchAddress("trigger",&trigger_); 
    if ( EXISTS("trigger_name") )                   itree_->SetBranchAddress("trigger_name",&trigger_name_); 
    if ( EXISTS("trigger_pass") )                   itree_->SetBranchAddress("trigger_pass",&trigger_pass_);
    if ( EXISTS("trigger_prescale") )               itree_->SetBranchAddress("trigger_prescale",&trigger_prescale_);    
    if ( EXISTS("trigger_HLTprescale") )            itree_->SetBranchAddress("trigger_HLTprescale",&trigger_HLTprescale_);
    if ( EXISTS("trigger_L1prescale") )             itree_->SetBranchAddress("trigger_L1prescale",&trigger_L1prescale_); 
    // **************************************************************
    
    
    // **************************************************************
    // ******************* Initialize MET ***************************
    // **************************************************************
    if (saveMET_){
        v_met_ = std::vector<MissingEnergy*>();
        otree_->Branch("MET",&v_met_);
        
        if ( EXISTS("met_sumet") )                      itree_->SetBranchAddress("met_sumet",&met_sumet_); 
        if ( EXISTS("met_pt") )                         itree_->SetBranchAddress("met_pt",&met_pt_); 
        if ( EXISTS("met_px") )                         itree_->SetBranchAddress("met_px",&met_px_);
        if ( EXISTS("met_py") )                         itree_->SetBranchAddress("met_py",&met_py_);    
        if ( EXISTS("met_phi") )                        itree_->SetBranchAddress("met_phi",&met_phi_); 
        if ( EXISTS("met_sig") )                        itree_->SetBranchAddress("met_sig",&met_sig_);  
    }
    // **************************************************************
    
    // **************************************************************
    // ******************* Initialize Electrons *********************
    // **************************************************************
    if (saveElectrons_){
        v_el_ = std::vector<Electron*>();
        otree_->Branch("Electrons",&v_el_);
    
        if ( EXISTS("el_n") )                           itree_->SetBranchAddress("el_n",&el_n_);
        if ( EXISTS("el_pt") )                          itree_->SetBranchAddress("el_pt",&el_pt_);
        if ( EXISTS("el_eta") )                         itree_->SetBranchAddress("el_eta",&el_eta_);
        if ( EXISTS("el_superCluster_eta") )            itree_->SetBranchAddress("el_superCluster_eta",&el_scleta_);
        if ( EXISTS("el_phi") )                         itree_->SetBranchAddress("el_phi",&el_phi_);
        if ( EXISTS("el_charge") )                      itree_->SetBranchAddress("el_charge",&el_charge_);
        if ( EXISTS("el_id") )                          itree_->SetBranchAddress("el_id",&el_id_);
        if ( EXISTS("el_m") )                           itree_->SetBranchAddress("el_m",&el_m_);
        if ( EXISTS("el_E") )                           itree_->SetBranchAddress("el_E",&el_E_);
        if ( EXISTS("el_gsfTrack_PV_dxy") )             itree_->SetBranchAddress("el_gsfTrack_PV_dxy",&el_dxy_);
        if ( EXISTS("el_gsfTrack_PV_dz") )              itree_->SetBranchAddress("el_gsfTrack_PV_dz",&el_dz_);
        if ( EXISTS("el_pfIso_sumChargedHadronPt") )    itree_->SetBranchAddress("el_pfIso_sumChargedHadronPt",&el_pfIso_sumChargedHadronPt_);
        if ( EXISTS("el_pfIso_sumNeutralHadronEt") )    itree_->SetBranchAddress("el_pfIso_sumNeutralHadronEt",&el_pfIso_sumNeutralHadronEt_);
        if ( EXISTS("el_pfIso_sumPhotonEt") )           itree_->SetBranchAddress("el_pfIso_sumPhotonEt",&el_pfIso_sumPhotonEt_);
        if ( EXISTS("el_looseCBId") )                   itree_->SetBranchAddress("el_looseCBId",&el_looseCBId_);
        if ( EXISTS("el_mediumCBId") )                  itree_->SetBranchAddress("el_mediumCBId",&el_mediumCBId_);
        if ( EXISTS("el_tightCBId") )                   itree_->SetBranchAddress("el_tightCBId",&el_tightCBId_);
    }
    // **************************************************************
    
    // **************************************************************
    // ******************* Initialize Muons *************************
    // **************************************************************
    if (saveMuons_){
        v_mu_ = std::vector<Muon*>();
        otree_->Branch("Muons",&v_mu_);
    
        if ( EXISTS("mu_n") )                           itree_->SetBranchAddress("mu_n",&mu_n_);
        if ( EXISTS("mu_pt") )                          itree_->SetBranchAddress("mu_pt",&mu_pt_);
        if ( EXISTS("mu_eta") )                         itree_->SetBranchAddress("mu_eta",&mu_eta_);
        if ( EXISTS("mu_phi") )                         itree_->SetBranchAddress("mu_phi",&mu_phi_);
        if ( EXISTS("mu_charge") )                      itree_->SetBranchAddress("mu_charge",&mu_charge_);
        if ( EXISTS("mu_id") )                          itree_->SetBranchAddress("mu_id",&mu_id_);
        if ( EXISTS("mu_m") )                           itree_->SetBranchAddress("mu_m",&mu_m_);
        if ( EXISTS("mu_E") )                           itree_->SetBranchAddress("mu_E",&mu_E_);
        if ( EXISTS("mu_innerTrack_PV_dxy") )           itree_->SetBranchAddress("mu_innerTrack_PV_dxy",&mu_dxy_);
        if ( EXISTS("mu_innerTrack_PV_dz") )            itree_->SetBranchAddress("mu_innerTrack_PV_dz",&mu_dz_);
        if ( EXISTS("mu_pfIso04_sumChargedHadronPt") )  itree_->SetBranchAddress("mu_pfIso04_sumChargedHadronPt",&mu_pfIso_sumChargedHadronPt_);
        if ( EXISTS("mu_pfIso04_sumNeutralHadronEt") )  itree_->SetBranchAddress("mu_pfIso04_sumNeutralHadronEt",&mu_pfIso_sumNeutralHadronEt_);
        if ( EXISTS("mu_pfIso04_sumPhotonEt") )         itree_->SetBranchAddress("mu_pfIso04_sumPhotonEt",&mu_pfIso_sumPhotonEt_);
        if ( EXISTS("mu_pfIso04_sumPUPt") )             itree_->SetBranchAddress("mu_pfIso04_sumPUPt",&mu_pfIso_sumPUPt_);
        if ( EXISTS("mu_isLooseMuon") )                 itree_->SetBranchAddress("mu_isLooseMuon",&mu_isLooseID_);
        if ( EXISTS("mu_isTightMuon") )                 itree_->SetBranchAddress("mu_isTightMuon",&mu_isTightID_);
    }
    // **************************************************************
    
    // **************************************************************
    // ******************* Initialize Jets *********************
    // **************************************************************
    if (saveJets_){
        v_jet_ = std::vector<Jet*>();
        otree_->Branch("Jets",&v_jet_);
    
        if ( EXISTS("jet_n") )                  itree_->SetBranchAddress("jet_n",&jet_n_);
        if ( EXISTS("jet_pt") )                 itree_->SetBranchAddress("jet_pt",&jet_pt_);
        if ( EXISTS("jet_eta") )                itree_->SetBranchAddress("jet_eta",&jet_eta_);
        if ( EXISTS("jet_phi") )                itree_->SetBranchAddress("jet_phi",&jet_phi_);
        if ( EXISTS("jet_m") )                  itree_->SetBranchAddress("jet_m",&jet_m_);
        if ( EXISTS("jet_E") )                  itree_->SetBranchAddress("jet_E",&jet_E_);
        if ( EXISTS("jet_charge") )             itree_->SetBranchAddress("jet_charge",&jet_charge_);
        if ( EXISTS("jet_chargeVec") )          itree_->SetBranchAddress("jet_chargeVec",&jet_chargeVec_);
        if ( EXISTS("jet_looseJetID") )         itree_->SetBranchAddress("jet_looseJetID",&jet_isLooseJetID_);
        if ( EXISTS("jet_tightJetID") )         itree_->SetBranchAddress("jet_tightJetID",&jet_isTightJetID_);
        if ( EXISTS("jet_hadronFlavour") )      itree_->SetBranchAddress("jet_hadronFlavour",&jet_hadronFlavour_);
        if ( EXISTS("jet_partonFlavour") )      itree_->SetBranchAddress("jet_partonFlavour",&jet_partonFlavour_);
        if ( EXISTS("jet_CSVv2") )              itree_->SetBranchAddress("jet_CSVv2", &jet_CSVv2_);        
        if ( EXISTS("jet_cMVAv2") )             itree_->SetBranchAddress("jet_cMVAv2", &jet_cMVAv2_);      
        if ( EXISTS("jet_CharmCvsL") )          itree_->SetBranchAddress("jet_CharmCvsL", &jet_CTagCvsL_);      
        if ( EXISTS("jet_CharmCvsB") )          itree_->SetBranchAddress("jet_CharmCvsB", &jet_CTagCvsB_);      
        if ( EXISTS("jet_DeepCSVBDiscr") )      itree_->SetBranchAddress("jet_DeepCSVBDiscr", &jet_DeepCSVBDiscr_);  
        if ( EXISTS("jet_DeepCSVCvsL") )        itree_->SetBranchAddress("jet_DeepCSVCvsL", &jet_DeepCSVCvsL_);    
        if ( EXISTS("jet_DeepCSVCvsB") )        itree_->SetBranchAddress("jet_DeepCSVCvsB", &jet_DeepCSVCvsB_);    
        if ( EXISTS("jet_DeepFlavourBDiscr") )  itree_->SetBranchAddress("jet_DeepFlavourBDiscr", &jet_DeepFlavourBDiscr_); 
        if ( EXISTS("jet_DeepFlavourCvsL") )    itree_->SetBranchAddress("jet_DeepFlavourCvsL", &jet_DeepFlavourCvsL_); 
        if ( EXISTS("jet_DeepFlavourCvsB") )    itree_->SetBranchAddress("jet_DeepFlavourCvsB", &jet_DeepFlavourCvsB_);
        if ( EXISTS("jet_hasGenJet") )          itree_->SetBranchAddress("jet_hasGenJet"    , &jet_HasGenJet_);
        if ( EXISTS("jet_genJet_pt") )          itree_->SetBranchAddress("jet_genJet_pt"    , &jet_genJetPt_);
        if ( EXISTS("jet_genJet_eta") )         itree_->SetBranchAddress("jet_genJet_eta"   , &jet_genJetEta_);
        if ( EXISTS("jet_genJet_phi") )         itree_->SetBranchAddress("jet_genJet_phi"   , &jet_genJetPhi_); 
        if ( EXISTS("jet_genJet_E") )           itree_->SetBranchAddress("jet_genJet_E"     , &jet_genJetE_); 
        if ( EXISTS("jet_genJet_m") )           itree_->SetBranchAddress("jet_genJet_m"     , &jet_genJetM_);  
        if ( EXISTS("jet_genJet_status") )      itree_->SetBranchAddress("jet_genJet_status", &jet_genJetStatus_);
        if ( EXISTS("jet_genJet_id") )          itree_->SetBranchAddress("jet_genJet_id"    , &jet_genJetID_);
        if ( EXISTS("jet_hasGenParton") )          itree_->SetBranchAddress("jet_hasGenParton"    , &jet_HasGenParton_);
        if ( EXISTS("jet_genParton_pt") )          itree_->SetBranchAddress("jet_genParton_pt"    , &jet_genPartonPt_);
        if ( EXISTS("jet_genParton_eta") )         itree_->SetBranchAddress("jet_genParton_eta"   , &jet_genPartonEta_);
        if ( EXISTS("jet_genParton_phi") )         itree_->SetBranchAddress("jet_genParton_phi"   , &jet_genPartonPhi_); 
        if ( EXISTS("jet_genParton_E") )           itree_->SetBranchAddress("jet_genParton_E"     , &jet_genPartonE_); 
        if ( EXISTS("jet_genParton_m") )           itree_->SetBranchAddress("jet_genParton_m"     , &jet_genPartonM_);  
        if ( EXISTS("jet_genParton_status") )      itree_->SetBranchAddress("jet_genParton_status", &jet_genPartonStatus_);
        if ( EXISTS("jet_genParton_id") )          itree_->SetBranchAddress("jet_genParton_id"    , &jet_genPartonID_);
  

        
    }
    // **************************************************************
    
    
    
    
    
    
    
    // ******************* Start Event Loop **********************
    for (Int_t iEvt = 0; iEvt < nen_; iEvt++){
    
        if (iEvt % (Int_t)round(nen_/10.) == 0){std::cout << "Processing event " << iEvt << "/" << nen_ << " (" << round(100.*iEvt/(float)nen_) << " %)" << std::endl;} //
        itree_->GetEntry(iEvt);
        
        
        // **************************************************************
        // ******************* Start Trigger ****************************
        // **************************************************************
        trigger_n_ = trigger_name_->size(); // the trigger_n_ variable is not properly filled... needs to be fixed --> https://github.com/kskovpen/FlatTree/blob/master/FlatTreeProducer/plugins/FlatTreeProducer.cc#L628-L672
        for (int iTrig = 0;  iTrig < trigger_n_; iTrig++){
            trig_ = new Trigger();
        
            if ( EXISTS("trigger") )                        trig_->setIdx(trigger_->at(iTrig)); 
            if ( EXISTS("trigger_name") )                   trig_->setName(trigger_name_->at(iTrig)); 
            if ( EXISTS("trigger_pass") )                   trig_->setPass(trigger_pass_->at(iTrig));
            if ( EXISTS("trigger_prescale") )               trig_->setPrescale(trigger_prescale_->at(iTrig));    
            if ( EXISTS("trigger_HLTprescale") )            trig_->setHLTprescale(trigger_HLTprescale_->at(iTrig)); 
            if ( EXISTS("trigger_L1prescale") )             trig_->setL1prescale(trigger_L1prescale_->at(iTrig)); 
        
            v_trig_.push_back(trig_);
        }
        // ******************* End Trigger **********************
        
        // **************************************************************
        // ******************* Start MET ********************************
        // **************************************************************
        if (saveMET_){
            met_ = new MissingEnergy();
            
            if ( EXISTS("met_sumet") )                      met_->setET(met_sumet_); 
            if ( EXISTS("met_pt") )                         met_->setPt(met_pt_); 
            if ( EXISTS("met_px") )                         met_->setPx(met_px_);
            if ( EXISTS("met_py") )                         met_->setPy(met_py_);    
            if ( EXISTS("met_phi") )                        met_->setPhi(met_phi_); 
            if ( EXISTS("met_sig") )                        met_->setSig(met_sig_); 
            
            v_met_.push_back(met_);
        }
        // ******************* End MET **********************
        
        // **************************************************************
        // ******************* Start Electron Loop **********************
        // **************************************************************
        if (saveElectrons_){
            for (int iElec = 0;  iElec < el_n_; iElec++){
                elec_ = new Electron();
                if ( EXISTS("el_pt") )                          elec_->setPt(el_pt_->at(iElec));
                if ( EXISTS("el_eta") )                         elec_->setEta(el_eta_->at(iElec)); 
                if ( EXISTS("el_phi") )                         elec_->setPhi(el_phi_->at(iElec)); 
                if ( EXISTS("el_charge") )                      elec_->setCharge(el_charge_->at(iElec));
                if ( EXISTS("el_E") )                           elec_->setE(el_E_->at(iElec));
                if ( EXISTS("el_superCluster_eta") )            elec_->setScleta(el_scleta_->at(iElec));
                if ( EXISTS("el_gsfTrack_PV_dxy") )             elec_->setDxy(el_dxy_->at(iElec));
                if ( EXISTS("el_gsfTrack_PV_dz") )              elec_->setDz(el_dz_->at(iElec));
                if ( EXISTS("el_m") )                           elec_->setM(el_m_->at(iElec));
                if ( EXISTS("el_id") )                          elec_->setId(el_id_->at(iElec));
                if ( EXISTS("el_looseCBId") )                   elec_->setIsLooseCBId(el_looseCBId_->at(iElec));
                if ( EXISTS("el_mediumCBId") )                  elec_->setIsMediumCBId(el_mediumCBId_->at(iElec));
                if ( EXISTS("el_tightCBId") )                   elec_->setIsTightCBId(el_tightCBId_->at(iElec));
                
                elec_->setRelIso(el_pfIso_sumChargedHadronPt_->at(iElec),el_pfIso_sumNeutralHadronEt_->at(iElec),el_pfIso_sumPhotonEt_->at(iElec));
                elec_->setp4();
                elec_->setIsLoose();
                elec_->setIsTight();
        
                v_el_.push_back(elec_);
            }
        }
        // ******************* End Electron Loop **********************
        
        // **************************************************************
        // ******************* Start Muon Loop **********************
        // **************************************************************
        if (saveMuons_){
            for (int iMuon = 0;  iMuon < mu_n_; iMuon++){
                muon_ = new Muon();
                if ( EXISTS("mu_pt") )                          muon_->setPt(mu_pt_->at(iMuon));
                if ( EXISTS("mu_eta") )                         muon_->setEta(mu_eta_->at(iMuon)); 
                if ( EXISTS("mu_phi") )                         muon_->setPhi(mu_phi_->at(iMuon)); 
                if ( EXISTS("mu_charge") )                      muon_->setCharge(mu_charge_->at(iMuon));
                if ( EXISTS("mu_id") )                          muon_->setId(mu_id_->at(iMuon));
                if ( EXISTS("mu_m") )                           muon_->setM(mu_m_->at(iMuon));
                if ( EXISTS("mu_E") )                           muon_->setE(mu_E_->at(iMuon));
                if ( EXISTS("mu_innerTrack_PV_dxy") )           muon_->setDxy(mu_dxy_->at(iMuon));
                if ( EXISTS("mu_innerTrack_PV_dz") )            muon_->setDz(mu_dz_->at(iMuon));
                if ( EXISTS("mu_isLooseMuon") )                 muon_->setIsLooseID(mu_isLooseID_->at(iMuon));
                if ( EXISTS("mu_isTightMuon") )                 muon_->setIsTightID(mu_isTightID_->at(iMuon));
                
                muon_->setRelIso(mu_pfIso_sumChargedHadronPt_->at(iMuon),mu_pfIso_sumNeutralHadronEt_->at(iMuon),mu_pfIso_sumPhotonEt_->at(iMuon), mu_pfIso_sumPUPt_->at(iMuon) );
                muon_->setp4();
                muon_->setIsLoose();
                muon_->setIsTight();
        
                v_mu_.push_back(muon_);
            }
        }
        // ******************* End Muon Loop **********************
        
        // **************************************************************
        // ******************* Start  Jet Loop **********************
        // **************************************************************
        if (saveJets_){
            for (int iJet = 0;  iJet < jet_n_; iJet++){
                jet_ = new Jet();
                if ( EXISTS("jet_pt") )                 jet_->setPt(jet_pt_->at(iJet));
                if ( EXISTS("jet_eta") )                jet_->setEta(jet_eta_->at(iJet)); 
                if ( EXISTS("jet_phi") )                jet_->setPhi(jet_phi_->at(iJet));
                if ( EXISTS("jet_m") )                  jet_->setM(jet_m_->at(iJet)); 
                if ( EXISTS("jet_E") )                  jet_->setE(jet_E_->at(iJet));
                if ( EXISTS("jet_charge") )             jet_->setCharge(jet_charge_->at(iJet));
                if ( EXISTS("jet_chargeVec") )          jet_->setChargeVec(jet_chargeVec_->at(iJet));
                if ( EXISTS("jet_looseJetID") )         jet_->setIsLooseJetID(jet_isLooseJetID_->at(iJet));
                if ( EXISTS("jet_tightJetID") )         jet_->setIsTightJetID(jet_isTightJetID_->at(iJet));
                if ( EXISTS("jet_hadronFlavour") )      jet_->setHadronFlavour(jet_hadronFlavour_->at(iJet));
                if ( EXISTS("jet_partonFlavour") )      jet_->setPartonFlavour(jet_partonFlavour_->at(iJet));
                if ( EXISTS("jet_CSVv2") )              jet_->setCSVv2(jet_CSVv2_->at(iJet));              
                if ( EXISTS("jet_cMVAv2") )             jet_->setCMVAv2(jet_cMVAv2_->at(iJet));
                if ( EXISTS("jet_CharmCvsL") )          jet_->setCTagCvsL(jet_CTagCvsL_->at(iJet));
                if ( EXISTS("jet_CharmCvsB") )          jet_->setCTagCvsB(jet_CTagCvsB_->at(iJet));     
                if ( EXISTS("jet_DeepCSVBDiscr") )      jet_->setDeepCSVBDiscr(jet_DeepCSVBDiscr_->at(iJet));
                if ( EXISTS("jet_DeepCSVCvsL") )        jet_->setDeepCSVCvsL(jet_DeepCSVCvsL_->at(iJet));
                if ( EXISTS("jet_DeepCSVCvsB") )        jet_->setDeepCSVCvsB(jet_DeepCSVCvsB_->at(iJet));
                if ( EXISTS("jet_DeepFlavourBDiscr") )  jet_->setDeepFlavourBDiscr(jet_DeepFlavourBDiscr_->at(iJet));
                if ( EXISTS("jet_DeepFlavourCvsL") )    jet_->setDeepFlavourCvsL(jet_DeepFlavourCvsL_->at(iJet));
                if ( EXISTS("jet_DeepFlavourCvsB") )    jet_->setDeepFlavourCvsB(jet_DeepFlavourCvsB_->at(iJet));
                if ( EXISTS("jet_hasGenJet") )          jet_->setHasGenJet(jet_HasGenJet_->at(iJet));
                if ( EXISTS("jet_genJet_pt") )          jet_->setGenJetPt(jet_genJetPt_->at(iJet));
                if ( EXISTS("jet_genJet_eta") )         jet_->setGenJetEta(jet_genJetEta_->at(iJet));
                if ( EXISTS("jet_genJet_phi") )         jet_->setGenJetPhi(jet_genJetPhi_->at(iJet));
                if ( EXISTS("jet_genJet_E") )           jet_->setGenJetE(jet_genJetE_->at(iJet));
                if ( EXISTS("jet_genJet_m") )           jet_->setGenJetM(jet_genJetM_->at(iJet));
                if ( EXISTS("jet_genJet_status") )      jet_->setGenJetStatus(jet_genJetStatus_->at(iJet));
                if ( EXISTS("jet_genJet_id") )          jet_->setGenJetID(jet_genJetID_->at(iJet));
                if ( EXISTS("jet_hasGenParton") )    jet_->setHasGenParton(jet_HasGenParton_->at(iJet));
                if ( EXISTS("jet_genParton_pt") )    jet_->setGenPartonPt(jet_genPartonPt_->at(iJet));
                if ( EXISTS("jet_genParton_eta") )   jet_->setGenPartonEta(jet_genPartonEta_->at(iJet));
                if ( EXISTS("jet_genParton_phi") )   jet_->setGenPartonPhi(jet_genPartonPhi_->at(iJet));
                if ( EXISTS("jet_genParton_E") )     jet_->setGenPartonE(jet_genPartonE_->at(iJet));
                if ( EXISTS("jet_genParton_m") )     jet_->setGenPartonM(jet_genPartonM_->at(iJet));
                if ( EXISTS("jet_genParton_status") )jet_->setGenPartonStatus(jet_genPartonStatus_->at(iJet));
                if ( EXISTS("jet_genParton_id") )    jet_->setGenPartonID(jet_genPartonID_->at(iJet));

                jet_->setp4();
        
                v_jet_.push_back(jet_);
            }
        }
        // ******************* End Jet Loop **********************



        otree_->Fill();
        v_el_.clear();
        v_mu_.clear();
        v_jet_.clear();
        v_met_.clear();
        v_trig_.clear();
    }
    // ******************* end Event Loop **********************
    
    
}

