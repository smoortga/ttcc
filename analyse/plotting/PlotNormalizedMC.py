import ROOT
import os
import sys
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
    3:    {"legend":"t#bar{t}b#bar{b}",
            "samples":["TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS","TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS","TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS"],
            "color":ROOT.kRed+3,
            "style":1,
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
            "style":2,
            "category":1
            },
    1:    {"legend":"t#bar{t}c#bar{c}",
            "samples":["TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS","TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS","TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS"],
            "color":ROOT.kOrange-2,
            "style":1,
            "category":2
            },
    2:    {"legend":"t#bar{t}cj",
            "samples":["TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS","TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS","TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS"],
            "color":ROOT.kOrange-7,
            "style":2,
            "category":3
            },
    5:    {"legend":"t#bar{t}jj",
            "samples":["TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS","TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS","TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS"],
            "color":ROOT.kRed-7,
            "style":1,
            "category":4
            },
    # 6:    {"legend":"t#bar{t} + Other",
#            "samples":["TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS","TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS","TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS"],
#            "color":ROOT.kOrange+6,
#            "category":-1
#            },
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

def Plot1D(var,x_name,y_name,nbins,xmin,xmax,logy=1,overflow=1, underflow = 1,weights_to_apply="", lepton_category=""):

    ###############################
    #
    #	PREAPRE HISTOGRAMS
    #
    ################################
    binwidth = float(xmax-xmin)/nbins
    if "[" in x_name: units_x = x_name.split("[")[1].split("]")[0]
    else: units_x = ""
    #datahist = ROOT.TH1D("data",";%s;%s / %.1f %s"%(x_name,y_name,binwidth,units_x),nbins,xmin,xmax)
    MC_hists = {}
    for order in range(max(display_dict.keys())):
        MC_hists[order+1] = ROOT.TH1D("MC_%i"%(order+1),";%s;%s / %.1f %s"%(x_name,y_name,binwidth,units_x),nbins,xmin,xmax)
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
            
            hist_tmp = ROOT.TH1D("h_"+f,";%s;%s / %.2f %s"%(x_name,y_name,binwidth,units_x),nbins,xmin,xmax)
            t_ = ROOT.TChain("tree")
            t_.Add(full_path)
            if (lepton_category == "elmu" or lepton_category=="muel"): weights_to_apply = "(lepton_Category==2)*"+weights_to_apply
            elif lepton_category == "elel": weights_to_apply = "(lepton_Category==0)*"+weights_to_apply
            if lepton_category == "mumu": weights_to_apply = "(lepton_Category==1)*"+weights_to_apply
            t_.Draw(var+">>h_"+f,weights_to_apply+"*(event_Category_VisiblePS == %s)*(mc_pu_trueNumInt>10 && mc_pu_trueNumInt<70)"%entry_dict["category"])
            if underflow: hist_tmp.SetBinContent(1,hist_tmp.GetBinContent(0)+hist_tmp.GetBinContent(1))
            t_.GetEntry(1)
            if t_.is_data == 1:
                continue

            xsec = xsec_table[f]*1000 #[fb]
            int_lumi=27.271 #[fb^-1	]
            scale = xsec*int_lumi/n_original
            #hist_tmp.SetBinContent(MC_hists[order_table[name]].GetNbinsX(),MC_hists[order_table[name]].GetBinContent(MC_hists[order_table[name]].GetNbinsX()+1))
            MC_hists[idx].Add(hist_tmp,scale)
            MC_hists[idx].SetLineColor(entry_dict["color"])
            MC_hists[idx].SetLineStyle(entry_dict["style"])
            if not MC_hists[idx].Integral() == 0: MC_hists[idx].Scale(1./MC_hists[idx].Integral())
            #MC_hists[order_table[name]].SetFillStyle(4333)
            del hist_tmp
    
    
    

    ###############################
    #
    #	STYLE
    #
    ################################
    
    #if overflow: datahist.GetXaxis().SetRange(1,datahist.GetNbinsX()+1)
    for idx,hist in MC_hists.iteritems():
        hist.SetLineWidth(3)
        if overflow: hist.GetXaxis().SetRange(1,hist.GetNbinsX()+1)
            

    ###############################
    #
    #	PLOTTING
    #
    ################################
    c = ROOT.TCanvas("c","c",800,700)
    c.cd()
