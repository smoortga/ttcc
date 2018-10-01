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
def MediumWPLight(x,syst="central"):
	if syst=="central":
		return 1.07268+5.03743e-05*x+6.07487e-08*x*x-(1.48248/x)
	elif syst=="up":
		return (1.07268+5.03743e-05*x+6.07487e-08*x*x-1.48248/x)*(1+(0.0260841-1.66457e-05*x+2.2344e-08*x*x))
	elif syst=="down":
		return (1.07268+5.03743e-05*x+6.07487e-08*x*x-1.48248/x)*(1-(0.0260841-1.66457e-05*x+2.2344e-08*x*x))
	    
x = np.arange(30,200,1)
y_l_central = MediumWPLight(x,"central")
y_l_up = MediumWPLight(x,"up")
y_l_down = MediumWPLight(x,"down")
y_l_uperr = y_l_up-y_l_central
y_l_downerr = y_l_central-y_l_down

c_l = ROOT.TCanvas("c_l","c_l",800,600)
c_l.SetGrid()
c_l.SetMargin(0.15,0.05,0.15,0.1)

mg_l = ROOT.TMultiGraph("mg_l",";jet p_{T} [GeV];SF_{light}")

ItertativeFit_graph_l_MediumWP = ROOT.TGraphAsymmErrors(1,np.asarray([80.]),np.asarray([hist_DeepCSVcTag_SFl.GetBinContent(2,2)]),np.asarray([50.]),np.asarray([120.]),np.asarray([hist_DeepCSVcTag_SFl_Up.GetBinContent(2,2)-hist_DeepCSVcTag_SFl.GetBinContent(2,2)]),np.asarray([hist_DeepCSVcTag_SFl.GetBinContent(2,2)-hist_DeepCSVcTag_SFl_Down.GetBinContent(2,2)]) )
ItertativeFit_graph_l_MediumWP.SetTitle(";pT;SFl")
ItertativeFit_graph_l_MediumWP.SetMarkerStyle(20)
ItertativeFit_graph_l_MediumWP.SetMarkerSize(2)
ItertativeFit_graph_l_MediumWP.SetMarkerColor(2)
ItertativeFit_graph_l_MediumWP.SetLineColor(2)
ItertativeFit_graph_l_MediumWP.SetLineWidth(4)
#ItertativeFit_graph_l_MediumWP.SetPoint(0,100,hist_DeepCSVcTag_SFl.GetBinContent(2,2))
#ItertativeFit_graph_l_MediumWP.DrawClone("APE")

MediumWP_l_Graph = ROOT.TGraphAsymmErrors(len(x),np.asarray([float(i) for i in x]),y_l_central,np.asarray([0.01]*len(x)),np.asarray([0.01]*len(x)),y_l_downerr,y_l_uperr)
MediumWP_l_Graph.SetFillColor(4)
MediumWP_l_Graph.SetFillStyle(3002)
MediumWP_l_Graph.SetLineWidth(2)
#MediumWP_l_Graph.DrawClone("E3same")



mg_l.Add(MediumWP_l_Graph,"3L")
mg_l.Add(ItertativeFit_graph_l_MediumWP,"P")

mg_l.Draw("AP3L")
mg_l.GetYaxis().SetRangeUser(0.95,1.2)
mg_l.GetYaxis().SetTitleSize(0.055)
mg_l.GetYaxis().SetTitleOffset(1.1)
mg_l.GetYaxis().CenterTitle()
mg_l.GetXaxis().SetTitleSize(0.055)
mg_l.GetXaxis().SetTitleOffset(1.1)

leg_l = ROOT.TLegend(0.2,0.65,0.7,0.87)
leg_l.SetHeader("Medium WP (DeepCSV c-tag)")
leg_l.SetTextSize(0.05)
leg_l.AddEntry(ItertativeFit_graph_l_MediumWP,"Iterative fit","pe")
leg_l.AddEntry(MediumWP_l_Graph,"W+c","fl")
leg_l.Draw("same")

c_l.SaveAs("./CompareLightSFMediumWP.pdf")






