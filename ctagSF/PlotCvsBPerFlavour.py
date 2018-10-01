import ROOT
import os
import sys
from argparse import ArgumentParser
from array import array
from xsec import xsec_table
import numpy as np
from math import sqrt
import pickle

ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetOptStat(0)

parser = ArgumentParser()
parser.add_argument('--indir', default="FILL",help='input directory that contains all the samples')
parser.add_argument('--outdir', default=os.getcwd(),help='name of output directory')
parser.add_argument('--readsamples', default=False,help='either read the samples from indir or load them from pkl files')
parser.add_argument('--NormalizeMCToData', default=True,help='Normalize MC to data yields')
#parser.add_argument('--xsecdir', "default=/user/smoortga/Analysis/NTupler/CMSSW_8_0_25/src/FlatTree/FlatTreeAnalyzer/ttcc/analyse/xsec.py",help='name of xsec dir')
args = parser.parse_args()

samples_MC = [i for i in os.listdir(args.indir) if not "31Mar2018" in i]
samples_Data = [i for i in os.listdir(args.indir) if "31Mar2018" in i]


###############################
#
#	PREAPRE HISTOGRAMS
#
################################

weight_string = "weight_btag_iterativefit*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*mc_weight"#*pu_weight"

custom_bins = np.arange(0,1.05,0.05)
nbins=len(custom_bins)-1

histo_dict = {}
histo_dict["jet1"] = {
    "b" : ROOT.TH1D("b1",";DeepCSV CvsB first jet;Events",nbins,array("d",custom_bins)),
    "c" : ROOT.TH1D("c1",";DeepCSV CvsB first jet;Events",nbins,array("d",custom_bins)),
    "l" : ROOT.TH1D("l1",";DeepCSV CvsB first jet;Events",nbins,array("d",custom_bins)),
}
histo_dict["jet2"] = {
    "b" : ROOT.TH1D("b2",";DeepCSV CvsB second jet;Events",nbins,array("d",custom_bins)),
    "c" : ROOT.TH1D("c2",";DeepCSV CvsB second jet;Events",nbins,array("d",custom_bins)),
    "l" : ROOT.TH1D("l2",";DeepCSV CvsB second jet;Events",nbins,array("d",custom_bins)),
}
histo_dict["jet3"] = {
    "b" : ROOT.TH1D("b3",";DeepCSV CvsB third jet;Events",nbins,array("d",custom_bins)),
    "c" : ROOT.TH1D("c3",";DeepCSV CvsB third jet;Events",nbins,array("d",custom_bins)),
    "l" : ROOT.TH1D("l3",";DeepCSV CvsB third jet;Events",nbins,array("d",custom_bins)),
}

datahisto_dict = {
    "jet1" : ROOT.TH1D("data1",";DeepCSV CvsB first jet;Events",nbins,array("d",custom_bins)),
    "jet2" : ROOT.TH1D("data2",";DeepCSV CvsB second jet;Events",nbins,array("d",custom_bins)),
    "jet3" : ROOT.TH1D("data3",";DeepCSV CvsB thirdt jet;Events",nbins,array("d",custom_bins)),

}


