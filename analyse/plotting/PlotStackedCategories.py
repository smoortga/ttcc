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
    1:    {"legend":"t#bar{t}b#bar{b}",
            "samples":["TT_TuneCUETP8M2T4_13TeV-powheg-pythia8"],
            "color":ROOT.kRed+3,
            "category":0
            },
    # 2:    {"legend":"t#bar{t}bc",
#             "samples":["TT_TuneCUETP8M2T4_13TeV-powheg-pythia8"],
#             "color":ROOT.kOrange+6,
#             "category":1
#             },
    2:    {"legend":"t#bar{t}bj",
            "samples":["TT_TuneCUETP8M2T4_13TeV-powheg-pythia8"],
            "color":ROOT.kRed+2,
            "category":1
            },
    3:    {"legend":"t#bar{t}c#bar{c}",
            "samples":["TT_TuneCUETP8M2T4_13TeV-powheg-pythia8"],
            "color":ROOT.kOrange-2,
            "category":2
            },
    4:    {"legend":"t#bar{t}c#bar{j}",
            "samples":["TT_TuneCUETP8M2T4_13TeV-powheg-pythia8"],
            "color":ROOT.kOrange-7,
            "category":3
            },
    5:    {"legend":"t#bar{t}jj",
            "samples":["TT_TuneCUETP8M2T4_13TeV-powheg-pythia8"],
            "color":ROOT.kRed-7,
            "category":4
            },
    6:    {"legend":"t#bar{t} + Other",
            "samples":["TT_TuneCUETP8M2T4_13TeV-powheg-pythia8"],
            "color":ROOT.kOrange+6,
            "category":-1
            },
    7:    {"legend":"Single top",
            "samples":["ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4","ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4","ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1","ST_t-channel_top_4f_inclusiveDecays_TuneCUETP8M2T4_13TeV-powhegV2-madspin","ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1"],
            "color":ROOT.kCyan+1,
            "category":-1
            },
    8:    {"legend":"Z + jets",
            "samples":["DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8","DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8"],
            "color":ROOT.kBlue,
            "category":-1
            },
    9:    {"legend":"t#bar{t}V",
            "samples":["ttZJets_13TeV_madgraphMLM","ttWJets_13TeV_madgraphMLM"],
            "color":ROOT.kMagenta+1,
            "category":-1
            },
    10:    {"legend":"ttH (h #rightarrow b#bar{b})",
            "samples":["ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8"],
            "color":1,
            "category":-1
            },
    -1:    {"legend":"data",
            "samples":["MuonEG_Run2016B_23Sep2016_v3_MINIAOD","MuonEG_Run2016C_23Sep2016_v1_MINIAOD","MuonEG_Run2016D_23Sep2016_v1_MINIAOD","MuonEG_Run2016E_23Sep2016_v1_MINIAOD","MuonEG_Run2016F_23Sep2016_v1_MINIAOD","MuonEG_Run2016G_23Sep2016_v1_MINIAOD"],
            "color":1,
            "category":-1
            }
}

