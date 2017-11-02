#ifndef CONVERTER_H
#define CONVERTER_H

#include <TFile.h>
#include <TTree.h>
#include <TChain.h>
#include "TLorentzVector.h"
#include <iostream>
#include <assert.h>
#include "../objects/Electron.h"
#include "../objects/Muon.h"
#include "../objects/Jet.h"
#include "../objects/MissingEnergy.h"
#include "../objects/Trigger.h"

//
// This converter assumes a FlatTree
// as produced by https://github.com/smoortga/FlatTree
//

class Converter
{
 public:
    Converter(TTree* intree, TTree* outtree, bool saveElectrons = true, bool saveMuons = true, bool saveJets = true, bool saveMET = true, int nen = -1);   
    ~Converter();
    
    void Convert();
    TTree* GetOutputTree(){return otree_;}
    
    bool EXISTS(TString br);
       
    
 protected:
    // trees
    TTree* itree_;
    vector<TString> branchnames_;
    
    TTree* otree_;
    // number of entries to copy
    int nen_;
    
    // objects to save
    bool saveElectrons_;
    bool saveMuons_;
    bool saveJets_;
    bool saveMET_;
 
    
    
    //************************************
    //
    //  EVENT-BASED VARIABLES
    //
    //************************************
    // event
    int ev_run_ = 0;
    int ev_id_ = 0;
    int ev_lumi_ = 0;
    float ev_rho_ = 0;
    float mc_weight_ = 1;
    int nvertex_ = 0;
    float pv_x_ = 0;
    float pv_y_ = 0;
    float pv_z_ = 0;
    float pv_xError_ = 0;
    float pv_yError_ = 0;
    float pv_zError_ = 0;
    float pv_chi2_ = 0;
    float pv_ndof_ = 0;
    float pv_rho_ = 0;
    int pv_isFake_ = 0;
    
    //************************************
    //
    //  MET
    //
    //************************************
    float met_px_ = 0;
    float met_py_ = 0;
    float met_pt_ = 0;
    float met_phi_ = 0;
    float met_sumet_ = 0;
    double met_sig_ = 0;
    
    // MET Object container
    MissingEnergy* met_;
    std::vector<MissingEnergy*> v_met_;
    
    //************************************
    //
    //  Trigger
    //
    //************************************
    int trigger_n_ = 0;
    std::vector<int> *  trigger_ = 0;
    std::vector<string> *  trigger_name_ = 0;
    std::vector<bool> *  trigger_pass_ = 0;
    std::vector<int> *  trigger_prescale_ = 0;
    std::vector<int> *  trigger_HLTprescale_ = 0;
    std::vector<int> *  trigger_L1prescale_ = 0;
    
    Trigger* trig_;
    std::vector<Trigger*> v_trig_;
    
    
    //************************************
    //
    //  ELECTRONS
    //
    //************************************
    
    // electron containers for SetBranchAddress of input tree
    int el_n_ = 0;
    std::vector<float> * el_pt_ = 0;
    std::vector<float> * el_eta_ = 0;
    std::vector<float> * el_scleta_ = 0;
    std::vector<float> * el_phi_ = 0;
    std::vector<int> * el_charge_ = 0;
    std::vector<int> * el_id_ = 0;
    std::vector<float> * el_m_ = 0;
    std::vector<float> * el_E_ = 0;
    std::vector<float> * el_dxy_ = 0;
    std::vector<float> * el_dz_ = 0;
    std::vector<float> * el_pfIso_sumChargedHadronPt_ = 0;
    std::vector<float> * el_pfIso_sumNeutralHadronEt_ = 0;
    std::vector<float> * el_pfIso_sumPhotonEt_ = 0;
    std::vector<bool> * el_looseCBId_ = 0;
    std::vector<bool> * el_mediumCBId_ = 0;
    std::vector<bool> * el_tightCBId_ = 0;
    
    // Electron Object container
    Electron* elec_;
    std::vector<Electron*> v_el_;
    
    
    
    
    //************************************
    //
    //  MUONS
    //
    //************************************
    
    int mu_n_ = 0;
    std::vector<float> * mu_pt_ = 0;
    std::vector<float> * mu_eta_ = 0;
    std::vector<float> * mu_phi_ = 0;
    std::vector<int> * mu_charge_ = 0;
    std::vector<int> * mu_id_ = 0;
    std::vector<float> * mu_m_ = 0;
    std::vector<float> * mu_E_ = 0;
    std::vector<float> * mu_dxy_ = 0;
    std::vector<float> * mu_dz_ = 0;
    std::vector<float> * mu_pfIso_sumChargedHadronPt_ = 0;
    std::vector<float> * mu_pfIso_sumNeutralHadronEt_ = 0;
    std::vector<float> * mu_pfIso_sumPhotonEt_ = 0;
    std::vector<float> * mu_pfIso_sumPUPt_ = 0;
    std::vector<bool> * mu_isLooseID_ = 0;
    std::vector<bool> * mu_isTightID_ = 0;

    
    // muectron Object container
    Muon* muon_;
    std::vector<Muon*> v_mu_;
    
    
    //************************************
    //
    //  JETS
    //
    //************************************
    
    int jet_n_ = 0;
    std::vector<float> * jet_pt_ = 0;
    std::vector<float> * jet_eta_ = 0;
    std::vector<float> * jet_phi_ = 0;
    std::vector<float> * jet_m_ = 0;
    std::vector<float> * jet_E_ = 0;
    std::vector<float> * jet_charge_ = 0;
    std::vector<float> * jet_chargeVec_ = 0;
    std::vector<bool> * jet_isLooseJetID_ = 0;
    std::vector<bool> * jet_isTightJetID_ = 0;
    std::vector<int> * jet_hadronFlavour_ = 0;
    std::vector<int> * jet_partonFlavour_ = 0;
    std::vector<float> * jet_CSVv2_ = 0;
    std::vector<float> * jet_cMVAv2_ = 0;
    std::vector<float> * jet_CTagCvsL_ = 0;
    std::vector<float> * jet_CTagCvsB_ = 0;
    std::vector<float> * jet_DeepCSVBDiscr_ = 0;
    std::vector<float> * jet_DeepCSVCvsL_ = 0;
    std::vector<float> * jet_DeepCSVCvsB_ = 0;
    std::vector<float> * jet_DeepFlavourBDiscr_ = 0;
    std::vector<float> * jet_DeepFlavourCvsL_ = 0;
    std::vector<float> * jet_DeepFlavourCvsB_ = 0;
    std::vector<bool> *  jet_HasGenJet_ = 0;
    std::vector<float> * jet_genJetPt_ = 0;
    std::vector<float> * jet_genJetEta_ = 0;
    std::vector<float> * jet_genJetPhi_ = 0;
    std::vector<float> * jet_genJetE_ = 0;
    std::vector<float> * jet_genJetM_ = 0;
    std::vector<int> *   jet_genJetStatus_ = 0;
    std::vector<int> *   jet_genJetID_ = 0;
    std::vector<bool> * jet_HasGenParton_ = 0;
    std::vector<float> * jet_genPartonPt_ = 0;
    std::vector<float> * jet_genPartonEta_ = 0;
    std::vector<float> * jet_genPartonPhi_ = 0;
    std::vector<float> * jet_genPartonE_ = 0;
    std::vector<float> * jet_genPartonM_ = 0;
    std::vector<int> * jet_genPartonStatus_ = 0;
    std::vector<int> * jet_genPartonID_ = 0;
        





    
    // muectron Object container
    Jet* jet_;
    std::vector<Jet*> v_jet_;
    
};
#endif