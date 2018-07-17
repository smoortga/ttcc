import ROOT
import os
import sys
from argparse import ArgumentParser
from array import array
from xsec import xsec_table, color_table, legend_array

ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetOptStat(0)

parser = ArgumentParser()
parser.add_argument('--indir', default="FILL",help='input directory that contains all the samples')
parser.add_argument('--outdir', default=os.getcwd(),help='name of output directory')
#parser.add_argument('--xsecdir', "default=/user/smoortga/Analysis/NTupler/CMSSW_8_0_25/src/FlatTree/FlatTreeAnalyzer/ttcc/analyse/xsec.py",help='name of xsec dir')
args = parser.parse_args()

display_dict = {
    3:    {"legend":"t#bar{t}b#bar{b}",
            "samples":["TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8"],
            "color":ROOT.kRed+3,
            "category":0
            },
    # 2:    {"legend":"t#bar{t}bc",
#             "samples":["TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8"],
#             "color":ROOT.kOrange+6,
#             "category":1
#             },
    4:    {"legend":"t#bar{t}bj",
            "samples":["TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8"],
            "color":ROOT.kRed+2,
            "category":1
            },
    1:    {"legend":"t#bar{t}c#bar{c}",
            "samples":["TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8"],
            "color":ROOT.kOrange-2,
            "category":2
            },
    2:    {"legend":"t#bar{t}cj",
            "samples":["TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8"],
            "color":ROOT.kOrange-7,
            "category":3
            },
    5:    {"legend":"t#bar{t}jj",
            "samples":["TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8"],
            "color":ROOT.kRed-7,
            "category":4
            },
    # 1:    {"legend":"t#bar{t} + Other",
#             "samples":["TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8"],
#             "color":ROOT.kOrange+6,
#             "category":-1
#             },
    6:    {"legend":"Single top",
            "samples":["ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8","ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8","ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8","ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8","ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8"], 
            "color":ROOT.kCyan+1,
            "category":-1
            },
    7:    {"legend":"Z + jets",
            "samples":["DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8"],
            "color":ROOT.kBlue,
            "category":-1
            },
   #  1:    {"legend":"Diboson",
#             "samples":["WW_TuneCP5_13TeV-pythia8","WZ_TuneCP5_13TeV-pythia8","ZZ_TuneCP5_13TeV-pythia8"],
#             "color":402,
#             "category":-1
#             },           
    8:    {"legend":"Rare",
            "samples":["WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8","WZZ_TuneCP5_13TeV-amcatnlo-pythia8","WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8","ZZZ_TuneCP5_13TeV-amcatnlo-pythia8","WW_TuneCP5_13TeV-pythia8","WZ_TuneCP5_13TeV-pythia8","ZZ_TuneCP5_13TeV-pythia8","ttHJetTobb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8","ttHJetToNonbb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8"],
            "color":1,
            "category":-1
            },
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

def Plot1D(var,x_name,y_name,nbins,xmin,xmax,use_custom_bins = 0,custom_bins = [0,1,2],logy=1,overflow=0,underflow=0,weights_to_apply="", lepton_category="", suffix=""):

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
            
            if use_custom_bins: hist_tmp = ROOT.TH1D("h_"+f,";%s;%s"%(x_name,y_name),nbins,array("d",custom_bins))
            else: hist_tmp = ROOT.TH1D("h_"+f,";%s;%s / %.2f %s"%(x_name,y_name,binwidth,units_x),nbins,xmin,xmax)
            t_ = ROOT.TChain("tree")
            t_.Add(full_path)
            if (lepton_category == "elmu" or lepton_category=="muel"): weights_to_apply = "(lepton_Category==2)*"+weights_to_apply
            elif lepton_category == "elel": weights_to_apply = "(lepton_Category==0)*"+weights_to_apply
            elif lepton_category == "mumu": weights_to_apply = "(lepton_Category==1)*"+weights_to_apply
            else: weights_to_apply = weights_to_apply
            t_.Draw(var+">>h_"+f,weights_to_apply+"*(event_Category == %s)*(mc_pu_trueNumInt>10 && mc_pu_trueNumInt<70)"%entry_dict["category"])#*(mc_pu_trueNumInt>0)
            t_.GetEntry(1)
            if t_.is_data == 1:
                continue
            # put underflow in the first bin
            if underflow: hist_tmp.SetBinContent(1,hist_tmp.GetBinContent(0)+hist_tmp.GetBinContent(1))
            
            xsec = xsec_table[f]*1000 #[fb]
            int_lumi=41.527 #[fb^-1	]35.921875594646 #27.271
            scale = float(xsec*int_lumi)/float(n_original)
            #hist_tmp.SetBinContent(MC_hists[order_table[name]].GetNbinsX(),MC_hists[order_table[name]].GetBinContent(MC_hists[order_table[name]].GetNbinsX()+1))
            MC_hists[idx].Add(hist_tmp,scale)
            MC_hists[idx].SetFillColor(entry_dict["color"])
            #MC_hists[order_table[name]].SetFillStyle(4333)
            del hist_tmp
    
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
        del hist_tmp
    
    
    

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
        summed_MC_hist = ROOT.TH1D("h_summed",";%s;%s"%(x_name,y_name),nbins,array("d",custom_bins))
    else:
        mg = ROOT.THStack("mg",";%s;%s / %.2f %s"%(x_name,y_name,binwidth,units_x))
        summed_MC_hist = ROOT.TH1D("h_summed",";%s;%s / %.2f %s"%(x_name,y_name,binwidth,units_x),nbins,xmin,xmax)
    summed_MC_hist.Sumw2()
    for idx,hist in MC_hists.iteritems():
        mg.Add(hist,"f")
        summed_MC_hist.Add(hist)
    mg.Draw("hist")
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
    
    
    # Error on the MC stats
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
    l.AddEntry(summed_MC_hist,"MC stat. unc.","f")
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
    weight_string = "weight_btag_iterativefit*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight"#*pu_weight
    weight_string_noPUweights = "weight_btag_iterativefit*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight"
    weights_string_noBtagWeights = "weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*pu_weight*mc_weight"
    
    no_weights = "1"
    lepton_channel="inclusive"#"mumu"#"elmu","inclusive","elel"
    
    #custom_bins_TopMatchingNN = [0.7,0.9,0.92,0.94,0.95,0.96,0.97,0.98,0.99,0.995,1.0]
    custom_bins_TopMatchingNN = [0.5,0.6,0.7,0.8,0.85,0.9,0.925,0.95,0.975,1.0]
    Plot1D("TopMatching_NN_best_value","Top matching NN value","Events",len(custom_bins_TopMatchingNN)-1,min(custom_bins_TopMatchingNN),max(custom_bins_TopMatchingNN),use_custom_bins = 1,custom_bins =custom_bins_TopMatchingNN,logy=1,overflow=0,underflow=1,weights_to_apply=weight_string,lepton_category=lepton_channel)
    #Plot1D("Jets._DeepCSVBDiscr","DeepCSVBDiscr discriminator (No btag weights)","Jets",40,0,1,logy=1,overflow=0,weights_to_apply=weights_string_noBtagWeights,lepton_category=lepton_channel,suffix="_NoBtagWeights")
#     Plot1D("Jets._DeepCSVCvsL","DeepCSVCvsL discriminator(No btag weights)","Jets",40,0,1,logy=1,overflow=0,weights_to_apply=weights_string_noBtagWeights,lepton_category=lepton_channel,suffix="_NoBtagWeights")
# 
    #Plot1D("Jets._DeepCSVBDiscr","DeepCSVBDiscr discriminator","Jets",40,0,1,logy=1,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     Plot1D("Jets._DeepCSVCvsL","DeepCSVCvsL discriminator","Jets",40,0,1,logy=1,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)

    Plot1D("lepton_Category","lepton category","Events",3,-0.5,2.5,logy=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
    Plot1D("DileptonInvariantMass","m_{ll} [GeV]","Events",20,0,500,logy=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
    Plot1D("DileptonDeltaR","#DeltaR(l,l)","Events",20,0,6,logy=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     Plot1D("CSVv2_addJet1","CSVv2 Discriminator first add. jet","Events",10,0,1,logy=1,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     Plot1D("CSVv2_addJet2","CSVv2 Discriminator second add. jet","Events",10,0,1,logy=1,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     #Plot1D("CSVv2_addJet1","CSVv2 Discriminator first add. jet","Events",10,0,1,logy=0,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     #Plot1D("CSVv2_addJet2","CSVv2 Discriminator second add. jet","Events",10,0,1,logy=0,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
    custom_bins_DeepCSVBdiscr = [ 0.,0.025,0.05,0.1,0.15,0.2,0.25,0.35,0.45,0.6,0.8,1.0]
    Plot1D("DeepCSVBDiscr_addJet1","DeepCSVBDiscr Discriminator first add. jet","Events",len(custom_bins_DeepCSVBdiscr)-1,min(custom_bins_DeepCSVBdiscr),max(custom_bins_DeepCSVBdiscr),use_custom_bins = 1,custom_bins =custom_bins_DeepCSVBdiscr,logy=1,overflow=0,underflow=1,weights_to_apply=weight_string,lepton_category=lepton_channel)
    Plot1D("DeepCSVBDiscr_addJet2","DeepCSVBDiscr Discriminator second add. jet","Events",len(custom_bins_DeepCSVBdiscr)-1,min(custom_bins_DeepCSVBdiscr),max(custom_bins_DeepCSVBdiscr),use_custom_bins = 1,custom_bins =custom_bins_DeepCSVBdiscr,logy=1,overflow=0,underflow=1,weights_to_apply=weight_string,lepton_category=lepton_channel)
    #Plot1D("DeepCSVBDiscr_addJet1","DeepCSVBDiscr Discriminator first add. jet (No BTag SF)","Events",len(custom_bins_DeepCSVBdiscr)-1,min(custom_bins_DeepCSVBdiscr),max(custom_bins_DeepCSVBdiscr),use_custom_bins = 1,custom_bins =custom_bins_DeepCSVBdiscr,logy=1,overflow=0,underflow=1,weights_to_apply=weights_string_noBtagWeights,lepton_category=lepton_channel,suffix="_NoBTagWeights")
    #Plot1D("DeepCSVBDiscr_addJet2","DeepCSVBDiscr Discriminator second add. jet (No BTag SF)","Events",len(custom_bins_DeepCSVBdiscr)-1,min(custom_bins_DeepCSVBdiscr),max(custom_bins_DeepCSVBdiscr),use_custom_bins = 1,custom_bins =custom_bins_DeepCSVBdiscr,logy=1,overflow=0,underflow=1,weights_to_apply=weights_string_noBtagWeights,lepton_category=lepton_channel,suffix="_NoBTagWeights")
    #Plot1D("DeepCSVBDiscr_addJet1","DeepCSVBDiscr Discriminator first add. jet","Events",10,0,1,logy=0,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
    #Plot1D("DeepCSVBDiscr_addJet2","DeepCSVBDiscr Discriminator second add. jet","Events",10,0,1,logy=0,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     Plot1D("cTagCvsL_addJet1","c-tagger CvsL Discriminator first add. jet","Events",10,-1,1,logy=0,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     Plot1D("cTagCvsL_addJet2","c-tagger CvsL Discriminator second add. jet","Events",10,-1,1,logy=0,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     Plot1D("cTagCvsB_addJet1","c-tagger CvsB Discriminator first add. jet","Events",10,-1,1,logy=0,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     Plot1D("cTagCvsB_addJet2","c-tagger CvsB Discriminator second add. jet","Events",10,-1,1,logy=0,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
    #Plot1D("cTagCvsL_addJet1","c-tagger CvsL Discriminator first add. jet","Events",10,-1,1,logy=1,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
    #Plot1D("cTagCvsL_addJet2","c-tagger CvsL Discriminator second add. jet","Events",10,-1,1,logy=1,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
    #Plot1D("cTagCvsB_addJet1","c-tagger CvsB Discriminator first add. jet","Events",10,-1,1,logy=1,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
    #Plot1D("cTagCvsB_addJet2","c-tagger CvsB Discriminator second add. jet","Events",10,-1,1,logy=1,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
    custom_bins_CvsL = [ 0.,0.05,0.075,0.1,0.15,0.2,0.25,0.35,0.45,0.6,0.8,1.0]
    Plot1D("DeepCSVcTagCvsL_addJet1","DeepCSV CvsL Discriminator first add. jet","Events",len(custom_bins_CvsL)-1,min(custom_bins_CvsL),max(custom_bins_CvsL),use_custom_bins = 1,custom_bins =custom_bins_CvsL,logy=1,overflow=0,underflow=1,weights_to_apply=weight_string,lepton_category=lepton_channel)
    Plot1D("DeepCSVcTagCvsL_addJet2","DeepCSV CvsL Discriminator second add. jet","Events",len(custom_bins_CvsL)-1,min(custom_bins_CvsL),max(custom_bins_CvsL),use_custom_bins = 1,custom_bins =custom_bins_CvsL,logy=1,overflow=0,underflow=1,weights_to_apply=weight_string,lepton_category=lepton_channel)
    custom_bins_CvsB = [ 0.,0.2,0.35,0.5,0.6,0.65,0.7,0.75,0.775,0.8,0.85,1.0]
    Plot1D("DeepCSVcTagCvsB_addJet1","DeepCSV CvsB Discriminator first add. jet","Events",len(custom_bins_CvsB)-1,min(custom_bins_CvsB),max(custom_bins_CvsB),use_custom_bins = 1,custom_bins =custom_bins_CvsB,logy=1,overflow=0,underflow=1,weights_to_apply=weight_string,lepton_category=lepton_channel)
    Plot1D("DeepCSVcTagCvsB_addJet2","DeepCSV CvsB Discriminator second add. jet","Events",len(custom_bins_CvsB)-1,min(custom_bins_CvsB),max(custom_bins_CvsB),use_custom_bins = 1,custom_bins =custom_bins_CvsB,logy=1,overflow=0,underflow=1,weights_to_apply=weight_string,lepton_category=lepton_channel)
    Plot1D("n_DeepCSVcTagger_L_Additional_ctagged","number of L additional DeepCSV c-tagged jets","Events",4,-0.5,3.5,logy=1,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
    Plot1D("n_DeepCSVcTagger_M_Additional_ctagged","number of M additional DeepCSV c-tagged jets","Events",4,-0.5,3.5,logy=1,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
    Plot1D("n_DeepCSVcTagger_T_Additional_ctagged","number of T additional DeepCSV c-tagged jets","Events",4,-0.5,3.5,logy=1,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
#    
    Plot1D("nvertex","Number of primary vertices","Events",int(70),-0.5,69.5,logy=0,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
    #Plot1D("nvertex","Number of primary vertices (before PU weights)","Events",int(70),-0.5,69.5,logy=0,overflow=0,weights_to_apply=weight_string_noPUweights,lepton_category=lepton_channel,suffix="_NoPUWeights")
    
if __name__ == "__main__":
    main()