if args.readsamples:
    ###############################
    #
    #	READ FILES
    #
    ################################

    # MC
    for file in samples_MC:
        f = file.split(".root")[0]
        print f
        full_path = args.indir + "/" + f + ".root"
        if not os.path.isfile(full_path): continue
        f_ = ROOT.TFile(full_path)
        n_original_h = f_.Get("hweight")
        n_original = n_original_h.GetBinContent(1)
        f_.Close()
        print n_original
    
        hist_tmp_b1 = ROOT.TH1D("h_b1_"+f,";CvsB first add. jet;Events",nbins,array("d",custom_bins))
        hist_tmp_c1 = ROOT.TH1D("h_c1_"+f,";CvsB first add. jet;Events",nbins,array("d",custom_bins))
        hist_tmp_l1 = ROOT.TH1D("h_l1_"+f,";CvsB first add. jet;Events",nbins,array("d",custom_bins))
        hist_tmp_b2 = ROOT.TH1D("h_b2_"+f,";CvsB second add. jet;Events",nbins,array("d",custom_bins))
        hist_tmp_c2 = ROOT.TH1D("h_c2_"+f,";CvsB second add. jet;Events",nbins,array("d",custom_bins))
        hist_tmp_l2 = ROOT.TH1D("h_l2_"+f,";CvsB second add. jet;Events",nbins,array("d",custom_bins))
        hist_tmp_b3 = ROOT.TH1D("h_b3_"+f,";CvsB thrid add. jet;Events",nbins,array("d",custom_bins))
        hist_tmp_c3 = ROOT.TH1D("h_c3_"+f,";CvsB thrid add. jet;Events",nbins,array("d",custom_bins))
        hist_tmp_l3 = ROOT.TH1D("h_l3_"+f,";CvsB thrid add. jet;Events",nbins,array("d",custom_bins))
        t_ = ROOT.TChain("tree")
        t_.Add(full_path)
        weights_to_apply = weight_string
        t_.Draw("DeepCSVcTagCvsB_addJet1>>h_b1_"+f,weights_to_apply+"*(hadronFlavour_addJet1 == 5)*(mc_pu_trueNumInt>10 && mc_pu_trueNumInt<70)")
        t_.Draw("DeepCSVcTagCvsB_addJet1>>h_c1_"+f,weights_to_apply+"*(hadronFlavour_addJet1 == 4)*(mc_pu_trueNumInt>10 && mc_pu_trueNumInt<70)")
        t_.Draw("DeepCSVcTagCvsB_addJet1>>h_l1_"+f,weights_to_apply+"*(hadronFlavour_addJet1 == 0)*(mc_pu_trueNumInt>10 && mc_pu_trueNumInt<70)")
        t_.Draw("DeepCSVcTagCvsB_addJet2>>h_b2_"+f,weights_to_apply+"*(hadronFlavour_addJet2 == 5)*(mc_pu_trueNumInt>10 && mc_pu_trueNumInt<70)")
        t_.Draw("DeepCSVcTagCvsB_addJet2>>h_c2_"+f,weights_to_apply+"*(hadronFlavour_addJet2 == 4)*(mc_pu_trueNumInt>10 && mc_pu_trueNumInt<70)")
        t_.Draw("DeepCSVcTagCvsB_addJet2>>h_l2_"+f,weights_to_apply+"*(hadronFlavour_addJet2 == 0)*(mc_pu_trueNumInt>10 && mc_pu_trueNumInt<70)")
        t_.Draw("DeepCSVcTagCvsB_addJet3>>h_b3_"+f,weights_to_apply+"*(hadronFlavour_addJet3 == 5)*(mc_pu_trueNumInt>10 && mc_pu_trueNumInt<70)")
        t_.Draw("DeepCSVcTagCvsB_addJet3>>h_c3_"+f,weights_to_apply+"*(hadronFlavour_addJet3 == 4)*(mc_pu_trueNumInt>10 && mc_pu_trueNumInt<70)")
        t_.Draw("DeepCSVcTagCvsB_addJet3>>h_l3_"+f,weights_to_apply+"*(hadronFlavour_addJet3 == 0)*(mc_pu_trueNumInt>10 && mc_pu_trueNumInt<70)")
    
    
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
        full_path = args.indir + "/" + f + ".root"
        if not os.path.isfile(full_path): continue
        f_ = ROOT.TFile(full_path)
        t_ = ROOT.TChain("tree")
        t_.Add(full_path)
    
        hist_tmp_data1 = ROOT.TH1D("h_data1_"+f,";CvsB first add. jet;Events",nbins,array("d",custom_bins))
        hist_tmp_data2 = ROOT.TH1D("h_data2_"+f,";CvsB second add. jet;Events",nbins,array("d",custom_bins))
        hist_tmp_data3 = ROOT.TH1D("h_data3_"+f,";CvsB thridt add. jet;Events",nbins,array("d",custom_bins))
        t_.Draw("DeepCSVcTagCvsB_addJet1>>h_data1_"+f)
        t_.Draw("DeepCSVcTagCvsB_addJet2>>h_data2_"+f)
        t_.Draw("DeepCSVcTagCvsB_addJet3>>h_data3_"+f)
    
        datahisto_dict["jet1"].Add(hist_tmp_data1.Clone())
        datahisto_dict["jet2"].Add(hist_tmp_data2.Clone())
        datahisto_dict["jet3"].Add(hist_tmp_data3.Clone())

    pickle.dump(histo_dict,open("MC_histograms.pkl","wb"))
    pickle.dump(datahisto_dict,open("Data_histograms.pkl","wb"))



