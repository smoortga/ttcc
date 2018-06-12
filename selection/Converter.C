#include "Converter.h"
//
// This converter assumes a FlatTree
// as produced by https://github.com/smoortga/FlatTree
//

Converter::Converter(TTree* intree, TTree* outtree, EffectiveAreas* effectiveAreas, bool isdata, std::string config, std::vector<int> trigger_indices, bool saveElectrons, bool saveMuons, bool saveJets, bool saveMET, bool saveTruth, int nen)
{
    assert(intree);
    assert(outtree);
    itree_ = intree;
    otree_ = outtree;
    
    config_ = config;
    
    saveElectrons_ = saveElectrons;
    saveMuons_ = saveMuons;
    saveJets_ = saveJets;
    saveMET_ = saveMET;
    saveTruth_ = saveTruth;
    
    is_data_ = isdata;
    
    trigger_indices_ = trigger_indices;
    
    if (nen<0 || nen>itree_->GetEntries()){nen_ = itree_->GetEntries();}
    else{nen_ = nen;}
    
    effectiveAreas_ = effectiveAreas;//new EffectiveAreas("/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/selection/config/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_80X.txt");
    
    
    // **************************************************************
    // ******************* BTagCalibration Object *******************
    // **************************************************************
    // https://twiki.cern.ch/twiki/bin/view/CMS/BTagCalibration
    // https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation
    calib = new BTagCalibration("csvv2","/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/selection/config/DeepCSV_94XSF_V2_B_F.csv");
    reader_iterativefit = new BTagCalibrationReader(BTagEntry::OP_RESHAPING,"central",
						   {"up_jes","down_jes","up_lf","down_lf",
							"up_hf","down_hf",
							"up_hfstats1","down_hfstats1",
							"up_hfstats2","down_hfstats2",
							"up_lfstats1","down_lfstats1",
							"up_lfstats2","down_lfstats2",
							"up_cferr1","down_cferr1",
							"up_cferr2","down_cferr2"});
    reader_iterativefit->load(*calib,BTagEntry::FLAV_B,"iterativefit");
    reader_iterativefit->load(*calib,BTagEntry::FLAV_C,"iterativefit");
    reader_iterativefit->load(*calib,BTagEntry::FLAV_UDSG,"iterativefit");
    
    
    // JER and JES
    //https://twiki.cern.ch/twiki/bin/view/CMS/JECDataMC <-- Files
    //( info on: https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetEnergyScale)
    jesTotal = new JetCorrectionUncertainty(*(new JetCorrectorParameters("/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/selection/config/Fall17_17Nov2017_V6_MC_Uncertainty_AK4PFchs.txt")));
    //https://github.com/cms-jet/JRDatabase/tree/master/textFiles/Fall17_25nsV1_MC
    jer = new JME::JetResolution("/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/selection/config/Fall17_25nsV1_MC_PtResolution_AK4PFchs.txt");
    rnd = new TRandom3();

    //https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetResolution
                    // Eta bin
    cJER[0] = 1.122; // 0.0-0.5
    cJER[1] = 1.167; // 0.5-0.8
    cJER[2] = 1.168; // 0.8-1.1
    cJER[3] = 1.029; // 1.1-1.3
    cJER[4] = 1.115; // 1.3-1.7
    cJER[5] = 1.041; // 1.7-1.9
    cJER[6] = 1.167; // 1.9-2.1
    cJER[7] = 1.094; // 2.1-2.3
    cJER[8] = 1.168; // 2.3-2.5
    cJER[9] = 1.266; // 2.5-2.8
    cJER[10] = 1.595; // 2.8-3.0
    cJER[11] = 0.998; // 3.0-3.2
    cJER[12] = 1.226; // 3.2-5.0

    cJER_down[0] = 1.096;
    cJER_down[1] = 1.119;
    cJER_down[2] = 1.122;
    cJER_down[3] = 0.963;
    cJER_down[4] = 1.085;
    cJER_down[5] = 0.979;
    cJER_down[6] = 1.081;
    cJER_down[7] = 1.001;
    cJER_down[8] = 1.048;
    cJER_down[9] = 1.134;
    cJER_down[10] = 1.420;
    cJER_down[11] = 0.932;
    cJER_down[12] = 1.081;

    cJER_up[0] = 1.148;
    cJER_up[1] = 1.215;
    cJER_up[2] = 1.214;
    cJER_up[3] = 1.095;
    cJER_up[4] = 1.145;
    cJER_up[5] = 1.103;
    cJER_up[6] = 1.253;
    cJER_up[7] = 1.187;
    cJER_up[8] = 1.288;
    cJER_up[9] = 1.398;
    cJER_up[10] = 1.770;
    cJER_up[11] = 1.064;
    cJER_up[12] = 1.371;
    
    
    // PU reweighting
    // https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_X/SimGeneral/MixingModule/python/mix_2016_25ns_Moriond17MC_PoissonOOTPU_cfi.py
    npu_[0] =  3.39597497605e-05;
    npu_[1] =  6.63688402133e-06;
    npu_[2] =  1.39533611284e-05;
    npu_[3] =  3.64963078209e-05;
    npu_[4] =  6.00872171664e-05;
    npu_[5] =  9.33932578027e-05;
    npu_[6] =  0.000120591524486;
    npu_[7] =  0.000128694546198;
    npu_[8] =  0.000361697233219;
    npu_[9] =  0.000361796847553;
    npu_[10] = 0.000702474896113;
    npu_[11] = 0.00133766053707;
    npu_[12] = 0.00237817050805;
    npu_[13] = 0.00389825605651;
    npu_[14] = 0.00594546732588;
    npu_[15] = 0.00856825906255;
    npu_[16] = 0.0116627396044;
    npu_[17] = 0.0148793350787;
    npu_[18] = 0.0179897368379;
    npu_[19] = 0.0208723871946;
    npu_[20] = 0.0232564170641;
    npu_[21] = 0.0249826433945;
    npu_[22] = 0.0262245860346;
    npu_[23] = 0.0272704617569;
    npu_[24] = 0.0283301107549;
    npu_[25] = 0.0294006137386;
    npu_[26] = 0.0303026836965;
    npu_[27] = 0.0309692426278;
    npu_[28] = 0.0308818046328;
    npu_[29] = 0.0310566806228;
    npu_[30] = 0.0309692426278;
    npu_[31] = 0.0310566806228;
    npu_[32] = 0.0310566806228;
    npu_[33] = 0.0310566806228;
    npu_[34] = 0.0307696426944;
    npu_[35] = 0.0300103336052;
    npu_[36] = 0.0288355370103;
    npu_[37] = 0.0273233309106;
    npu_[38] = 0.0264343533951;
    npu_[39] = 0.0255453758796;
    npu_[40] = 0.0235877272306;
    npu_[41] = 0.0215627588047;
    npu_[42] = 0.0195825559393;
    npu_[43] = 0.0177296309658;
    npu_[44] = 0.0160560731931;
    npu_[45] = 0.0146022004183;
    npu_[46] = 0.0134080690078;
    npu_[47] = 0.0129586991411;
    npu_[48] = 0.0125093292745;
    npu_[49] = 0.0124360740539;
    npu_[50] = 0.0123547104433;
    npu_[51] = 0.0123953922486;
    npu_[52] = 0.0124360740539;
    npu_[53] = 0.0124360740539;
    npu_[54] = 0.0123547104433;
    npu_[55] = 0.0124360740539;
    npu_[56] = 0.0123387597772;
    npu_[57] = 0.0122414455005;
    npu_[58] = 0.011705203844;
    npu_[59] = 0.0108187105305;
    npu_[60] = 0.00963985508986;
    npu_[61] = 0.00827210065136;
    npu_[62] = 0.00683770076341;
    npu_[63] = 0.00545237697118;
    npu_[64] = 0.00420456901556;
    npu_[65] = 0.00367513566191;
    npu_[66] = 0.00314570230825;
    npu_[67] = 0.0022917978982;
    npu_[68] = 0.00163221454973;
    npu_[69] = 0.00114065309494;
    npu_[70] = 0.000784838366118;
    npu_[71] = 0.000533204105387;
    npu_[72] = 0.000358474034915;
    npu_[73] = 0.000238881117601;
    npu_[74] = 0.0001984254989;
    npu_[75] =  0.000157969880198;
    npu_[76] =  0.00010375646169;
    npu_[77] =  6.77366175538e-05;
    npu_[78] =  4.39850477645e-05;
    npu_[79] =  2.84298066026e-05;
    npu_[80] =  1.83041729561e-05;
    npu_[81] =  1.17473542058e-05;
    npu_[82] =  7.51982735129e-06;
    npu_[83] =  6.16160108867e-06;
    npu_[84] =  4.80337482605e-06;
    npu_[85] = 3.06235473369e-06;
    npu_[86] = 1.94863396999e-06;
    npu_[87] = 1.23726800704e-06;
    npu_[88] = 7.83538083774e-07;
    npu_[89] = 4.94602064224e-07;
    npu_[90] = 3.10989480331e-07;
    npu_[91] = 1.94628487765e-07;
    npu_[92] = 1.57888581037e-07;
    npu_[93] = 1.2114867431e-07;
    npu_[94] = 7.49518929908e-08;
    npu_[95] = 4.6060444984e-08;
    npu_[96] = 2.81008884326e-08;
    npu_[97] = 1.70121486128e-08;
    npu_[98] = 1.02159894812e-08;

    puNom = "/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/selection/config/Pileup.root";
	_fpu = TFile::Open(puNom.c_str(),"READ");
    _fpu->GetObject("pileup",_hpu);
	puUp = "/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/selection/config/Pileup_Up.root";
	_fpu_Up = TFile::Open(puUp.c_str(),"READ");
    _fpu_Up->GetObject("pileup",_hpu_Up);
	puDown = "/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/selection/config/Pileup_Down.root";
    _fpu_Down = TFile::Open(puDown.c_str(),"READ");
    _fpu_Down->GetObject("pileup",_hpu_Down);
    
    
    // Electron ID SFs
    // (2016) https://twiki.cern.ch/twiki/bin/view/CMS/EgammaIDRecipesRun2#Efficiencies_and_scale_factors
    // (2017) https://twiki.cern.ch/twiki/bin/viewauth/CMS/Egamma2017DataRecommendations#Efficiency_Scale_Factors
    // CB ID
    std::string egCBID = "/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/selection/config/EGamma_Efficiency_SF_CB_Medium_94X.root";
	_fegammaCBID = TFile::Open(egCBID.c_str(),"READ");
    _fegammaCBID->GetObject("EGamma_SF2D",_hegammaCBID);
    
    // MVA ID
    std::string egMVAID = "/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/selection/config/EGamma_Efficiency_SF_MVAID_ISO_WP80_94X.root";
	_fegammaMVAID = TFile::Open(egMVAID.c_str(),"READ");
    _fegammaMVAID->GetObject("EGamma_SF2D",_hegammaMVAID);
    
    // Electron Reconstruction SFs
    std::string egReco = "/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/selection/config/EGamma_Reconstruction_SF_94X.root";
	_fegammaReco = TFile::Open(egReco.c_str(),"READ");
    _fegammaReco->GetObject("EGamma_SF2D",_hegammaReco);
    
    // Electron Trigger SFs
    std::string egTrig = "/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/selection/config/EGammaTrigger_SF_BCDEF.root";
	_fegammaTrig = TFile::Open(egTrig.c_str(),"READ");
    _fegammaTrig->GetObject("Ele27_WPTight_Gsf",_hegammaTrig);
    
    
    // Muon SFs
    // (2016) https://twiki.cern.ch/twiki/bin/viewauth/CMS/MuonWorkInProgressAndPagResults
    // (2017) https://twiki.cern.ch/twiki/bin/view/CMS/MuonReferenceEffs2017
    
    // Muon ID scale factors (Tight ID for now)
    std::string muId = "/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/selection/config/MuonID_Efficiency_SF_BCDEF_94X.root";
	_fMuonID = TFile::Open(muId.c_str(),"READ");
	//_fMuonID->cd("MC_NUM_TightID_DEN_genTracks_PAR_pt_eta");
    _fMuonID->GetObject("NUM_TightID_DEN_genTracks_pt_abseta",_hMuonID);
    
    // Muon Isolation scale factors (Tight Isolation for Tight ID)
    std::string muIso = "/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/selection/config/MuonISO_Efficiency_SF_BCDEF_94X.root";
	_fMuonIso = TFile::Open(muIso.c_str(),"READ");
	//_fMuonIso->cd("TightISO_TightID_pt_eta");
    _fMuonIso->GetObject("NUM_TightRelIso_DEN_TightIDandIPCut_pt_abseta",_hMuonIso);
    
    // Muon Trigger scale factors
    std::string muTrig = "/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/selection/config/MuonTrigger_SF_BCDEF_94X.root";
	_fMuonTrig = TFile::Open(muTrig.c_str(),"READ");
    _fMuonTrig->GetObject("IsoMu27_PtEtaBins/abseta_pt_ratio",_hMuonTrig);
    
    
    // initialize a vector with all the available branch names in the input tree
    branchnames_.clear();
    TObjArray* branchlist = (TObjArray*)itree_->GetListOfBranches();
    for (Int_t i = 0; i < branchlist->GetEntries(); i++){
        branchnames_.push_back(branchlist->At(i)->GetName());
    }
}

