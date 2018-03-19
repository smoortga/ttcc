#ifndef CONVERTER_H
#define CONVERTER_H

#include <TFile.h>
#include <TTree.h>
#include <TChain.h>
#include "TLorentzVector.h"
#include <iostream>
#include <TString.h>
#include <vector>
#include <string>
#include <assert.h>
#include "TH2F.h"
#include "TRandom3.h"
#include "./BTagCalibrationStandalone.h"
#include "../objects/Electron.h"
#include "../objects/Muon.h"
#include "../objects/Jet.h"
#include "../objects/MissingEnergy.h"
#include "../objects/Trigger.h"
#include "../objects/Truth.h"
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/ini_parser.hpp>

#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"
#include "JetMETCorrections/Modules/interface/JetResolution.h"
#include "RecoEgamma/EgammaTools/interface/EffectiveAreas.h"

#define VDEF -666

//
// This converter assumes a FlatTree
// as produced by https://github.com/smoortga/FlatTree
//

class Converter
{
 public:
    Converter(TTree* intree, TTree* outtree, EffectiveAreas* effectiveAreas, bool isdata, std::string config, bool saveElectrons = true, bool saveMuons = true, bool saveJets = true, bool saveMET = true, bool saveTruth = false, int nen = -1);   
    ~Converter();
    
    void Convert();
    TTree* GetOutputTree(){return otree_;}
    
    bool EXISTS(TString br);
       
    
 protected:
    // trees
    TTree* itree_;
    std::vector<TString> branchnames_;
    
    TTree* otree_;
    // number of entries to copy
    int nen_;
    std::string config_;
    
    // objects to save
    bool saveElectrons_;
    bool saveMuons_;
    bool saveJets_;
    bool saveMET_;
    bool saveTruth_;
    bool is_data_;
    
    // BTagCalibrations
    BTagCalibration *calib;
    BTagCalibrationReader *reader_iterativefit;
    
    // JES and JER
    JetCorrectionUncertainty *jesTotal;
    JME::JetResolution *jer;

    TRandom3 *rnd;
    
    // Electron SFs
    TFile* _fegammaCBID;
    TH2F* _hegammaCBID;
    TFile* _fegammaMVAID;
    TH2F* _hegammaMVAID;
    TFile* _fegammaReco;
    TH2F* _hegammaReco;
    
    // Muon SFs
    TFile* _fMuonID;
    TH2F* _hMuonID;
    TFile* _fMuonIso;
    TH2F* _hMuonIso;

    // JEC
    double cJER[13];
    double cJER_down[13];
    double cJER_up[13];
    
    // PU weights
    double npuSummer16_25ns[75];
    double _PUweights[75];
    double _PUweightsUp[75];
    double _PUweightsDown[75];
    // filenames of PU ROOT files created with selection/config/CalculatePileUpHistograms.py
    std::string puNom; 
	std::string puUp;
	std::string puDown;
	// files buffers
	TFile* _fpu;
	TFile* _fpu_Up;
	TFile* _fpu_Down;
	// histogram buffers
    TH1D* _hpu;
    TH1D* _hpu_Up;
    TH1D* _hpu_Down;
    // function to get PU weight
    double getPUWeight(int nPU,std::string opt);

 
    
    
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
    float pu_weight_ = 1;
    float pu_weight_up_ = 1;
    float pu_weight_down_ = 1;
    int mc_pu_trueNumInt_ = 0;
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
    int genTTX_id_ = -1;
    
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
    std::vector<std::string> *  trigger_name_ = 0;
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
    std::vector<bool> * el_mediumMVAId_ = 0;
    std::vector<bool> * el_tightMVAId_ = 0;
    
    // Electron Object container
    Electron* elec_;
    std::vector<Electron*> v_el_;
    
    EffectiveAreas* effectiveAreas_;
    
    
    
    
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
    std::vector<float> * jet_DeepCSVProbudsg_ = 0;
    std::vector<float> * jet_DeepCSVProbb_ = 0;
    std::vector<float> * jet_DeepCSVProbbb_ = 0;
    std::vector<float> * jet_DeepCSVProbc_ = 0;
    std::vector<float> * jet_DeepCSVProbcc_ = 0;
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
    
    // Jet Object container
    Jet* jet_;
    std::vector<Jet*> v_jet_;
        
    //************************************
    //
    //  GENJETS (mostly needed for JES and JER
    //
    //************************************
    int genJet_n_ = 0;
    std::vector<float> * genJet_pt_ = 0;
    std::vector<float> * genJet_eta_ = 0;
    std::vector<float> * genJet_phi_ = 0;
    std::vector<float> * genJet_m_ = 0;
    std::vector<float> * genJet_E_ = 0;
    
    
    //************************************
    //
    //  TRUTH
    //
    //************************************
    int             gen_n_ = 0;
    std::vector<float>   * gen_pt_ = 0;
    std::vector<float>   * gen_eta_ = 0;
    std::vector<float>   * gen_phi_ = 0;
    std::vector<float>   * gen_m_ = 0;
    std::vector<float>   * gen_E_ = 0;
    std::vector<int>     * gen_status_ = 0;
    std::vector<int>     * gen_id_ = 0;
    std::vector<int>     * gen_charge_ = 0;
    std::vector<int>     * gen_index_ = 0;
    std::vector<int>     * gen_mother_index_ = 0;
    std::vector<int>     * gen_daughter_n_ = 0;
    std::vector<std::vector<int> > * gen_daughter_index_ = 0;
    
    // function to get unique object in decay chain
    int getUnique(int p);
    
    // Truth Object container
    Truth* truth_;
    std::vector<Truth*> v_truth_;

    

    
    
    
};
#endif