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
def LooseWPLight(x,syst="central"):
	if syst=="central":
		return 1.03262-0.000133225*x+5.46948e-08*x*x-1.8915/x
	elif syst=="up":
		return (1.03262-0.000133225*x+5.46948e-08*x*x-1.8915/x)*(1+(0.00916472+3.66768e-05*x-7.22425e-09*x*x))
	elif syst=="down":
		return (1.03262-0.000133225*x+5.46948e-08*x*x-1.8915/x)*(1-(0.00916472+3.66768e-05*x-7.22425e-09*x*x))
	    
x = np.arange(30,200,1)
y_l_central = LooseWPLight(x,"central")
y_l_up = LooseWPLight(x,"up")
y_l_down = LooseWPLight(x,"down")
y_l_uperr = y_l_up-y_l_central
y_l_downerr = y_l_central-y_l_down

c_l = ROOT.TCanvas("c_l","c_l",800,600)
c_l.SetGrid()
c_l.SetMargin(0.15,0.05,0.15,0.1)

mg_l = ROOT.TMultiGraph("mg_l",";jet p_{T} [GeV];SF_{light}")

ItertativeFit_graph_l_LooseWP = ROOT.TGraphAsymmErrors(1,np.asarray([80.]),np.asarray([hist_DeepCSVcTag_SFl.GetBinContent(2,2)]),np.asarray([50.]),np.asarray([120.]),np.asarray([hist_DeepCSVcTag_SFl_Up.GetBinContent(2,2)-hist_DeepCSVcTag_SFl.GetBinContent(2,2)]),np.asarray([hist_DeepCSVcTag_SFl.GetBinContent(2,2)-hist_DeepCSVcTag_SFl_Down.GetBinContent(2,2)]) )
ItertativeFit_graph_l_LooseWP.SetTitle(";pT;SFl")
ItertativeFit_graph_l_LooseWP.SetMarkerStyle(20)
ItertativeFit_graph_l_LooseWP.SetMarkerSize(2)
ItertativeFit_graph_l_LooseWP.SetMarkerColor(2)
ItertativeFit_graph_l_LooseWP.SetLineColor(2)
ItertativeFit_graph_l_LooseWP.SetLineWidth(4)
#ItertativeFit_graph_l_LooseWP.SetPoint(0,100,hist_DeepCSVcTag_SFl.GetBinContent(2,2))
#ItertativeFit_graph_l_LooseWP.DrawClone("APE")

LooseWP_l_Graph = ROOT.TGraphAsymmErrors(len(x),np.asarray([float(i) for i in x]),y_l_central,np.asarray([0.01]*len(x)),np.asarray([0.01]*len(x)),y_l_downerr,y_l_uperr)
LooseWP_l_Graph.SetFillColor(4)
LooseWP_l_Graph.SetFillStyle(3002)
LooseWP_l_Graph.SetLineWidth(2)
#LooseWP_l_Graph.DrawClone("E3same")



mg_l.Add(LooseWP_l_Graph,"3L")
mg_l.Add(ItertativeFit_graph_l_LooseWP,"P")

mg_l.Draw("AP3L")
mg_l.GetYaxis().SetRangeUser(0.95,1.05)
mg_l.GetYaxis().SetTitleSize(0.055)
mg_l.GetYaxis().SetTitleOffset(1.1)
mg_l.GetYaxis().CenterTitle()
mg_l.GetXaxis().SetTitleSize(0.055)
mg_l.GetXaxis().SetTitleOffset(1.1)

leg_l = ROOT.TLegend(0.2,0.65,0.7,0.87)
leg_l.SetHeader("Loose WP (DeepCSV c-tag)")
leg_l.SetTextSize(0.05)
leg_l.AddEntry(ItertativeFit_graph_l_LooseWP,"Iterative fit","pe")
leg_l.AddEntry(LooseWP_l_Graph,"W+c","fl")
leg_l.Draw("same")

c_l.SaveAs("./CompareLightSFLooseWP.pdf")