def Plot1D(var,x_name,y_name,nbins,xmin,xmax,logy=1,overflow=1,weights_to_apply=""):

    ###############################
    #
    #	PREAPRE HISTOGRAMS
    #
    ################################
    binwidth = float(xmax-xmin)/nbins
    if "[" in x_name: units_x = x_name.split("[")[1].split("]")[0]
    else: units_x = ""
    datahist = ROOT.TH1D("data",";%s;%s / %.1f %s"%(x_name,y_name,binwidth,units_x),nbins,xmin,xmax)
    MC_hists = {}
    for order in range(max(display_dict.keys())):
        MC_hists[order+1] = ROOT.TH1D("MC_%i"%(order+1),";%s;%s / %.1f %s"%(x_name,y_name,binwidth,units_x),nbins,xmin,xmax)
        MC_hists[order+1].Sumw2()
    ratio_hist = ROOT.TH1D("ratio",";%s;Data/MC"%(x_name),nbins,xmin,xmax)

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
            n_original = n_original_h.GetEntries()
            f_.Close()
            print n_original
            
            hist_tmp = ROOT.TH1D("h_"+f,";%s;%s / %.2f %s"%(x_name,y_name,binwidth,units_x),nbins,xmin,xmax)
            t_ = ROOT.TChain("tree")
            t_.Add(full_path)
            t_.Draw(var+">>h_"+f,weights_to_apply+"*(event_Category == %s)"%entry_dict["category"])
            t_.GetEntry(1)
            if t_.is_data == 1:
                continue

            xsec = xsec_table[f]*1000 #[fb]
            int_lumi=27.271 #[fb^-1	]
            scale = xsec*int_lumi/n_original
            #hist_tmp.SetBinContent(MC_hists[order_table[name]].GetNbinsX(),MC_hists[order_table[name]].GetBinContent(MC_hists[order_table[name]].GetNbinsX()+1))
            MC_hists[idx].Add(hist_tmp,scale)
            MC_hists[idx].SetFillColor(entry_dict["color"])
            #MC_hists[order_table[name]].SetFillStyle(4333)
            del hist_tmp
    
    #Data
    entry_dict = display_dict[-1]
    for f in entry_dict["samples"]:
        print f
        full_path = args.indir + "/" + f + ".root"
        hist_tmp = ROOT.TH1D("h_"+f,";%s;%s / %.2f %s"%(x_name,y_name,binwidth,units_x),nbins,xmin,xmax)
        t_ = ROOT.TChain("tree")
        t_.Add(full_path)
        t_.Draw(var+">>h_"+f)
        t_.GetEntry(1)
        if t_.is_data == 0:
            print "MIGHT NOT BE DATA, SKIPPING"
            continue
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
    mg = ROOT.THStack("mg",";%s;%s / %.2f %s"%(x_name,y_name,binwidth,units_x))
    summed_MC_hist = ROOT.TH1D("h_summed",";%s;%s / %.2f %s"%(x_name,y_name,binwidth,units_x),nbins,xmin,xmax)
    for idx,hist in MC_hists.iteritems():
        mg.Add(hist,"f")
        summed_MC_hist.Add(hist)
    mg.Draw("hist")
    if overflow: mg.GetXaxis().SetRange(1,mg.GetHistogram().GetNbinsX()+1)
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
    
    datahist.Draw("epx0 same")

    #redraw borders
    ROOT.gPad.RedrawAxis()
    line = ROOT.TLine()
    if overflow: line.DrawLine(xmax+binwidth, ROOT.gPad.GetUymin(), xmax+binwidth, ROOT.gPad.GetUymax())
    else:line.DrawLine(xmax, ROOT.gPad.GetUymin(), xmax, ROOT.gPad.GetUymax())
    
    #########
    # TEXT
    #########
    lumi = "%.1f"%int_lumi
    year = "2016"
    latex = ROOT.TLatex()
    latex.SetTextFont(42)
    latex.SetTextSize(0.05)
    latex.SetTextAlign(32)
    latex.DrawLatexNDC(0.94,0.94,lumi+" fb^{-1}, "+year)
    
    latex_cms = ROOT.TLatex()
    latex_cms.SetTextFont(42)
    latex_cms.SetTextSize(0.06)
    latex.SetTextAlign(11)
    latex_cms.DrawLatexNDC(0.19,0.83,"#bf{CMS} #it{Preliminary}")
    
    
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
    l.SetBorderSize(0)
    l.SetTextSize(0.05)
    l.Draw("same")
    
    
    
    

    downpad.cd()
    ROOT.gPad.SetMargin(0.15,0.05,0.4,0.01)
    #ROOT.gPad.SetGridy(1)
    ratio_hist = datahist.Clone()
    ratio_hist.Divide(summed_MC_hist)
    ratio_hist.SetMarkerStyle(20)
    ratio_hist.Draw("pe1x0")
    ratio_hist.GetYaxis().SetRangeUser(0.4,1.6)
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
    
    line3 = ROOT.TLine()
    line3.SetLineColor(1)
    line3.SetLineStyle(2)
    line3.SetLineWidth(2)
    if overflow: line3.DrawLine(xmin, 1, xmax+binwidth, 1)
    else: line3.DrawLine(xmin, 1, xmax, 1)
    line3.SetLineWidth(1)
    if overflow: line3.DrawLine(xmin, 0.75, xmax+binwidth, 0.75)
    else: line3.DrawLine(xmin, 0.75, xmax, 0.75)
    if overflow: line3.DrawLine(xmin, 1.25, xmax+binwidth, 1.25)
    else: line3.DrawLine(xmin, 1.25, xmax, 1.25)

	
    if not os.path.isdir(args.outdir): os.mkdir(args.outdir)
	
    if (logy): 
        c.SaveAs(args.outdir+"/"+var+"_stacked_Log.pdf")
        c.SaveAs(args.outdir+"/"+var+"_stacked_Log.png")
        c.SaveAs(args.outdir+"/"+var+"_stacked_Log.C")
    else: 
        c.SaveAs(args.outdir+"/"+var+"_stacked_Linear.pdf")
        c.SaveAs(args.outdir+"/"+var+"_stacked_Linear.png")
        c.SaveAs(args.outdir+"/"+var+"_stacked_Linear.C")
    




def main():
    
    weight_string = "weight_btag_iterativefit*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*pu_weight"
    no_weights = "1"
    
    Plot1D("DileptonInvariantMass","m_{ll} [GeV]","Events",20,0,500,logy=0,weights_to_apply=weight_string)
    Plot1D("DileptonDeltaR","#DeltaR(l,l)","Events",20,0,6,logy=0,weights_to_apply=weight_string)
    Plot1D("CSVv2_addJet1","CSVv2 Discriminator fisrt add. jet","Jets",10,0,1,logy=1,overflow=0,weights_to_apply=weight_string)
    Plot1D("CSVv2_addJet2","CSVv2 Discriminator second add. jet","Jets",10,0,1,logy=1,overflow=0,weights_to_apply=weight_string)
    Plot1D("nvertex","Number of primary vertices","Vertices",int(50/2.),-0.5,49.5,logy=0,overflow=0,weights_to_apply=weight_string)

if __name__ == "__main__":
    main()