else:
    histo_dict = pickle.load(open("MC_histograms.pkl","rb"))
    datahisto_dict = pickle.load(open("Data_histograms.pkl","rb"))



histo_dict["jet1"]["b"].SetFillColor(2)
histo_dict["jet1"]["c"].SetFillColor(ROOT.kGreen + 2)
histo_dict["jet1"]["l"].SetFillColor(4)
histo_dict["jet2"]["b"].SetFillColor(2)
histo_dict["jet2"]["c"].SetFillColor(ROOT.kGreen + 2)
histo_dict["jet2"]["l"].SetFillColor(4)
histo_dict["jet3"]["b"].SetFillColor(2)
histo_dict["jet3"]["c"].SetFillColor(ROOT.kGreen + 2)
histo_dict["jet3"]["l"].SetFillColor(4)

###############################
#
#	PLOTTING
#
################################

#
# Add Jet 1
#

c1 = ROOT.TCanvas("c1","c1",800,700)
c1.cd()
uppad1 = ROOT.TPad("u1","u1",0.,0.25,1.,1.)
downpad1 = ROOT.TPad("d1","d1",0.,0.0,1.,0.25)
uppad1.Draw()
downpad1.Draw()

uppad1.cd()
ROOT.gPad.SetLogy(0)
ROOT.gPad.SetMargin(0.15,0.05,0.01,0.1)

mg1 = ROOT.THStack("mg1",";CvsB first add. jet;Events")
summed_MC_hist1 = ROOT.TH1F("h_summed1",";CvsB first add. jet;Events",nbins,array("d",custom_bins))
summed_MC_hist1.Sumw2()

for flav,hist in histo_dict["jet1"].iteritems():
    mg1.Add(hist,"f")
    summed_MC_hist1.Add(hist)  

if (args.NormalizeMCToData):
    for flav,hist in histo_dict["jet1"].iteritems():
        hist.Scale(datahisto_dict["jet1"].Integral()/summed_MC_hist1.Integral()) 
    summed_MC_hist1.Scale(datahisto_dict["jet1"].Integral()/summed_MC_hist1.Integral())

mg1.Draw("hist")
mg1.GetHistogram().SetLineWidth(0)
ROOT.TGaxis.SetMaxDigits(3)
mg1.SetMinimum(0.1)
mg1.SetMaximum(1.4*summed_MC_hist1.GetBinContent(summed_MC_hist1.GetMaximumBin()))
mg1.GetYaxis().SetLabelSize(0.05)
mg1.GetYaxis().SetLabelOffset(0.01)
mg1.GetYaxis().SetTitleSize(0.06)
mg1.GetYaxis().SetTitleOffset(1.2)
mg1.GetXaxis().SetTitleSize(0.0)
mg1.GetXaxis().SetLabelSize(0.0)

summed_MC_hist1.SetFillStyle(3244)
summed_MC_hist1.SetFillColor(13)
summed_MC_hist1.SetLineWidth(0)
summed_MC_hist1.Draw("same E2")

datahisto_dict["jet1"].SetMarkerStyle(20)
datahisto_dict["jet1"].SetLineColor(1)
datahisto_dict["jet1"].SetLineWidth(2)
datahisto_dict["jet1"].Draw("epx0 same")