def LooseWPB(x,syst="central"):
	if syst=="central":
		if x >= 30 and x < 60:
			return 1.0498
		elif x >= 60 and x < 100:
			return 1.0386
		elif x >= 100 and x < 140:
			return 1.2231
		else: 
			return 1.1007
	elif syst=="up":
		if x >= 30 and x < 60:
			return 1.233
		elif x >= 60 and x < 100:
			return 1.1713
		elif x >= 100 and x < 140:
			return 1.2745
		else: 
			return 1.1556
	elif syst=="down":
		if x >= 30 and x < 60:
			return 0.86656
		elif x >= 60 and x < 100:
			return 0.90589
		elif x >= 100 and x < 140:
			return 1.1717
		else: 
			return 1.0458
			

y_b_central = np.asarray([LooseWPB(i,"central") for i in x])
y_b_up = np.asarray([LooseWPB(i,"up") for i in x])
y_b_down = np.asarray([LooseWPB(i,"down") for i in x])
y_b_uperr = y_b_up-y_b_central
y_b_downerr = y_b_central-y_b_down

c_b = ROOT.TCanvas("c_b","c_b",800,600)
c_b.SetGrid()
c_b.SetMargin(0.15,0.05,0.15,0.1)

mg_b = ROOT.TMultiGraph("mg_b",";jet p_{T} [GeV];SF_{b}")

ItertativeFit_graph_b_LooseWP = ROOT.TGraphAsymmErrors(1,np.asarray([80.]),np.asarray([hist_DeepCSVcTag_SFb.GetBinContent(2,2)]),np.asarray([50.]),np.asarray([120.]),np.asarray([hist_DeepCSVcTag_SFb_Up.GetBinContent(2,2)-hist_DeepCSVcTag_SFb.GetBinContent(2,2)]),np.asarray([hist_DeepCSVcTag_SFb.GetBinContent(2,2)-hist_DeepCSVcTag_SFb_Down.GetBinContent(2,2)]) )
ItertativeFit_graph_b_LooseWP.SetTitle(";pT;SFl")
ItertativeFit_graph_b_LooseWP.SetMarkerStyle(20)
ItertativeFit_graph_b_LooseWP.SetMarkerSize(2)
ItertativeFit_graph_b_LooseWP.SetMarkerColor(2)
ItertativeFit_graph_b_LooseWP.SetLineColor(2)
ItertativeFit_graph_b_LooseWP.SetLineWidth(4)
#ItertativeFit_graph_b_LooseWP.SetPoint(0,100,hist_DeepCSVcTag_SFl.GetBinContent(2,2))
#ItertativeFit_graph_b_LooseWP.DrawClone("APE")

LooseWP_b_Graph = ROOT.TGraphAsymmErrors(len(x),np.asarray([float(i) for i in x]),y_b_central,np.asarray([0.01]*len(x)),np.asarray([0.01]*len(x)),y_b_downerr,y_b_uperr)
LooseWP_b_Graph.SetFillColor(4)
LooseWP_b_Graph.SetFillStyle(3002)
LooseWP_b_Graph.SetLineWidth(2)
#LooseWP_b_Graph.DrawClone("E3same")



mg_b.Add(LooseWP_b_Graph,"3L")
mg_b.Add(ItertativeFit_graph_b_LooseWP,"P")

mg_b.Draw("AP3L")
mg_b.GetYaxis().SetRangeUser(0.85,1.55)
mg_b.GetYaxis().SetTitleSize(0.055)
mg_b.GetYaxis().SetTitleOffset(1.1)
mg_b.GetYaxis().CenterTitle()
mg_b.GetXaxis().SetTitleSize(0.055)
mg_b.GetXaxis().SetTitleOffset(1.1)

leg_b = ROOT.TLegend(0.2,0.65,0.7,0.87)
leg_b.SetHeader("Loose WP (DeepCSV c-tag)")
leg_b.SetTextSize(0.05)
leg_b.AddEntry(ItertativeFit_graph_b_LooseWP,"Iterative fit","pe")
leg_b.AddEntry(LooseWP_b_Graph,"W+c","fl")
leg_b.Draw("same")

c_b.SaveAs("./CompareBSFLooseWP.pdf")





