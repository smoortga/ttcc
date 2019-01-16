import ROOT
import os
import sys
from argparse import ArgumentParser
from array import array
from xsec import xsec_table, color_table, legend_array
from math import sqrt
import pickle

ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetOptStat(0)

parser = ArgumentParser()
parser.add_argument('--indir', default="FILL",help='input directory that contains all the samples')
parser.add_argument('--outdir', default=os.getcwd(),help='name of output directory')
parser.add_argument('--originalNeventsDict', default="/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/test/initial_nevents_dict_NewElectronIDv2.pkl",help='name of dictionary (pkl file) with original nevents')
args = parser.parse_args()


#syst_list=["weight_btag_iterativefit_JesUp","weight_btag_iterativefit_JesDown","weight_btag_iterativefit_HfUp","weight_btag_iterativefit_HfDown","weight_btag_iterativefit_Hfstats1Up","weight_btag_iterativefit_Hfstats1Down","weight_btag_iterativefit_Hfstats2Up","weight_btag_iterativefit_Hfstats2Down","weight_btag_iterativefit_Lfstats1Up","weight_btag_iterativefit_Lfstats1Down","weight_btag_iterativefit_Lfstats2Up","weight_btag_iterativefit_Lfstats2Down","weight_btag_iterativefit_Cferr1Up","weight_btag_iterativefit_Cferr1Down","weight_btag_iterativefit_Cferr2Up","weight_btag_iterativefit_Cferr2Down"]
syst_list=["weight_ctag_iterativefit_Up","weight_ctag_iterativefit_Down"]


display_dict = {
    3:    {"legend":"t#bar{t}b#bar{b}",
            "samples":["TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS","TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS","TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS"],
            "color":ROOT.kRed+3,
            "category":0
            },
    # 2:    {"legend":"t#bar{t}bc",
#             "samples":["TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS","TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS","TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS"],
#             "color":ROOT.kOrange+6,
#             "category":1
#             },
    4:    {"legend":"t#bar{t}bj",
            "samples":["TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS","TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS","TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS"],
            "color":ROOT.kRed+2,
            "category":1
            },
    1:    {"legend":"t#bar{t}c#bar{c}",
            "samples":["TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS","TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS","TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS"],
            "color":ROOT.kOrange-2,
            "category":2
            },
    2:    {"legend":"t#bar{t}cj",
            "samples":["TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS","TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS","TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS"],
            "color":ROOT.kOrange-7,
            "category":3
            },
    5:    {"legend":"t#bar{t}jj",
            "samples":["TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS","TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS","TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS"],
            "color":ROOT.kRed-7,
            "category":4
            },
    6:    {"legend":"t#bar{t} + Other",
           "samples":["TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS","TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS","TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS"],
           "color":ROOT.kOrange+6,
           "category":-1
           },
    7:    {"legend":"Single top",
            "samples":["ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8","ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8","ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8","ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8","ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8"], #
            "color":ROOT.kCyan+1,
            "category":-1
            },
    8:    {"legend":"Z + jets",
            "samples":["DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8"],#,"DYJetsToLL_M-5to50_TuneCP5_13TeV-madgraphMLM-pythia8"],#,"DYJetsToLL_M-4to50_HT-70to100_TuneCP5_13TeV-madgraphMLM-pythia8","DYJetsToLL_M-4to50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8","DYJetsToLL_M-4to50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8","DYJetsToLL_M-4to50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8","DYJetsToLL_M-4to50_HT-600toInf_TuneCP5_13TeV-madgraphMLM-pythia8"],#,"DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8_ext"],#,"DYJetsToLL_M-4to50_HT-70to100_TuneCP5_13TeV-madgraphMLM-pythia8","DYJetsToLL_M-4to50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8","DYJetsToLL_M-4to50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8","DYJetsToLL_M-4to50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8","DYJetsToLL_M-4to50_HT-600toInf_TuneCP5_13TeV-madgraphMLM-pythia8"],
            "color":ROOT.kBlue,
            "category":-1
            },
   #  1:    {"legend":"Diboson",
#             "samples":["WW_TuneCP5_13TeV-pythia8","WZ_TuneCP5_13TeV-pythia8","ZZ_TuneCP5_13TeV-pythia8"],
#             "color":402,
#             "category":-1
#             },           
    9:    {"legend":"Rare",
            "samples":["WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8","WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8","WZZ_TuneCP5_13TeV-amcatnlo-pythia8","WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8","ZZZ_TuneCP5_13TeV-amcatnlo-pythia8","WW_TuneCP5_13TeV-pythia8","WZ_TuneCP5_13TeV-pythia8","ZZ_TuneCP5_13TeV-pythia8","ttHJetTobb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8","ttHJetToNonbb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8","WW_TuneCP5_13TeV-pythia8","WZ_TuneCP5_13TeV-pythia8","ZZ_TuneCP5_13TeV-pythia8"],
            "color":1,
            "category":-1
            },
    # 9:    {"legend":"W + jets",
#             "samples":["WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8"],
#             "color":ROOT.kMagenta+1,
#             "category":-1
#             },
    # 9:    {"legend":"t#bar{t}V",
#             "samples":["ttZJets_13TeV_madgraphMLM","ttWJets_13TeV_madgraphMLM"],
#             "color":ROOT.kMagenta+1,
#             "category":-1
#             },
#     10:    {"legend":"ttH (h #rightarrow b#bar{b})",
#             "samples":["ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8"],
#             "color":1,
#             "category":-1
#             },
    -1:    {"legend":"data",
            "samples":["DoubleMuon_Run2017E_31Mar2018_v1_MINIAOD","DoubleEG_Run2017B_31Mar2018_v1_MINIAOD","MuonEG_Run2017C_31Mar2018_v1_MINIAOD","MuonEG_Run2017E_31Mar2018_v1_MINIAOD",
                        "DoubleMuon_Run2017F_31Mar2018_v1_MINIAOD","DoubleMuon_Run2017C_31Mar2018_v1_MINIAOD","MuonEG_Run2017F_31Mar2018_v1_MINIAOD","DoubleEG_Run2017D_31Mar2018_v1_MINIAOD",
                        "DoubleMuon_Run2017D_31Mar2018_v1_MINIAOD","DoubleEG_Run2017C_31Mar2018_v1_MINIAOD","MuonEG_Run2017B_31Mar2018_v1_MINIAOD","DoubleMuon_Run2017B_31Mar2018_v1_MINIAOD",
                        "DoubleEG_Run2017F_31Mar2018_v1_MINIAOD","DoubleEG_Run2017E_31Mar2018_v1_MINIAOD","MuonEG_Run2017D_31Mar2018_v1_MINIAOD"
                        ],
            "color":1,
            "category":-1
            }
}