#     uppad = ROOT.TPad("u","u",0.,0.25,1.,1.)
#     downpad = ROOT.TPad("d","d",0.,0.0,1.,0.25)
#     uppad.Draw()
#     downpad.Draw()

    #uppad.cd()
    ROOT.gPad.SetLogy(logy)
    ROOT.gPad.SetMargin(0.15,0.05,0.15,0.1)
    mg = ROOT.THStack("mg",";%s;%s / %.2f %s"%(x_name,y_name,binwidth,units_x))
    #summed_MC_hist = ROOT.TH1D("h_summed",";%s;%s / %.2f %s"%(x_name,y_name,binwidth,units_x),nbins,xmin,xmax)
    max_bin_content = 0
    for idx,hist in MC_hists.iteritems():
        mg.Add(hist,"hist")
        if hist.GetBinContent(hist.GetMaximumBin()) > max_bin_content: max_bin_content = hist.GetBinContent(hist.GetMaximumBin())
        #summed_MC_hist.Add(hist)
    mg.Draw("hist nostack")
    if overflow: mg.GetXaxis().SetRange(1,mg.GetHistogram().GetNbinsX()+1)
    ROOT.TGaxis.SetMaxDigits(3)
    if (logy): 
        mg.SetMinimum(0.0001)
        mg.SetMaximum(10000)
    else:
        mg.SetMinimum(0)
        mg.SetMaximum(2*max_bin_content)
    mg.GetYaxis().SetLabelSize(0.05)
    mg.GetYaxis().SetLabelOffset(0.01)
    mg.GetYaxis().SetTitleSize(0.06)
    mg.GetYaxis().SetTitleOffset(1.2)
    mg.GetXaxis().SetTitleSize(0.06)
    mg.GetXaxis().SetTitleOffset(1.2)
    mg.GetXaxis().SetLabelSize(0.05)
    
    
    #redraw borders
    ROOT.gPad.RedrawAxis()
    line = ROOT.TLine()
    if overflow: line.DrawLine(xmax+binwidth, ROOT.gPad.GetUymin(), xmax+binwidth, ROOT.gPad.GetUymax())
    else:line.DrawLine(xmax, ROOT.gPad.GetUymin(), xmax, ROOT.gPad.GetUymax())
    
    #########
    # TEXT
    #########
    lumi = "%.1f"%int_lumi
    year = "2017"
    latex = ROOT.TLatex()
    latex.SetTextFont(42)
    latex.SetTextSize(0.05)
    latex.SetTextAlign(32)
    latex.DrawLatexNDC(0.94,0.94,year + ", 94X")
    
    latex_cms = ROOT.TLatex()
    latex_cms.SetTextFont(42)
    latex_cms.SetTextSize(0.045)
    latex_cms.SetTextAlign(11)
    latex_cms.DrawLatexNDC(0.19,0.83,"#bf{CMS} #it{Simulation}")
    
    latex_lepton_category = ROOT.TLatex()
    latex_lepton_category.SetTextFont(42)
    latex_lepton_category.SetTextSize(0.045)
    latex_lepton_category.SetTextAlign(11)
    if (lepton_category == "elmu" or lepton_category=="muel"): latex_lepton_category.DrawLatexNDC(0.19,0.77,"e^{#pm}#mu^{#mp} channel")
    elif (lepton_category == "elel"): latex_lepton_category.DrawLatexNDC(0.19,0.77,"e^{+}e^{-} channel")
    elif (lepton_category == "mumu"): latex_lepton_category.DrawLatexNDC(0.19,0.77,"#mu^{+}#mu^{-} channel")
    else: latex_lepton_category.DrawLatexNDC(0.19,0.77,"dilepton channel")
    
    # latex_lepton_category = ROOT.TMathText()
