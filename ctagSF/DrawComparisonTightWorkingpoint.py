import ROOT
import numpy as np

ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetOptStat(0)

import os

cTagSFf_ = ROOT.TFile("DeepCSV_cTag_SFs_94X.root")
hist_DeepCSVcTag_SFb = cTagSFf_.Get("SFb_hist_central")
hist_DeepCSVcTag_SFc = cTagSFf_.Get("SFc_hist_central")
hist_DeepCSVcTag_SFl = cTagSFf_.Get("SFl_hist_central")
hist_DeepCSVcTag_SFb_Up = cTagSFf_.Get("SFb_hist_Up")
hist_DeepCSVcTag_SFc_Up = cTagSFf_.Get("SFc_hist_Up")
hist_DeepCSVcTag_SFl_Up = cTagSFf_.Get("SFl_hist_Up")
hist_DeepCSVcTag_SFb_Down = cTagSFf_.Get("SFb_hist_Down")
hist_DeepCSVcTag_SFc_Down = cTagSFf_.Get("SFc_hist_Down")
hist_DeepCSVcTag_SFl_Down = cTagSFf_.Get("SFl_hist_Down")

# see working points at: https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation94X
def TightWPLight(x,syst="central"):
	if syst=="central":
		return 0.48786-0.000380882*x+1.29355e-06*x*x+0.0838231/x
	elif syst=="up":
		return 1*x/x
	elif syst=="down":
		return 0*x/x
	    
x = np.arange(30,200,1)
y_l_central = TightWPLight(x,"central")
y_l_up = TightWPLight(x,"up")
y_l_down = TightWPLight(x,"down")
y_l_uperr = y_l_up-y_l_central
y_l_downerr = y_l_central-y_l_down

c_l = ROOT.TCanvas("c_l","c_l",800,600)
c_l.SetGrid()
c_l.SetMargin(0.15,0.05,0.15,0.1)

mg_l = ROOT.TMultiGraph("mg_l",";jet p_{T} [GeV];SF_{light}")

ItertativeFit_graph_l_TightWP = ROOT.TGraphAsymmErrors(1,np.asarray([80.]),np.asarray([hist_DeepCSVcTag_SFl.GetBinContent(2,2)]),np.asarray([50.]),np.asarray([120.]),np.asarray([hist_DeepCSVcTag_SFl_Up.GetBinContent(2,2)-hist_DeepCSVcTag_SFl.GetBinContent(2,2)]),np.asarray([hist_DeepCSVcTag_SFl.GetBinContent(2,2)-hist_DeepCSVcTag_SFl_Down.GetBinContent(2,2)]) )
ItertativeFit_graph_l_TightWP.SetTitle(";pT;SFl")
ItertativeFit_graph_l_TightWP.SetMarkerStyle(20)
ItertativeFit_graph_l_TightWP.SetMarkerSize(2)
ItertativeFit_graph_l_TightWP.SetMarkerColor(2)
ItertativeFit_graph_l_TightWP.SetLineColor(2)
ItertativeFit_graph_l_TightWP.SetLineWidth(4)
#ItertativeFit_graph_l_TightWP.SetPoint(0,100,hist_DeepCSVcTag_SFl.GetBinContent(2,2))
#ItertativeFit_graph_l_TightWP.DrawClone("APE")

TightWP_l_Graph = ROOT.TGraphAsymmErrors(len(x),np.asarray([float(i) for i in x]),y_l_central,np.asarray([0.01]*len(x)),np.asarray([0.01]*len(x)),y_l_downerr,y_l_uperr)
TightWP_l_Graph.SetFillColor(4)
TightWP_l_Graph.SetFillStyle(3002)
TightWP_l_Graph.SetLineWidth(2)
#TightWP_l_Graph.DrawClone("E3same")



mg_l.Add(TightWP_l_Graph,"3L")
mg_l.Add(ItertativeFit_graph_l_TightWP,"P")

mg_l.Draw("AP3L")
mg_l.GetYaxis().SetRangeUser(-0.1,1.8)
mg_l.GetYaxis().SetTitleSize(0.055)
mg_l.GetYaxis().SetTitleOffset(1.1)
mg_l.GetYaxis().CenterTitle()
mg_l.GetXaxis().SetTitleSize(0.055)
mg_l.GetXaxis().SetTitleOffset(1.1)