original_nevents_dict = pickle.load(open(args.originalNeventsDict,"rb"))

def Plot1D(var,x_name,y_name,nbins,xmin,xmax,use_custom_bins = 0,custom_bins = [0,1,2],logy=1,overflow=0,underflow=0,weights_to_apply="", lepton_category="", suffix="",NormalizeMCToData=True,AddSystUnc = False):

    ###############################
    #
    #	PREAPRE HISTOGRAMS
    #
    ################################
    binwidth = float(xmax-xmin)/nbins
    if "[" in x_name: units_x = x_name.split("[")[1].split("]")[0]
    else: units_x = ""
    if use_custom_bins:
        datahist = ROOT.TH1D("data",";%s;%s"%(x_name,y_name),nbins,array("d",custom_bins))
    else:
        datahist = ROOT.TH1D("data",";%s;%s / %.1f %s"%(x_name,y_name,binwidth,units_x),nbins,xmin,xmax)
    datahist.Sumw2()
    MC_hists = {}
    for order in range(max(display_dict.keys())):
        if use_custom_bins: MC_hists[order+1] = ROOT.TH1D("MC_%i"%(order+1),";%s;%s"%(x_name,y_name),nbins,array("d",custom_bins))
        else: MC_hists[order+1] = ROOT.TH1D("MC_%i"%(order+1),";%s;%s / %.1f %s"%(x_name,y_name,binwidth,units_x),nbins,xmin,xmax)
        MC_hists[order+1].Sumw2()
    ratio_hist = ROOT.TH1D("ratio",";%s;Data/MC"%(x_name),nbins,xmin,xmax)
    ratio_hist.Sumw2()
    
    # For systematics caluclations --> dictionary of form (for example): {"btagJesUp":{"0":TH1D(),"1":TH1D(),...}, "btagJesDown":{"0":TH1D(),"1":TH1D(),...} }
    if AddSystUnc:
        syst_MC_hists = {}
        for syst_source in syst_list:
            syst_MC_hists[syst_source] = {}
            for order in range(max(display_dict.keys())):
                if use_custom_bins:syst_MC_hists[syst_source][order+1] = ROOT.TH1D("MC_%s_%i"%(syst_source,order+1),";%s;%s"%(x_name,y_name),nbins,array("d",custom_bins))
                else: syst_MC_hists[syst_source][order+1] = ROOT.TH1D("MC_%s_%i"%(syst_source,order+1),";%s;%s / %.1f %s"%(x_name,y_name,binwidth,units_x),nbins,xmin,xmax)
                syst_MC_hists[syst_source][order+1].Sumw2()
    ###############################
    #
    #	READ FILES
    #
    ################################

    # MC
    for idx,entry_dict in display_dict.iteritems():
        if entry_dict["legend"]=="data": continue
        for f in entry_dict["samples"]:
            print f
            full_path = args.indir + "/" + f + ".root"
            if not os.path.isfile(full_path): continue
            f_ = ROOT.TFile(full_path)
            n_original_h = f_.Get("hweight")
            n_original = n_original_h.GetBinContent(1)
            #n_original = original_nevents_dict[f+".root"]
            f_.Close()
            print n_original
            
            if use_custom_bins: hist_tmp = ROOT.TH1D("h_"+f,";%s;%s"%(x_name,y_name),nbins,array("d",custom_bins))
            else: hist_tmp = ROOT.TH1D("h_"+f,";%s;%s / %.2f %s"%(x_name,y_name,binwidth,units_x),nbins,xmin,xmax)
            t_ = ROOT.TChain("tree")
            t_.Add(full_path)
            if (lepton_category == "elmu" or lepton_category=="muel"): weights_to_apply = "(lepton_Category==2)*"+weights_to_apply
            elif lepton_category == "elel": weights_to_apply = "(lepton_Category==0)*"+weights_to_apply
            elif lepton_category == "mumu": weights_to_apply = "(lepton_Category==1)*"+weights_to_apply
            else: weights_to_apply = weights_to_apply
            t_.Draw(var+">>h_"+f,weights_to_apply+"*(event_Category_VisiblePS == %s)*(mc_pu_trueNumInt>10 && mc_pu_trueNumInt<70)"%entry_dict["category"])#*(mc_pu_trueNumInt>0)*(mc_pu_trueNumInt>10 && mc_pu_trueNumInt<70)
            t_.GetEntry(1)
            if t_.is_data == 1:
                continue
            # put underflow in the first bin
            if underflow: hist_tmp.SetBinContent(1,hist_tmp.GetBinContent(0)+hist_tmp.GetBinContent(1))
            
            xsec = xsec_table[f]*1000 #[fb]
            int_lumi=41.527 #[fb^-1	]35.921875594646 #27.271
            scale = float(xsec*int_lumi)/float(n_original)
            MC_hists[idx].Add(hist_tmp,scale)
            MC_hists[idx].SetFillColor(entry_dict["color"])
            del hist_tmp
            
            # Adding systematic uncertainty belt according to sources listed in syst_list
            if AddSystUnc:
                for syst_source in syst_list:
                    if use_custom_bins: hist_tmp = ROOT.TH1D("h_"+f+"_"+syst_source,";%s;%s"%(x_name,y_name),nbins,array("d",custom_bins))
                    else: hist_tmp = ROOT.TH1D("h_"+f+"_"+syst_source,";%s;%s / %.2f %s"%(x_name,y_name,binwidth,units_x),nbins,xmin,xmax)
                    #weights_to_apply_tmp = weights_to_apply# + "*" + syst_source # THIS NEEDS TO BE CHANGED!!! REPLACE CENTRAL SOURCE BY UP/DOWN SOURCE
                    #affected_weight = weights_to_apply.split("_")[:-1]
                    #weights_to_apply_tmp = "weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*"+syst_source
                    weights_to_apply_tmp = "weight_bcjets_btag_DeepCSVMedium*weight_udsgjets_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight*"+syst_source
                    t_.Draw(var+">>h_"+f+"_"+syst_source,weights_to_apply_tmp+"*(event_Category_VisiblePS == %s)*(mc_pu_trueNumInt>10 && mc_pu_trueNumInt<70)"%entry_dict["category"])
                    syst_MC_hists[syst_source][idx].Add(hist_tmp,scale)
    
    #Data
    entry_dict = display_dict[-1]
    samples_to_process = [i for i in entry_dict["samples"]]
    for f in samples_to_process:
        print f
        full_path = args.indir + "/" + f + ".root"
        if use_custom_bins: hist_tmp = ROOT.TH1D("h_"+f,";%s;%s"%(x_name,y_name),nbins,array("d",custom_bins))
        else: hist_tmp = ROOT.TH1D("h_"+f,";%s;%s / %.2f %s"%(x_name,y_name,binwidth,units_x),nbins,xmin,xmax)
        t_ = ROOT.TChain("tree")
        t_.Add(full_path)
        if (lepton_category == "elmu" or lepton_category=="muel"): t_.Draw(var+">>h_"+f,"(lepton_Category==2)")
        elif (lepton_category == "elel"): t_.Draw(var+">>h_"+f,"(lepton_Category==0)")
        elif (lepton_category == "mumu"): t_.Draw(var+">>h_"+f,"(lepton_Category==1)")
        else: t_.Draw(var+">>h_"+f)
        t_.GetEntry(1)
        if t_.is_data == 0:
            print "MIGHT NOT BE DATA, SKIPPING"
            continue
        if underflow: hist_tmp.SetBinContent(1,hist_tmp.GetBinContent(0)+hist_tmp.GetBinContent(1))
        datahist.Add(hist_tmp.Clone())
        #print "DATA INTEGRAL %s: "%f, hist_tmp.Integral()
        del hist_tmp
    
    
    print "DATA INTEGRAL: ", datahist.Integral()
    

    ###############################
    #
    #	STYLE
    #
    ################################
    datahist.SetMarkerStyle(20)
    datahist.SetLineColor(1)
    datahist.SetLineWidth(2)
    
    if overflow: datahist.GetXaxis().SetRange(1,datahist.GetNbinsX()+1)
    for idx,hist in MC_hists.iteritems():
        hist.SetLineWidth(0)
        if overflow: hist.GetXaxis().SetRange(1,hist.GetNbinsX()+1)
            

    ###############################
    #
    #	PLOTTING
    #
    ################################
    c = ROOT.TCanvas("c","c",800,700)
    c.cd()
    uppad = ROOT.TPad("u","u",0.,0.25,1.,1.)
    downpad = ROOT.TPad("d","d",0.,0.0,1.,0.25)
    uppad.Draw()
    downpad.Draw()

    uppad.cd()
    ROOT.gPad.SetLogy(logy)
    ROOT.gPad.SetMargin(0.15,0.05,0.01,0.1)
    if use_custom_bins:
        mg = ROOT.THStack("mg",";%s;%s"%(x_name,y_name))
        summed_MC_hist = ROOT.TH1F("h_summed",";%s;%s"%(x_name,y_name),nbins,array("d",custom_bins))
    else:
        mg = ROOT.THStack("mg",";%s;%s / %.2f %s"%(x_name,y_name,binwidth,units_x))
        summed_MC_hist = ROOT.TH1F("h_summed",";%s;%s / %.2f %s"%(x_name,y_name,binwidth,units_x),nbins,xmin,xmax)
    summed_MC_hist.Sumw2()
    
    if AddSystUnc:
        summed_syst_hists={}
        for syst_source in syst_list:
            if use_custom_bins: summed_syst_hists[syst_source] = ROOT.TH1D("h_summed_"+syst_source,";%s;%s"%(x_name,y_name),nbins,array("d",custom_bins))
            else: summed_syst_hists[syst_source] = ROOT.TH1D("h_summed_"+syst_source,";%s;%s / %.2f %s"%(x_name,y_name,binwidth,units_x),nbins,xmin,xmax)
            for idx,hist in syst_MC_hists[syst_source].iteritems():
                summed_syst_hists[syst_source].Add(hist)
            
            
    
    for idx,hist in MC_hists.iteritems():
        mg.Add(hist,"f")
        summed_MC_hist.Add(hist)  
    mg.Draw("hist")
    
    #In case of MC-data-normalization
    if (NormalizeMCToData):
        print "MC yield has been normalized to Data yield by a factor data/MC = ",datahist.Integral()/summed_MC_hist.Integral()
        norm_scale=datahist.Integral()/summed_MC_hist.Integral()
        for idx,hist in MC_hists.iteritems():
            hist.Scale(norm_scale) 
        summed_MC_hist.Scale(norm_scale)
        if AddSystUnc:
            for syst_source in syst_list:
                summed_syst_hists[syst_source].Scale(norm_scale)#summed_syst_hists[syst_source].Integral())
        
    mg.GetHistogram().SetLineWidth(0)
    if overflow: 
        mg.GetXaxis().SetRange(1,mg.GetHistogram().GetNbinsX()+1)
        summed_MC_hist.GetXaxis().SetRange(1,summed_MC_hist.GetNbinsX()+1)
        datahist.GetXaxis().SetRange(1,datahist.GetNbinsX()+1)
    ROOT.TGaxis.SetMaxDigits(3)
    if (logy): 
        mg.SetMinimum(1)
        mg.SetMaximum(2*summed_MC_hist.GetBinContent(summed_MC_hist.GetMaximumBin())**2)
    else:
        mg.SetMinimum(0.1)
        mg.SetMaximum(2*summed_MC_hist.GetBinContent(summed_MC_hist.GetMaximumBin()))
    mg.GetYaxis().SetLabelSize(0.05)
    mg.GetYaxis().SetLabelOffset(0.01)
    mg.GetYaxis().SetTitleSize(0.06)
    mg.GetYaxis().SetTitleOffset(1.2)
    mg.GetXaxis().SetTitleSize(0.0)
    mg.GetXaxis().SetLabelSize(0.0)
    
    
    # Error on the MC stats (and systematics if needed)
    if AddSystUnc:
        #mg = ROOT.TMultiGraph()
        graph_x = array("d",[1]*summed_MC_hist.GetNbinsX())
        graph_y = array("d",[1]*summed_MC_hist.GetNbinsX())
        graph_exl = array("d",[0]*summed_MC_hist.GetNbinsX())
        graph_exh = array("d",[0]*summed_MC_hist.GetNbinsX())
        graph_eyl = array("d",[0]*summed_MC_hist.GetNbinsX())
        graph_eyh = array("d",[0]*summed_MC_hist.GetNbinsX())
        for ibin in range(summed_MC_hist.GetNbinsX()):
            graph_eyh[ibin] = summed_MC_hist.GetBinError(ibin+1)
            graph_eyl[ibin] = summed_MC_hist.GetBinError(ibin+1)
            graph_exl[ibin] = summed_MC_hist.GetBinCenter(ibin+1)-summed_MC_hist.GetXaxis().GetBinLowEdge(ibin+1)
            graph_exh[ibin] = summed_MC_hist.GetXaxis().GetBinLowEdge(ibin+2) - summed_MC_hist.GetBinCenter(ibin+1)
            graph_x[ibin] = summed_MC_hist.GetBinCenter(ibin+1)
            graph_y[ibin] = summed_MC_hist.GetBinContent(ibin+1)
        
        for syst_source in syst_list:
            summed_syst_hists[syst_source].Add(summed_MC_hist,-1)
            for ibin in range(summed_MC_hist.GetNbinsX()):
                #orig_error = summed_MC_hist.GetBinError(ibin+1)
                #summed_MC_hist.SetBinError(ibin+1,sqrt(orig_error**2 + (summed_syst_hists[syst_source].GetBinContent(ibin+1))**2))
                
                this_error = summed_syst_hists[syst_source].GetBinContent(ibin+1)
                #print syst_source, this_error
                if this_error >= 0: graph_eyh[ibin] = sqrt(graph_eyh[ibin]**2 + (this_error)**2)
                if this_error < 0: graph_eyl[ibin] = sqrt(graph_eyl[ibin]**2 + (this_error)**2)
                
       # print graph_eyl,graph_eyh
               
        summed_MC_hist.SetFillStyle(3244)
        summed_MC_hist.SetFillColor(13)
        summed_MC_hist.SetLineWidth(0)
        #summed_MC_hist.Draw("same E2")
        summed_assymGraph = ROOT.TGraphAsymmErrors(len(graph_x),graph_x,graph_y,graph_exl,graph_exh,graph_eyl,graph_eyh)
        summed_assymGraph.SetFillColor(13)
        summed_assymGraph.SetFillStyle(3244)
        summed_assymGraph.Draw("2")
    
    else:
        summed_MC_hist.SetFillStyle(3244)
        summed_MC_hist.SetFillColor(13)
        summed_MC_hist.SetLineWidth(0)
        summed_MC_hist.Draw("same E2")
    
    datahist.Draw("epx0 same")

    #redraw borders
    ROOT.gPad.RedrawAxis()
    line = ROOT.TLine()
    if overflow: 
        if use_custom_bins: line.DrawLine(xmax+(custom_bins[-1]-custom_bins[-2]), ROOT.gPad.GetUymin(), xmax+(custom_bins[-1]-custom_bins[-2]), ROOT.gPad.GetUymax())
        else:line.DrawLine(xmax+binwidth, ROOT.gPad.GetUymin(), xmax+binwidth, ROOT.gPad.GetUymax())
    else:line.DrawLine(xmax, ROOT.gPad.GetUymin(), xmax, ROOT.gPad.GetUymax())
