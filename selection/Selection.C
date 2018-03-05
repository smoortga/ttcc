#include "Selection.h"
#include "TSystem.h"




using namespace std;

void Selection(std::string infiledirectory, std::string outfilepath, std::string config, Int_t nevents){

    EffectiveAreas* effectiveAreas_ = new EffectiveAreas("/user/smoortga/Analysis/NTupler/CMSSW_8_0_25/src/FlatTree/FlatTreeAnalyzer/ttcc/selection/config/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_80X.txt");
    

    // Input files
    std::string filename = GetOutputFileName(outfilepath);
    TString infiledir(infiledirectory);
    TString outfilename(outfilepath);
    TChain *superTree = new TChain("FlatTree/tree");
    vector<TString> filenames = listfiles(infiledir);
    // Add all the files in the directory until nevents is reached
    for (vector<TString>::iterator it = filenames.begin(); it != filenames.end(); it++){
        std::cout << (*it) << std::endl;
        if (!(*it).BeginsWith("output_")){continue;}
        //TFile * f_ = TFile::Open(infiledir+"/"+(*it));
        //superTree->Add(infiledir+"output_*.root");
        superTree->Add(infiledir+"/"+(*it));
        if (nevents > 0 && superTree->GetEntries() > nevents) {break;}
    }
    Int_t nEntries = superTree->GetEntries();
    if (nevents > 0 && nevents < nEntries){nEntries = nevents;}
    std::cout << "The tree " + filename +" has " << nEntries << " Events" << std::endl;
    
    
    // read in the config
    boost::property_tree::ptree ptree;
    boost::property_tree::ini_parser::read_ini(config, ptree);
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
    float ev_rho = 0;
    
    int el_n = 0;
    std::vector<float> * el_pt = 0;
    std::vector<float> * el_eta = 0;
    std::vector<float> * el_scleta = 0;
    std::vector<float> * el_phi = 0;
    std::vector<int> * el_charge = 0;
    std::vector<float> * el_pfIso_sumChargedHadronPt = 0;
    std::vector<float> * el_pfIso_sumNeutralHadronEt = 0;
    std::vector<float> * el_pfIso_sumPhotonEt = 0;
    
    int mu_n = 0;
    std::vector<float> * mu_pt = 0;
    std::vector<float> * mu_eta = 0;
    std::vector<float> * mu_phi = 0;
    std::vector<int> * mu_charge = 0;
    std::vector<float> * mu_pfIso04_sumChargedHadronPt = 0;
    std::vector<float> * mu_pfIso04_sumNeutralHadronEt = 0;
    std::vector<float> * mu_pfIso04_sumPhotonEt = 0;
    std::vector<float> * mu_pfIso04_sumPUPt = 0;

    int jet_n = 0;
    std::vector<float> * jet_pt = 0;
    std::vector<float> * jet_eta = 0;
    std::vector<float> * jet_phi = 0;

    
    
    superTree->SetBranchAddress("met_pt",&met_pt);
    superTree->SetBranchAddress("ev_rho",&ev_rho);
    
    superTree->SetBranchAddress("el_n",&el_n);
    superTree->SetBranchAddress("el_pt",&el_pt);
    superTree->SetBranchAddress("el_eta",&el_eta);
    superTree->SetBranchAddress("el_superCluster_eta",&el_scleta);
    superTree->SetBranchAddress("el_phi",&el_phi);
    superTree->SetBranchAddress("el_charge",&el_charge);
    superTree->SetBranchAddress("el_pfIso_sumChargedHadronPt",&el_pfIso_sumChargedHadronPt);
    superTree->SetBranchAddress("el_pfIso_sumNeutralHadronEt",&el_pfIso_sumNeutralHadronEt);
    superTree->SetBranchAddress("el_pfIso_sumPhotonEt",&el_pfIso_sumPhotonEt);
    
    superTree->SetBranchAddress("mu_n",&mu_n);
    superTree->SetBranchAddress("mu_pt",&mu_pt);
    superTree->SetBranchAddress("mu_eta",&mu_eta);
    superTree->SetBranchAddress("mu_phi",&mu_phi);
    superTree->SetBranchAddress("mu_charge",&mu_charge);
    superTree->SetBranchAddress("mu_pfIso04_sumChargedHadronPt",&mu_pfIso04_sumChargedHadronPt);
    superTree->SetBranchAddress("mu_pfIso04_sumNeutralHadronEt",&mu_pfIso04_sumNeutralHadronEt);
    superTree->SetBranchAddress("mu_pfIso04_sumPhotonEt",&mu_pfIso04_sumPhotonEt);
    superTree->SetBranchAddress("mu_pfIso04_sumPUPt",&mu_pfIso04_sumPUPt);
    
    
    superTree->SetBranchAddress("jet_n",&jet_n);
    superTree->SetBranchAddress("jet_pt",&jet_pt);
    superTree->SetBranchAddress("jet_eta",&jet_eta);
    superTree->SetBranchAddress("jet_phi",&jet_phi);
    
    
    
    // Output Files
    TString outfiledir = TString(outfilename);
    outfiledir.Remove(outfilename.Last('/'));
    std::cout << outfiledir << std::endl;
    std::cout << outfilename << std::endl;
    if (!DirExists(outfiledir)){mkdir(outfiledir, S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);}
    TFile* outfile = new TFile(outfilename,"RECREATE");
    TTree* outtree = (TTree*)superTree->CloneTree(0);

    // Loop over events
    for (Int_t iEvt = 0; iEvt < nEntries; iEvt++){
        
        if (iEvt % (Int_t)round(nEntries/20.) == 0){std::cout << filename + ": Processing event " << iEvt << "/" << nEntries << " (" << round(100.*iEvt/(float)nEntries) << " %)" << std::endl;} //
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
            float eA = effectiveAreas_->getEffectiveArea(fabs(el_scleta->at(iElec)));
            //Double_t RelIso_elec = (el_pfIso_sumChargedHadronPt->at(iElec) + el_pfIso_sumNeutralHadronEt->at(iElec) + el_pfIso_sumPhotonEt->at(iElec))/el_pt->at(iElec);
            Double_t RelIso_elec = (el_pfIso_sumChargedHadronPt->at(iElec) + std::max(el_pfIso_sumNeutralHadronEt->at(iElec)+el_pfIso_sumPhotonEt->at(iElec)-(eA*ev_rho),0.0f))/el_pt->at(iElec);
            if (RelIso_elec < electron_reliso_max && el_pt->at(iElec) > electron_pt_min && el_pt->at(iElec) < electron_pt_max && fabs(el_eta->at(iElec)) < electron_abseta_max && fabs(el_eta->at(iElec)) > electron_abseta_min){
                n_elec_selected++;
            }
        }
        if (n_elec_selected < nelectron_min || n_elec_selected > nelectron_max){continue;}
        
        //std::cout << "Electron passed" << std::endl;
        
        int n_muon_selected = 0;
        for (int iMuon = 0;  iMuon < mu_n; iMuon++){
            //Double_t RelIso_muon = (mu_pfIso04_sumChargedHadronPt->at(iMuon) + mu_pfIso04_sumNeutralHadronEt->at(iMuon) + mu_pfIso04_sumPhotonEt->at(iMuon))/mu_pt->at(iMuon);
            Double_t RelIso_muon = (mu_pfIso04_sumChargedHadronPt->at(iMuon)+std::max(mu_pfIso04_sumNeutralHadronEt->at(iMuon)+mu_pfIso04_sumPhotonEt->at(iMuon)-(float)(0.5*mu_pfIso04_sumPUPt->at(iMuon)),0.0f))/mu_pt->at(iMuon);
            if (RelIso_muon < muon_reliso_max && mu_pt->at(iMuon) > muon_pt_min && mu_pt->at(iMuon) < muon_pt_max && fabs(mu_eta->at(iMuon)) < muon_abseta_max && fabs(mu_eta->at(iMuon)) > muon_abseta_min){
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
            if (jet_pt->at(iJet) > jet_pt_min && jet_pt->at(iJet) < jet_pt_max && fabs(jet_eta->at(iJet)) < jet_abseta_max && fabs(jet_eta->at(iJet)) > jet_abseta_min){
                n_jet_selected++;
            }
        }
        if (n_jet_selected < njet_min || n_jet_selected > njet_max){continue;}
        
        //std::cout << "Jet passed" << std::endl;
        
        
        
        
        
        
        outtree->Fill();

    }
    //************** end loop over events *******************
    
    std::cout << filename + ": Selected " << outtree->GetEntries() << " (" << round(100000*outtree->GetEntries()/nEntries)/1000 << " %) events from initial " << nEntries << std::endl;
    
    
    //************** Convert Tree Format To Object Oriented *******************
    
    TTree* ObjectTree = new TTree("tree","tree");
    
    // see whether the file is data and whether it was ttbar MC
    // IMPORTANT NOTE: the output filename is tested here, so it should be the same as the input!!!
    // This probably needs to be fixed!
    bool isdata_ = false;
    if (filename.find("Run20") != string::npos){ isdata_ = true;}
    bool isttbar_ = false;
    if (filename.find("TT_Tune") != string::npos){ isttbar_ = true;}
    bool store_muon = true;
    bool store_elec = true;
    bool store_jets = true;
    bool store_MET = true;
    bool store_Truth = isttbar_;
    Converter* conv = new Converter(outtree,ObjectTree, effectiveAreas_, isdata_, config, store_muon, store_elec, store_jets, store_MET, store_Truth); // store flags: electrons, muons, jets, MET, Truth
    conv->Convert();
    
    std::cout << filename + ": DONE CONVERTING" << std::endl;
    
    
    outfile->cd();
    ObjectTree->Write();
    
    // Copy the hcount and hweight to save the original amount of simulated events
    TH1D* hcount = new TH1D("hcount","hcount",1,0.,1.);
    TH1D* hweight = new TH1D("hweight","hweight",1,0.,1.);
    //vector<TString> filenames = listfiles(infiledir);
    for (vector<TString>::iterator it = filenames.begin(); it != filenames.end(); it++){
        TFile * f_ = TFile::Open(infiledir+"/"+(*it));
        hcount->Add((TH1D*)f_->Get("FlatTree/hcount"));
        hweight->Add((TH1D*)f_->Get("FlatTree/hweight"));
        f_->Close();
    }
    if (nevents > 0 && nevents < superTree->GetEntries()){
        hcount->SetBinContent(1,nevents*hcount->GetBinContent(1)/(float)superTree->GetEntries());
        hweight->SetBinContent(1,nevents*hweight->GetBinContent(1)/(float)superTree->GetEntries());
    }
    outfile->cd();
    hcount->Write();
    hweight->Write();
    
    outfile->Close();
    
    
    

}



