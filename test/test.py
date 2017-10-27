from ROOT import *
gSystem.Load('../objects/Electron_C')
from ROOT import Electron

# object = Electron()
# 
# v = ROOT.std.vector( Electron )()
# v.push_back(object)
# v.push_back(object)
# 
# f = TFile("test.root", "recreate")
# mytree = TTree("mytree", "testing tree appending")
# mytree.Branch("electron", v) 
# mytree.Fill()  
# 
# f.WriteTObject(mytree)
# f.Close()
# 
# f = TFile("test.root")
# t = f.Get("mytree")
# nEntries = t.GetEntries()
# print nEntries
# for i in range(nEntries):
#     t.GetEntry(i)
#     el_collection = t.electron
#     print el_collection.size()
#     for el in el_collection:
#         print el.Pt()
#         el.setp4()

def Selection(infiledir, outfilename):
    superTree = TChain("FlatTree/tree")
    superTree.Add(infiledir+"output_10.root")
    
    v_el = ROOT.std.vector( Electron )()
    
    # Output Files
    outfile = TFile(outfilename,"RECREATE")
    outtree = TTree("tree","tree")
    outtree.Branch("electrons",v_el)
    
    selected_tree = superTree.CloneTree(0)
    
    nEntries = superTree.GetEntries()
    for iEvt in range(nEntries):
        if (iEvt % int(nEntries/20.) == 0): print "Processing event " + str(iEvt) + "/" + str(nEntries) 
        superTree.GetEntry(iEvt)
        
       #  Electrons
#         for iElec in range(superTree.el_n):
#             el_pt = superTree.el_pt[iElec]
#             el_eta = superTree.el_eta[iElec]
#             el_phi = superTree.el_phi[iElec]
#             if (el_pt > 30 and abs(el_eta)<2.4):
#                 pt = el_pt
#                 electron_ = Electron()
#                 electron_.setPt(el_pt)
#                 electron_.setEta(el_eta)
#                 electron_.setPhi(el_phi)
#                 v_el.push_back(electron_)
        
        #****************************************************
        #
        # MET SELECTION (ISOLATION, PT, ETA, CHARGE, INVARIANT MASS)
        #
        #****************************************************
        
        if (supertree.met_pt < 30): continue
        
        #****************************************************
        #
        # DILEPTON (emu) SELECTION (ISOLATION, PT, ETA, CHARGE, INVARIANT MASS)
        #
        #****************************************************
        Int_t n_elec_isolated = 0
        Int_t isolated_electron_Idx = -1
        isolated_electron_p4 = TLorentzVector()
        Int_t n_muon_isolated = 0
        Int_t isolated_muon_Idx = -1
        solated_muon_p4 = TLorentzVector()
        for iElec in range(superTree.el_n):
            RelIso_elec = (superTree.el_pfIso_sumChargedHadronPt[iElec] + superTree.el_pfIso_sumNeutralHadronEt[iElec] + superTree.el_pfIso_sumPhotonEt[iElec])/superTree.el_pt[iElec]
            if (RelIso_elec > 0.15 && superTree.el_pt[iElec]> 20 && abs(superTree.el_eta[iElec])<2.4){
                n_elec_isolated++
                if (superTree.el_pt[iElec]>isolated_electron_p4->Pt()){
                    isolated_electron_p4.SetPtEtaPhiE(superTree.el_pt[iElec],superTree.el_eta[iElec],superTree.el_phi[iElec],superTree.el_E[iElec])
                    isolated_electron_Idx = iElec
                }
            }
        }
        for iMuon in range(superTree.mu_n):
            RelIso_muon = (superTree.mu_pfIso03_sumChargedHadronPt[iMuon] + superTree.mu_pfIso03_sumNeutralHadronEt[iMuon] + superTree.mu_pfIso03_sumPhotonEt[iMuon])/superTree.mu_pt[iMuon]
            if (RelIso_muon > 0.15 && superTree.mu_pt[iMuon]> 20 && abs(superTree.mu_eta[iMuon])<2.4){
                n_muon_isolated++
                if (superTree.mu_pt[iMuon]>isolated_muon_p4->Pt()){
                    isolated_muon_p4.SetPtEtaPhiE(superTree.mu_pt[iMuon],superTree.mu_eta[iMuon],vmu_phi[iMuon],superTree.mu_E[iMuon])
                    isolated_muon_Idx = iMuon
                }
            }
        }
        if (n_elec_isolated != 1 || n_muon_isolated != 1): continue
        if (superTree.el_charge[isolated_electron_Idx] == superTree.mu_charge[isolated_muon_Idx]): continue
        # float mll = (*isolated_electron_p4+*isolated_muon_p4).M()
#         float Z_mass_window = 20
#         if (mll < 12 || (mll > (91.1876 - Z_mass_window) && mll < (91.1876 + Z_mass_window))): continue

        #****************************************************
        #
        # (b-)jet selection
        #
        #****************************************************
        if (jet_n < 4): continue
        Int_t n_selected_jets = 0
        Int_t n_selected_btagged_jets = 0
        for iJet in range(superTree.jet_n):
            if (superTree.jet_pt[iJet] > 30 && abs(superTree.jet_eta[iJet]) < 2.5){
                n_selected_jets++
                if (superTree.jet_CSVv2[iJet] > 0.8484): n_selected_btagged_jets++
            }
        }
        if (n_selected_jets < 4): continue
        if (n_selected_btagged_jets < 2): continue
            
            
        selected_tree.Fill()
    
    outfile.cd()
    selected_tree.Write()
    outfile.Close()

Selection("/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/FirstTests-25102017/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16MiniAODv2_PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_v1_MINIAODSIM/171025_114734/0000/","/user/smoortga/Analysis/NTupler/CMSSW_8_0_25/src/FlatTree/FlatTreeAnalyzer/test/SelectedSamples/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8.root")
        