#########
# TEXT
#########
int_lumi=41.527
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

if (args.NormalizeMCToData): 
    latex_normalized = ROOT.TLatex()   
    latex_normalized.SetTextFont(72)
    latex_normalized.SetTextSize(0.04)
    latex_normalized.SetTextAlign(11)
    latex_normalized.DrawLatexNDC(0.19,0.75,"MC normalized to data")
    
#############
# LEGEND
#############
l = ROOT.TLegend(0.7,0.55,0.94,0.89)
l.SetNColumns(1)
l.AddEntry(histo_dict["jet1"]["b"],"b jets","f")
l.AddEntry(histo_dict["jet1"]["c"],"c jets","f")
l.AddEntry(histo_dict["jet1"]["l"],"udsg jets","f")
l.AddEntry(datahisto_dict["jet1"],"Data","ep")
l.SetFillStyle(0)
l.SetBorderSize(0)
l.SetTextSize(0.05)
l.Draw("same")



downpad1.cd()
ROOT.gPad.SetMargin(0.15,0.05,0.4,0.01)
#ratio hist
ratio_hist1 = datahisto_dict["jet1"].Clone()
ratio_hist1.Divide(summed_MC_hist1)
ratio_hist1.SetMarkerStyle(20)
ratio_hist1.Draw("pe1x0")
ratio_hist1.GetYaxis().SetRangeUser(0.3,1.7)
ratio_hist1.GetYaxis().SetNdivisions(4)
ratio_hist1.GetYaxis().SetLabelSize(0.14)
ratio_hist1.GetYaxis().SetLabelOffset(0.01)
ratio_hist1.GetYaxis().SetTitle("#frac{data}{MC}")
ratio_hist1.GetYaxis().SetTitleSize(0.16)
ratio_hist1.GetYaxis().CenterTitle()
ratio_hist1.GetYaxis().SetTitleOffset(0.4)
ratio_hist1.GetXaxis().SetTitleSize(0.19)
ratio_hist1.GetXaxis().SetTitleOffset(0.9)
ratio_hist1.GetXaxis().SetLabelSize(0.14)

# MC stat uncertainty
MC_ratio_hist1 = summed_MC_hist1.Clone()
MC_ratio_hist1.Divide(summed_MC_hist1)
MC_ratio_hist1.Draw("same E2")

ratio_hist1.Draw("same pe1x0")

line3 = ROOT.TLine()
line3.SetLineColor(1)
line3.SetLineStyle(2)
line3.SetLineWidth(2)
line3.SetLineWidth(1)
line3.DrawLine(min(custom_bins), 0.75, max(custom_bins), 0.75)
line3.DrawLine(min(custom_bins), 1.25, max(custom_bins), 1.25)

c1.SaveAs(args.outdir+"/CvsB_AddJet1.pdf")


#
# Add Jet 2
#

c2 = ROOT.TCanvas("c2","c2",800,700)
c2.cd()
uppad2 = ROOT.TPad("u2","u2",0.,0.25,1.,1.)
downpad2 = ROOT.TPad("d2","d2",0.,0.0,1.,0.25)
uppad2.Draw()
downpad2.Draw()

uppad2.cd()
ROOT.gPad.SetLogy(0)
ROOT.gPad.SetMargin(0.15,0.05,0.01,0.1)

mg2 = ROOT.THStack("mg2",";CvsB first add. jet;Events")
summed_MC_hist2 = ROOT.TH1F("h_summed2",";CvsB first add. jet;Events",nbins,array("d",custom_bins))
summed_MC_hist2.Sumw2()

for flav,hist in histo_dict["jet2"].iteritems():
    mg2.Add(hist,"f")
    summed_MC_hist2.Add(hist)  