std::vector<TString> listfiles(TString indir){
    DIR *dir;
    struct dirent *ent;
    std::vector<TString> filenames;
    if ((dir = opendir (indir)) != NULL) {
      /* print all the files and directories within directory */
      while ((ent = readdir (dir)) != NULL) {
        TString name = ent->d_name;
        if (name.BeginsWith("output_")){
            filenames.push_back(name);
        }
      }
      closedir (dir);
    }
    return filenames;
}


bool DirExists(TString indir){
    DIR *dir;
    return ((dir = opendir (indir)) != NULL);
}


std::vector<std::string> split(const std::string &s, char delim) {
  std::stringstream ss(s);
  std::string item;
  std::vector<std::string> elems;
  while (std::getline(ss, item, delim)) {
    elems.push_back(item);
  }
  return elems;
}

std::string GetOutputFileName(std::string output){
    std::vector<std::string> sample_name_v = split(output, '/');
    for (std::vector<std::string>::iterator it = sample_name_v.begin(); it != sample_name_v.end(); it++){
        TString buffer(*it);
        if (buffer.EndsWith(".root")) return split(*it, '.')[0];
    }
    return "NOTFOUND";
}




int main(int argc, char *argv[])
{
   if( argc < 4 )
     {
	std::cout << "NtupleProducer usage:" << std::endl;
	std::cout << "--infiledirectory: input directory" << std::endl;
	std::cout << "--outfilepath: output file" << std::endl;
	std::cout << "--config: config file" << std::endl;
	std::cout << "--nevents : Number of events" << std::endl;
	exit(1);
     }
   
   std::string infiledirectory_str = "";
   std::string outfilepath_str = "";
   std::string config_str = "";
   Int_t nevents=-1;
   
   //std::cout << argc << std::endl;
   
   for(int i=0;i<argc;i++)
     {
	if( ! strcmp(argv[i],"--infiledirectory") ) infiledirectory_str = argv[i+1];
	if( ! strcmp(argv[i],"--outfilepath") ) outfilepath_str = argv[i+1];
	if( ! strcmp(argv[i],"--config") ) config_str = argv[i+1];
	if( ! strcmp(argv[i],"--nevents") ) nevents = atof(argv[i+1]);
     }   
    
    // std::cout << "infiledirectory: " << infiledirectory_str << std::endl;
//     std::cout << "outfilepath: " << outfilepath_str << std::endl;
//     std::cout << "nevents: " << nevents << std::endl;
   
   Selection(infiledirectory_str, outfilepath_str, config_str, nevents);

}