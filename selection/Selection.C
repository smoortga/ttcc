#include "Selection.h"
#include "TSystem.h"




using namespace std;

void Selection(TString infiledir, TString outfilename){
    // Input files
    TChain *superTree = new TChain("FlatTree/tree");
    superTree->Add(infiledir+"output_*.root");
    Int_t nEntries = superTree->GetEntries();
    std::cout << "The tree has " << nEntries << " Events" << std::endl;
    
    
    // read in the config
    boost::property_tree::ptree ptree;
    boost::property_tree::ini_parser::read_ini("config.ini", ptree);
    int nmuon_min = ptree.get<int>("muon.n_min");
    int nmuon_max = ptree.get<int>("muon.n_max");
    float muon_pt_min = ptree.get<float>("muon.pt_min");
    float muon_pt_max = ptree.get<float>("muon.pt_max");
    float muon_abseta_min = ptree.get<float>("muon.abseta_min");
    float muon_abseta_max = ptree.get<float>("muon.abseta_max");
    float muon_reliso_max = ptree.get<float>("muon.reliso_max");
    
    int nelectron_min = ptree.get<int>("electron.n_min");
    int nelectron_max = ptree.get<int>("electron.n_max");
    float electron_pt_min = ptree.get<float>("electron.pt_min");
    float electron_pt_max = ptree.get<float>("electron.pt_max");
    float electron_abseta_min = ptree.get<float>("electron.abseta_min");
    float electron_abseta_max = ptree.get<float>("electron.abseta_max");
    float electron_reliso_max = ptree.get<float>("electron.reliso_max");
    
    int nlepton_min = ptree.get<int>("lepton.n_min");
    int nlepton_max = ptree.get<int>("lepton.n_max");
    
    int njet_min = ptree.get<int>("jet.n_min");
    int njet_max = ptree.get<int>("jet.n_max");
    float jet_pt_min = ptree.get<float>("jet.pt_min");
    float jet_pt_max = ptree.get<float>("jet.pt_max");
    float jet_abseta_min = ptree.get<float>("jet.abseta_min");
    float jet_abseta_max = ptree.get<float>("jet.abseta_max");
    
    float met_pt_min = ptree.get<float>("met.pt_min");
    float met_pt_max = ptree.get<float>("met.pt_max");
    
    
    // Setting address for those branches
    float met_pt = 0;
    
    int el_n = 0;
    std::vector<float> * el_pt = 0;
    std::vector<float> * el_eta = 0;
    std::vector<float> * el_phi = 0;
    std::vector<int> * el_charge = 0;
    std::vector<float> * el_m = 0;
    std::vector<float> * el_E = 0;
    std::vector<float> * el_pfIso_sumChargedHadronPt = 0;
    std::vector<float> * el_pfIso_sumNeutralHadronEt = 0;
    std::vector<float> * el_pfIso_sumPhotonEt = 0;
    
    int mu_n = 0;
    std::vector<float> * mu_pt = 0;
    std::vector<float> * mu_eta = 0;
    std::vector<float> * mu_phi = 0;
    std::vector<int> * mu_charge = 0;
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
    std::vector<int> * jet_partonFlavour = 0;
    std::vector<int> * jet_hadronFlavour = 0;
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
    nEntries = 100000;
    for (Int_t iEvt = 0; iEvt < nEntries; iEvt++){
        
        if (iEvt % (Int_t)round(nEntries/20.) == 0){std::cout << "Processing event " << iEvt << "/" << nEntries << " (" << round(100.*iEvt/(float)nEntries) << " %)" << std::endl;} //
        superTree->GetEntry(iEvt);
        
        //****************************************************
        //
        // MET SELECTION (ISOLATION, PT, ETA, CHARGE, INVARIANT MASS)
        //
        //****************************************************
        
        if (met_pt < met_pt_min){continue;}
        if (met_pt > met_pt_max){continue;}
        
        //std::cout << "MET passed" << std::endl;
        
        //****************************************************
        //
        // LEPTON SELECTION
        //
        //****************************************************
        int n_elec_selected = 0;
        for (int iElec = 0;  iElec < el_n; iElec++){
            Double_t RelIso_elec = (el_pfIso_sumChargedHadronPt->at(iElec) + el_pfIso_sumNeutralHadronEt->at(iElec) + el_pfIso_sumPhotonEt->at(iElec))/el_pt->at(iElec);
            if (RelIso_elec < electron_reliso_max && el_pt->at(iElec) > electron_pt_min && el_pt->at(iElec) < electron_pt_max && abs(el_eta->at(iElec)) < electron_abseta_max && abs(el_eta->at(iElec)) > electron_abseta_min){
                n_elec_selected++;
            }
        }
        if (n_elec_selected < nelectron_min || n_elec_selected > nelectron_max){continue;}
        
        //std::cout << "Electron passed" << std::endl;
        
        int n_muon_selected = 0;
        for (int iMuon = 0;  iMuon < mu_n; iMuon++){
            Double_t RelIso_muon = (mu_pfIso03_sumChargedHadronPt->at(iMuon) + mu_pfIso03_sumNeutralHadronEt->at(iMuon) + mu_pfIso03_sumPhotonEt->at(iMuon))/mu_pt->at(iMuon);
            if (RelIso_muon < muon_reliso_max && mu_pt->at(iMuon) > muon_pt_min && mu_pt->at(iMuon) < muon_pt_max && abs(mu_eta->at(iMuon)) < muon_abseta_max && abs(mu_eta->at(iMuon)) > muon_abseta_min){
                n_muon_selected++;
            }
        }
        
        if (n_muon_selected < nmuon_min || n_muon_selected > nmuon_max){continue;}
        
        //std::cout << "Muon passed" << std::endl;
        
        if (n_muon_selected + n_elec_selected < nlepton_min || n_muon_selected + n_elec_selected > nlepton_max){continue;}

        //****************************************************
        //
        // jet selection
        //
        //****************************************************
        //if (jet_n < 4){continue;}
        int n_jet_selected = 0;
        for (int iJet = 0;  iJet < jet_n; iJet++){
            if (jet_pt->at(iJet) > jet_pt_min && jet_pt->at(iJet) < jet_pt_max && abs(jet_eta->at(iJet)) < jet_abseta_max && abs(jet_eta->at(iJet)) > jet_abseta_min){
                n_jet_selected++;
            }
        }
        if (n_jet_selected < njet_min || n_jet_selected > njet_max){continue;}
        
        //std::cout << "Jet passed" << std::endl;
        
        
        
        
        
        
        outtree->Fill();

    }
    //************** end loop over events *******************
    
    std::cout << "Selected " << outtree->GetEntries() << " (" << round(100000*outtree->GetEntries()/nEntries)/1000 << " %) events from initial " << nEntries << std::endl;
    
    
    //************** Convert Tree Format To Object Oriented *******************
    
    TTree* ObjectTree = new TTree("tree","tree");
    
    Converter* conv = new Converter(outtree,ObjectTree);
    conv->Convert();
    
    
    
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