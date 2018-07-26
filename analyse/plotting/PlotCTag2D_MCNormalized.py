import ROOT
import os
import sys
from math import sqrt,ceil
from argparse import ArgumentParser
from xsec import xsec_table, color_table, legend_array

ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetOptStat(0)

parser = ArgumentParser()
parser.add_argument('--indir', default="FILL",help='input directory that contains all the samples')
parser.add_argument('--outdir', default=os.getcwd(),help='name of output directory')
#parser.add_argument('--xsecdir', "default=/user/smoortga/Analysis/NTupler/CMSSW_8_0_25/src/FlatTree/FlatTreeAnalyzer/ttcc/analyse/xsec.py",help='name of xsec dir')
args = parser.parse_args()

display_dict = {
    1:    {"legend":"t#bar{t}b#bar{b}",
            "samples":["TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8"],
            "color":ROOT.kRed+3,
            "category":0
            },
    # 2:    {"legend":"t#bar{t}bc",
#             "samples":["TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8"],
#             "color":ROOT.kOrange+6,
#             "category":1
#             },
    2:    {"legend":"t#bar{t}bj",
            "samples":["TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8"],
            "color":ROOT.kRed+2,
            "category":1
            },
    3:    {"legend":"t#bar{t}c#bar{c}",
            "samples":["TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8"],
            "color":ROOT.kOrange-2,
            "category":2
            },
    4:    {"legend":"t#bar{t}cj",
            "samples":["TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8"],
            "color":ROOT.kOrange-7,
            "category":3
            },
    5:    {"legend":"t#bar{t}jj",
            "samples":["TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8"],
            "color":ROOT.kRed-7,
            "category":4
            },
#     6:    {"legend":"t#bar{t} + Other",
#             "samples":["TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8"],
#             "color":ROOT.kOrange+6,
#             "category":-1
#             },
 #    7:    {"legend":"Single top",
#             "samples":["ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4","ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4","ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1","ST_t-channel_top_4f_inclusiveDecays_TuneCUETP8M2T4_13TeV-powhegV2-madspin","ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1"],
#             "color":ROOT.kCyan+1,
#             "category":-1
#             },
#     8:    {"legend":"Z + jets",
#             "samples":["DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8","DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8"],
#             "color":ROOT.kBlue,
#             "category":-1
#             },
#     9:    {"legend":"t#bar{t}V",
#             "samples":["ttZJets_13TeV_madgraphMLM","ttWJets_13TeV_madgraphMLM"],
#             "color":ROOT.kMagenta+1,
#             "category":-1
#             },
#     10:    {"legend":"ttH (h #rightarrow b#bar{b})",
#             "samples":["ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8"],
#             "color":1,
#             "category":-1
#             },
#     -1:    {"legend":"data",
#             "samples":["MuonEG_Run2016B_23Sep2016_v3_MINIAOD","MuonEG_Run2016C_23Sep2016_v1_MINIAOD","MuonEG_Run2016D_23Sep2016_v1_MINIAOD","MuonEG_Run2016E_23Sep2016_v1_MINIAOD","MuonEG_Run2016F_23Sep2016_v1_MINIAOD","MuonEG_Run2016G_23Sep2016_v1_MINIAOD"],
#             "color":1,
#             "category":-1
#             }
}

