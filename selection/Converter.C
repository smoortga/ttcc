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



        otree_->Fill();
        v_el_.clear();
    }
    // ******************* end Event Loop **********************
    
    
}