def LooseWPC(x,syst="central"):
	if syst=="central":
		if x >= 30 and x < 50:
			return 0.985581
		elif x >= 50 and x < 70:
			return 0.981402
		else: 
			return 1.020696
	elif syst=="up":
		if x >= 30 and x < 50:
			return 0.985581+0.022196
		elif x >= 50 and x < 70:
			return 0.981402+0.024072
		else: 
			return 1.020696+0.033555
	elif syst=="down":
		if x >= 30 and x < 50:
			return 0.985581-0.022196
		elif x >= 50 and x < 70:
			return 0.981402-0.024072
		else: 
			return 1.020696-0.033555
			

y_c_central = np.asarray([LooseWPC(i,"central") for i in x])
y_c_up = np.asarray([LooseWPC(i,"up") for i in x])
y_c_down = np.asarray([LooseWPC(i,"down") for i in x])
y_c_uperr = y_c_up-y_c_central
y_c_downerr = y_c_central-y_c_down

c_c = ROOT.TCanvas("c_c","c_c",800,600)
c_c.SetGrid()
c_c.SetMargin(0.15,0.05,0.15,0.1)

mg_c = ROOT.TMultiGraph("mg_c",";jet p_{T} [GeV];SF_{c}")

ItertativeFit_graph_c_LooseWP = ROOT.TGraphAsymmErrors(1,np.asarray([80.]),np.asarray([hist_DeepCSVcTag_SFc.GetBinContent(2,2)]),np.asarray([50.]),np.asarray([120.]),np.asarray([hist_DeepCSVcTag_SFc_Up.GetBinContent(2,2)-hist_DeepCSVcTag_SFc.GetBinContent(2,2)]),np.asarray([hist_DeepCSVcTag_SFc.GetBinContent(2,2)-hist_DeepCSVcTag_SFc_Down.GetBinContent(2,2)]) )
ItertativeFit_graph_c_LooseWP.SetTitle(";pT;SFl")
ItertativeFit_graph_c_LooseWP.SetMarkerStyle(20)
ItertativeFit_graph_c_LooseWP.SetMarkerSize(2)
ItertativeFit_graph_c_LooseWP.SetMarkerColor(2)
ItertativeFit_graph_c_LooseWP.SetLineColor(2)
ItertativeFit_graph_c_LooseWP.SetLineWidth(4)
#ItertativeFit_graph_c_LooseWP.SetPoint(0,100,hist_DeepCSVcTag_SFl.GetBinContent(2,2))
#ItertativeFit_graph_c_LooseWP.DrawClone("APE")

LooseWP_c_Graph = ROOT.TGraphAsymmErrors(len(x),np.asarray([float(i) for i in x]),y_c_central,np.asarray([0.01]*len(x)),np.asarray([0.01]*len(x)),y_c_downerr,y_c_uperr)
LooseWP_c_Graph.SetFillColor(4)
LooseWP_c_Graph.SetFillStyle(3002)
LooseWP_c_Graph.SetLineWidth(2)
#LooseWP_c_Graph.DrawClone("E3same")



mg_c.Add(LooseWP_c_Graph,"3L")
mg_c.Add(ItertativeFit_graph_c_LooseWP,"P")

mg_c.Draw("AP3L")
mg_c.GetYaxis().SetRangeUser(0.9,1.17)
mg_c.GetYaxis().SetTitleSize(0.055)
mg_c.GetYaxis().SetTitleOffset(1.1)
mg_c.GetYaxis().CenterTitle()
mg_c.GetXaxis().SetTitleSize(0.055)
mg_c.GetXaxis().SetTitleOffset(1.1)

leg_c = ROOT.TLegend(0.2,0.65,0.7,0.87)
leg_c.SetHeader("Loose WP (DeepCSV c-tag)")
leg_c.SetTextSize(0.05)
leg_c.AddEntry(ItertativeFit_graph_c_LooseWP,"Iterative fit","pe")
leg_c.AddEntry(LooseWP_c_Graph,"W+c","fl")
leg_c.Draw("same")

c_c.SaveAs("./CompareCSFLooseWP.pdf")