Converter::~Converter()
{
    _fegammaCBID->Close();
    _fegammaMVAID->Close();
    _fegammaReco->Close();
    _fegammaTrig->Close();
    _fMuonID->Close();
    _fMuonIso->Close();
    _fMuonTrig->Close();
}

bool Converter::EXISTS(TString br)
{
    if (std::find(branchnames_.begin(),branchnames_.end(), br) != branchnames_.end()) return true;
    else{ 
        std::cout << "Error: could not find branch with name: " << br << std::endl;
        return false;
    }
}

void Converter::Convert()
{

    std::cout << "Converting " << nen_ << " events from FlatTree To ObjectOriented Tree" << std::endl;
    
    
    // **************************************************************
    // ************ CONFIG INIT (save only relevant objects) ********
    // **************************************************************
    boost::property_tree::ptree ptree;
    boost::property_tree::ini_parser::read_ini(config_, ptree);
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
    
    // ************** initialize PU weights **************
    double tot = 0;
    double totUp = 0;
    double totDown = 0;
    for(unsigned int npu=0;npu<99;++npu)
     {	
        const double npuEst = _hpu->GetBinContent(_hpu->GetXaxis()->FindBin(npu));
        _PUweights[npu] = (npu_[npu]) ? npuEst / npu_[npu] : 0.;
        tot += npuEst;

        const double npuEstUp = _hpu_Up->GetBinContent(_hpu_Up->GetXaxis()->FindBin(npu));
        _PUweightsUp[npu] = (npu_[npu]) ? npuEstUp / npu_[npu] : 0.;
        totUp += npuEstUp;

        const double npuEstDown = _hpu_Down->GetBinContent(_hpu_Down->GetXaxis()->FindBin(npu));
        _PUweightsDown[npu] = (npu_[npu]) ? npuEstDown / npu_[npu] : 0.;
        totDown += npuEstDown;
     }

    for(unsigned int npu=0;npu<99;++npu)
     {
        _PUweights[npu] /= tot;
        _PUweightsUp[npu] /= totUp;
        _PUweightsDown[npu] /= totDown;
    }
    // ************** end PU weights **************
    
    // is it data?
    otree_->Branch("is_data",&is_data_);
    
    // **************************************************************
    // ******************* Initialize Event-based *******************
    // **************************************************************
    if ( EXISTS("ev_run") )                         itree_->SetBranchAddress("ev_run",&ev_run_); 
    if ( EXISTS("ev_id") )                          itree_->SetBranchAddress("ev_id",&ev_id_);
    if ( EXISTS("ev_lumi") )                        itree_->SetBranchAddress("ev_lumi",&ev_lumi_);
    if ( EXISTS("ev_rho") )                         itree_->SetBranchAddress("ev_rho",&ev_rho_);
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
    if ( EXISTS("genTTX_id") )                      itree_->SetBranchAddress("genTTX_id",&genTTX_id_);
    if ( EXISTS("mc_pu_trueNumInt") )               itree_->SetBranchAddress("mc_pu_trueNumInt",&mc_pu_trueNumInt_);
    otree_->Branch("ev_run",&ev_run_); 
    otree_->Branch("ev_id",&ev_id_);
    otree_->Branch("ev_lumi",&ev_lumi_);
    otree_->Branch("ev_rho",&ev_rho_);
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
    // https://twiki.cern.ch/twiki/bin/view/CMSPublic/GenHFHadronMatcher
    // https://github.com/kskovpen/FlatTree/blob/master/FlatTreeProducer/plugins/GenTTXCategorizer.cc
    otree_->Branch("genTTX_id",&genTTX_id_);
    otree_->Branch("mc_pu_trueNumInt",&mc_pu_trueNumInt_);
    otree_->Branch("pu_weight",&pu_weight_);
    otree_->Branch("pu_weight_up",&pu_weight_up_);
    otree_->Branch("pu_weight_down",&pu_weight_down_);

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
        //if ( EXISTS("el_mediumMVAId") )                  itree_->SetBranchAddress("el_mediumMVAId",&el_mediumMVAId_);
        //if ( EXISTS("el_tightMVAId") )                   itree_->SetBranchAddress("el_tightMVAId",&el_tightMVAId_);

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
        //if ( EXISTS("jet_charge") )             itree_->SetBranchAddress("jet_charge",&jet_charge_);
        //if ( EXISTS("jet_chargeVec") )          itree_->SetBranchAddress("jet_chargeVec",&jet_chargeVec_);
        //if ( EXISTS("jet_looseJetID") )         itree_->SetBranchAddress("jet_looseJetID",&jet_isLooseJetID_);
        if ( EXISTS("jet_tightJetID") )         itree_->SetBranchAddress("jet_tightJetID",&jet_isTightJetID_);
        if ( EXISTS("jet_hadronFlavour") && !is_data_ )      itree_->SetBranchAddress("jet_hadronFlavour",&jet_hadronFlavour_);
        if ( EXISTS("jet_partonFlavour") && !is_data_ )      itree_->SetBranchAddress("jet_partonFlavour",&jet_partonFlavour_);
        if ( EXISTS("jet_CSVv2") )              itree_->SetBranchAddress("jet_CSVv2", &jet_CSVv2_);        
        if ( EXISTS("jet_cMVAv2") )             itree_->SetBranchAddress("jet_cMVAv2", &jet_cMVAv2_);      
        if ( EXISTS("jet_CharmCvsL") )          itree_->SetBranchAddress("jet_CharmCvsL", &jet_CTagCvsL_);      
        if ( EXISTS("jet_CharmCvsB") )          itree_->SetBranchAddress("jet_CharmCvsB", &jet_CTagCvsB_); 
        if ( EXISTS("jet_DeepCSVProbudsg") )    itree_->SetBranchAddress("jet_DeepCSVProbudsg", &jet_DeepCSVProbudsg_);
        if ( EXISTS("jet_DeepCSVProbb") )       itree_->SetBranchAddress("jet_DeepCSVProbb", &jet_DeepCSVProbb_);  
        if ( EXISTS("jet_DeepCSVProbbb") )      itree_->SetBranchAddress("jet_DeepCSVProbbb", &jet_DeepCSVProbbb_);  
        if ( EXISTS("jet_DeepCSVProbc") )       itree_->SetBranchAddress("jet_DeepCSVProbc", &jet_DeepCSVProbc_);  
        if ( EXISTS("jet_DeepCSVProbcc") )      itree_->SetBranchAddress("jet_DeepCSVProbcc", &jet_DeepCSVProbcc_);      
        //if ( EXISTS("jet_DeepCSVBDiscr") )      itree_->SetBranchAddress("jet_DeepCSVBDiscr", &jet_DeepCSVBDiscr_);  
        //if ( EXISTS("jet_DeepCSVCvsL") )        itree_->SetBranchAddress("jet_DeepCSVCvsL", &jet_DeepCSVCvsL_);    
        //if ( EXISTS("jet_DeepCSVCvsB") )        itree_->SetBranchAddress("jet_DeepCSVCvsB", &jet_DeepCSVCvsB_);    
        //if ( EXISTS("jet_DeepFlavourBDiscr") )  itree_->SetBranchAddress("jet_DeepFlavourBDiscr", &jet_DeepFlavourBDiscr_); 
        //if ( EXISTS("jet_DeepFlavourCvsL") )    itree_->SetBranchAddress("jet_DeepFlavourCvsL", &jet_DeepFlavourCvsL_); 
        //if ( EXISTS("jet_DeepFlavourCvsB") )    itree_->SetBranchAddress("jet_DeepFlavourCvsB", &jet_DeepFlavourCvsB_);
        if ( !is_data_ ){
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
        
    }
    // **************************************************************
    
    // **************************************************************
    // ******************* Initialize GenJets *********************
    // **************************************************************
    if (saveJets_){ // No need to save genJets (info saved in jet collections), but some info is needed for JES and JER specifically (with possibly different matching to jets)
        if ( !is_data_ ){
            if ( EXISTS("genJet_n") )                  itree_->SetBranchAddress("genJet_n",&genJet_n_);
            if ( EXISTS("genJet_pt") )                 itree_->SetBranchAddress("genJet_pt",&genJet_pt_);
            if ( EXISTS("genJet_eta") )                itree_->SetBranchAddress("genJet_eta",&genJet_eta_);
            if ( EXISTS("genJet_phi") )                itree_->SetBranchAddress("genJet_phi",&genJet_phi_);
            if ( EXISTS("genJet_m") )                  itree_->SetBranchAddress("genJet_m",&genJet_m_);
            if ( EXISTS("genJet_E") )                  itree_->SetBranchAddress("genJet_E",&genJet_E_);
        }        
    }
    // **************************************************************
    
    // **************************************************************
    // ******************* Initialize MC Truth info *****************
    // **************************************************************
    if (saveTruth_){ // Only for signal process, in my case TTbar
        v_truth_ = std::vector<Truth*>();
        otree_->Branch("Truth",&v_truth_);
        
        if ( EXISTS("gen_n") )                  itree_->SetBranchAddress("gen_n",&gen_n_);
        if ( EXISTS("gen_pt") )                 itree_->SetBranchAddress("gen_pt",&gen_pt_);
        if ( EXISTS("gen_eta") )                itree_->SetBranchAddress("gen_eta",&gen_eta_);
        if ( EXISTS("gen_phi") )                itree_->SetBranchAddress("gen_phi",&gen_phi_);
        if ( EXISTS("gen_m") )                  itree_->SetBranchAddress("gen_m",&gen_m_);
        if ( EXISTS("gen_E") )                  itree_->SetBranchAddress("gen_E",&gen_E_);
        if ( EXISTS("gen_status") )             itree_->SetBranchAddress("gen_status",&gen_status_);
        if ( EXISTS("gen_id") )                 itree_->SetBranchAddress("gen_id",&gen_id_);
        if ( EXISTS("gen_charge") )             itree_->SetBranchAddress("gen_charge",&gen_charge_);
        if ( EXISTS("gen_index") )              itree_->SetBranchAddress("gen_index",&gen_index_);
        if ( EXISTS("gen_mother_index") )       itree_->SetBranchAddress("gen_mother_index",&gen_mother_index_);
        if ( EXISTS("gen_daughter_n") )         itree_->SetBranchAddress("gen_daughter_n",&gen_daughter_n_);
        if ( EXISTS("gen_daughter_index") )     itree_->SetBranchAddress("gen_daughter_index",&gen_daughter_index_);
        
    }
    // **************************************************************
    
    
    
    
    
    
    
    
    // ******************* Start Event Loop **********************
    for (Int_t iEvt = 0; iEvt < nen_; iEvt++){
    
        if (iEvt % std::max((Int_t)round(nen_/10.),1) == 0){std::cout << "Converting event " << iEvt << "/" << nen_ << " (" << round(100.*iEvt/(float)nen_) << " %)" << std::endl;} //
        itree_->GetEntry(iEvt);
        
        // **************************************************************
        // ******************* Start PU weights *************************
        // **************************************************************
        if( !is_data_ )
        {	
            pu_weight_ = getPUWeight(mc_pu_trueNumInt_,"");
            pu_weight_up_ = getPUWeight(mc_pu_trueNumInt_,"up");
            pu_weight_down_ = getPUWeight(mc_pu_trueNumInt_,"down");
        }
        
         // ******************* End PU weights **********************
        
        // **************************************************************
        // ******************* Start Trigger ****************************
        // **************************************************************
        trigger_n_ = trigger_name_->size(); // the trigger_n_ variable is not properly filled... needs to be fixed --> https://github.com/kskovpen/FlatTree/blob/master/FlatTreeProducer/plugins/FlatTreeProducer.cc#L628-L672
        for (int iTrig = 0;  iTrig < trigger_name_->size(); iTrig++){
            // First check if trigger is given via trigger_indices
            if (std::find(trigger_indices_.begin(), trigger_indices_.end(), iTrig) != trigger_indices_.end()){
                //std::cout << trigger_name_->at(iTrig) << std::endl;
                trig_ = new Trigger();
        
                trig_->setIdx(trigger_->at(iTrig)); 
                trig_->setName(trigger_name_->at(iTrig)); 
                trig_->setPass(trigger_pass_->at(iTrig));
                trig_->setPrescale(trigger_prescale_->at(iTrig));    
                trig_->setHLTprescale(trigger_HLTprescale_->at(iTrig)); 
                trig_->setL1prescale(trigger_L1prescale_->at(iTrig)); 
        
                v_trig_.push_back(trig_);
            }
        }
        // ******************* End Trigger **********************
        
        // **************************************************************
        // ******************* Start MET ********************************
        // **************************************************************
        if (saveMET_){
            met_ = new MissingEnergy();
            
            if (met_pt_ > met_pt_min && met_pt_ < met_pt_max)
            {
                met_->setET(met_sumet_); 
                met_->setPt(met_pt_); 
                met_->setPx(met_px_);
                met_->setPy(met_py_);    
                met_->setPhi(met_phi_); 
                met_->setSig(met_sig_); 
            
                v_met_.push_back(met_);
            }
        }
        // ******************* End MET **********************
        
        // **************************************************************
        // ******************* Start Electron Loop **********************
        // **************************************************************
        if (saveElectrons_){
            for (int iElec = 0;  iElec < el_n_; iElec++){
            
                if (el_pt_->at(iElec) < electron_pt_min || el_pt_->at(iElec) > electron_pt_max){continue;}
                if (fabs(el_eta_->at(iElec)) < electron_abseta_min || fabs(el_eta_->at(iElec)) > electron_abseta_max){continue;}
                
                elec_ = new Electron();
                elec_->setPt(el_pt_->at(iElec));
                elec_->setEta(el_eta_->at(iElec)); 
                elec_->setPhi(el_phi_->at(iElec)); 
                elec_->setCharge(el_charge_->at(iElec));
                elec_->setE(el_E_->at(iElec));
                elec_->setScleta(el_scleta_->at(iElec));
                elec_->setDxy(el_dxy_->at(iElec));
                elec_->setDz(el_dz_->at(iElec));
                elec_->setM(el_m_->at(iElec));
                elec_->setId(el_id_->at(iElec));
                elec_->setIsLooseCBId(el_looseCBId_->at(iElec));
                elec_->setIsMediumCBId(el_mediumCBId_->at(iElec));
                elec_->setIsTightCBId(el_tightCBId_->at(iElec));
                //elec_->setIsMediumMVAId(el_mediumMVAId_->at(iElec));
                //elec_->setIsTightMVAId(el_tightMVAId_->at(iElec));
                
                float eA = effectiveAreas_->getEffectiveArea(fabs(el_scleta_->at(iElec)));
                elec_->setRelIso(el_pfIso_sumChargedHadronPt_->at(iElec),el_pfIso_sumNeutralHadronEt_->at(iElec),el_pfIso_sumPhotonEt_->at(iElec),eA,ev_rho_);
                elec_->setp4();
                elec_->setIsLoose();
                elec_->setIsMedium();
                elec_->setIsTight();
                
                // Electron ID and Reco scale factors
                if( !is_data_ )
                {	
                    // CB ID
                    std::pair<float,float> sf_CBID = elec_->GetSF(_hegammaCBID);
                    elec_->setWeightCBId(sf_CBID.first);
                    elec_->setWeightCBIdUp(sf_CBID.first+sf_CBID.second);
                    elec_->setWeightCBIdDown(std::max(float(0.),float(sf_CBID.first-sf_CBID.second)));
                    
                    // MVA ID
                    std::pair<float,float> sf_MVAID = elec_->GetSF(_hegammaMVAID);
                    elec_->setWeightMVAId(sf_MVAID.first);
                    elec_->setWeightMVAIdUp(sf_MVAID.first+sf_MVAID.second);
                    elec_->setWeightMVAIdDown(std::max(float(0.),float(sf_MVAID.first-sf_MVAID.second)));
                
                    // Reconstruction eff
                    std::pair<float,float> sf_Reco = elec_->GetSF(_hegammaReco);
                    elec_->setWeightReco(sf_Reco.first);
                    elec_->setWeightRecoUp(sf_Reco.first+sf_Reco.second);
                    elec_->setWeightRecoDown(std::max(float(0.),float(sf_Reco.first-sf_Reco.second)));
                    
                    // Trigger eff
                    std::pair<float,float> sf_Trig = elec_->GetSFTrigger(_hegammaTrig);
                    elec_->setWeightTrig(sf_Trig.first);
                    elec_->setWeightTrigUp(sf_Trig.first+sf_Trig.second);
                    elec_->setWeightTrigDown(std::max(float(0.),float(sf_Trig.first-sf_Trig.second)));
                
                }
        
                v_el_.push_back(elec_);
            }
        }
        // ******************* End Electron Loop **********************
        
        // **************************************************************
        // ******************* Start Muon Loop **********************
        // **************************************************************
        if (saveMuons_){
            for (int iMuon = 0;  iMuon < mu_n_; iMuon++){
            
                if (mu_pt_->at(iMuon) < muon_pt_min || mu_pt_->at(iMuon) > muon_pt_max){continue;}
                if (fabs(mu_eta_->at(iMuon)) < muon_abseta_min || fabs(mu_eta_->at(iMuon)) > muon_abseta_max){continue;}
            
                muon_ = new Muon();
                muon_->setPt(mu_pt_->at(iMuon));
                muon_->setEta(mu_eta_->at(iMuon)); 
                muon_->setPhi(mu_phi_->at(iMuon)); 
                muon_->setCharge(mu_charge_->at(iMuon));
                muon_->setId(mu_id_->at(iMuon));
                muon_->setM(mu_m_->at(iMuon));
                muon_->setE(mu_E_->at(iMuon));
                muon_->setDxy(mu_dxy_->at(iMuon));
                muon_->setDz(mu_dz_->at(iMuon));
                muon_->setIsLooseID(mu_isLooseID_->at(iMuon));
                muon_->setIsTightID(mu_isTightID_->at(iMuon));
                
                muon_->setRelIso(mu_pfIso_sumChargedHadronPt_->at(iMuon),mu_pfIso_sumNeutralHadronEt_->at(iMuon),mu_pfIso_sumPhotonEt_->at(iMuon), mu_pfIso_sumPUPt_->at(iMuon) );
                muon_->setp4();
                muon_->setIsLoose();
                muon_->setIsTight();
                
                // Muon ID and Isolation scale factors
                if( !is_data_ )
                {	
                    // Muon Tight ID
                    std::pair<float,float> sf_MuID = muon_->GetSF_pteta(_hMuonID);
                    muon_->setWeightId(sf_MuID.first);
                    muon_->setWeightIdUp(sf_MuID.first+sf_MuID.second);
                    muon_->setWeightIdDown(std::max(float(0.),float(sf_MuID.first-sf_MuID.second)));
                    
                    // Muon Tight Isolation for Tight ID
                    std::pair<float,float> sf_MuIso = muon_->GetSF_pteta(_hMuonIso);
                    muon_->setWeightIso(sf_MuIso.first);
                    muon_->setWeightIsoUp(sf_MuIso.first+sf_MuIso.second);
                    muon_->setWeightIsoDown(std::max(float(0.),float(sf_MuIso.first-sf_MuIso.second)));
                    
                    // Muon Trigger eff
                    std::pair<float,float> sf_MuTrig = muon_->GetSF_etapt(_hMuonTrig);
                    muon_->setWeightTrig(sf_MuTrig.first);
                    muon_->setWeightTrigUp(sf_MuTrig.first+sf_MuTrig.second);
                    muon_->setWeightTrigDown(std::max(float(0.),float(sf_MuTrig.first-sf_MuTrig.second)));
                    
                
                }
        
                v_mu_.push_back(muon_);
            }
        }
        // ******************* End Muon Loop **********************
        
        // **************************************************************
        // ******************* Start  Jet Loop **************************
        // **************************************************************
        if (saveJets_){
            for (int iJet = 0;  iJet < jet_n_; iJet++){
                
                if (jet_pt_->at(iJet) < jet_pt_min || jet_pt_->at(iJet) > jet_pt_max){continue;}
                if (fabs(jet_eta_->at(iJet)) < jet_abseta_min || fabs(jet_eta_->at(iJet)) > jet_abseta_max){continue;}
                
                jet_ = new Jet();
                jet_->setPt(jet_pt_->at(iJet));
                jet_->setEta(jet_eta_->at(iJet)); 
                jet_->setPhi(jet_phi_->at(iJet));
                jet_->setM(jet_m_->at(iJet)); 
                jet_->setE(jet_E_->at(iJet));
                //jet_->setCharge(jet_charge_->at(iJet));
                //jet_->setChargeVec(jet_chargeVec_->at(iJet));
                //jet_->setIsLooseJetID(jet_isLooseJetID_->at(iJet));
                jet_->setIsTightJetID(jet_isTightJetID_->at(iJet));
                if ( !is_data_ )      jet_->setHadronFlavour(jet_hadronFlavour_->at(iJet));
                if ( !is_data_ )      jet_->setPartonFlavour(jet_partonFlavour_->at(iJet));
                jet_->setCSVv2(jet_CSVv2_->at(iJet));              
                jet_->setCMVAv2(jet_cMVAv2_->at(iJet));
                jet_->setCTagCvsL(jet_CTagCvsL_->at(iJet));
                jet_->setCTagCvsB(jet_CTagCvsB_->at(iJet));   
                jet_->setDeepCSVProbudsg(jet_DeepCSVProbudsg_->at(iJet)); 
                jet_->setDeepCSVProbb(jet_DeepCSVProbb_->at(iJet)) ;
                jet_->setDeepCSVProbbb(jet_DeepCSVProbbb_->at(iJet));
                jet_->setDeepCSVProbc(jet_DeepCSVProbc_->at(iJet)); 
                jet_->setDeepCSVProbcc(jet_DeepCSVProbcc_->at(iJet));
                float DeepCSVBDiscr = ( jet_DeepCSVProbb_->at(iJet) != -1 ) ? ( jet_DeepCSVProbb_->at(iJet) + jet_DeepCSVProbbb_->at(iJet) )  : -1;
                float DeepCSVCvsL = ( jet_DeepCSVProbc_->at(iJet) != -1 ) ? ( jet_DeepCSVProbc_->at(iJet) / ( jet_DeepCSVProbc_->at(iJet) +  jet_DeepCSVProbudsg_->at(iJet) ) ) : -1;
                float DeepCSVCvsB = ( jet_DeepCSVProbc_->at(iJet) != -1 ) ? ( jet_DeepCSVProbc_->at(iJet) / ( jet_DeepCSVProbc_->at(iJet) +  jet_DeepCSVProbb_->at(iJet) +  jet_DeepCSVProbbb_->at(iJet) ) ) : -1;
                jet_->setDeepCSVBDiscr(DeepCSVBDiscr);
                jet_->setDeepCSVCvsL(DeepCSVCvsL);
                jet_->setDeepCSVCvsB(DeepCSVCvsB);
                //jet_->setDeepFlavourBDiscr(jet_DeepFlavourBDiscr_->at(iJet));
                //jet_->setDeepFlavourCvsL(jet_DeepFlavourCvsL_->at(iJet));
                //jet_->setDeepFlavourCvsB(jet_DeepFlavourCvsB_->at(iJet));
                if( !is_data_ )
                {
                    jet_->setHasGenJet(jet_HasGenJet_->at(iJet));
                    jet_->setGenJetPt(jet_genJetPt_->at(iJet));
                    jet_->setGenJetEta(jet_genJetEta_->at(iJet));
                    jet_->setGenJetPhi(jet_genJetPhi_->at(iJet));
                    jet_->setGenJetE(jet_genJetE_->at(iJet));
                    jet_->setGenJetM(jet_genJetM_->at(iJet));
                    jet_->setGenJetStatus(jet_genJetStatus_->at(iJet));
                    jet_->setGenJetID(jet_genJetID_->at(iJet));
                    jet_->setHasGenParton(jet_HasGenParton_->at(iJet));
                    jet_->setGenPartonPt(jet_genPartonPt_->at(iJet));
                    jet_->setGenPartonEta(jet_genPartonEta_->at(iJet));
                    jet_->setGenPartonPhi(jet_genPartonPhi_->at(iJet));
                    jet_->setGenPartonE(jet_genPartonE_->at(iJet));
                    jet_->setGenPartonM(jet_genPartonM_->at(iJet));
                    jet_->setGenPartonStatus(jet_genPartonStatus_->at(iJet));
                    jet_->setGenPartonID(jet_genPartonID_->at(iJet));
                }

                jet_->setp4();
                
                // BTagCalibration
                // https://twiki.cern.ch/twiki/bin/viewauth/CMS/BTagCalibration
                // https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation
                	
                float aeta = fabs(jet_eta_->at(iJet));
                float _eta = jet_eta_->at(iJet);
                float _pt = jet_pt_->at(iJet);
                float _phi = jet_phi_->at(iJet);
                float _E = jet_E_->at(iJet);
                float _CSVv2 = jet_CSVv2_->at(iJet);
                if( !is_data_ )
                {
                    if( abs(jet_hadronFlavour_->at(iJet)) == 5 )
                      {	
                         jet_->setSfIterativeFitCentral(reader_iterativefit->eval_auto_bounds("central",BTagEntry::FLAV_B,aeta,_pt,_CSVv2));
                         jet_->setSfIterativeFitJesUp(reader_iterativefit->eval_auto_bounds("up_jes",BTagEntry::FLAV_B,aeta,_pt,_CSVv2));
                         jet_->setSfIterativeFitJesDown(reader_iterativefit->eval_auto_bounds("down_jes",BTagEntry::FLAV_B,aeta,_pt,_CSVv2));
                         jet_->setSfIterativeFitLfUp(reader_iterativefit->eval_auto_bounds("up_lf",BTagEntry::FLAV_B,aeta,_pt,_CSVv2));
                         jet_->setSfIterativeFitLfDown(reader_iterativefit->eval_auto_bounds("down_lf",BTagEntry::FLAV_B,aeta,_pt,_CSVv2));
                         jet_->setSfIterativeFitHfstats1Up(reader_iterativefit->eval_auto_bounds("up_hfstats1",BTagEntry::FLAV_B,aeta,_pt,_CSVv2));
                         jet_->setSfIterativeFitHfstats1Down(reader_iterativefit->eval_auto_bounds("down_hfstats1",BTagEntry::FLAV_B,aeta,_pt,_CSVv2));
                         jet_->setSfIterativeFitHfstats2Up(reader_iterativefit->eval_auto_bounds("up_hfstats2",BTagEntry::FLAV_B,aeta,_pt,_CSVv2));
                         jet_->setSfIterativeFitHfstats2Down(reader_iterativefit->eval_auto_bounds("down_hfstats2",BTagEntry::FLAV_B,aeta,_pt,_CSVv2));
                         jet_->setSfIterativeFitHfUp(jet_->SfIterativeFitCentral());
                         jet_->setSfIterativeFitHfDown(jet_->SfIterativeFitCentral());
                         jet_->setSfIterativeFitCferr1Up(jet_->SfIterativeFitCentral());
                         jet_->setSfIterativeFitCferr1Down(jet_->SfIterativeFitCentral());
                         jet_->setSfIterativeFitCferr2Up(jet_->SfIterativeFitCentral());
                         jet_->setSfIterativeFitCferr2Down(jet_->SfIterativeFitCentral());
                         jet_->setSfIterativeFitLfstats1Up(jet_->SfIterativeFitCentral());
                         jet_->setSfIterativeFitLfstats1Down(jet_->SfIterativeFitCentral());
                         jet_->setSfIterativeFitLfstats2Up(jet_->SfIterativeFitCentral());
                         jet_->setSfIterativeFitLfstats2Down(jet_->SfIterativeFitCentral());
                      }
                    else if( abs(jet_hadronFlavour_->at(iJet)) == 4 )
                      {
                         jet_->setSfIterativeFitCentral(reader_iterativefit->eval_auto_bounds("central",BTagEntry::FLAV_C,aeta,_pt,_CSVv2));
                         jet_->setSfIterativeFitJesUp(jet_->SfIterativeFitCentral());
                         jet_->setSfIterativeFitJesDown(jet_->SfIterativeFitCentral());
                         jet_->setSfIterativeFitLfUp(jet_->SfIterativeFitCentral());
                         jet_->setSfIterativeFitLfDown(jet_->SfIterativeFitCentral());
                         jet_->setSfIterativeFitHfstats1Up(jet_->SfIterativeFitCentral());
                         jet_->setSfIterativeFitHfstats1Down(jet_->SfIterativeFitCentral());
                         jet_->setSfIterativeFitHfstats2Up(jet_->SfIterativeFitCentral());
                         jet_->setSfIterativeFitHfstats2Down(jet_->SfIterativeFitCentral());
                         jet_->setSfIterativeFitHfUp(jet_->SfIterativeFitCentral());
                         jet_->setSfIterativeFitHfDown(jet_->SfIterativeFitCentral());
                         jet_->setSfIterativeFitCferr1Up(reader_iterativefit->eval_auto_bounds("up_cferr1",BTagEntry::FLAV_C,aeta,_pt,_CSVv2));
                         jet_->setSfIterativeFitCferr1Down(reader_iterativefit->eval_auto_bounds("down_cferr1",BTagEntry::FLAV_C,aeta,_pt,_CSVv2));
                         jet_->setSfIterativeFitCferr2Up(reader_iterativefit->eval_auto_bounds("up_cferr2",BTagEntry::FLAV_C,aeta,_pt,_CSVv2));
                         jet_->setSfIterativeFitCferr2Down(reader_iterativefit->eval_auto_bounds("down_cferr2",BTagEntry::FLAV_C,aeta,_pt,_CSVv2));
                         jet_->setSfIterativeFitLfstats1Up(jet_->SfIterativeFitCentral());
                         jet_->setSfIterativeFitLfstats1Down(jet_->SfIterativeFitCentral());
                         jet_->setSfIterativeFitLfstats2Up(jet_->SfIterativeFitCentral());
                         jet_->setSfIterativeFitLfstats2Down(jet_->SfIterativeFitCentral());
                      }
                    else
                      {
                         jet_->setSfIterativeFitCentral(reader_iterativefit->eval_auto_bounds("central",BTagEntry::FLAV_UDSG,aeta,_pt,_CSVv2));
                         jet_->setSfIterativeFitJesUp(reader_iterativefit->eval_auto_bounds("up_jes",BTagEntry::FLAV_UDSG,aeta,_pt,_CSVv2));
                         jet_->setSfIterativeFitJesDown(reader_iterativefit->eval_auto_bounds("down_jes",BTagEntry::FLAV_UDSG,aeta,_pt,_CSVv2));
                         jet_->setSfIterativeFitLfUp(jet_->SfIterativeFitCentral());
                         jet_->setSfIterativeFitLfDown(jet_->SfIterativeFitCentral());
                         jet_->setSfIterativeFitHfstats1Up(jet_->SfIterativeFitCentral());
                         jet_->setSfIterativeFitHfstats1Down(jet_->SfIterativeFitCentral());
                         jet_->setSfIterativeFitHfstats2Up(jet_->SfIterativeFitCentral());
                         jet_->setSfIterativeFitHfstats2Down(jet_->SfIterativeFitCentral());
                         jet_->setSfIterativeFitHfUp(reader_iterativefit->eval_auto_bounds("up_hf",BTagEntry::FLAV_UDSG,aeta,_pt,_CSVv2));
                         jet_->setSfIterativeFitHfDown(reader_iterativefit->eval_auto_bounds("down_hf",BTagEntry::FLAV_UDSG,aeta,_pt,_CSVv2));
                         jet_->setSfIterativeFitCferr1Up(jet_->SfIterativeFitCentral());
                         jet_->setSfIterativeFitCferr1Down(jet_->SfIterativeFitCentral());
                         jet_->setSfIterativeFitCferr2Up(jet_->SfIterativeFitCentral());
                         jet_->setSfIterativeFitCferr2Down(jet_->SfIterativeFitCentral());
                         jet_->setSfIterativeFitLfstats1Up(reader_iterativefit->eval_auto_bounds("up_lfstats1",BTagEntry::FLAV_UDSG,aeta,_pt,_CSVv2));
                         jet_->setSfIterativeFitLfstats1Down(reader_iterativefit->eval_auto_bounds("down_lfstats1",BTagEntry::FLAV_UDSG,aeta,_pt,_CSVv2));
                         jet_->setSfIterativeFitLfstats2Up(reader_iterativefit->eval_auto_bounds("up_lfstats2",BTagEntry::FLAV_UDSG,aeta,_pt,_CSVv2));
                         jet_->setSfIterativeFitLfstats2Down(reader_iterativefit->eval_auto_bounds("down_lfstats2",BTagEntry::FLAV_UDSG,aeta,_pt,_CSVv2));
                      }   
                }
                
                
                // JER and JES
                //https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetResolution
                
                jet_->setp4_jesTotalDown(_pt,_eta,_phi,_E);
                jet_->setp4_jesTotalUp(_pt,_eta,_phi,_E);
                jet_->setp4_jerTotalDown(_pt,_eta,_phi,_E);
                jet_->setp4_jerTotalUp(_pt,_eta,_phi,_E);

                if( !is_data_ )
                {	
                    // JER

                    JME::JetParameters pjer;
                    pjer.setJetPt(_pt);
                    pjer.setJetEta(_eta);
                    pjer.setRho(ev_rho_);

                    float dpt;
                    float dR;
                    float dpt_min = 99999;
                    int idx_matched_genjet = -1;

                    float resol = jer->getResolution(pjer)*_pt;

                    for(int ij=0;ij<genJet_n_;ij++)
                      {
                         dpt = fabs(_pt-genJet_pt_->at(ij));
                         float DeltaPhi = TMath::Abs(_phi - genJet_phi_->at(ij));
                         if (DeltaPhi > 3.141593 ) DeltaPhi -= 2.*3.141593;
                         dR = TMath::Sqrt( (_eta-genJet_eta_->at(ij))*(_eta-genJet_eta_->at(ij)) + DeltaPhi*DeltaPhi );
                         if( dR < 0.2 )
                           {
                          if( dpt < (3*fabs(resol)) )
                            {
                               if( dpt <= dpt_min )
                             {
                                idx_matched_genjet = ij;
                                dpt_min = dpt;
                             }
                            }
                           }
                      }

                    int etaIdx = -1;
                    if( fabs(_eta) >= 0. && fabs(_eta) < 0.5 ) etaIdx = 0;
                    if( fabs(_eta) >= 0.5 && fabs(_eta) < 0.8 ) etaIdx = 1;
                    if( fabs(_eta) >= 0.8 && fabs(_eta) < 1.1 ) etaIdx = 2;
                    if( fabs(_eta) >= 1.1 && fabs(_eta) < 1.3 ) etaIdx = 3;
                    if( fabs(_eta) >= 1.3 && fabs(_eta) < 1.7 ) etaIdx = 4;
                    if( fabs(_eta) >= 1.7 && fabs(_eta) < 1.9 ) etaIdx = 5;
                    if( fabs(_eta) >= 1.9 && fabs(_eta) < 2.1 ) etaIdx = 6;
                    if( fabs(_eta) >= 2.1 && fabs(_eta) < 2.3 ) etaIdx = 7;
                    if( fabs(_eta) >= 2.3 && fabs(_eta) < 2.5 ) etaIdx = 8;
                    if( fabs(_eta) >= 2.5 && fabs(_eta) < 2.8 ) etaIdx = 9;
                    if( fabs(_eta) >= 2.8 && fabs(_eta) < 3.0 ) etaIdx = 10;
                    if( fabs(_eta) >= 3.0 && fabs(_eta) < 3.2 ) etaIdx = 11;
                    if( fabs(_eta) >= 3.2 && fabs(_eta) < 5.0 ) etaIdx = 12;

                    float jpt_c = _pt;
                    float jpt_c_up = _pt;
                    float jpt_c_down = _pt;

                    if( idx_matched_genjet >= 0 )
                      {	     	
                         if( etaIdx >= 0 )
                           {
                          float genpt = genJet_pt_->at(idx_matched_genjet);

                          if( genpt >= 0. )
                            {
                               jpt_c = std::max(float(0.1),float(genpt+cJER[etaIdx]*(_pt-genpt)));		       
                               jpt_c_down = std::max(float(0.1),float(genpt+cJER_down[etaIdx]*(_pt-genpt)));
                               jpt_c_up = std::max(float(0.1),float(genpt+cJER_up[etaIdx]*(_pt-genpt)));
                            }	     
                           }	 
                      }
                    else
                      {
                         if( etaIdx >= 0 )
                           {		  
                          float smear = rnd->Gaus(0.,1.);

                          float sig = std::sqrt(std::max(float(0.),float(cJER[etaIdx]*cJER[etaIdx]-1.)))*resol*_pt;
                          float sigUp = std::sqrt(std::max(float(0.),float(cJER_up[etaIdx]*cJER_up[etaIdx]-1.)))*resol*_pt;
                          float sigDn = std::sqrt(std::max(float(0.),float(cJER_down[etaIdx]*cJER_down[etaIdx]-1.)))*resol*_pt;
                            
                          jpt_c = std::max(float(0.1),float(smear*sig+_pt));
                          jpt_c_up = std::max(float(0.1),float(smear*sigUp+_pt));
                          jpt_c_down = std::max(float(0.1),float(smear*sigDn+_pt));
                           }
                      }

                    float jerCor = jpt_c/_pt;
                    float jerCorUp = jpt_c_up/_pt;
                    float jerCorDown = jpt_c_down/_pt;
                    
                    // Sometimes (when jpt_c(_sys) is truncated at 0 because it was negative), pT is rescaled to 0 and 4-vectors can not be filled!!!
                    // This will give some warnings in the output
                    jet_->setp4(_pt*jerCor,_eta,_phi,_E*jerCor);
                    jet_->setp4_jerTotalDown(_pt*jerCorDown,_eta,_phi,_E*jerCorDown);
                    jet_->setp4_jerTotalUp(_pt*jerCorUp,_eta,_phi,_E*jerCorUp);

                    // JES

                    float ptjer = jet_->p4().Pt();
                    float phijer = jet_->p4().Phi();
                    float etajer = jet_->p4().PseudoRapidity();
                    float ejer = jet_->p4().E();

                    jesTotal->setJetPt(ptjer);
                    jesTotal->setJetEta(etajer);

                    double uncert = jesTotal->getUncertainty(true);

                    jet_->setp4_jesTotalUp(ptjer*(1.+uncert),etajer,phijer,ejer*(1.+uncert));
                    jet_->setp4_jesTotalDown(ptjer*(1.-uncert),etajer,phijer,ejer*(1.-uncert));
                } 
                
                
        
                v_jet_.push_back(jet_);
            }
        }
        // ******************* End Jet Loop **********************
        
        
        // **************************************************************
        // ******************* Start Truth Loop *************************
        // **************************************************************
        if (saveTruth_){
            //truth_ = new Truth();
            
            bool foundTop1 = 0;
            bool foundTop2 = 0;
            int nGen = gen_n_;
            
            for(int i=0;i<nGen;i++){
                if( abs(gen_id_->at(i)) != 6 ) continue; // only consider tops and trace their decay chain

	            int c = getUnique(i);
	
	            int pdgid = gen_id_->at(c);
                int status = gen_status_->at(c);
                
                // begin TOP
                if( status == 62 && ((pdgid == 6 && !foundTop1) || (pdgid == -6 && !foundTop2)) )
                {
                    truth_ = new Truth();
                    
                    if( pdgid == 6 ) foundTop1 = 1;
                    if( pdgid == -6 ) foundTop2 = 1;
         
                    truth_->setPt(gen_pt_->at(c));
                    truth_->setEta(gen_eta_->at(c));
                    truth_->setPhi(gen_phi_->at(c));
                    truth_->setE(gen_E_->at(c));
                    truth_->setM(gen_m_->at(c));
                    truth_->setCharge(gen_charge_->at(c));
                    truth_->setId(gen_id_->at(c));
         
                    if( pdgid == 6 ) 
                    {
                       truth_->setLabel(1);
                       truth_->setLabelName("top");
                    }
                    else 
                    {
                       truth_->setLabel(2);
                       truth_->setLabelName("antitop");
                    }
                    
                    v_truth_.push_back(truth_);
                    
                    // begin loop over top daughters
                    for(int j=0;j<gen_daughter_n_->at(c);j++)
                    {
                        int idx = gen_daughter_index_->at(c)[j];
          
                        int pdgid_c = gen_id_->at(idx);

                        bool foundq1 = 0;
                        bool foundq2 = 0;
                        
                        // TopW
                        if( abs(pdgid_c) == 24 )
                          {
                             int cc = getUnique(idx);
           
                             truth_ = new Truth();
                             
                             truth_->setPt(gen_pt_->at(cc));
                             truth_->setEta(gen_eta_->at(cc));
                             truth_->setPhi(gen_phi_->at(cc));
                             truth_->setE(gen_E_->at(cc));
                             truth_->setM(gen_m_->at(cc));
                             truth_->setCharge(gen_charge_->at(cc));
                             truth_->setId(gen_id_->at(cc));
           
                             if( pdgid == 6 ) 
                               {
                                  truth_->setLabel(11);
                                  truth_->setLabelName("top_W");
                               }
                             else 
                               {
                                  truth_->setLabel(21);
                                  truth_->setLabelName("antitop_W");;
                               }
                               
                             v_truth_.push_back(truth_);
                             
                             // start loop over W daughters
                             for(int j2=0;j2<gen_daughter_n_->at(cc);j2++)
                             {
                                  int idx2 = gen_daughter_index_->at(cc)[j2];
          
                                  int pdgid_cc = gen_id_->at(idx2);
          
                                  int momPdgid_cc = gen_id_->at(gen_mother_index_->at(idx2));
                
                                  // TopW->l/nu
                                  if( (abs(pdgid_cc) == 11 || abs(pdgid_cc) == 13 || abs(pdgid_cc) == 15 || abs(pdgid_cc) == 12 || abs(pdgid_cc) == 14 || abs(pdgid_cc) == 16) && abs(momPdgid_cc) != 15 )
                                    {
                                       int ccc = getUnique(idx2);
                 
                                       truth_ = new Truth();
                                       
                                       truth_->setPt(gen_pt_->at(ccc));
                                       truth_->setEta(gen_eta_->at(ccc));
                                       truth_->setPhi(gen_phi_->at(ccc));
                                       truth_->setE(gen_E_->at(ccc));
                                       truth_->setM(gen_m_->at(ccc));
                                       truth_->setCharge(gen_charge_->at(ccc));
                                       truth_->setId(gen_id_->at(ccc));
                 
                                       if( (abs(pdgid_cc) == 11 || abs(pdgid_cc) == 13 || abs(pdgid_cc) == 15) && pdgid == 6 ) 
                                         {
                                            truth_->setLabel(110);
                                            truth_->setLabelName("top_lep");
                                         }
                                       if( (abs(pdgid_cc) == 11 || abs(pdgid_cc) == 13 || abs(pdgid_cc) == 15) && pdgid == -6 ) 
                                         {
                                            truth_->setLabel(210);
                                            truth_->setLabelName("antitop_lep");
                                         }
                                       if( (abs(pdgid_cc) == 12 || abs(pdgid_cc) == 14 || abs(pdgid_cc) == 16) && pdgid == 6 ) 
                                         {
                                            truth_->setLabel(111);
                                            truth_->setLabelName("top_nu");
                                         }
                                       if( (abs(pdgid_cc) == 12 || abs(pdgid_cc) == 14 || abs(pdgid_cc) == 16) && pdgid == -6 ) 
                                         {
                                            truth_->setLabel(211);
                                            truth_->setLabelName("antitop_nu");
                                         }
                                         
                                        v_truth_.push_back(truth_);
                                  } // end TopW->lnu
    
                                  // TopW->qq
                                  if( abs(pdgid_cc) <= 6 && gen_status_->at(idx2) == 23 )
                                  {
                                       int ccc = getUnique(idx2);
                 
                                       truth_ = new Truth();
                                       
                                       truth_->setPt(gen_pt_->at(ccc));
                                       truth_->setEta(gen_eta_->at(ccc));
                                       truth_->setPhi(gen_phi_->at(ccc));
                                       truth_->setE(gen_E_->at(ccc));
                                       truth_->setM(gen_m_->at(ccc));
                                       truth_->setCharge(gen_charge_->at(ccc));
                                       truth_->setId(gen_id_->at(ccc));
    
                                       if( pdgid == 6 ) 
                                         {
                                            if( !foundq1 ) 
                                              {
                                                 truth_->setLabel(112);
                                                 truth_->setLabelName("top_had1");
                                              }
                                            else 
                                              {
                                                 truth_->setLabel(113);
                                                 truth_->setLabelName("top_had2");
                                              }
                                            foundq1 = 1;
                                         }
                                       else 
                                         {
                                            if( !foundq2 ) 
                                              {
                                                 truth_->setLabel(212);
                                                 truth_->setLabelName("antitop_had1");
                                              }
                                            else 
                                              {
                                                 truth_->setLabel(213);
                                                 truth_->setLabelName("antitop_had2");
                                              }
                                            foundq2 = 1;
                                         }
                                         
                                        v_truth_.push_back(truth_);
                                    } // end TopW -> qq
                                    
                           } //  end loop over W daughters
                        } // end TopW
     
                        // TopB
                        if( (abs(pdgid_c) == 5 || abs(pdgid_c) == 3 || abs(pdgid_c) == 1) && gen_status_->at(idx) == 23 )
                        {
                             int cc = getUnique(idx);
                             
                             truth_ = new Truth();
                             
                             truth_->setPt(gen_pt_->at(cc));
                             truth_->setEta(gen_eta_->at(cc));
                             truth_->setPhi(gen_phi_->at(cc));
                             truth_->setE(gen_E_->at(cc));
                             truth_->setM(gen_m_->at(cc));
                             truth_->setCharge(gen_charge_->at(cc));
                             truth_->setId(gen_id_->at(cc));
           
                             if( pdgid == 6 ) 
                               {
                                  truth_->setLabel(10);
                                  truth_->setLabelName("top_b");
                               }
                             else 
                               {
                                  truth_->setLabel(20);
                                  truth_->setLabelName("antitop_b");;
                               }
                             v_truth_.push_back(truth_);
                        } // end TopB 
                    } // end loop over top daugthers
                     
                     
                }// end TOP
            }// end for
        }
        // ******************* End Truth Loop **********************

        otree_->Fill();
        v_el_.clear();
        v_mu_.clear();
        v_jet_.clear();
        v_met_.clear();
        v_trig_.clear();
        v_truth_.clear();
    }
    // ******************* end Event Loop **********************
    
    
}