#     
    #########
    # TEXT
    #########
    lumi = "%.1f"%int_lumi
    year = "2017"
    latex = ROOT.TLatex()
    latex.SetTextFont(42)
    latex.SetTextSize(0.05)
    latex.SetTextAlign(32)
    latex.DrawLatexNDC(0.94,0.94,lumi+" fb^{-1}, "+year)
    
    latex_cms = ROOT.TLatex()
    latex_cms.SetTextFont(42)
    latex_cms.SetTextSize(0.06)
    latex_cms.SetTextAlign(11)
    latex_cms.DrawLatexNDC(0.19,0.83,"#bf{CMS} #it{Preliminary}")
    
    latex_lepton_category = ROOT.TLatex()
    latex_lepton_category.SetTextFont(42)
    latex_lepton_category.SetTextSize(0.06)
    latex_lepton_category.SetTextAlign(11)
    if (lepton_category == "elmu" or lepton_category=="muel"): latex_lepton_category.DrawLatexNDC(0.19,0.75,"e^{#pm}#mu^{#mp} channel")
    elif (lepton_category == "elel"): latex_lepton_category.DrawLatexNDC(0.19,0.75,"e^{+}e^{-} channel")
    elif (lepton_category == "mumu"): latex_lepton_category.DrawLatexNDC(0.19,0.75,"#mu^{+}#mu^{-} channel")
    else: latex_lepton_category.DrawLatexNDC(0.19,0.75,"dilepton channel")
    
    
    if (NormalizeMCToData): 
        latex_normalized = ROOT.TLatex()   
        latex_normalized.SetTextFont(72)
        latex_normalized.SetTextSize(0.04)
        latex_normalized.SetTextAlign(11)
        latex_normalized.DrawLatexNDC(0.19,0.68,"MC normalized to data")
    
    #############
    # LEGEND
    #############
    if len(display_dict.keys()) <= 4: 
        l = ROOT.TLegend(0.7,0.55,0.94,0.89)
        l.SetNColumns(1)
    elif len(display_dict.keys()) > 4: 
        l = ROOT.TLegend(0.5,0.55,0.94,0.89)
        l.SetNColumns(2)
    entries_dict={}
    for idx,e in display_dict.iteritems():
        if idx == -1: continue
        entries_dict[e["legend"]]=l.AddEntry(None,e["legend"],"f")
        entries_dict[e["legend"]].SetFillStyle(1000)
        entries_dict[e["legend"]].SetFillColor(e["color"])
        entries_dict[e["legend"]].SetLineWidth(0)
    l.AddEntry(datahist,"Data","ep")
    if AddSystUnc: l.AddEntry(summed_MC_hist,"stat. + syst.","f")
    else: l.AddEntry(summed_MC_hist,"MC stat. unc.","f")
    l.SetBorderSize(0)
    l.SetTextSize(0.05)
    l.Draw("same")
    
    
    
    

    downpad.cd()
    ROOT.gPad.SetMargin(0.15,0.05,0.4,0.01)
    #ratio hist
    ratio_hist = datahist.Clone()
    ratio_hist.Divide(summed_MC_hist)
    ratio_hist.SetMarkerStyle(20)
    ratio_hist.Draw("pe1x0")
    ratio_hist.GetYaxis().SetRangeUser(0.3,1.7)
    ratio_hist.GetYaxis().SetNdivisions(4)
    ratio_hist.GetYaxis().SetLabelSize(0.14)
    ratio_hist.GetYaxis().SetLabelOffset(0.01)
    ratio_hist.GetYaxis().SetTitle("#frac{data}{MC}")
    ratio_hist.GetYaxis().SetTitleSize(0.16)
    ratio_hist.GetYaxis().CenterTitle()
    ratio_hist.GetYaxis().SetTitleOffset(0.4)
    ratio_hist.GetXaxis().SetTitleSize(0.19)
    ratio_hist.GetXaxis().SetTitleOffset(0.9)
    ratio_hist.GetXaxis().SetLabelSize(0.14)
    
    # MC stat uncertainty
    if AddSystUnc:
        ratio_graph_x = graph_x
        ratio_graph_y = array("d",[1]*summed_MC_hist.GetNbinsX())
        ratio_graph_exl = graph_exl
        ratio_graph_exh = graph_exh
        ratio_graph_eyl = array("d",[0]*summed_MC_hist.GetNbinsX())
        ratio_graph_eyh = array("d",[0]*summed_MC_hist.GetNbinsX())
        for ibin in range(summed_MC_hist.GetNbinsX()):
            ratio_graph_eyh[ibin] = float(graph_eyh[ibin])/float(graph_y[ibin])
            ratio_graph_eyl[ibin] = float(graph_eyl[ibin])/float(graph_y[ibin])
            ratio_graph_x[ibin] = summed_MC_hist.GetBinCenter(ibin+1)
        
        ratio_assymGraph = ROOT.TGraphAsymmErrors(len(ratio_graph_x),ratio_graph_x,ratio_graph_y,ratio_graph_exl,ratio_graph_exh,ratio_graph_eyl,ratio_graph_eyh)
        ratio_assymGraph.SetFillColor(13)
        ratio_assymGraph.SetFillStyle(3244)
        ratio_assymGraph.Draw("2")
    else: 
        MC_ratio_hist = summed_MC_hist.Clone()
        MC_ratio_hist.Divide(summed_MC_hist)
        MC_ratio_hist.Draw("same E2")
    
    
    #Redraw ratio_hist
    ratio_hist.Draw("same pe1x0")
    
    
    
    line3 = ROOT.TLine()
    line3.SetLineColor(1)
    line3.SetLineStyle(2)
    line3.SetLineWidth(2)
    if overflow: 
        if use_custom_bins: line3.DrawLine(xmin, 1, xmax+(custom_bins[-1]-custom_bins[-2]), 1)
        else: line3.DrawLine(xmin, 1, xmax+binwidth, 1)
    else: line3.DrawLine(xmin, 1, xmax, 1)
    line3.SetLineWidth(1)
    if overflow: 
        if use_custom_bins: line3.DrawLine(xmin, 0.75, xmax+(custom_bins[-1]-custom_bins[-2]), 0.75)
        else:line3.DrawLine(xmin, 0.75, xmax+binwidth, 0.75)
    else: line3.DrawLine(xmin, 0.75, xmax, 0.75)
    if overflow: 
        if use_custom_bins: line3.DrawLine(xmin, 1.25, xmax+(custom_bins[-1]-custom_bins[-2]), 1.25)
        else: line3.DrawLine(xmin, 1.25, xmax+binwidth, 1.25)
    else: line3.DrawLine(xmin, 1.25, xmax, 1.25)

	
    if not os.path.isdir(args.outdir): os.mkdir(args.outdir)
	
    lepton_category_postfix = ""
    if ( (lepton_category == "elmu") or (lepton_category == "muel") or (lepton_category == "elel") or (lepton_category == "mumu") ) :lepton_category_postfix = "_"+lepton_category
    else: lepton_category_postfix = "_ll"
    if (logy): 
        c.SaveAs(args.outdir+"/"+var+"%s%s_stacked_Log.pdf"%(lepton_category_postfix,suffix))
        c.SaveAs(args.outdir+"/"+var+"%s%s_stacked_Log.png"%(lepton_category_postfix,suffix))
        c.SaveAs(args.outdir+"/"+var+"%s%s_stacked_Log.C"%(lepton_category_postfix,suffix))
    else: 
        c.SaveAs(args.outdir+"/"+var+"%s%s_stacked_Linear.pdf"%(lepton_category_postfix,suffix))
        c.SaveAs(args.outdir+"/"+var+"%s%s_stacked_Linear.png"%(lepton_category_postfix,suffix))
        c.SaveAs(args.outdir+"/"+var+"%s%s_stacked_Linear.C"%(lepton_category_postfix,suffix))
    