def MediumWPB(x,syst="central"):
	if syst=="central":
		if x >= 30 and x < 60:
			return 1.0551
		elif x >= 60 and x < 100:
			return 1.0479
		elif x >= 100 and x < 140:
			return 1.1365
		else: 
			return 1.1011
	elif syst=="up":
		if x >= 30 and x < 60:
			return 1.1351
		elif x >= 60 and x < 100:
			return 1.1181
		elif x >= 100 and x < 140:
			return 1.174
		else: 
			return 1.1392
	elif syst=="down":
		if x >= 30 and x < 60:
			return 0.97515
		elif x >= 60 and x < 100:
			return 0.97772
		elif x >= 100 and x < 140:
			return 1.0989
		else: 
			return 1.063
			

y_b_central = np.asarray([MediumWPB(i,"central") for i in x])
y_b_up = np.asarray([MediumWPB(i,"up") for i in x])
y_b_down = np.asarray([MediumWPB(i,"down") for i in x])
y_b_uperr = y_b_up-y_b_central
y_b_downerr = y_b_central-y_b_down

c_b = ROOT.TCanvas("c_b","c_b",800,600)
c_b.SetGrid()
c_b.SetMargin(0.15,0.05,0.15,0.1)

mg_b = ROOT.TMultiGraph("mg_b",";jet p_{T} [GeV];SF_{b}")

ItertativeFit_graph_b_MediumWP = ROOT.TGraphAsymmErrors(1,np.asarray([80.]),np.asarray([hist_DeepCSVcTag_SFb.GetBinContent(2,2)]),np.asarray([50.]),np.asarray([120.]),np.asarray([hist_DeepCSVcTag_SFb_Up.GetBinContent(2,2)-hist_DeepCSVcTag_SFb.GetBinContent(2,2)]),np.asarray([hist_DeepCSVcTag_SFb.GetBinContent(2,2)-hist_DeepCSVcTag_SFb_Down.GetBinContent(2,2)]) )
ItertativeFit_graph_b_MediumWP.SetTitle(";pT;SFl")
ItertativeFit_graph_b_MediumWP.SetMarkerStyle(20)
ItertativeFit_graph_b_MediumWP.SetMarkerSize(2)
ItertativeFit_graph_b_MediumWP.SetMarkerColor(2)
ItertativeFit_graph_b_MediumWP.SetLineColor(2)
ItertativeFit_graph_b_MediumWP.SetLineWidth(4)
#ItertativeFit_graph_b_MediumWP.SetPoint(0,100,hist_DeepCSVcTag_SFl.GetBinContent(2,2))
#ItertativeFit_graph_b_MediumWP.DrawClone("APE")

MediumWP_b_Graph = ROOT.TGraphAsymmErrors(len(x),np.asarray([float(i) for i in x]),y_b_central,np.asarray([0.01]*len(x)),np.asarray([0.01]*len(x)),y_b_downerr,y_b_uperr)
MediumWP_b_Graph.SetFillColor(4)
MediumWP_b_Graph.SetFillStyle(3002)
MediumWP_b_Graph.SetLineWidth(2)
#MediumWP_b_Graph.DrawClone("E3same")



mg_b.Add(MediumWP_b_Graph,"3L")
mg_b.Add(ItertativeFit_graph_b_MediumWP,"P")

mg_b.Draw("AP3L")
mg_b.GetYaxis().SetRangeUser(0.9,1.35)
mg_b.GetYaxis().SetTitleSize(0.055)
mg_b.GetYaxis().SetTitleOffset(1.1)
mg_b.GetYaxis().CenterTitle()
mg_b.GetXaxis().SetTitleSize(0.055)
mg_b.GetXaxis().SetTitleOffset(1.1)

leg_b = ROOT.TLegend(0.2,0.65,0.7,0.87)
leg_b.SetHeader("Medium WP (DeepCSV c-tag)")
leg_b.SetTextSize(0.05)
leg_b.AddEntry(ItertativeFit_graph_b_MediumWP,"Iterative fit","pe")
leg_b.AddEntry(MediumWP_b_Graph,"W+c","fl")
leg_b.Draw("same")

c_b.SaveAs("./CompareBSFMediumWP.pdf")





