#include "Converter.h"
//
// This converter assumes a FlatTree
// as produced by https://github.com/smoortga/FlatTree
//

Converter::Converter(TTree* intree, TTree* outtree, bool saveElectrons, bool saveMuons, bool saveJets, int nen)
{
    assert(intree);
    assert(outtree);
    itree_ = intree;
    otree_ = outtree;
    
    saveElectrons_ = saveElectrons;
    saveMuons_ = saveMuons;
    saveJets_ = saveJets;
    
    if (nen<0 || nen>itree_->GetEntries()){nen_ = itree_->GetEntries();}
    else{nen_ = nen;}
}

Converter::~Converter()
{
}

void Converter::Convert()
{

    std::cout << "Converting " << nen_ << " events from FlatTree To ObjectOriented Tree" << std::endl;
    
    // **************************************************************
    // ******************* Initialize Electrons *********************
    // **************************************************************
    if (saveElectrons_){
        v_el_ = std::vector<Electron*>();
        otree_->Branch("Electrons",&v_el_);
    
        itree_->SetBranchAddress("el_n",&el_n_);
        itree_->SetBranchAddress("el_pt",&el_pt_);
        itree_->SetBranchAddress("el_eta",&el_eta_);
        //itree_->SetBranchAddress("el_superCluster_eta",&el_scleta_);
        itree_->SetBranchAddress("el_phi",&el_phi_);
        itree_->SetBranchAddress("el_charge",&el_charge_);
        itree_->SetBranchAddress("el_id",&el_id_);
        itree_->SetBranchAddress("el_m",&el_m_);
        itree_->SetBranchAddress("el_E",&el_E_);
        itree_->SetBranchAddress("el_gsfTrack_PV_dxy",&el_dxy_);
        itree_->SetBranchAddress("el_gsfTrack_PV_dz",&el_dz_);
        itree_->SetBranchAddress("el_pfIso_sumChargedHadronPt",&el_pfIso_sumChargedHadronPt_);
        itree_->SetBranchAddress("el_pfIso_sumNeutralHadronEt",&el_pfIso_sumNeutralHadronEt_);
        itree_->SetBranchAddress("el_pfIso_sumPhotonEt",&el_pfIso_sumPhotonEt_);
        //itree_->SetBranchAddress("el_looseCBId",&el_looseCBId_);
        //itree_->SetBranchAddress("el_mediumCBId",&el_mediumCBId_);
        //itree_->SetBranchAddress("el_tightCBId",&el_tightCBId_);
    }
    // **************************************************************
    
    // **************************************************************
    // ******************* Initialize Muons *********************
    // **************************************************************
    if (saveMuons_){
        v_mu_ = std::vector<Muon*>();
        otree_->Branch("Muons",&v_mu_);
    
        itree_->SetBranchAddress("mu_n",&mu_n_);
        itree_->SetBranchAddress("mu_pt",&mu_pt_);
        itree_->SetBranchAddress("mu_eta",&mu_eta_);
        itree_->SetBranchAddress("mu_phi",&mu_phi_);
        itree_->SetBranchAddress("mu_charge",&mu_charge_);
        itree_->SetBranchAddress("mu_id",&mu_id_);
        itree_->SetBranchAddress("mu_m",&mu_m_);
        itree_->SetBranchAddress("mu_E",&mu_E_);
        // itree_->SetBranchAddress("mu_innerTrack_PV_dxy",&mu_dxy_);
//         itree_->SetBranchAddress("mu_innerTrack_PV_dz",&mu_dz_);
        itree_->SetBranchAddress("mu_pfIso04_sumChargedHadronPt",&mu_pfIso_sumChargedHadronPt_);
        itree_->SetBranchAddress("mu_pfIso04_sumNeutralHadronEt",&mu_pfIso_sumNeutralHadronEt_);
        itree_->SetBranchAddress("mu_pfIso04_sumPhotonEt",&mu_pfIso_sumPhotonEt_);
        itree_->SetBranchAddress("mu_pfIso04_sumPUPt",&mu_pfIso_sumPUPt_);
        itree_->SetBranchAddress("mu_isLooseMuon",&mu_isLooseID_);
        itree_->SetBranchAddress("mu_isTightMuon",&mu_isTightID_);
    }
    // **************************************************************
    
    
    
    
    
    
    
    // ******************* Start Event Loop **********************
    for (Int_t iEvt = 0; iEvt < nen_; iEvt++){
    
        if (iEvt % (Int_t)round(nen_/10.) == 0){std::cout << "Processing event " << iEvt << "/" << nen_ << " (" << round(100.*iEvt/(float)nen_) << " %)" << std::endl;} //
        itree_->GetEntry(iEvt);
        
        // **************************************************************
        // ******************* Start Electron Loop **********************
        // **************************************************************
        if (saveElectrons_){
            for (int iElec = 0;  iElec < el_n_; iElec++){
                elec_ = new Electron();
                elec_->setPt(el_pt_->at(iElec));
                elec_->setEta(el_eta_->at(iElec)); 
                elec_->setPhi(el_phi_->at(iElec)); 
                elec_->setCharge(el_charge_->at(iElec));
                elec_->setE(el_E_->at(iElec));
                elec_->setRelIso(el_pfIso_sumChargedHadronPt_->at(iElec),el_pfIso_sumNeutralHadronEt_->at(iElec),el_pfIso_sumPhotonEt_->at(iElec));
                elec_->setp4();
                //elec_->setScleta(el_scleta_->at(iElec));
                elec_->setDxy(el_dxy_->at(iElec));
                elec_->setDz(el_dz_->at(iElec));
                elec_->setM(el_m_->at(iElec));
                elec_->setId(el_id_->at(iElec));
                //elec_->setIsLooseCBId(el_looseCBId_->at(iElec));
                //elec_->setIsMediumCBId(el_mediumCBId_->at(iElec));
                //elec_->setIsTightCBId(el_tightCBId_->at(iElec));
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
                muon_->setPt(mu_pt_->at(iMuon));
                muon_->setEta(mu_eta_->at(iMuon)); 
                muon_->setPhi(mu_phi_->at(iMuon)); 
                muon_->setCharge(mu_charge_->at(iMuon));
                muon_->setE(mu_E_->at(iMuon));
                muon_->setRelIso(mu_pfIso_sumChargedHadronPt_->at(iMuon),mu_pfIso_sumNeutralHadronEt_->at(iMuon),mu_pfIso_sumPhotonEt_->at(iMuon), mu_pfIso_sumPUPt_->at(iMuon) );
                muon_->setp4();
                // muon_->setDxy(mu_dxy_->at(iMuon));
//                 muon_->setDz(mu_dz_->at(iMuon));
                muon_->setM(mu_m_->at(iMuon));
                muon_->setId(mu_id_->at(iMuon));
                muon_->setIsLooseID(mu_isLooseID_->at(iMuon));
                muon_->setIsTightID(mu_isTightID_->at(iMuon));
                muon_->setIsLoose();
                muon_->setIsTight();
        
                v_mu_.push_back(muon_);
            }
        }
        // ******************* End Electron Loop **********************



        otree_->Fill();
        v_el_.clear();
        v_mu_.clear();
    }
    // ******************* end Event Loop **********************
    
    
}