def main():
    
    # 
    # HOW TO CALCULATE LUMI
    #    https://cms-service-lumi.web.cern.ch/cms-service-lumi/brilwsdoc.html
    # 
    # export PATH=$HOME/.local/bin:/afs/cern.ch/cms/lumi/brilconda-1.1.7/bin:$PATH
    # 
    # brilcalc lumi --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -i ./Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt
    #
    
    
    #weight_string = "weight_btag_iterativefit*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*pu_weight*mc_weight"
    weight_string = "weight_bcjets_btag_DeepCSVMedium*weight_udsgjets_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"#weight_btag_iterativefit*
    weight_string_withcTagWeights = "weight_ctag_iterativefit*weight_bcjets_btag_DeepCSVMedium*weight_udsgjets_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
    weight_string_noPUweights = "weight_ctag_iterativefit*weight_bcjets_btag_DeepCSVMedium*weight_udsgjets_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight"
    weights_string_noBtagWeights = "weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*pu_weight*mc_weight"
    
    no_weights = "1"
    lepton_channel="inclusive"#"mumu"#"elmu","inclusive","elel"
    
    custom_bins_ttHFSelector_CvsL = [0,0.1,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1.0]
    Plot1D("ttHF_selector_NN_CvsL","#Delta_{L}^{c} discriminator","Events",len(custom_bins_ttHFSelector_CvsL)-1,min(custom_bins_ttHFSelector_CvsL),max(custom_bins_ttHFSelector_CvsL),use_custom_bins = 1,custom_bins =custom_bins_ttHFSelector_CvsL,logy=1,overflow=0,underflow=1,weights_to_apply=weight_string,lepton_category=lepton_channel)
    Plot1D("ttHF_selector_NN_CvsL","#Delta_{L}^{c} discriminator","Events",len(custom_bins_ttHFSelector_CvsL)-1,min(custom_bins_ttHFSelector_CvsL),max(custom_bins_ttHFSelector_CvsL),use_custom_bins = 1,custom_bins =custom_bins_ttHFSelector_CvsL,logy=1,overflow=0,underflow=1,weights_to_apply=weight_string_withcTagWeights,lepton_category=lepton_channel,suffix="_WithcTagWeights",AddSystUnc = True)
    custom_bins_ttHFSelector_CvsB = [0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,1.0]
    Plot1D("ttHF_selector_NN_CvsB","#Delta_{b}^{c} discriminator","Events",len(custom_bins_ttHFSelector_CvsB)-1,min(custom_bins_ttHFSelector_CvsB),max(custom_bins_ttHFSelector_CvsB),use_custom_bins = 1,custom_bins =custom_bins_ttHFSelector_CvsB,logy=1,overflow=0,underflow=1,weights_to_apply=weight_string,lepton_category=lepton_channel)
    Plot1D("ttHF_selector_NN_CvsB","#Delta_{b}^{c} discriminator","Events",len(custom_bins_ttHFSelector_CvsB)-1,min(custom_bins_ttHFSelector_CvsB),max(custom_bins_ttHFSelector_CvsB),use_custom_bins = 1,custom_bins =custom_bins_ttHFSelector_CvsB,logy=1,overflow=0,underflow=1,weights_to_apply=weight_string_withcTagWeights,lepton_category=lepton_channel,suffix="_WithcTagWeights",AddSystUnc = True)
    
    #sys.exit(1)
    
    Plot1D("nvertex","Number of primary vertices","Events",int(70),-0.5,69.5,logy=0,overflow=0,weights_to_apply= weight_string_withcTagWeights,lepton_category=lepton_channel)
    Plot1D("nvertex","Number of primary vertices (before PU weights)","Events",int(70),-0.5,69.5,logy=0,overflow=0,weights_to_apply=weight_string_noPUweights,lepton_category=lepton_channel,suffix="_NoPUWeights")
    
    #custom_bins_TopMatchingNN = [0.7,0.9,0.92,0.94,0.95,0.96,0.97,0.98,0.99,0.995,1.0]
    custom_bins_ttHFSelector = [0,0.05,0.075,0.1,0.15,0.2,0.25,0.3,0.4,0.5,0.6,0.7,1.0]
    #Plot1D("ttHF_selector_NN","ttHF selector NN output","Events",len(custom_bins_ttHFSelector)-1,min(custom_bins_ttHFSelector),max(custom_bins_ttHFSelector),use_custom_bins = 1,custom_bins =custom_bins_ttHFSelector,logy=1,overflow=0,underflow=1,weights_to_apply=weight_string,lepton_category=lepton_channel)
    custom_bins_TopMatchingNN = [0.5,0.6,0.7,0.8,0.85,0.9,0.925,0.95,0.975,1.0]
    Plot1D("TopMatching_NN_best_value","Top matching NN value","Events",len(custom_bins_TopMatchingNN)-1,min(custom_bins_TopMatchingNN),max(custom_bins_TopMatchingNN),use_custom_bins = 1,custom_bins =custom_bins_TopMatchingNN,logy=1,overflow=0,underflow=1,weights_to_apply=weight_string_withcTagWeights,lepton_category=lepton_channel)
    #Plot1D("Jets._DeepCSVBDiscr","DeepCSVBDiscr discriminator (No btag weights)","Jets",40,0,1,logy=1,overflow=0,weights_to_apply=weights_string_noBtagWeights,lepton_category=lepton_channel,suffix="_NoBtagWeights")
