import ROOT
import os
import sys
from argparse import ArgumentParser
from array import array
from xsec import xsec_table
import numpy as np
from math import sqrt
import pickle
from scipy.optimize import fmin,fminbound,minimize,brentq,ridder,fsolve
from copy import deepcopy
from binning import *


ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetOptStat(0)


def DeriveSFs(indir, outdir, weightstring):

    samples_to_consider_MC = [
    "TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8.root",
    "DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8.root",
    "DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8.root",
    "ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8.root",
    "ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8.root",
    "ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8.root",
    "ST_t-channel_antitop_5f_TuneCP5_PSweights_13TeV-powheg-pythia8.root",
    "ST_t-channel_top_5f_TuneCP5_13TeV-powheg-pythia8.root",
    "WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8.root"
	]


    samples_MC = [i for i in os.listdir(indir) if not "31Mar2018" in i and i in samples_to_consider_MC]
    samples_Data = [i for i in os.listdir(indir) if "31Mar2018" in i]

    if not os.path.isdir(outdir): os.mkdir(outdir)

    ###############################
    #
    #	PREAPRE HISTOGRAMS
    #
    ################################

    weight_string = weightstring#"weight_btag_iterativefit*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*mc_weight"#*pu_weight"

    # custom_bins_CvsL = [0,0.2,0.4,0.6,0.8,1.]#[0,0.25,0.5,0.75,1.]#[0,0.1,0.2,0.3,0.5,0.7,0.85,1.0]#np.arange(0,1.05,0.1)
    # nbins_CvsL = len(custom_bins_CvsL)-1

    # custom_bins_CvsL_jet1 = [0,0.15,0.3,0.5,0.7,1.]#[0,0.25,0.5,0.75,1.]#[0,0.1,0.2,0.3,0.5,0.7,0.85,1.0]#np.arange(0,1.05,0.1)
