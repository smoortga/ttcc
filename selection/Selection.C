#include "Selection.h"
#include "TSystem.h"
#include "../objects/Electron.h"



using namespace std;

void Selection(TString infiledir, TString outfilename){
    // Input files
    TChain *superTree = new TChain("FlatTree/tree");
    superTree->Add(infiledir+"output_10.root");
    Int_t nEntries = superTree->GetEntries();
    std::cout << "The tree has " << nEntries << " Events" << std::endl;
    
    // Deciding on which branches to keep
    superTree->SetBranchStatus("genJet_*",0);
    superTree->SetBranchStatus("gen_*",0);
    superTree->SetBranchStatus("mu_pfIso04*",0);
    superTree->SetBranchStatus("el_gsfTrack_*",0);
    superTree->SetBranchStatus("tau_*",0);
    superTree->SetBranchStatus("tau_n",1);
    // superTree->SetBranchStatus("met_pt",1);
//     
//     superTree->SetBranchStatus("el_n",1);
//     superTree->SetBranchStatus("el_pt",1);
//     superTree->SetBranchStatus("el_eta",1);
//     superTree->SetBranchStatus("el_phi",1);
//     superTree->SetBranchStatus("el_m",1);
//     superTree->SetBranchStatus("el_E",1);
//     superTree->SetBranchStatus("el_charge",1);
//     superTree->SetBranchStatus("el_pfIso_sumChargedHadronPt",1);
//     superTree->SetBranchStatus("el_pfIso_sumNeutralHadronEt",1);
//     superTree->SetBranchStatus("el_pfIso_sumPhotonEt",1);
// 
//     superTree->SetBranchStatus("mu_n",1);
//     superTree->SetBranchStatus("mu_pt",1);
//     superTree->SetBranchStatus("mu_eta",1);
//     superTree->SetBranchStatus("mu_phi",1);
//     superTree->SetBranchStatus("mu_charge",1);
//     superTree->SetBranchStatus("mu_m",1);
//     superTree->SetBranchStatus("mu_E",1);
//     superTree->SetBranchStatus("mu_pfIso03_sumChargedHadronPt",1);
//     superTree->SetBranchStatus("mu_pfIso03_sumNeutralHadronEt",1);
//     superTree->SetBranchStatus("mu_pfIso03_sumPhotonEt",1);
// 
//     superTree->SetBranchStatus("jet_n",1);
//     superTree->SetBranchStatus("jet_pt",1);
//     superTree->SetBranchStatus("jet_eta",1);
//     superTree->SetBranchStatus("jet_phi",1);
//     superTree->SetBranchStatus("jet_partonFlavour",1);
//     superTree->SetBranchStatus("jet_hadronFlavour",1);
//     superTree->SetBranchStatus("jet_CSVv2",1);
//     superTree->SetBranchStatus("jet_CharmCvsL",1);
//     superTree->SetBranchStatus("jet_CharmCvsB",1);
    
    
    
    
    
    // Setting address for those branches
    float met_pt = 0;
    
    int el_n = 0;
    std::vector<float> * el_pt = 0;
    std::vector<float> * el_eta = 0;
    std::vector<float> * el_phi = 0;
    std::vector<float> * el_charge = 0;
    std::vector<float> * el_m = 0;
    std::vector<float> * el_E = 0;
    std::vector<float> * el_pfIso_sumChargedHadronPt = 0;
    std::vector<float> * el_pfIso_sumNeutralHadronEt = 0;
    std::vector<float> * el_pfIso_sumPhotonEt = 0;
    
    int mu_n = 0;
    std::vector<float> * mu_pt = 0;
    std::vector<float> * mu_eta = 0;
    std::vector<float> * mu_phi = 0;
    std::vector<float> * mu_charge = 0;
    std::vector<float> * mu_m = 0;
    std::vector<float> * mu_E = 0;
    std::vector<float> * mu_pfIso03_sumChargedHadronPt = 0;
    std::vector<float> * mu_pfIso03_sumNeutralHadronEt = 0;
    std::vector<float> * mu_pfIso03_sumPhotonEt = 0;
    
    int tau_n = 0;
    
    int jet_n = 0;
    std::vector<float> * jet_pt = 0;
    std::vector<float> * jet_eta = 0;
    std::vector<float> * jet_phi = 0;
    std::vector<float> * jet_partonFlavour = 0;
    std::vector<float> * jet_hadronFlavour = 0;
    std::vector<float> * jet_CSVv2 = 0;
    std::vector<float> * jet_CharmCvsL = 0;
    std::vector<float> * jet_CharmCvsB = 0;
    
    
    superTree->SetBranchAddress("met_pt",&met_pt);
    superTree->SetBranchAddress("el_n",&el_n);
    superTree->SetBranchAddress("el_pt",&el_pt);
    superTree->SetBranchAddress("el_eta",&el_eta);
    superTree->SetBranchAddress("el_phi",&el_phi);
    superTree->SetBranchAddress("el_charge",&el_charge);
    superTree->SetBranchAddress("el_m",&el_m);
    superTree->SetBranchAddress("el_E",&el_E);
    superTree->SetBranchAddress("el_pfIso_sumChargedHadronPt",&el_pfIso_sumChargedHadronPt);
    superTree->SetBranchAddress("el_pfIso_sumNeutralHadronEt",&el_pfIso_sumNeutralHadronEt);
    superTree->SetBranchAddress("el_pfIso_sumPhotonEt",&el_pfIso_sumPhotonEt);
    
    superTree->SetBranchAddress("mu_n",&mu_n);
    superTree->SetBranchAddress("mu_pt",&mu_pt);
    superTree->SetBranchAddress("mu_eta",&mu_eta);
    superTree->SetBranchAddress("mu_phi",&mu_phi);
    superTree->SetBranchAddress("mu_charge",&mu_charge);
    superTree->SetBranchAddress("mu_m",&mu_m);
    superTree->SetBranchAddress("mu_E",&mu_E);
    superTree->SetBranchAddress("mu_pfIso03_sumChargedHadronPt",&mu_pfIso03_sumChargedHadronPt);
    superTree->SetBranchAddress("mu_pfIso03_sumNeutralHadronEt",&mu_pfIso03_sumNeutralHadronEt);
    superTree->SetBranchAddress("mu_pfIso03_sumPhotonEt",&mu_pfIso03_sumPhotonEt);
    
    superTree->SetBranchAddress("tau_n",&tau_n);
    
    superTree->SetBranchAddress("jet_n",&jet_n);
    superTree->SetBranchAddress("jet_pt",&jet_pt);
    superTree->SetBranchAddress("jet_eta",&jet_eta);
    superTree->SetBranchAddress("jet_phi",&jet_phi);
    superTree->SetBranchAddress("jet_partonFlavour",&jet_partonFlavour);
    superTree->SetBranchAddress("jet_hadronFlavour",&jet_hadronFlavour);
    superTree->SetBranchAddress("jet_CSVv2",&jet_CSVv2);
    superTree->SetBranchAddress("jet_CharmCvsL",&jet_CharmCvsL);
    superTree->SetBranchAddress("jet_CharmCvsB",&jet_CharmCvsB);
    
    
    
    // Output Files
    TString outfiledir = outfilename;
    outfiledir.Remove(outfilename.Last('/'));
    if (!DirExists(outfiledir)){mkdir(outfiledir, S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);}
    TFile* outfile = new TFile(outfilename,"RECREATE");
    TTree* outtree = (TTree*)superTree->CloneTree(0);
    //outtree->CopyAddresses(superTree);
    
    //outtree->Print();
    
    // Loop over events
    for (Int_t iEvt = 0; iEvt < nEntries; iEvt++){
        
        if (iEvt % (Int_t)round(nEntries/20.) == 0){std::cout << "Processing event " << iEvt << "/" << nEntries << " (" << round(100.*iEvt/(float)nEntries) << " %)" << std::endl;} //
        superTree->GetEntry(iEvt);
        
        //****************************************************
        //
        // MET SELECTION (ISOLATION, PT, ETA, CHARGE, INVARIANT MASS)
        //
        //****************************************************
        
        if (met_pt < 30){continue;}
        
        //****************************************************
        //
        // DILEPTON (emu) SELECTION (ISOLATION, PT, ETA, CHARGE, INVARIANT MASS)
        //
        //****************************************************
        Int_t n_elec_isolated = 0;
        Int_t isolated_electron_Idx = -1;
        TLorentzVector* isolated_electron_p4 = new TLorentzVector();
        Int_t n_muon_isolated = 0;
        Int_t isolated_muon_Idx = -1;
        TLorentzVector* isolated_muon_p4 = new TLorentzVector();
        for (int iElec = 0;  iElec < el_n; iElec++){
            Double_t RelIso_elec = (el_pfIso_sumChargedHadronPt->at(iElec) + el_pfIso_sumNeutralHadronEt->at(iElec) + el_pfIso_sumPhotonEt->at(iElec))/el_pt->at(iElec);
            if (RelIso_elec > 0.15 && el_pt->at(iElec)> 20 && abs(el_eta->at(iElec))<2.4){
                n_elec_isolated++;
                if (el_pt->at(iElec)>isolated_electron_p4->Pt()){
                    isolated_electron_p4->SetPtEtaPhiE(el_pt->at(iElec),el_eta->at(iElec),el_phi->at(iElec),el_E->at(iElec));
                    isolated_electron_Idx = iElec;
                }
            }
        }
        for (int iMuon = 0;  iMuon < mu_n; iMuon++){
            Double_t RelIso_muon = (mu_pfIso03_sumChargedHadronPt->at(iMuon) + mu_pfIso03_sumNeutralHadronEt->at(iMuon) + mu_pfIso03_sumPhotonEt->at(iMuon))/mu_pt->at(iMuon);
            if (RelIso_muon > 0.15 && mu_pt->at(iMuon)> 20 && abs(mu_eta->at(iMuon))<2.4){
                n_muon_isolated++;
                if (mu_pt->at(iMuon)>isolated_muon_p4->Pt()){
                    isolated_muon_p4->SetPtEtaPhiE(mu_pt->at(iMuon),mu_eta->at(iMuon),mu_phi->at(iMuon),mu_E->at(iMuon));
                    isolated_muon_Idx = iMuon;
                }
            }
        }
        if (n_elec_isolated != 1 || n_muon_isolated != 1){continue;}
        if (el_charge->at(isolated_electron_Idx) == mu_charge->at(isolated_muon_Idx)){continue;}
        // float mll = (*isolated_electron_p4+*isolated_muon_p4).M();
//         float Z_mass_window = 20;
//         if (mll < 12 || (mll > (91.1876 - Z_mass_window) && mll < (91.1876 + Z_mass_window))){continue;}

        //****************************************************
        //
        // (b-)jet selection
        //
        //****************************************************
        if (jet_n < 4){continue;}
        Int_t n_selected_jets = 0;
        Int_t n_selected_btagged_jets = 0;
        for (int iJet = 0;  iJet < jet_n; iJet++){
            if (jet_pt->at(iJet) > 30 && abs(jet_eta->at(iJet)) < 2.5){
                n_selected_jets++;
                if (MediumBTag(jet_CSVv2->at(iJet))){n_selected_btagged_jets++;}
            }
        }
        if (n_selected_jets < 4){continue;}
        if (n_selected_btagged_jets < 2){continue;}

        
        
        
        
        
        
        outtree->Fill();

    }
    //************** end loop over events *******************
    
    std::cout << "Selected " << outtree->GetEntries() << " (" << round(100000*outtree->GetEntries()/nEntries)/1000 << " %) events from initial " << nEntries << std::endl;
    
    
    //************** Convert Tree Format To Object Oriented *******************
    
    TTree* ObjectTree = new TTree("tree","tree");
    Int_t out_nEntries = outtree->GetEntries();
    std::vector<Electron*> v_el = std::vector<Electron*>();
    ObjectTree->Branch("Electrons",&v_el);
    
    //outtree->SetBranchAddress("met_pt",&met_pt);
    outtree->SetBranchAddress("el_n",&el_n);
    outtree->SetBranchAddress("el_pt",&el_pt);
    outtree->SetBranchAddress("el_eta",&el_eta);
    outtree->SetBranchAddress("el_phi",&el_phi);
    outtree->SetBranchAddress("el_charge",&el_charge);
    outtree->SetBranchAddress("el_m",&el_m);
    outtree->SetBranchAddress("el_E",&el_E);
    outtree->SetBranchAddress("el_pfIso_sumChargedHadronPt",&el_pfIso_sumChargedHadronPt);
    outtree->SetBranchAddress("el_pfIso_sumNeutralHadronEt",&el_pfIso_sumNeutralHadronEt);
    outtree->SetBranchAddress("el_pfIso_sumPhotonEt",&el_pfIso_sumPhotonEt);
    
    // outtree->SetBranchAddress("mu_n",&mu_n);
//     outtree->SetBranchAddress("mu_pt",&mu_pt);
//     outtree->SetBranchAddress("mu_eta",&mu_eta);
//     outtree->SetBranchAddress("mu_phi",&mu_phi);
//     outtree->SetBranchAddress("mu_charge",&mu_charge);
//     outtree->SetBranchAddress("mu_m",&mu_m);
//     outtree->SetBranchAddress("mu_E",&mu_E);
//     outtree->SetBranchAddress("mu_pfIso03_sumChargedHadronPt",&mu_pfIso03_sumChargedHadronPt);
//     outtree->SetBranchAddress("mu_pfIso03_sumNeutralHadronEt",&mu_pfIso03_sumNeutralHadronEt);
//     outtree->SetBranchAddress("mu_pfIso03_sumPhotonEt",&mu_pfIso03_sumPhotonEt);
//     
//     outtree->SetBranchAddress("tau_n",&tau_n);
//     
//     outtree->SetBranchAddress("jet_n",&jet_n);
//     outtree->SetBranchAddress("jet_pt",&jet_pt);
//     outtree->SetBranchAddress("jet_eta",&jet_eta);
//     outtree->SetBranchAddress("jet_phi",&jet_phi);
//     outtree->SetBranchAddress("jet_partonFlavour",&jet_partonFlavour);
//     outtree->SetBranchAddress("jet_hadronFlavour",&jet_hadronFlavour);
//     outtree->SetBranchAddress("jet_CSVv2",&jet_CSVv2);
//     outtree->SetBranchAddress("jet_CharmCvsL",&jet_CharmCvsL);
//     outtree->SetBranchAddress("jet_CharmCvsB",&jet_CharmCvsB);
    
    for (Int_t iEvt = 0; iEvt < out_nEntries; iEvt++){
        
        if (iEvt % (Int_t)round(out_nEntries/10.) == 0){std::cout << "Processing event " << iEvt << "/" << out_nEntries << " (" << round(100.*iEvt/(float)out_nEntries) << " %)" << std::endl;} //
        outtree->GetEntry(iEvt);
        
        //****************************************************
        //
        // Electrons
        //
        //****************************************************

        for (int iElec = 0;  iElec < el_n; iElec++){
            Electron* elec_ = new Electron();
            elec_->setPt(el_pt->at(iElec));
            elec_->setEta(el_eta->at(iElec)); 
            elec_->setPhi(el_phi->at(iElec)); 
            elec_->setE(el_E->at(iElec));
            elec_->setRelIso(el_pfIso_sumChargedHadronPt->at(iElec),el_pfIso_sumNeutralHadronEt->at(iElec),el_pfIso_sumPhotonEt->at(iElec));
            elec_->setp4(); 
            
            v_el.push_back(elec_);
        }

        ObjectTree->Fill();

    }
    
    
    outfile->cd();
    ObjectTree->Write();
    
    // Copy the hcount and hweight to save the original amount of simulated events
    TH1D* hcount = new TH1D("hcount","hcount",1,0.,1.);
    TH1D* hweight = new TH1D("hweight","hweight",1,0.,1.);
    vector<TString> filenames = listfiles(infiledir);
    for (vector<TString>::iterator it = filenames.begin(); it != filenames.end(); it++){
        TFile * f_ = TFile::Open(infiledir+"/"+(*it));
        hcount->Add((TH1D*)f_->Get("FlatTree/hcount"));
        hweight->Add((TH1D*)f_->Get("FlatTree/hweight"));
        f_->Close();
    }
    outfile->cd();
    hcount->Write();
    hweight->Write();
    
    outfile->Close();
    
    
    

}