leg_l = ROOT.TLegend(0.2,0.65,0.7,0.87)
leg_l.SetHeader("Tight WP (DeepCSV c-tag)")
leg_l.SetTextSize(0.05)
leg_l.AddEntry(ItertativeFit_graph_l_TightWP,"Iterative fit","pe")
leg_l.AddEntry(TightWP_l_Graph,"W+c","fl")
leg_l.Draw("same")

c_l.SaveAs("./CompareLightSFTightWP.pdf")






def TightWPB(x,syst="central"):
	if syst=="central":
		if x >= 30 and x < 60:
			return 0.96424
		elif x >= 60 and x < 100:
			return 0.98614
		elif x >= 100 and x < 140:
			return 0.90355
		else: 
			return 0.93414
	elif syst=="up":
		if x >= 30 and x < 60:
			return 1.062
		elif x >= 60 and x < 100:
			return 1.0607
		elif x >= 100 and x < 140:
			return 0.94879
		else: 
			return 0.99416
	elif syst=="down":
		if x >= 30 and x < 60:
			return 0.86644
		elif x >= 60 and x < 100:
			return 0.91159
		elif x >= 100 and x < 140:
			return 0.85832
		else: 
			return 0.87412
			

y_b_central = np.asarray([TightWPB(i,"central") for i in x])
y_b_up = np.asarray([TightWPB(i,"up") for i in x])
y_b_down = np.asarray([TightWPB(i,"down") for i in x])
y_b_uperr = y_b_up-y_b_central
y_b_downerr = y_b_central-y_b_down

c_b = ROOT.TCanvas("c_b","c_b",800,600)
c_b.SetGrid()
c_b.SetMargin(0.15,0.05,0.15,0.1)

mg_b = ROOT.TMultiGraph("mg_b",";jet p_{T} [GeV];SF_{b}")

ItertativeFit_graph_b_TightWP = ROOT.TGraphAsymmErrors(1,np.asarray([80.]),np.asarray([hist_DeepCSVcTag_SFb.GetBinContent(2,2)]),np.asarray([50.]),np.asarray([120.]),np.asarray([hist_DeepCSVcTag_SFb_Up.GetBinContent(2,2)-hist_DeepCSVcTag_SFb.GetBinContent(2,2)]),np.asarray([hist_DeepCSVcTag_SFb.GetBinContent(2,2)-hist_DeepCSVcTag_SFb_Down.GetBinContent(2,2)]) )
ItertativeFit_graph_b_TightWP.SetTitle(";pT;SFl")
ItertativeFit_graph_b_TightWP.SetMarkerStyle(20)
ItertativeFit_graph_b_TightWP.SetMarkerSize(2)
ItertativeFit_graph_b_TightWP.SetMarkerColor(2)
ItertativeFit_graph_b_TightWP.SetLineColor(2)
ItertativeFit_graph_b_TightWP.SetLineWidth(4)
#ItertativeFit_graph_b_TightWP.SetPoint(0,100,hist_DeepCSVcTag_SFl.GetBinContent(2,2))
#ItertativeFit_graph_b_TightWP.DrawClone("APE")

TightWP_b_Graph = ROOT.TGraphAsymmErrors(len(x),np.asarray([float(i) for i in x]),y_b_central,np.asarray([0.01]*len(x)),np.asarray([0.01]*len(x)),y_b_downerr,y_b_uperr)
TightWP_b_Graph.SetFillColor(4)
TightWP_b_Graph.SetFillStyle(3002)
TightWP_b_Graph.SetLineWidth(2)
#TightWP_b_Graph.DrawClone("E3same")



mg_b.Add(TightWP_b_Graph,"3L")
mg_b.Add(ItertativeFit_graph_b_TightWP,"P")

mg_b.Draw("AP3L")
mg_b.GetYaxis().SetRangeUser(0.8,1.25)
mg_b.GetYaxis().SetTitleSize(0.055)
mg_b.GetYaxis().SetTitleOffset(1.1)
mg_b.GetYaxis().CenterTitle()
mg_b.GetXaxis().SetTitleSize(0.055)
mg_b.GetXaxis().SetTitleOffset(1.1)