def Plot2D(var_x,x_name,nbinsx,xmin,xmax,var_y,y_name,nbinsy,ymin,ymax,logz=1,overflow=1,weights_to_apply="", lepton_category=""):

    ###############################
    #
    #	PREAPRE HISTOGRAMS
    #
    ################################
    binwidthx = float(xmax-xmin)/nbinsx
    binwidthy = float(ymax-ymin)/nbinsy
    if "[" in x_name: units_x = x_name.split("[")[1].split("]")[0]
    else: units_x = ""
    if "[" in y_name: units_y = y_name.split("[")[1].split("]")[0]
    else: units_y = ""
    #datahist = ROOT.TH1D("data",";%s;%s / %.1f %s"%(x_name,y_name,binwidth,units_x),nbins,xmin,xmax)
    MC_hists = {}
    for order in range(max(display_dict.keys())):
        MC_hists[order+1] = ROOT.TH2D("MC_%i"%(order+1),"%s;%s / %.1f %s;%s / %.1f %s"%(display_dict[order+1]["legend"],x_name,binwidthx,units_x,y_name,binwidthy,units_y),nbinsx,xmin,xmax,nbinsy,ymin,ymax)
        MC_hists[order+1].Sumw2()
    #ratio_hist = ROOT.TH1D("ratio",";%s;Data/MC"%(x_name),nbins,xmin,xmax)

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
            f_ = ROOT.TFile(full_path)
            n_original_h = f_.Get("hweight")
            n_original = n_original_h.GetBinContent(1)
            f_.Close()
            print n_original
            
            hist_tmp = ROOT.TH2D("h_"+f,";%s / %.1f %s;%s / %.1f %s"%(x_name,binwidthx,units_x,y_name,binwidthy,units_y),nbinsx,xmin,xmax,nbinsy,ymin,ymax)
            t_ = ROOT.TChain("tree")
            t_.Add(full_path)
            if (lepton_category == "elmu" or lepton_category=="muel"): weights_to_apply = "(lepton_Category==2)*"+weights_to_apply
            elif lepton_category == "elel": weights_to_apply = "(lepton_Category==0)*"+weights_to_apply
            if lepton_category == "mumu": weights_to_apply = "(lepton_Category==1)*"+weights_to_apply
            t_.Draw(var_y+":"+var_x+">>h_"+f,weights_to_apply+"*(event_Category == %s)"%entry_dict["category"])
            t_.GetEntry(1)
            if t_.is_data == 1:
                continue

            xsec = xsec_table[f]*1000 #[fb]
            int_lumi=27.271 #[fb^-1	]
            scale = xsec*int_lumi/n_original
            #hist_tmp.SetBinContent(MC_hists[order_table[name]].GetNbinsX(),MC_hists[order_table[name]].GetBinContent(MC_hists[order_table[name]].GetNbinsX()+1))
            MC_hists[idx].Add(hist_tmp,scale)
            #MC_hists[idx].SetLineColor(entry_dict["color"])
            if not MC_hists[idx].Integral() == 0: MC_hists[idx].Scale(1./MC_hists[idx].Integral())
            #MC_hists[order_table[name]].SetFillStyle(4333)
            del hist_tmp
    
    
    

    ###############################
    #
    #	STYLE
    #
    ################################
    
    if overflow: datahist.GetXaxis().SetRange(1,datahist.GetNbinsX()+1)
    for idx,hist in MC_hists.iteritems():
        if overflow: 
            hist.GetXaxis().SetRange(1,hist.GetNbinsX()+1)
            hist.GetYaxis().SetRange(1,hist.GetNbinsY()+1)
        #if not hist.Integral() == 0: hist.Scale(1./hist.Integral())

    ###############################
    #
    #	PLOTTING
    #
    ################################
    c = ROOT.TCanvas("c","c",1000,700)
    rows = int(sqrt(len(display_dict)))
    columns = int(ceil(len(display_dict)/float(rows)))
    c.Divide(columns,rows)
    for idx,hist in MC_hists.iteritems():
        c.cd(idx)
        ROOT.gPad.SetMargin(0.12,0.12,0.1,0.1)
        hist.Draw("COLZ")
        if (logz): ROOT.gPad.SetLogz(1)
        hist.GetZaxis().SetLabelSize(0.04)
        hist.GetXaxis().SetLabelSize(0.04)
        hist.GetXaxis().SetTitleSize(0.05)
        hist.GetXaxis().SetTitleOffset(1.)
        hist.GetYaxis().SetLabelSize(0.04)
        hist.GetYaxis().SetTitleSize(0.05)
        hist.GetYaxis().SetTitleOffset(1.2)
        ROOT.gPad.RedrawAxis()
        ROOT.gPad.SetTicks(1,1)
        
    
    if not os.path.isdir(args.outdir): os.mkdir(args.outdir)
	
    lepton_category_postfix = ""
    if ( (lepton_category == "elmu") or (lepton_category == "muel") or (lepton_category == "elel") or (lepton_category == "mumu") ) :lepton_category_postfix = "_"+lepton_category
    else: lepton_category_postfix = "_ll"
    if (logz): 
        c.SaveAs(args.outdir+"/"+var_x+"_"+var_y+"%s_normalizedMC_Log.pdf"%lepton_category_postfix)
        c.SaveAs(args.outdir+"/"+var_x+"_"+var_y+"%s_normalizedMC_Log.png"%lepton_category_postfix)
        c.SaveAs(args.outdir+"/"+var_x+"_"+var_y+"%s_normalizedMC_Log.C"%lepton_category_postfix)
    else: 
        c.SaveAs(args.outdir+"/"+var_x+"_"+var_y+"%s_normalizedMC_Linear.pdf"%lepton_category_postfix)
        c.SaveAs(args.outdir+"/"+var_x+"_"+var_y+"%s_normalizedMC_Linear.pdng"%lepton_category_postfix)
        c.SaveAs(args.outdir+"/"+var_x+"_"+var_y+"%s_normalizedMC_Linear.C"%lepton_category_postfix)



def main():
    
    weight_string = "weight_btag_iterativefit*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*pu_weight*mc_weight"
    no_weights = "1"
    lepton_channel="inclusive"
    
    Plot2D("DeepCSVcTagCvsL_addJet1","DeepCSV CvsL first add. jet",10,0,1,"DeepCSVcTagCvsB_addJet1","DeepCSV CvsB first add. jet",10,0,1,logz=1,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
    Plot2D("DeepCSVcTagCvsL_addJet2","DeepCSV CvsL second add. jet",10,0,1,"DeepCSVcTagCvsB_addJet2","DeepCSV CvsB second add. jet",10,0,1,logz=1,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
    
    
if __name__ == "__main__":
    main()