double Converter::getPUWeight(int nPU,std::string opt)
{   
   double w = 1.;
   
   if( nPU >= 99 )
     {	
        w = _PUweights[99];
        if( opt == "up" ) w = _PUweightsUp[99];
        if( opt == "down" ) w = _PUweightsDown[99];
     } 
   else if(nPU < 0)
     { 
        std::cout << "WARNING: found event with nPU < 0 (" << nPU << ")! Taking PU weight from nPU = 0" << std::endl;
        w = _PUweights[0];
        if( opt == "up" ) w = _PUweightsUp[0];
        if( opt == "down" ) w = _PUweightsDown[0];
     }  
   else
     {	
        w = _PUweights[nPU];
        if( opt == "up" ) w = _PUweightsUp[nPU];
        if( opt == "down" ) w = _PUweightsDown[nPU];
     }      

   return w;
}

int Converter::getUnique(int p)
{   
   int pcur = p;
   
   int nLimit = 1000; // temporary fix
      
   int iter = 0;
   while( 1 )
     {	
	bool foundDupl = false;
	
	std::vector<int> daug = gen_daughter_index_->at(pcur);
	int Ndaug = gen_daughter_n_->at(pcur);
	  
	for(int ip=0;ip<Ndaug;ip++)
	  {	     
	     int d = daug[ip];

	     if( gen_id_->at(d) == gen_id_->at(pcur) && pcur != d )
	       {
		  pcur = d;
		  foundDupl = true;
		  break;
	       }
	  }	
	
	if( !foundDupl ) break;
	if( iter > nLimit ) break;
	iter++;
     }
   
   return pcur;
}