#     Plot1D("Jets._DeepCSVCvsL","DeepCSVCvsL discriminator(No btag weights)","Jets",40,0,1,logy=1,overflow=0,weights_to_apply=weights_string_noBtagWeights,lepton_category=lepton_channel,suffix="_NoBtagWeights")
# 
    #Plot1D("Jets._DeepCSVBDiscr","DeepCSVBDiscr discriminator","Jets",40,0,1,logy=1,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     Plot1D("Jets._DeepCSVCvsL","DeepCSVCvsL discriminator","Jets",40,0,1,logy=1,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)

    Plot1D("MET._pt","p_{T}^{miss} [GeV]","Events",40,0,300,logy=1,overflow=1,weights_to_apply=weight_string_withcTagWeights,lepton_category=lepton_channel)
    #Plot1D("MET._ET","E_{T}^{miss} [GeV]","Events",40,0,5000,logy=0,overflow=1,weights_to_apply=weight_string_withcTagWeights,lepton_category=lepton_channel)

    Plot1D("lepton_Category","lepton category","Events",3,-0.5,2.5,logy=0,weights_to_apply=weight_string_withcTagWeights,lepton_category=lepton_channel)
    Plot1D("DileptonInvariantMass","m_{ll} [GeV]","Events",20,0,500,logy=0,weights_to_apply=weight_string_withcTagWeights,lepton_category=lepton_channel)
    Plot1D("DileptonDeltaR","#DeltaR(l,l)","Events",20,0,6,logy=0,weights_to_apply=weight_string_withcTagWeights,lepton_category=lepton_channel)
    Plot1D("DeltaR_addJets","#DeltaR(add. jet 1,add. jet 2)","Events",20,0,6,logy=0,weights_to_apply=weight_string_withcTagWeights,lepton_category=lepton_channel)
    Plot1D("Minv_addJets","M_{inv}(add. jet 1,add. jet 2) [GeV]","Events",20,0,500,logy=0,weights_to_apply=weight_string_withcTagWeights,lepton_category=lepton_channel)
    
    
    
    #sys.exit(1)