def MediumWPC(x,syst="central"):
	if syst=="central":
		if x >= 30 and x < 50:
			return 0.937367
		elif x >= 50 and x < 70:
			return 0.949114
		else: 
			return 0.984301
	elif syst=="up":
		if x >= 30 and x < 50:
			return 0.937367+0.027096
		elif x >= 50 and x < 70:
			return 0.949114+0.042109
		else: 
			return 0.984301+0.035577
	elif syst=="down":
		if x >= 30 and x < 50:
			return 0.937367-0.027096
		elif x >= 50 and x < 70:
			return 0.949114-0.042109
		else: 
			return 0.984301-0.035577
			

y_c_central = np.asarray([MediumWPC(i,"central") for i in x])
y_c_up = np.asarray([MediumWPC(i,"up") for i in x])
y_c_down = np.asarray([MediumWPC(i,"down") for i in x])
y_c_uperr = y_c_up-y_c_central
y_c_downerr = y_c_central-y_c_down

c_c = ROOT.TCanvas("c_c","c_c",800,600)
c_c.SetGrid()
c_c.SetMargin(0.15,0.05,0.15,0.1)

mg_c = ROOT.TMultiGraph("mg_c",";jet p_{T} [GeV];SF_{c}")

ItertativeFit_graph_c_MediumWP = ROOT.TGraphAsymmErrors(1,np.asarray([80.]),np.asarray([hist_DeepCSVcTag_SFc.GetBinContent(2,2)]),np.asarray([50.]),np.asarray([120.]),np.asarray([hist_DeepCSVcTag_SFc_Up.GetBinContent(2,2)-hist_DeepCSVcTag_SFc.GetBinContent(2,2)]),np.asarray([hist_DeepCSVcTag_SFc.GetBinContent(2,2)-hist_DeepCSVcTag_SFc_Down.GetBinContent(2,2)]) )
ItertativeFit_graph_c_MediumWP.SetTitle(";pT;SFl")
ItertativeFit_graph_c_MediumWP.SetMarkerStyle(20)
ItertativeFit_graph_c_MediumWP.SetMarkerSize(2)
ItertativeFit_graph_c_MediumWP.SetMarkerColor(2)
ItertativeFit_graph_c_MediumWP.SetLineColor(2)
ItertativeFit_graph_c_MediumWP.SetLineWidth(4)
#ItertativeFit_graph_c_MediumWP.SetPoint(0,100,hist_DeepCSVcTag_SFl.GetBinContent(2,2))
#ItertativeFit_graph_c_MediumWP.DrawClone("APE")

MediumWP_c_Graph = ROOT.TGraphAsymmErrors(len(x),np.asarray([float(i) for i in x]),y_c_central,np.asarray([0.01]*len(x)),np.asarray([0.01]*len(x)),y_c_downerr,y_c_uperr)
MediumWP_c_Graph.SetFillColor(4)
MediumWP_c_Graph.SetFillStyle(3002)
MediumWP_c_Graph.SetLineWidth(2)
#MediumWP_c_Graph.DrawClone("E3same")



mg_c.Add(MediumWP_c_Graph,"3L")
mg_c.Add(ItertativeFit_graph_c_MediumWP,"P")

mg_c.Draw("AP3L")
mg_c.GetYaxis().SetRangeUser(0.85,1.3)
mg_c.GetYaxis().SetTitleSize(0.055)
mg_c.GetYaxis().SetTitleOffset(1.1)
mg_c.GetYaxis().CenterTitle()
mg_c.GetXaxis().SetTitleSize(0.055)
mg_c.GetXaxis().SetTitleOffset(1.1)

leg_c = ROOT.TLegend(0.2,0.65,0.7,0.87)
leg_c.SetHeader("Medium WP (DeepCSV c-tag)")
leg_c.SetTextSize(0.05)
leg_c.AddEntry(ItertativeFit_graph_c_MediumWP,"Iterative fit","pe")
leg_c.AddEntry(MediumWP_c_Graph,"W+c","fl")
leg_c.Draw("same")

c_c.SaveAs("./CompareCSFMediumWP.pdf")