if (args.NormalizeMCToData):
    for flav,hist in histo_dict["jet2"].iteritems():
        hist.Scale(datahisto_dict["jet2"].Integral()/summed_MC_hist2.Integral()) 
    summed_MC_hist2.Scale(datahisto_dict["jet2"].Integral()/summed_MC_hist2.Integral())

mg2.Draw("hist")
mg2.GetHistogram().SetLineWidth(0)
ROOT.TGaxis.SetMaxDigits(3)
mg2.SetMinimum(0.1)
mg2.SetMaximum(1.6*summed_MC_hist2.GetBinContent(summed_MC_hist2.GetMaximumBin()))
mg2.GetYaxis().SetLabelSize(0.05)
mg2.GetYaxis().SetLabelOffset(0.01)
mg2.GetYaxis().SetTitleSize(0.06)
mg2.GetYaxis().SetTitleOffset(1.2)
mg2.GetXaxis().SetTitleSize(0.0)
mg2.GetXaxis().SetLabelSize(0.0)

summed_MC_hist2.SetFillStyle(3244)
summed_MC_hist2.SetFillColor(13)
summed_MC_hist2.SetLineWidth(0)
summed_MC_hist2.Draw("same E2")

datahisto_dict["jet2"].SetMarkerStyle(20)
datahisto_dict["jet2"].SetLineColor(1)
datahisto_dict["jet2"].SetLineWidth(2)
datahisto_dict["jet2"].Draw("epx0 same")

#########
# TEXT
#########

latex.DrawLatexNDC(0.94,0.94,lumi+" fb^{-1}, "+year)
latex_cms.DrawLatexNDC(0.19,0.83,"#bf{CMS} #it{Preliminary}")

if (args.NormalizeMCToData): 
    latex_normalized.DrawLatexNDC(0.19,0.75,"MC normalized to data")
    
#############
# LEGEND
#############
l.Draw("same")



downpad2.cd()
ROOT.gPad.SetMargin(0.15,0.05,0.4,0.01)
#ratio hist
ratio_hist2 = datahisto_dict["jet2"].Clone()
ratio_hist2.Divide(summed_MC_hist2)
ratio_hist2.SetMarkerStyle(20)
ratio_hist2.Draw("pe1x0")
ratio_hist2.GetYaxis().SetRangeUser(0.3,1.7)
ratio_hist2.GetYaxis().SetNdivisions(4)
ratio_hist2.GetYaxis().SetLabelSize(0.14)
ratio_hist2.GetYaxis().SetLabelOffset(0.01)
ratio_hist2.GetYaxis().SetTitle("#frac{data}{MC}")
ratio_hist2.GetYaxis().SetTitleSize(0.16)
ratio_hist2.GetYaxis().CenterTitle()
ratio_hist2.GetYaxis().SetTitleOffset(0.4)
ratio_hist2.GetXaxis().SetTitleSize(0.19)
ratio_hist2.GetXaxis().SetTitleOffset(0.9)
ratio_hist2.GetXaxis().SetLabelSize(0.14)

# MC stat uncertainty
MC_ratio_hist2 = summed_MC_hist2.Clone()
MC_ratio_hist2.Divide(summed_MC_hist2)
MC_ratio_hist2.Draw("same E2")

ratio_hist2.Draw("same pe1x0")

line3.DrawLine(min(custom_bins), 0.75, max(custom_bins), 0.75)
line3.DrawLine(min(custom_bins), 1.25, max(custom_bins), 1.25)

c2.SaveAs(args.outdir+"/CvsB_AddJet2.pdf")


#
# Add Jet 3
#

c3 = ROOT.TCanvas("c3","c3",800,700)
c3.cd()
uppad3 = ROOT.TPad("u3","u3",0.,0.25,1.,1.)
downpad3 = ROOT.TPad("d3","d3",0.,0.0,1.,0.25)
uppad3.Draw()
downpad3.Draw()

uppad3.cd()
ROOT.gPad.SetLogy(0)
ROOT.gPad.SetMargin(0.15,0.05,0.01,0.1)