#     Plot1D("CSVv2_addJet1","CSVv2 Discriminator first add. jet","Events",10,0,1,logy=1,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     Plot1D("CSVv2_addJet2","CSVv2 Discriminator second add. jet","Events",10,0,1,logy=1,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     #Plot1D("CSVv2_addJet1","CSVv2 Discriminator first add. jet","Events",10,0,1,logy=0,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     #Plot1D("CSVv2_addJet2","CSVv2 Discriminator second add. jet","Events",10,0,1,logy=0,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
    custom_bins_DeepCSVBdiscr = [ 0.,0.025,0.05,0.1,0.15,0.2,0.25,0.35,0.45,0.6,0.8,1.0]
    Plot1D("DeepCSVBDiscr_addJet1","DeepCSVBDiscr Discriminator first add. jet","Events",len(custom_bins_DeepCSVBdiscr)-1,min(custom_bins_DeepCSVBdiscr),max(custom_bins_DeepCSVBdiscr),use_custom_bins = 1,custom_bins =custom_bins_DeepCSVBdiscr,logy=1,overflow=0,underflow=1,weights_to_apply=weight_string,lepton_category=lepton_channel)#,AddSystUnc = True)
    Plot1D("DeepCSVBDiscr_addJet2","DeepCSVBDiscr Discriminator second add. jet","Events",len(custom_bins_DeepCSVBdiscr)-1,min(custom_bins_DeepCSVBdiscr),max(custom_bins_DeepCSVBdiscr),use_custom_bins = 1,custom_bins =custom_bins_DeepCSVBdiscr,logy=1,overflow=0,underflow=1,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     Plot1D("DeepCSVBDiscr_addJet1","DeepCSVBDiscr Discriminator first add. jet (no btag weights)","Events",len(custom_bins_DeepCSVBdiscr)-1,min(custom_bins_DeepCSVBdiscr),max(custom_bins_DeepCSVBdiscr),use_custom_bins = 1,custom_bins =custom_bins_DeepCSVBdiscr,logy=1,overflow=0,underflow=1,weights_to_apply=weights_string_noBtagWeights,lepton_category=lepton_channel,suffix="_WithoutbTagWeights")#,AddSystUnc = True)
#     Plot1D("DeepCSVBDiscr_addJet2","DeepCSVBDiscr Discriminator second add. jet (no btag weights)","Events",len(custom_bins_DeepCSVBdiscr)-1,min(custom_bins_DeepCSVBdiscr),max(custom_bins_DeepCSVBdiscr),use_custom_bins = 1,custom_bins =custom_bins_DeepCSVBdiscr,logy=1,overflow=0,underflow=1,weights_to_apply=weights_string_noBtagWeights,lepton_category=lepton_channel,suffix="_WithoutbTagWeights")
    
    Plot1D("DeepCSVBDiscr_addJet1","DeepCSVBDiscr Discriminator first add. jet","Events",len(custom_bins_DeepCSVBdiscr)-1,min(custom_bins_DeepCSVBdiscr),max(custom_bins_DeepCSVBdiscr),use_custom_bins = 1,custom_bins =custom_bins_DeepCSVBdiscr,logy=1,overflow=0,underflow=1,weights_to_apply=weight_string_withcTagWeights,lepton_category=lepton_channel,suffix="_WithcTagWeights",AddSystUnc = True)
    Plot1D("DeepCSVBDiscr_addJet2","DeepCSVBDiscr Discriminator second add. jet","Events",len(custom_bins_DeepCSVBdiscr)-1,min(custom_bins_DeepCSVBdiscr),max(custom_bins_DeepCSVBdiscr),use_custom_bins = 1,custom_bins =custom_bins_DeepCSVBdiscr,logy=1,overflow=0,underflow=1,weights_to_apply=weight_string_withcTagWeights,lepton_category=lepton_channel,suffix="_WithcTagWeights",AddSystUnc = True)
    
    custom_bins_CvsL = [ 0.,0.075,0.1,0.125,0.15,0.2,0.25,0.3,0.35,0.45,0.6,0.8,1.0]
    Plot1D("DeepCSVcTagCvsL_addJet1","DeepCSV CvsL Discriminator first add. jet","Events",len(custom_bins_CvsL)-1,min(custom_bins_CvsL),max(custom_bins_CvsL),use_custom_bins = 1,custom_bins =custom_bins_CvsL,logy=1,overflow=0,underflow=1,weights_to_apply=weight_string,lepton_category=lepton_channel)
    Plot1D("DeepCSVcTagCvsL_addJet2","DeepCSV CvsL Discriminator second add. jet","Events",len(custom_bins_CvsL)-1,min(custom_bins_CvsL),max(custom_bins_CvsL),use_custom_bins = 1,custom_bins =custom_bins_CvsL,logy=1,overflow=0,underflow=1,weights_to_apply=weight_string,lepton_category=lepton_channel)
    Plot1D("DeepCSVcTagCvsL_addJet1","DeepCSV CvsL Discriminator first add. jet","Events",len(custom_bins_CvsL)-1,min(custom_bins_CvsL),max(custom_bins_CvsL),use_custom_bins = 1,custom_bins =custom_bins_CvsL,logy=1,overflow=0,underflow=1,weights_to_apply=weight_string_withcTagWeights,lepton_category=lepton_channel,suffix="_WithcTagWeights",AddSystUnc = True)
    Plot1D("DeepCSVcTagCvsL_addJet2","DeepCSV CvsL Discriminator second add. jet","Events",len(custom_bins_CvsL)-1,min(custom_bins_CvsL),max(custom_bins_CvsL),use_custom_bins = 1,custom_bins =custom_bins_CvsL,logy=1,overflow=0,underflow=1,weights_to_apply=weight_string_withcTagWeights,lepton_category=lepton_channel,suffix="_WithcTagWeights",AddSystUnc = True)

#     Plot1D("DeepCSVcTagCvsL_addJet1","DeepCSV CvsL Discriminator first add. jet (No BTag SF)","Events",len(custom_bins_CvsL)-1,min(custom_bins_CvsL),max(custom_bins_CvsL),use_custom_bins = 1,custom_bins =custom_bins_CvsL,logy=1,overflow=0,underflow=1,weights_to_apply=weights_string_noBtagWeights,lepton_category=lepton_channel,suffix="_NoBTagWeights")
#     Plot1D("DeepCSVcTagCvsL_addJet2","DeepCSV CvsL Discriminator second add. jet (No BTag SF)","Events",len(custom_bins_CvsL)-1,min(custom_bins_CvsL),max(custom_bins_CvsL),use_custom_bins = 1,custom_bins =custom_bins_CvsL,logy=1,overflow=0,underflow=1,weights_to_apply=weights_string_noBtagWeights,lepton_category=lepton_channel,suffix="_NoBTagWeights")

#     Plot1D("DeepCSVcTagCvsL_reweight_addJet1","Transformed DeepCSV CvsL first add. jet","Events",len(custom_bins_CvsL)-1,min(custom_bins_CvsL),max(custom_bins_CvsL),use_custom_bins = 1,custom_bins =custom_bins_CvsL,logy=1,overflow=0,underflow=1,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     Plot1D("DeepCSVcTagCvsL_reweight_addJet2","Transformed DeepCSV CvsL second add. jet","Events",len(custom_bins_CvsL)-1,min(custom_bins_CvsL),max(custom_bins_CvsL),use_custom_bins = 1,custom_bins =custom_bins_CvsL,logy=1,overflow=0,underflow=1,weights_to_apply=weight_string,lepton_category=lepton_channel)
    custom_bins_CvsB = [ 0.,0.2,0.35,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,1.0]
    Plot1D("DeepCSVcTagCvsB_addJet1","DeepCSV CvsB Discriminator first add. jet","Events",len(custom_bins_CvsB)-1,min(custom_bins_CvsB),max(custom_bins_CvsB),use_custom_bins = 1,custom_bins =custom_bins_CvsB,logy=1,overflow=0,underflow=1,weights_to_apply=weight_string,lepton_category=lepton_channel)
    Plot1D("DeepCSVcTagCvsB_addJet2","DeepCSV CvsB Discriminator second add. jet","Events",len(custom_bins_CvsB)-1,min(custom_bins_CvsB),max(custom_bins_CvsB),use_custom_bins = 1,custom_bins =custom_bins_CvsB,logy=1,overflow=0,underflow=1,weights_to_apply=weight_string,lepton_category=lepton_channel)
    Plot1D("DeepCSVcTagCvsB_addJet1","DeepCSV CvsB Discriminator first add. jet","Events",len(custom_bins_CvsB)-1,min(custom_bins_CvsB),max(custom_bins_CvsB),use_custom_bins = 1,custom_bins =custom_bins_CvsB,logy=1,overflow=0,underflow=1,weights_to_apply=weight_string_withcTagWeights,lepton_category=lepton_channel,suffix="_WithcTagWeights",AddSystUnc = True)
    Plot1D("DeepCSVcTagCvsB_addJet2","DeepCSV CvsB Discriminator second add. jet","Events",len(custom_bins_CvsB)-1,min(custom_bins_CvsB),max(custom_bins_CvsB),use_custom_bins = 1,custom_bins =custom_bins_CvsB,logy=1,overflow=0,underflow=1,weights_to_apply=weight_string_withcTagWeights,lepton_category=lepton_channel,suffix="_WithcTagWeights",AddSystUnc = True)

#     Plot1D("DeepCSVcTagCvsB_addJet1","DeepCSV CvsB Discriminator first add. jet (No BTag SF)","Events",len(custom_bins_CvsB)-1,min(custom_bins_CvsB),max(custom_bins_CvsB),use_custom_bins = 1,custom_bins =custom_bins_CvsB,logy=1,overflow=0,underflow=1,weights_to_apply=weights_string_noBtagWeights,lepton_category=lepton_channel,suffix="_NoBTagWeights")
#     Plot1D("DeepCSVcTagCvsB_addJet2","DeepCSV CvsB Discriminator second add. jet (No BTag SF)","Events",len(custom_bins_CvsB)-1,min(custom_bins_CvsB),max(custom_bins_CvsB),use_custom_bins = 1,custom_bins =custom_bins_CvsB,logy=1,overflow=0,underflow=1,weights_to_apply=weights_string_noBtagWeights,lepton_category=lepton_channel,suffix="_NoBTagWeights")
    
#     Plot1D("DeepCSVcTagCvsB_reweight_addJet1","Transformed DeepCSV CvsB first add. jet","Events",len(custom_bins_CvsB)-1,min(custom_bins_CvsB),max(custom_bins_CvsB),use_custom_bins = 1,custom_bins =custom_bins_CvsB,logy=1,overflow=0,underflow=1,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     Plot1D("DeepCSVcTagCvsB_reweight_addJet2","Transformed DeepCSV CvsB second add. jet","Events",len(custom_bins_CvsB)-1,min(custom_bins_CvsB),max(custom_bins_CvsB),use_custom_bins = 1,custom_bins =custom_bins_CvsB,logy=1,overflow=0,underflow=1,weights_to_apply=weight_string,lepton_category=lepton_channel)
    # Plot1D("n_DeepCSVcTagger_L_Additional_ctagged","number of L additional DeepCSV c-tagged jets","Events",4,-0.5,3.5,logy=1,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     Plot1D("n_DeepCSVcTagger_M_Additional_ctagged","number of M additional DeepCSV c-tagged jets","Events",4,-0.5,3.5,logy=1,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     Plot1D("n_DeepCSVcTagger_T_Additional_ctagged","number of T additional DeepCSV c-tagged jets","Events",4,-0.5,3.5,logy=1,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
#    
    # Plot1D("Pt_addJet1","p_{T} first add. jet [GeV]","Events",20,0,300,logy=1,overflow=1,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     Plot1D("Pt_addJet2","p_{T} second add. jet [GeV]","Events",20,0,300,logy=1,overflow=1,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     Plot1D("Eta_addJet1","#eta first add. jet","Events",20,-2.6,2.6,logy=0,overflow=1,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     Plot1D("Eta_addJet2","#eta second add. jet","Events",20,-2.6,2.6,logy=0,overflow=1,weights_to_apply=weight_string,lepton_category=lepton_channel)
    
    #Plot1D("nvertex","Number of primary vertices","Events",int(70),-0.5,69.5,logy=0,overflow=0,weights_to_apply=weight_string_withcTagWeights,lepton_category=lepton_channel)
    #Plot1D("nvertex","Number of primary vertices (before PU weights)","Events",int(70),-0.5,69.5,logy=0,overflow=0,weights_to_apply=weight_string_noPUweights,lepton_category=lepton_channel,suffix="_NoPUWeights")
    
if __name__ == "__main__":
    main()