#     latex_lepton_category.SetNDC()
#     latex_lepton_category.SetTextFont(42)
#     latex_lepton_category.SetTextSize(0.05)
#     latex_lepton_category.SetTextAlign(11)
#     if (lepton_category == "elmu" or lepton_category=="muel"): latex_lepton_category.DrawMathText(0.19,0.75,"e^{\\pm}#mu^{\\mp} channel")
#     elif (lepton_category == "elel"): latex_lepton_category.DrawMathText(0.19,0.75,"e^{+}e^{-} channel")
#     elif (lepton_category == "mumu"): latex_lepton_category.DrawMathText(0.19,0.75,"\\mu^{+}\\mu^{-} channel")
#     else: latex_lepton_category.DrawMathText(0.19,0.75,"\\ell^{+}\\ell^{-} channel")
    

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
        entries_dict[e["legend"]]=l.AddEntry(None,e["legend"],"l")
        entries_dict[e["legend"]].SetFillStyle(1000)
        entries_dict[e["legend"]].SetLineColor(e["color"])
        entries_dict[e["legend"]].SetLineStyle(e["style"])
        entries_dict[e["legend"]].SetLineWidth(7)
    #l.AddEntry(datahist,"Data","ep")
    l.SetBorderSize(0)
    l.SetTextSize(0.06)
    l.Draw("same")
    
    
    
    

    #downpad.cd()
    
	
    if not os.path.isdir(args.outdir): os.mkdir(args.outdir)
	
    lepton_category_postfix = ""
    if ( (lepton_category == "elmu") or (lepton_category == "muel") or (lepton_category == "elel") or (lepton_category == "mumu") ) :lepton_category_postfix = "_"+lepton_category
    else: lepton_category_postfix = "_ll"
    if (logy): 
        c.SaveAs(args.outdir+"/"+var+"%s_normalizedMC_Log.pdf"%lepton_category_postfix)
        c.SaveAs(args.outdir+"/"+var+"%s_normalizedMC_Log.png"%lepton_category_postfix)
        c.SaveAs(args.outdir+"/"+var+"%s_normalizedMC_Log.C"%lepton_category_postfix)
    else: 
        c.SaveAs(args.outdir+"/"+var+"%s_normalizedMC_Linear.pdf"%lepton_category_postfix)
        c.SaveAs(args.outdir+"/"+var+"%s_normalizedMC_Linear.png"%lepton_category_postfix)
        c.SaveAs(args.outdir+"/"+var+"%s_normalizedMC_Linear.C"%lepton_category_postfix)
    