mg3 = ROOT.THStack("mg3",";CvsB first add. jet;Events")
summed_MC_hist3 = ROOT.TH1F("h_summed3",";CvsB first add. jet;Events",nbins,array("d",custom_bins))
summed_MC_hist3.Sumw2()

for flav,hist in histo_dict["jet3"].iteritems():
    mg3.Add(hist,"f")
    summed_MC_hist3.Add(hist)  

if (args.NormalizeMCToData):
    for flav,hist in histo_dict["jet3"].iteritems():
        hist.Scale(datahisto_dict["jet3"].Integral()/summed_MC_hist3.Integral()) 
    summed_MC_hist3.Scale(datahisto_dict["jet3"].Integral()/summed_MC_hist3.Integral())

mg3.Draw("hist")
mg3.GetHistogram().SetLineWidth(0)
ROOT.TGaxis.SetMaxDigits(3)
mg3.SetMinimum(0.1)
mg3.SetMaximum(1.6*summed_MC_hist3.GetBinContent(summed_MC_hist3.GetMaximumBin()))
mg3.GetYaxis().SetLabelSize(0.05)
mg3.GetYaxis().SetLabelOffset(0.01)
mg3.GetYaxis().SetTitleSize(0.06)
mg3.GetYaxis().SetTitleOffset(1.2)
mg3.GetXaxis().SetTitleSize(0.0)
mg3.GetXaxis().SetLabelSize(0.0)

summed_MC_hist3.SetFillStyle(3244)
summed_MC_hist3.SetFillColor(13)
summed_MC_hist3.SetLineWidth(0)
summed_MC_hist3.Draw("same E2")

datahisto_dict["jet3"].SetMarkerStyle(20)
datahisto_dict["jet3"].SetLineColor(1)
datahisto_dict["jet3"].SetLineWidth(2)
datahisto_dict["jet3"].Draw("epx0 same")

#########
# TEXT
#########
latex.DrawLatexNDC(0.94,0.94,lumi+" fb^{-1}, "+year)
latex_cms.DrawLatexNDC(0.19,0.83,"#bf{CMS} #it{Preliminary}")

if (args.NormalizeMCToData): 
    latex_normalized.DrawLatexNDC(0.19,0.75,"MC normalized to data")
    
#############
# LEGEND
#############
l.Draw("same")



downpad3.cd()
ROOT.gPad.SetMargin(0.15,0.05,0.4,0.01)
#ratio hist
ratio_hist3 = datahisto_dict["jet3"].Clone()
ratio_hist3.Divide(summed_MC_hist3)
ratio_hist3.SetMarkerStyle(20)
ratio_hist3.Draw("pe1x0")
ratio_hist3.GetYaxis().SetRangeUser(0.3,1.7)
ratio_hist3.GetYaxis().SetNdivisions(4)
ratio_hist3.GetYaxis().SetLabelSize(0.14)
ratio_hist3.GetYaxis().SetLabelOffset(0.01)
ratio_hist3.GetYaxis().SetTitle("#frac{data}{MC}")
ratio_hist3.GetYaxis().SetTitleSize(0.16)
ratio_hist3.GetYaxis().CenterTitle()
ratio_hist3.GetYaxis().SetTitleOffset(0.4)
ratio_hist3.GetXaxis().SetTitleSize(0.19)
ratio_hist3.GetXaxis().SetTitleOffset(0.9)
ratio_hist3.GetXaxis().SetLabelSize(0.14)

# MC stat uncertainty
MC_ratio_hist3 = summed_MC_hist3.Clone()
MC_ratio_hist3.Divide(summed_MC_hist3)
MC_ratio_hist3.Draw("same E2")

ratio_hist3.Draw("same pe1x0")

line3.DrawLine(min(custom_bins), 0.75, max(custom_bins), 0.75)
line3.DrawLine(min(custom_bins), 1.25, max(custom_bins), 1.25)

c3.SaveAs(args.outdir+"/CvsB_AddJet3.pdf")