leg_b = ROOT.TLegend(0.2,0.65,0.7,0.87)
leg_b.SetHeader("Tight WP (DeepCSV c-tag)")
leg_b.SetTextSize(0.05)
leg_b.AddEntry(ItertativeFit_graph_b_TightWP,"Iterative fit","pe")
leg_b.AddEntry(TightWP_b_Graph,"W+c","fl")
leg_b.Draw("same")

c_b.SaveAs("./CompareBSFTightWP.pdf")





def TightWPC(x,syst="central"):
	if syst=="central":
		if x >= 30 and x < 50:
			return 0.804223
		elif x >= 50 and x < 70:
			return 0.805358
		else: 
			return 0.760651
	elif syst=="up":
		if x >= 30 and x < 50:
			return 0.804223+0.037553
		elif x >= 50 and x < 70:
			return 0.805358+0.045192
		else: 
			return 0.760651+0.037794
	elif syst=="down":
		if x >= 30 and x < 50:
			return 0.804223-0.037553
		elif x >= 50 and x < 70:
			return 0.805358-0.045192
		else: 
			return 0.760651-0.037794
			

y_c_central = np.asarray([TightWPC(i,"central") for i in x])
y_c_up = np.asarray([TightWPC(i,"up") for i in x])
y_c_down = np.asarray([TightWPC(i,"down") for i in x])
y_c_uperr = y_c_up-y_c_central
y_c_downerr = y_c_central-y_c_down

c_c = ROOT.TCanvas("c_c","c_c",800,600)
c_c.SetGrid()
c_c.SetMargin(0.15,0.05,0.15,0.1)

mg_c = ROOT.TMultiGraph("mg_c",";jet p_{T} [GeV];SF_{c}")

ItertativeFit_graph_c_TightWP = ROOT.TGraphAsymmErrors(1,np.asarray([80.]),np.asarray([hist_DeepCSVcTag_SFc.GetBinContent(2,2)]),np.asarray([50.]),np.asarray([120.]),np.asarray([hist_DeepCSVcTag_SFc_Up.GetBinContent(2,2)-hist_DeepCSVcTag_SFc.GetBinContent(2,2)]),np.asarray([hist_DeepCSVcTag_SFc.GetBinContent(2,2)-hist_DeepCSVcTag_SFc_Down.GetBinContent(2,2)]) )
ItertativeFit_graph_c_TightWP.SetTitle(";pT;SFl")
ItertativeFit_graph_c_TightWP.SetMarkerStyle(20)
ItertativeFit_graph_c_TightWP.SetMarkerSize(2)
ItertativeFit_graph_c_TightWP.SetMarkerColor(2)
ItertativeFit_graph_c_TightWP.SetLineColor(2)
ItertativeFit_graph_c_TightWP.SetLineWidth(4)
#ItertativeFit_graph_c_TightWP.SetPoint(0,100,hist_DeepCSVcTag_SFl.GetBinContent(2,2))
#ItertativeFit_graph_c_TightWP.DrawClone("APE")

TightWP_c_Graph = ROOT.TGraphAsymmErrors(len(x),np.asarray([float(i) for i in x]),y_c_central,np.asarray([0.01]*len(x)),np.asarray([0.01]*len(x)),y_c_downerr,y_c_uperr)
TightWP_c_Graph.SetFillColor(4)
TightWP_c_Graph.SetFillStyle(3002)
TightWP_c_Graph.SetLineWidth(2)
#TightWP_c_Graph.DrawClone("E3same")



mg_c.Add(TightWP_c_Graph,"3L")
mg_c.Add(ItertativeFit_graph_c_TightWP,"P")

mg_c.Draw("AP3L")
mg_c.GetYaxis().SetRangeUser(0.55,1.15)
mg_c.GetYaxis().SetTitleSize(0.055)
mg_c.GetYaxis().SetTitleOffset(1.1)
mg_c.GetYaxis().CenterTitle()
mg_c.GetXaxis().SetTitleSize(0.055)
mg_c.GetXaxis().SetTitleOffset(1.1)

leg_c = ROOT.TLegend(0.2,0.65,0.7,0.87)
leg_c.SetHeader("Tight WP (DeepCSV c-tag)")
leg_c.SetTextSize(0.05)
leg_c.AddEntry(ItertativeFit_graph_c_TightWP,"Iterative fit","pe")
leg_c.AddEntry(TightWP_c_Graph,"W+c","fl")
leg_c.Draw("same")

c_c.SaveAs("./CompareCSFTightWP.pdf")