def main():
    
    #weight_string = "weight_ctag_iterativefit*weight_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
    weight_string = "weight_bjets_ctag_iterativefit*weight_cjets_ctag_iterativefit*weight_udsgjets_ctag_iterativefit*weight_bcjets_btag_DeepCSVMedium*weight_udsgjets_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
    
    no_weights = "1"
    lepton_channel="inclusive"
    
    
    Plot1D("TopMatching_NN_best_value","Top matching NN value","Events (norm.)",20,0.7,1,logy=0,overflow=1, underflow = 1,weights_to_apply=weight_string,lepton_category=lepton_channel)
    
    
    Plot1D("Minv_addJets","M_{inv}(add. jets) [GeV]","Events (norm.)",20,0,300,logy=0,overflow=1, underflow = 1,weights_to_apply=weight_string,lepton_category=lepton_channel)
    Plot1D("DeltaR_addJets","#DeltaR(add. jets)","Events",20,0.4,5,logy=0,overflow=1, underflow = 1,weights_to_apply=weight_string,lepton_category=lepton_channel)
    
    Plot1D("ttHF_selector_NN_CvsL","#Delta_{L}^{c} discriminator","Events",20,0.,1.,logy=0,overflow=1, underflow = 1,weights_to_apply=weight_string,lepton_category=lepton_channel)
    Plot1D("ttHF_selector_NN_CvsB","#Delta_{b}^{c} discriminator","Events",20,0.,1.,logy=0,overflow=1, underflow = 1,weights_to_apply=weight_string,lepton_category=lepton_channel)
    
    Plot1D("Pt_addJet1","p_{T} 1st add. jet [GeV]","Events (norm.)",20,20,500,logy=1,overflow=1, underflow = 1,weights_to_apply=weight_string,lepton_category=lepton_channel)
    Plot1D("Pt_addJet2","p_{T} 2nd add. jet [GeV]","Events (norm.)",20,20,500,logy=1,overflow=1, underflow = 1,weights_to_apply=weight_string,lepton_category=lepton_channel)
    Plot1D("Eta_addJet1","#eta 1st add. jet","Events (norm.)",20,-2.6,2.6,logy=0,overflow=0, underflow = 0,weights_to_apply=weight_string,lepton_category=lepton_channel)
    Plot1D("Eta_addJet2","#eta 2nd add. jet","Events (norm.)",20,-2.6,2.6,logy=0,overflow=0, underflow = 0,weights_to_apply=weight_string,lepton_category=lepton_channel)

    
    
    # Plot1D("hadronFlavour_addJet1","Hadron flavour of leading add. jet","Events (norm.)",6,-0.5,5.5,logy=0,overflow=1,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     Plot1D("hadronFlavour_addJet2","Hadron flavour of subleading add. jet","Events (norm.)",6,-0.5,5.5,logy=0,overflow=1,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     Plot1D("partonFlavour_addJet1","Parton flavour of leading add. jet","Events (norm.)",22,-0.5,21.5,logy=0,overflow=1,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     Plot1D("partonFlavour_addJet2","Parton flavour of subleading add. jet","Events (norm.)",22,-0.5,21.5,logy=0,overflow=1,weights_to_apply=weight_string,lepton_category=lepton_channel)

    # Plot1D("DileptonInvariantMass","m_{ll} [GeV]","Events",20,0,500,logy=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     Plot1D("DileptonDeltaR","#DeltaR(l,l)","Events",20,0,6,logy=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     Plot1D("DileptonDeltaR","#DeltaR(l,l)","Events",20,0,6,logy=1,weights_to_apply=weight_string,lepton_category=lepton_channel)
    #Plot1D("CSVv2_addJet1","CSVv2 Discriminator 1st add. jet","Jets (norm.)",10,0,1,logy=1,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
    #Plot1D("CSVv2_addJet2","CSVv2 Discriminator 2nd add. jet","Jets (norm.)",10,0,1,logy=1,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
    # Plot1D("DeepCSVBDiscr_addJet1","DeepCSVBDiscr Discriminator 1st add. jet","Events (norm.)",10,0,1,logy=1,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     Plot1D("DeepCSVBDiscr_addJet2","DeepCSVBDiscr Discriminator 2nd add. jet","Events (norm.)",10,0,1,logy=1,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
    # Plot1D("CSVv2_addJet1","CSVv2 Discriminator 1st add. jet","Jets (norm.)",10,0,1,logy=1,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     Plot1D("CSVv2_addJet2","CSVv2 Discriminator 2nd add. jet","Jets (norm.)",10,0,1,logy=1,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     Plot1D("DeepCSVBDiscr_addJet1","DeepCSV BDiscriminator 1st add. jet","Jets (norm.)",10,0,1,logy=1,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     Plot1D("DeepCSVBDiscr_addJet2","DeepCSV BDiscriminator 2nd add. jet","Jets (norm.)",10,0,1,logy=1,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
    Plot1D("DeepCSVcTagCvsL_addJet1","DeepCSV CvsL Discriminator 1st add. jet","Events (norm.)",20,0,1,logy=0,overflow=0, underflow = 1,weights_to_apply=weight_string,lepton_category=lepton_channel)
    Plot1D("DeepCSVcTagCvsL_addJet2","DeepCSV CvsL Discriminator 2nd add. jet","Events (norm.)",20,0,1,logy=0,overflow=0, underflow = 1,weights_to_apply=weight_string,lepton_category=lepton_channel)
    Plot1D("DeepCSVcTagCvsB_addJet1","DeepCSV CvsB Discriminator 1st add. jet","Events (norm.)",20,0,1,logy=0,overflow=0, underflow = 1,weights_to_apply=weight_string,lepton_category=lepton_channel)
    Plot1D("DeepCSVcTagCvsB_addJet2","DeepCSV CvsB Discriminator 2nd add. jet","Events (norm.)",20,0,1,logy=0,overflow=0, underflow = 1,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     Plot1D("n_cTagger_L_ctagged","number of L c-tagged jets","Jets (norm.)",6,-0.5,5.5,logy=0,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     Plot1D("n_cTagger_M_ctagged","number of M c-tagged jets","Jets (norm.)",6,-0.5,5.5,logy=0,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     Plot1D("n_cTagger_T_ctagged","number of T c-tagged jets","Jets (norm.)",6,-0.5,5.5,logy=0,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     Plot1D("n_cTagger_L_Additional_ctagged","number of L additional c-tagged jets","Jets (norm.)",6,-0.5,5.5,logy=0,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     Plot1D("n_cTagger_M_Additional_ctagged","number of M additional c-tagged jets","Jets (norm.)",6,-0.5,5.5,logy=0,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     Plot1D("n_cTagger_T_Additional_ctagged","number of T additional c-tagged jets","Jets (norm.)",6,-0.5,5.5,logy=0,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
    #Plot1D("TopMatching_NN_best_value","Top matching NN value","Events (norm.)",20,0,1,logy=1,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
    #Plot1D("Jets._SfIterativeFitCentral","SF IterativeFit Central","Jets (norm.)",20,0.7,1.4,logy=0,overflow=1,weights_to_apply=no_weights,lepton_category=lepton_channel)
    #Plot1D("weight_btag_iterativefit","BTagging Shape reweighting SF","Jets (norm.)",20,0.5,1.4,logy=0,overflow=1,weights_to_apply=no_weights,lepton_category=lepton_channel)

if __name__ == "__main__":
    main()