#     nbins_CvsL_jet1 = len(custom_bins_CvsL_jet1)-1
# 
#     custom_bins_CvsB_jet1 = [0,0.4,0.55,0.65,0.8,1.]#[0,0.25,0.5,0.75,1.]#[0,0.15,0.3,0.5,0.7,0.8,1.0]#np.arange(0,1.05,0.1)
#     nbins_CvsB_jet1 = len(custom_bins_CvsB_jet1)-1
# 
#     custom_bins_CvsL_jet2 = [0,0.15,0.3,0.5,0.7,1.]#[0,0.25,0.5,0.75,1.]#[0,0.1,0.2,0.3,0.5,0.7,0.85,1.0]#np.arange(0,1.05,0.1)
#     nbins_CvsL_jet2 = len(custom_bins_CvsL_jet2)-1
# 
#     custom_bins_CvsB_jet2 = [0,0.4,0.55,0.65,0.8,1.]#[0,0.25,0.5,0.75,1.]#[0,0.15,0.3,0.5,0.7,0.8,1.0]#np.arange(0,1.05,0.1)
#     nbins_CvsB_jet2 = len(custom_bins_CvsB_jet2)-1
# 
#     custom_bins_CvsL_jet3 = [0,0.15,0.3,0.5,0.7,1.]#[0,0.25,0.5,0.75,1.]#[0,0.1,0.2,0.3,0.5,0.7,0.85,1.0]#np.arange(0,1.05,0.1)
#     nbins_CvsL_jet3 = len(custom_bins_CvsL_jet3)-1
# 
#     custom_bins_CvsB_jet3 = [0,0.4,0.55,0.65,0.8,1.]#[0,0.25,0.5,0.75,1.]#[0,0.15,0.3,0.5,0.7,0.8,1.0]#np.arange(0,1.05,0.1)
#     nbins_CvsB_jet3 = len(custom_bins_CvsB_jet3)-1

    histo_dict = {}
    histo_dict["jet1"] = {
        "b" : ROOT.TH2D("b1",";DeepCSV CvsL first jet;DeepCSV CvsB first jet;Events",nbins_CvsL_jet1,array("d",custom_bins_CvsL_jet1),nbins_CvsB_jet1,array("d",custom_bins_CvsB_jet1)),
        "c" : ROOT.TH2D("c1",";DeepCSV CvsL first jet;DeepCSV CvsB first jet;Events",nbins_CvsL_jet1,array("d",custom_bins_CvsL_jet1),nbins_CvsB_jet1,array("d",custom_bins_CvsB_jet1)),
        "l" : ROOT.TH2D("l1",";DeepCSV CvsL first jet;DeepCSV CvsB first jet;Events",nbins_CvsL_jet1,array("d",custom_bins_CvsL_jet1),nbins_CvsB_jet1,array("d",custom_bins_CvsB_jet1)),
    }
    histo_dict["jet2"] = {
        "b" : ROOT.TH2D("b2",";DeepCSV CvsL second jet;DeepCSV CvsB second jet;Events",nbins_CvsL_jet2,array("d",custom_bins_CvsL_jet2),nbins_CvsB_jet2,array("d",custom_bins_CvsB_jet2)),
        "c" : ROOT.TH2D("c2",";DeepCSV CvsL second jet;DeepCSV CvsB second jet;Events",nbins_CvsL_jet2,array("d",custom_bins_CvsL_jet2),nbins_CvsB_jet2,array("d",custom_bins_CvsB_jet2)),
        "l" : ROOT.TH2D("l2",";DeepCSV CvsL second jet;DeepCSV CvsB second jet;Events",nbins_CvsL_jet2,array("d",custom_bins_CvsL_jet2),nbins_CvsB_jet2,array("d",custom_bins_CvsB_jet2)),
    }
    histo_dict["jet3"] = {
        "b" : ROOT.TH2D("b3",";DeepCSV CvsL third jet;DeepCSV CvsB third jet;Events",nbins_CvsL_jet3,array("d",custom_bins_CvsL_jet3),nbins_CvsB_jet3,array("d",custom_bins_CvsB_jet3)),
        "c" : ROOT.TH2D("c3",";DeepCSV CvsL third jet;DeepCSV CvsB third jet;Events",nbins_CvsL_jet3,array("d",custom_bins_CvsL_jet3),nbins_CvsB_jet3,array("d",custom_bins_CvsB_jet3)),
        "l" : ROOT.TH2D("l3",";DeepCSV CvsL third jet;DeepCSV CvsB third jet;Events",nbins_CvsL_jet3,array("d",custom_bins_CvsL_jet3),nbins_CvsB_jet3,array("d",custom_bins_CvsB_jet3)),
    }
    datahisto_dict = {
        "jet1" : ROOT.TH2D("data1",";DeepCSV CvsL first jet;DeepCSV CvsB first jet;Events",nbins_CvsL_jet1,array("d",custom_bins_CvsL_jet1),nbins_CvsB_jet1,array("d",custom_bins_CvsB_jet1)),
        "jet2" : ROOT.TH2D("data2",";DeepCSV CvsL second jet;DeepCSV CvsB second jet;Events",nbins_CvsL_jet2,array("d",custom_bins_CvsL_jet2),nbins_CvsB_jet2,array("d",custom_bins_CvsB_jet2)),
        "jet3" : ROOT.TH2D("data3",";DeepCSV CvsL third jet;DeepCSV CvsB third jet;Events",nbins_CvsL_jet3,array("d",custom_bins_CvsL_jet3),nbins_CvsB_jet3,array("d",custom_bins_CvsB_jet3)),
    }

    SFb_hist = ROOT.TH2D("SFb_hist",";CvsL;CvsB;SFb",nbins_CvsL_jet1,array("d",custom_bins_CvsL_jet1),nbins_CvsB_jet1,array("d",custom_bins_CvsB_jet1))
    SFc_hist = ROOT.TH2D("SFc_hist",";CvsL;CvsB;SFc",nbins_CvsL_jet2,array("d",custom_bins_CvsL_jet2),nbins_CvsB_jet2,array("d",custom_bins_CvsB_jet2))
    SFl_hist = ROOT.TH2D("SFl_hist",";CvsL;CvsB;SFl",nbins_CvsL_jet3,array("d",custom_bins_CvsL_jet3),nbins_CvsB_jet3,array("d",custom_bins_CvsB_jet3))


    ###############################
    #
    #	READ FILES
    #
    ################################

    # MC
    for file in samples_MC:
        f = file.split(".root")[0]
        print f
        full_path = indir + "/" + f + ".root"
        if not os.path.isfile(full_path): continue
        f_ = ROOT.TFile(full_path)
        n_original_h = f_.Get("hweight")
        n_original = n_original_h.GetBinContent(1)
        f_.Close()
        print n_original

        hist_tmp_b1 = ROOT.TH2D("h_b1_"+f,";CvsL first add. jet;CvsB first add. jet;Events",nbins_CvsL_jet1,array("d",custom_bins_CvsL_jet1),nbins_CvsB_jet1,array("d",custom_bins_CvsB_jet1))
        hist_tmp_c1 = ROOT.TH2D("h_c1_"+f,";CvsL first add. jet;CvsB first add. jet;Events",nbins_CvsL_jet1,array("d",custom_bins_CvsL_jet1),nbins_CvsB_jet1,array("d",custom_bins_CvsB_jet1))
        hist_tmp_l1 = ROOT.TH2D("h_l1_"+f,";CvsL first add. jet;CvsB first add. jet;Events",nbins_CvsL_jet1,array("d",custom_bins_CvsL_jet1),nbins_CvsB_jet1,array("d",custom_bins_CvsB_jet1))
        hist_tmp_b2 = ROOT.TH2D("h_b2_"+f,";CvsL second add. jet;CvsB second add. jet;Events",nbins_CvsL_jet2,array("d",custom_bins_CvsL_jet2),nbins_CvsB_jet2,array("d",custom_bins_CvsB_jet2))
        hist_tmp_c2 = ROOT.TH2D("h_c2_"+f,";CvsL second add. jet;CvsB second add. jet;Events",nbins_CvsL_jet2,array("d",custom_bins_CvsL_jet2),nbins_CvsB_jet2,array("d",custom_bins_CvsB_jet2))
        hist_tmp_l2 = ROOT.TH2D("h_l2_"+f,";CvsL second add. jet;CvsB second add. jet;Events",nbins_CvsL_jet2,array("d",custom_bins_CvsL_jet2),nbins_CvsB_jet2,array("d",custom_bins_CvsB_jet2))
        hist_tmp_b3 = ROOT.TH2D("h_b3_"+f,";CvsL third add. jet;CvsB third add. jet;Events",nbins_CvsL_jet3,array("d",custom_bins_CvsL_jet3),nbins_CvsB_jet3,array("d",custom_bins_CvsB_jet3))
        hist_tmp_c3 = ROOT.TH2D("h_c3_"+f,";CvsL third add. jet;CvsB third add. jet;Events",nbins_CvsL_jet3,array("d",custom_bins_CvsL_jet3),nbins_CvsB_jet3,array("d",custom_bins_CvsB_jet3))
        hist_tmp_l3 = ROOT.TH2D("h_l3_"+f,";CvsL third add. jet;CvsB third add. jet;Events",nbins_CvsL_jet3,array("d",custom_bins_CvsL_jet3),nbins_CvsB_jet3,array("d",custom_bins_CvsB_jet3))
        t_ = ROOT.TChain("tree")
        t_.Add(full_path)
        weights_to_apply = weight_string
        t_.Draw("DeepCSVcTagCvsB_addJet1:DeepCSVcTagCvsL_addJet1>>h_b1_"+f,weights_to_apply+"*(hadronFlavour_addJet1 == 5)")
        t_.Draw("DeepCSVcTagCvsB_addJet1:DeepCSVcTagCvsL_addJet1>>h_c1_"+f,weights_to_apply+"*(hadronFlavour_addJet1 == 4)")
        t_.Draw("DeepCSVcTagCvsB_addJet1:DeepCSVcTagCvsL_addJet1>>h_l1_"+f,weights_to_apply+"*(hadronFlavour_addJet1 == 0)")
        t_.Draw("DeepCSVcTagCvsB_addJet2:DeepCSVcTagCvsL_addJet2>>h_b2_"+f,weights_to_apply+"*(hadronFlavour_addJet2 == 5)")
        t_.Draw("DeepCSVcTagCvsB_addJet2:DeepCSVcTagCvsL_addJet2>>h_c2_"+f,weights_to_apply+"*(hadronFlavour_addJet2 == 4)")
        t_.Draw("DeepCSVcTagCvsB_addJet2:DeepCSVcTagCvsL_addJet2>>h_l2_"+f,weights_to_apply+"*(hadronFlavour_addJet2 == 0)")
        t_.Draw("DeepCSVcTagCvsB_addJet3:DeepCSVcTagCvsL_addJet3>>h_b3_"+f,weights_to_apply+"*(hadronFlavour_addJet3 == 5)")
        t_.Draw("DeepCSVcTagCvsB_addJet3:DeepCSVcTagCvsL_addJet3>>h_c3_"+f,weights_to_apply+"*(hadronFlavour_addJet3 == 4)")
        t_.Draw("DeepCSVcTagCvsB_addJet3:DeepCSVcTagCvsL_addJet3>>h_l3_"+f,weights_to_apply+"*(hadronFlavour_addJet3 == 0)")


        xsec = xsec_table[f]*1000 #[fb]
        int_lumi=41.527 #[fb^-1	]35.921875594646 #27.271
        scale = float(xsec*int_lumi)/float(n_original)
        histo_dict["jet1"]["b"].Add(hist_tmp_b1,scale)
        histo_dict["jet1"]["c"].Add(hist_tmp_c1,scale)
        histo_dict["jet1"]["l"].Add(hist_tmp_l1,scale)
        histo_dict["jet2"]["b"].Add(hist_tmp_b2,scale)
        histo_dict["jet2"]["c"].Add(hist_tmp_c2,scale)
        histo_dict["jet2"]["l"].Add(hist_tmp_l2,scale)
        histo_dict["jet3"]["b"].Add(hist_tmp_b3,scale)
        histo_dict["jet3"]["c"].Add(hist_tmp_c3,scale)
        histo_dict["jet3"]["l"].Add(hist_tmp_l3,scale)

        del hist_tmp_b1
        del hist_tmp_c1
        del hist_tmp_l1
        del hist_tmp_b2
        del hist_tmp_c2
        del hist_tmp_l2
        del hist_tmp_b3
        del hist_tmp_c3
        del hist_tmp_l3

    
   
    #Data
    for file in samples_Data:
        f = file.split(".root")[0]
        print f
        full_path = indir + "/" + f + ".root"
        if not os.path.isfile(full_path): continue
        f_ = ROOT.TFile(full_path)
        t_ = ROOT.TChain("tree")
        t_.Add(full_path)

        hist_tmp_data1 = ROOT.TH2D("h_data1_"+f,";CvsL third add. jet;CvsB third add. jet;Events",nbins_CvsL_jet1,array("d",custom_bins_CvsL_jet1),nbins_CvsB_jet1,array("d",custom_bins_CvsB_jet1))
        hist_tmp_data2 = ROOT.TH2D("h_data2_"+f,";CvsL third add. jet;CvsB third add. jet;Events",nbins_CvsL_jet2,array("d",custom_bins_CvsL_jet2),nbins_CvsB_jet2,array("d",custom_bins_CvsB_jet2))
        hist_tmp_data3 = ROOT.TH2D("h_data3_"+f,";CvsL third add. jet;CvsB third add. jet;Events",nbins_CvsL_jet3,array("d",custom_bins_CvsL_jet3),nbins_CvsB_jet3,array("d",custom_bins_CvsB_jet3))
        t_.Draw("DeepCSVcTagCvsB_addJet1:DeepCSVcTagCvsL_addJet1>>h_data1_"+f)
        t_.Draw("DeepCSVcTagCvsB_addJet2:DeepCSVcTagCvsL_addJet2>>h_data2_"+f)
        t_.Draw("DeepCSVcTagCvsB_addJet3:DeepCSVcTagCvsL_addJet3>>h_data3_"+f)

        datahisto_dict["jet1"].Add(hist_tmp_data1.Clone())
        datahisto_dict["jet2"].Add(hist_tmp_data2.Clone())
        datahisto_dict["jet3"].Add(hist_tmp_data3.Clone())



    

    pickle.dump(histo_dict,open(outdir+"/MC_histograms2D.pkl","wb"))
    pickle.dump(datahisto_dict,open(outdir+"/Data_histograms2D.pkl","wb"))


def main():

    parser = ArgumentParser()
    parser.add_argument('--indir', default="FILL",help='input directory that contains all the samples')
    parser.add_argument('--outdir', default=os.getcwd(),help='name of output directory')
    parser.add_argument('--weightstring', default="weight_btag_iterativefit*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*mc_weight",help='weights to use')
    args = parser.parse_args()
    
    DeriveSFs(args.indir, args.outdir, args.weightstring)
    
    

if __name__ == "__main__":
	main()
