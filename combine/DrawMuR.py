import os
import sys
import ROOT
from array import array
from math import sqrt

ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetOptStat(0)

infile = "./testCombineOutput.root"

f_ = ROOT.TFile(infile)
h_ttbb = f_.Get("h_ttbb")
h_ttbb.SetFillColor(ROOT.kRed+3)
h_ttbb.SetLineWidth(0)
h_ttbj = f_.Get("h_ttbj")
h_ttbj.SetFillColor(ROOT.kRed+2)
h_ttbj.SetLineWidth(0)
h_ttcc = f_.Get("h_ttcc")
h_ttcc.SetFillColor(ROOT.kOrange-2)
h_ttcc.SetLineWidth(0)
h_ttcc.GetYaxis().SetTitle("Events")
h_ttcj = f_.Get("h_ttcj")
h_ttcj.SetFillColor(ROOT.kOrange-7)
h_ttcj.SetLineWidth(0)
h_ttjj = f_.Get("h_ttjj")
h_ttjj.SetFillColor(ROOT.kRed-7)
h_ttjj.SetLineWidth(0)
h_ttother = f_.Get("h_ttother")
h_ttother.SetFillColor(ROOT.kOrange+6)
h_ttother.SetLineWidth(0)
h_bkg = f_.Get("h_bkg")
h_bkg.SetFillColor(1)
h_bkg.SetLineWidth(0)
h_data =  f_.Get("h_data_obs")
h_data.SetMarkerStyle(20)
h_data.SetLineColor(1)
h_data.SetLineWidth(2)

syst_dict = {}
syst_list = set([i.GetName().split("_")[-1][:-2] for i in f_.GetListOfKeys() if "Up" in i.GetName()])
for syst in syst_list:
    syst_dict[syst+"Up"]={}
    syst_dict[syst+"Up"]["h_ttbb"] = f_.Get("h_ttbb_"+syst+"Up")
    syst_dict[syst+"Up"]["h_ttbb"].Scale(float(h_ttbb.Integral())/syst_dict[syst+"Up"]["h_ttbb"].Integral())
    syst_dict[syst+"Up"]["h_ttbj"] = f_.Get("h_ttbj_"+syst+"Up")
    syst_dict[syst+"Up"]["h_ttbj"].Scale(float(h_ttbj.Integral())/syst_dict[syst+"Up"]["h_ttbj"].Integral())
    syst_dict[syst+"Up"]["h_ttcc"] = f_.Get("h_ttcc_"+syst+"Up")
    syst_dict[syst+"Up"]["h_ttcc"].Scale(float(h_ttcc.Integral())/syst_dict[syst+"Up"]["h_ttcc"].Integral())
    syst_dict[syst+"Up"]["h_ttcj"] = f_.Get("h_ttcj_"+syst+"Up")
    syst_dict[syst+"Up"]["h_ttcj"].Scale(float(h_ttcj.Integral())/syst_dict[syst+"Up"]["h_ttcj"].Integral())
    syst_dict[syst+"Up"]["h_ttjj"] = f_.Get("h_ttjj_"+syst+"Up")
    syst_dict[syst+"Up"]["h_ttjj"].Scale(float(h_ttjj.Integral())/syst_dict[syst+"Up"]["h_ttjj"].Integral())
    syst_dict[syst+"Up"]["h_ttother"] = f_.Get("h_ttother_"+syst+"Up")
    syst_dict[syst+"Up"]["h_ttother"].Scale(float(h_ttother.Integral())/syst_dict[syst+"Up"]["h_ttother"].Integral())
    #syst_dict[syst+"Up"]["h_bkg"] = f_.Get("h_bkg_"+syst+"Up")
    #syst_dict[syst+"Up"]["h_bkg"].Scale(float(h_bkg.Integral())/syst_dict[syst+"Up"]["h_bkg"].Integral())
    syst_dict[syst+"Down"]={}
    syst_dict[syst+"Down"]["h_ttbb"] = f_.Get("h_ttbb_"+syst+"Down")
    syst_dict[syst+"Down"]["h_ttbb"].Scale(float(h_ttbb.Integral())/syst_dict[syst+"Down"]["h_ttbb"].Integral())
    syst_dict[syst+"Down"]["h_ttbj"] = f_.Get("h_ttbj_"+syst+"Down")
    syst_dict[syst+"Down"]["h_ttbj"].Scale(float(h_ttbj.Integral())/syst_dict[syst+"Down"]["h_ttbj"].Integral())
    syst_dict[syst+"Down"]["h_ttcc"] = f_.Get("h_ttcc_"+syst+"Down")
    syst_dict[syst+"Down"]["h_ttcc"].Scale(float(h_ttcc.Integral())/syst_dict[syst+"Down"]["h_ttcc"].Integral())
    syst_dict[syst+"Down"]["h_ttcj"] = f_.Get("h_ttcj_"+syst+"Down")
    syst_dict[syst+"Down"]["h_ttcj"].Scale(float(h_ttcj.Integral())/syst_dict[syst+"Down"]["h_ttcj"].Integral())
    syst_dict[syst+"Down"]["h_ttjj"] = f_.Get("h_ttjj_"+syst+"Down")
    syst_dict[syst+"Down"]["h_ttjj"].Scale(float(h_ttjj.Integral())/syst_dict[syst+"Down"]["h_ttjj"].Integral())
    syst_dict[syst+"Down"]["h_ttother"] = f_.Get("h_ttother_"+syst+"Down")
    syst_dict[syst+"Down"]["h_ttother"].Scale(float(h_ttother.Integral())/syst_dict[syst+"Down"]["h_ttother"].Integral())
    #syst_dict[syst+"Down"]["h_bkg"] = f_.Get("h_bkg_"+syst+"Down")
    #syst_dict[syst+"Down"]["h_bkg"].Scale(float(h_bkg.Integral())/syst_dict[syst+"Down"]["h_bkg"].Integral())



c_pre = ROOT.TCanvas("c_pre","c_pre",1200,900)
c_pre.Divide(3,2)


c_pre.cd(1)
uppad_pre_ttbb = ROOT.TPad("u_pre","u_pre",0.,0.25,1.,1.)
downpad_pre_ttbb = ROOT.TPad("d_pre","d_pre",0.,0.0,1.,0.25)
uppad_pre_ttbb.Draw()
downpad_pre_ttbb.Draw()
uppad_pre_ttbb.cd()
ROOT.gPad.SetLogy(1)
ROOT.gPad.SetMargin(0.15,0.05,0.01,0.1)
h_ttbb.GetYaxis().SetRangeUser(0.1, 2*h_ttbb.GetBinContent(h_ttbb.GetMaximumBin())**1.6)
h_ttbb.Draw("hist")
syst_dict["muRUp"]["h_ttbb"].SetLineColor(1)
syst_dict["muRUp"]["h_ttbb"].SetLineStyle(2)
syst_dict["muRUp"]["h_ttbb"].SetLineWidth(2)
syst_dict["muRUp"]["h_ttbb"].Draw("hist same")
syst_dict["muRDown"]["h_ttbb"].SetLineColor(1)
syst_dict["muRDown"]["h_ttbb"].SetLineStyle(3)
syst_dict["muRDown"]["h_ttbb"].SetLineWidth(2)
syst_dict["muRDown"]["h_ttbb"].Draw("hist same")
latex_cms = ROOT.TLatex()
latex_cms.SetTextFont(42)
latex_cms.SetTextSize(0.1)
latex_cms.SetTextAlign(11)
latex_cms.DrawLatexNDC(0.2,0.8,"ttbb")
l_ttbb = ROOT.TLegend(0.5,0.6,0.94,0.89)
l_ttbb.SetNColumns(1)
l_ttbb.AddEntry(h_ttbb,"nominal","f")
l_ttbb.AddEntry(syst_dict["muRUp"]["h_ttbb"],"#mu_{R} Up","l")
l_ttbb.AddEntry(syst_dict["muRDown"]["h_ttbb"],"#mu_{R} Down","l")
l_ttbb.SetBorderSize(0)
l_ttbb.SetTextSize(0.08)
l_ttbb.Draw("same")
downpad_pre_ttbb.cd()
ROOT.gPad.SetMargin(0.15,0.05,0.4,0.01)
#ratio hist
h_ttbb.GetXaxis().SetTitle("bin number")
ratio_hist_ttbbUp = syst_dict["muRUp"]["h_ttbb"].Clone()
ratio_hist_ttbbUp.Divide(h_ttbb)
#ratio_hist_ttbbUp.SetMarkerStyle(20)
ratio_hist_ttbbUp.Draw("hist")
ratio_hist_ttbbUp.GetYaxis().SetRangeUser(0.95,1.05)
ratio_hist_ttbbUp.GetYaxis().SetNdivisions(4)
ratio_hist_ttbbUp.GetYaxis().SetLabelSize(0.14)
ratio_hist_ttbbUp.GetYaxis().SetLabelOffset(0.01)
ratio_hist_ttbbUp.GetYaxis().SetTitle("#frac{syst.}{nom.}")
ratio_hist_ttbbUp.GetYaxis().SetTitleSize(0.16)
ratio_hist_ttbbUp.GetYaxis().CenterTitle()
ratio_hist_ttbbUp.GetYaxis().SetTitleOffset(0.4)
ratio_hist_ttbbUp.GetXaxis().SetTitleSize(0.19)
ratio_hist_ttbbUp.GetXaxis().SetTitleOffset(0.9)
ratio_hist_ttbbUp.GetXaxis().SetLabelSize(0.14)
ratio_hist_ttbbDown = syst_dict["muRDown"]["h_ttbb"].Clone()
ratio_hist_ttbbDown.Divide(h_ttbb)
#ratio_hist_ttbbDown.SetMarkerStyle(20)
ratio_hist_ttbbDown.Draw("hist same")

c_pre.cd(2)
uppad_pre_ttbj = ROOT.TPad("u_pre","u_pre",0.,0.25,1.,1.)
downpad_pre_ttbj = ROOT.TPad("d_pre","d_pre",0.,0.0,1.,0.25)
uppad_pre_ttbj.Draw()
downpad_pre_ttbj.Draw()
uppad_pre_ttbj.cd()
ROOT.gPad.SetLogy(1)
ROOT.gPad.SetMargin(0.15,0.05,0.01,0.1)
h_ttbj.GetYaxis().SetRangeUser(0.1, 2*h_ttbj.GetBinContent(h_ttbj.GetMaximumBin())**1.6)
h_ttbj.Draw("hist")
syst_dict["muRUp"]["h_ttbj"].SetLineColor(1)
syst_dict["muRUp"]["h_ttbj"].SetLineStyle(2)
syst_dict["muRUp"]["h_ttbj"].SetLineWidth(2)
syst_dict["muRUp"]["h_ttbj"].Draw("hist same")
syst_dict["muRDown"]["h_ttbj"].SetLineColor(1)
syst_dict["muRDown"]["h_ttbj"].SetLineStyle(3)
syst_dict["muRDown"]["h_ttbj"].SetLineWidth(2)
syst_dict["muRDown"]["h_ttbj"].Draw("hist same")
latex_cms.DrawLatexNDC(0.2,0.8,"ttbj")
l_ttbj = ROOT.TLegend(0.5,0.6,0.94,0.89)
l_ttbj.SetNColumns(1)
l_ttbj.AddEntry(h_ttbj,"nominal","f")
l_ttbj.AddEntry(syst_dict["muRUp"]["h_ttbj"],"#mu_{R} Up","l")
l_ttbj.AddEntry(syst_dict["muRDown"]["h_ttbj"],"#mu_{R} Down","l")
l_ttbj.SetBorderSize(0)
l_ttbj.SetTextSize(0.08)
l_ttbj.Draw("same")
downpad_pre_ttbj.cd()
ROOT.gPad.SetMargin(0.15,0.05,0.4,0.01)
#ratio hist
h_ttbj.GetXaxis().SetTitle("bin number")
ratio_hist_ttbjUp = syst_dict["muRUp"]["h_ttbj"].Clone()
ratio_hist_ttbjUp.Divide(h_ttbj)
#ratio_hist_ttbjUp.SetMarkerStyle(20)
ratio_hist_ttbjUp.Draw("hist")
ratio_hist_ttbjUp.GetYaxis().SetRangeUser(0.95,1.05)
ratio_hist_ttbjUp.GetYaxis().SetNdivisions(4)
ratio_hist_ttbjUp.GetYaxis().SetLabelSize(0.14)
ratio_hist_ttbjUp.GetYaxis().SetLabelOffset(0.01)
ratio_hist_ttbjUp.GetYaxis().SetTitle("#frac{syst.}{nom.}")
ratio_hist_ttbjUp.GetYaxis().SetTitleSize(0.16)
ratio_hist_ttbjUp.GetYaxis().CenterTitle()
ratio_hist_ttbjUp.GetYaxis().SetTitleOffset(0.4)
ratio_hist_ttbjUp.GetXaxis().SetTitleSize(0.19)
ratio_hist_ttbjUp.GetXaxis().SetTitleOffset(0.9)
ratio_hist_ttbjUp.GetXaxis().SetLabelSize(0.14)
ratio_hist_ttbjDown = syst_dict["muRDown"]["h_ttbj"].Clone()
ratio_hist_ttbjDown.Divide(h_ttbj)
#ratio_hist_ttbjDown.SetMarkerStyle(20)
ratio_hist_ttbjDown.Draw("hist same")

c_pre.cd(3)
uppad_pre_ttcc = ROOT.TPad("u_pre","u_pre",0.,0.25,1.,1.)
downpad_pre_ttcc = ROOT.TPad("d_pre","d_pre",0.,0.0,1.,0.25)
uppad_pre_ttcc.Draw()
downpad_pre_ttcc.Draw()
uppad_pre_ttcc.cd()
ROOT.gPad.SetLogy(1)
ROOT.gPad.SetMargin(0.15,0.05,0.01,0.1)
h_ttcc.GetYaxis().SetRangeUser(0.1, 2*h_ttcc.GetBinContent(h_ttcc.GetMaximumBin())**1.6)
h_ttcc.Draw("hist")
syst_dict["muRUp"]["h_ttcc"].SetLineColor(1)
syst_dict["muRUp"]["h_ttcc"].SetLineStyle(2)
syst_dict["muRUp"]["h_ttcc"].SetLineWidth(2)
syst_dict["muRUp"]["h_ttcc"].Draw("hist same")
syst_dict["muRDown"]["h_ttcc"].SetLineColor(1)
syst_dict["muRDown"]["h_ttcc"].SetLineStyle(3)
syst_dict["muRDown"]["h_ttcc"].SetLineWidth(2)
syst_dict["muRDown"]["h_ttcc"].Draw("hist same")
latex_cms.DrawLatexNDC(0.2,0.8,"ttcc")
l_ttcc = ROOT.TLegend(0.5,0.6,0.94,0.89)
l_ttcc.SetNColumns(1)
l_ttcc.AddEntry(h_ttcc,"nominal","f")
l_ttcc.AddEntry(syst_dict["muRUp"]["h_ttcc"],"#mu_{R} Up","l")
l_ttcc.AddEntry(syst_dict["muRDown"]["h_ttcc"],"#mu_{R} Down","l")
l_ttcc.SetBorderSize(0)
l_ttcc.SetTextSize(0.08)
l_ttcc.Draw("same")
downpad_pre_ttcc.cd()
ROOT.gPad.SetMargin(0.15,0.05,0.4,0.01)
#ratio hist
h_ttcc.GetXaxis().SetTitle("bin number")
ratio_hist_ttccUp = syst_dict["muRUp"]["h_ttcc"].Clone()
ratio_hist_ttccUp.Divide(h_ttcc)
#ratio_hist_ttccUp.SetMarkerStyle(20)
ratio_hist_ttccUp.Draw("hist")
ratio_hist_ttccUp.GetYaxis().SetRangeUser(0.95,1.05)
ratio_hist_ttccUp.GetYaxis().SetNdivisions(4)
ratio_hist_ttccUp.GetYaxis().SetLabelSize(0.14)
ratio_hist_ttccUp.GetYaxis().SetLabelOffset(0.01)
ratio_hist_ttccUp.GetYaxis().SetTitle("#frac{syst.}{nom.}")
ratio_hist_ttccUp.GetYaxis().SetTitleSize(0.16)
ratio_hist_ttccUp.GetYaxis().CenterTitle()
ratio_hist_ttccUp.GetYaxis().SetTitleOffset(0.4)
ratio_hist_ttccUp.GetXaxis().SetTitleSize(0.19)
ratio_hist_ttccUp.GetXaxis().SetTitleOffset(0.9)
ratio_hist_ttccUp.GetXaxis().SetLabelSize(0.14)
ratio_hist_ttccDown = syst_dict["muRDown"]["h_ttcc"].Clone()
ratio_hist_ttccDown.Divide(h_ttcc)
#ratio_hist_ttccDown.SetMarkerStyle(20)
ratio_hist_ttccDown.Draw("hist same")


c_pre.cd(4)
uppad_pre_ttcj = ROOT.TPad("u_pre","u_pre",0.,0.25,1.,1.)
downpad_pre_ttcj = ROOT.TPad("d_pre","d_pre",0.,0.0,1.,0.25)
uppad_pre_ttcj.Draw()
downpad_pre_ttcj.Draw()
uppad_pre_ttcj.cd()
ROOT.gPad.SetLogy(1)
ROOT.gPad.SetMargin(0.15,0.05,0.01,0.1)
h_ttcj.GetYaxis().SetRangeUser(0.1, 2*h_ttcj.GetBinContent(h_ttcj.GetMaximumBin())**1.6)
h_ttcj.Draw("hist")
syst_dict["muRUp"]["h_ttcj"].SetLineColor(1)
syst_dict["muRUp"]["h_ttcj"].SetLineStyle(2)
syst_dict["muRUp"]["h_ttcj"].SetLineWidth(2)
syst_dict["muRUp"]["h_ttcj"].Draw("hist same")
syst_dict["muRDown"]["h_ttcj"].SetLineColor(1)
syst_dict["muRDown"]["h_ttcj"].SetLineStyle(3)
syst_dict["muRDown"]["h_ttcj"].SetLineWidth(2)
syst_dict["muRDown"]["h_ttcj"].Draw("hist same")
latex_cms.DrawLatexNDC(0.2,0.8,"ttcj")
l_ttcj = ROOT.TLegend(0.5,0.6,0.94,0.89)
l_ttcj.SetNColumns(1)
l_ttcj.AddEntry(h_ttcj,"nominal","f")
l_ttcj.AddEntry(syst_dict["muRUp"]["h_ttcj"],"#mu_{R} Up","l")
l_ttcj.AddEntry(syst_dict["muRDown"]["h_ttcj"],"#mu_{R} Down","l")
l_ttcj.SetBorderSize(0)
l_ttcj.SetTextSize(0.08)
l_ttcj.Draw("same")
downpad_pre_ttcj.cd()
ROOT.gPad.SetMargin(0.15,0.05,0.4,0.01)
#ratio hist
h_ttcj.GetXaxis().SetTitle("bin number")
ratio_hist_ttcjUp = syst_dict["muRUp"]["h_ttcj"].Clone()
ratio_hist_ttcjUp.Divide(h_ttcj)
#ratio_hist_ttcjUp.SetMarkerStyle(20)
ratio_hist_ttcjUp.Draw("hist")
ratio_hist_ttcjUp.GetYaxis().SetRangeUser(0.95,1.05)
ratio_hist_ttcjUp.GetYaxis().SetNdivisions(4)
ratio_hist_ttcjUp.GetYaxis().SetLabelSize(0.14)
ratio_hist_ttcjUp.GetYaxis().SetLabelOffset(0.01)
ratio_hist_ttcjUp.GetYaxis().SetTitle("#frac{syst.}{nom.}")
ratio_hist_ttcjUp.GetYaxis().SetTitleSize(0.16)
ratio_hist_ttcjUp.GetYaxis().CenterTitle()
ratio_hist_ttcjUp.GetYaxis().SetTitleOffset(0.4)
ratio_hist_ttcjUp.GetXaxis().SetTitleSize(0.19)
ratio_hist_ttcjUp.GetXaxis().SetTitleOffset(0.9)
ratio_hist_ttcjUp.GetXaxis().SetLabelSize(0.14)
ratio_hist_ttcjDown = syst_dict["muRDown"]["h_ttcj"].Clone()
ratio_hist_ttcjDown.Divide(h_ttcj)
#ratio_hist_ttcjDown.SetMarkerStyle(20)
ratio_hist_ttcjDown.Draw("hist same")


c_pre.cd(5)
uppad_pre_ttjj = ROOT.TPad("u_pre","u_pre",0.,0.25,1.,1.)
downpad_pre_ttjj = ROOT.TPad("d_pre","d_pre",0.,0.0,1.,0.25)
uppad_pre_ttjj.Draw()
downpad_pre_ttjj.Draw()
uppad_pre_ttjj.cd()
ROOT.gPad.SetLogy(1)
ROOT.gPad.SetMargin(0.15,0.05,0.01,0.1)
h_ttjj.GetYaxis().SetRangeUser(0.1, 2*h_ttjj.GetBinContent(h_ttjj.GetMaximumBin())**1.6)
h_ttjj.Draw("hist")
syst_dict["muRUp"]["h_ttjj"].SetLineColor(1)
syst_dict["muRUp"]["h_ttjj"].SetLineStyle(2)
syst_dict["muRUp"]["h_ttjj"].SetLineWidth(2)
syst_dict["muRUp"]["h_ttjj"].Draw("hist same")
syst_dict["muRDown"]["h_ttjj"].SetLineColor(1)
syst_dict["muRDown"]["h_ttjj"].SetLineStyle(3)
syst_dict["muRDown"]["h_ttjj"].SetLineWidth(2)
syst_dict["muRDown"]["h_ttjj"].Draw("hist same")
latex_cms.DrawLatexNDC(0.2,0.8,"ttjj")
l_ttjj = ROOT.TLegend(0.5,0.6,0.94,0.89)
l_ttjj.SetNColumns(1)
l_ttjj.AddEntry(h_ttjj,"nominal","f")
l_ttjj.AddEntry(syst_dict["muRUp"]["h_ttjj"],"#mu_{R} Up","l")
l_ttjj.AddEntry(syst_dict["muRDown"]["h_ttjj"],"#mu_{R} Down","l")
l_ttjj.SetBorderSize(0)
l_ttjj.SetTextSize(0.08)
l_ttjj.Draw("same")
downpad_pre_ttjj.cd()
ROOT.gPad.SetMargin(0.15,0.05,0.4,0.01)
#ratio hist
h_ttjj.GetXaxis().SetTitle("bin number")
ratio_hist_ttjjUp = syst_dict["muRUp"]["h_ttjj"].Clone()
ratio_hist_ttjjUp.Divide(h_ttjj)
#ratio_hist_ttjjUp.SetMarkerStyle(20)
ratio_hist_ttjjUp.Draw("hist")
ratio_hist_ttjjUp.GetYaxis().SetRangeUser(0.95,1.05)
ratio_hist_ttjjUp.GetYaxis().SetNdivisions(4)
ratio_hist_ttjjUp.GetYaxis().SetLabelSize(0.14)
ratio_hist_ttjjUp.GetYaxis().SetLabelOffset(0.01)
ratio_hist_ttjjUp.GetYaxis().SetTitle("#frac{syst.}{nom.}")
ratio_hist_ttjjUp.GetYaxis().SetTitleSize(0.16)
ratio_hist_ttjjUp.GetYaxis().CenterTitle()
ratio_hist_ttjjUp.GetYaxis().SetTitleOffset(0.4)
ratio_hist_ttjjUp.GetXaxis().SetTitleSize(0.19)
ratio_hist_ttjjUp.GetXaxis().SetTitleOffset(0.9)
ratio_hist_ttjjUp.GetXaxis().SetLabelSize(0.14)
ratio_hist_ttjjDown = syst_dict["muRDown"]["h_ttjj"].Clone()
ratio_hist_ttjjDown.Divide(h_ttjj)
#ratio_hist_ttjjDown.SetMarkerStyle(20)
ratio_hist_ttjjDown.Draw("hist same")


c_pre.cd(6)
uppad_pre_ttother = ROOT.TPad("u_pre","u_pre",0.,0.25,1.,1.)
downpad_pre_ttother = ROOT.TPad("d_pre","d_pre",0.,0.0,1.,0.25)
uppad_pre_ttother.Draw()
downpad_pre_ttother.Draw()
uppad_pre_ttother.cd()
ROOT.gPad.SetLogy(1)
ROOT.gPad.SetMargin(0.15,0.05,0.01,0.1)
h_ttother.GetYaxis().SetRangeUser(0.1, 2*h_ttother.GetBinContent(h_ttother.GetMaximumBin())**1.6)
h_ttother.Draw("hist")
syst_dict["muRUp"]["h_ttother"].SetLineColor(1)
syst_dict["muRUp"]["h_ttother"].SetLineStyle(2)
syst_dict["muRUp"]["h_ttother"].SetLineWidth(2)
syst_dict["muRUp"]["h_ttother"].Draw("hist same")
syst_dict["muRDown"]["h_ttother"].SetLineColor(1)
syst_dict["muRDown"]["h_ttother"].SetLineStyle(3)
syst_dict["muRDown"]["h_ttother"].SetLineWidth(2)
syst_dict["muRDown"]["h_ttother"].Draw("hist same")
latex_cms.DrawLatexNDC(0.2,0.8,"ttother")
l_ttother = ROOT.TLegend(0.5,0.6,0.94,0.89)
l_ttother.SetNColumns(1)
l_ttother.AddEntry(h_ttother,"nominal","f")
l_ttother.AddEntry(syst_dict["muRUp"]["h_ttother"],"#mu_{R} Up","l")
l_ttother.AddEntry(syst_dict["muRDown"]["h_ttother"],"#mu_{R} Down","l")
l_ttother.SetBorderSize(0)
l_ttother.SetTextSize(0.08)
l_ttother.Draw("same")
downpad_pre_ttother.cd()
ROOT.gPad.SetMargin(0.15,0.05,0.4,0.01)
#ratio hist
h_ttother.GetXaxis().SetTitle("bin number")
ratio_hist_ttotherUp = syst_dict["muRUp"]["h_ttother"].Clone()
ratio_hist_ttotherUp.Divide(h_ttother)
#ratio_hist_ttotherUp.SetMarkerStyle(20)
ratio_hist_ttotherUp.Draw("hist")
ratio_hist_ttotherUp.GetYaxis().SetRangeUser(0.95,1.05)
ratio_hist_ttotherUp.GetYaxis().SetNdivisions(4)
ratio_hist_ttotherUp.GetYaxis().SetLabelSize(0.14)
ratio_hist_ttotherUp.GetYaxis().SetLabelOffset(0.01)
ratio_hist_ttotherUp.GetYaxis().SetTitle("#frac{syst.}{nom.}")
ratio_hist_ttotherUp.GetYaxis().SetTitleSize(0.16)
ratio_hist_ttotherUp.GetYaxis().CenterTitle()
ratio_hist_ttotherUp.GetYaxis().SetTitleOffset(0.4)
ratio_hist_ttotherUp.GetXaxis().SetTitleSize(0.19)
ratio_hist_ttotherUp.GetXaxis().SetTitleOffset(0.9)
ratio_hist_ttotherUp.GetXaxis().SetLabelSize(0.14)
ratio_hist_ttotherDown = syst_dict["muRDown"]["h_ttother"].Clone()
ratio_hist_ttotherDown.Divide(h_ttother)
#ratio_hist_ttotherDown.SetMarkerStyle(20)
ratio_hist_ttotherDown.Draw("hist same")





#Redraw ratio_hist_ttbj
#ratio_hist_ttbjUp.Draw("same pe1x0")

c_pre.SaveAs("./muRVariations.pdf")
c_pre.SaveAs("./muRVariations.png")

f_.Close()
"""

mg = ROOT.THStack()
mg.Add(h_ttcc)
mg.Add(h_ttcj)
mg.Add(h_ttbj)
mg.Add(h_ttbj)
mg.Add(h_ttjj)
mg.Add(h_ttother)
mg.Add(h_bkg)
summed_MC_hist = h_ttcc.Clone()
summed_MC_hist.Add(h_ttcj)
summed_MC_hist.Add(h_ttbj)
summed_MC_hist.Add(h_ttbj)
summed_MC_hist.Add(h_ttjj)
summed_MC_hist.Add(h_ttother)
summed_MC_hist.Add(h_bkg)
summed_MC_hist.SetFillStyle(3244)
summed_MC_hist.SetFillColor(13)
summed_MC_hist.SetLineWidth(0)

c_pre = ROOT.TCanvas("c_pre","c_pre",800,700)
c_pre.cd()
uppad_pre_ttbj = ROOT.TPad("u_pre","u_pre",0.,0.25,1.,1.)
downpad_pre_ttbj = ROOT.TPad("d_pre","d_pre",0.,0.0,1.,0.25)
uppad_pre_ttbj.Draw()
downpad_pre_ttbj.Draw()

uppad_pre_ttbj.cd()
ROOT.gPad.SetLogy(1)
ROOT.gPad.SetMargin(0.15,0.05,0.01,0.1)
mg.Draw("hist")
mg.GetHistogram().SetLineWidth(0)

mg.GetYaxis().SetTitle("Events")
mg.GetYaxis().SetLabelSize(0.05)
mg.GetYaxis().SetLabelOffset(0.01)
mg.GetYaxis().SetTitleSize(0.06)
mg.GetYaxis().SetTitleOffset(1.2)
mg.GetXaxis().SetTitleSize(0.0)
mg.GetXaxis().SetLabelSize(0.0)
mg.SetMinimum(1)
mg.SetMaximum(2*summed_MC_hist.GetBinContent(summed_MC_hist.GetMaximumBin())**2)

h_data.Draw("epx0 same")



ROOT.gPad.RedrawAxis()
# line = ROOT.TLine()
# line.DrawLine(h_data.GetNbinsX(), ROOT.gPad.GetUymin(), h_data.GetNbinsX(), ROOT.gPad.GetUymax())

#############
# LEGEND
#############
l = ROOT.TLegend(0.5,0.55,0.94,0.89)
l.SetNColumns(2)
entries_dict={}
l.AddEntry(h_ttcc,"t#bar{t}c#bar{c}","f")
l.AddEntry(h_ttcj,"t#bar{t}cL","f")
l.AddEntry(h_ttbj,"t#bar{t}b#bar{b}","f")
l.AddEntry(h_ttbj,"t#bar{t}bL","f")
l.AddEntry(h_ttjj,"t#bar{t}LF","f")
l.AddEntry(h_ttother,"t#bar{t} + Other","f")
l.AddEntry(h_bkg,"backgrounds","f")
l.AddEntry(h_data,"Data","ep")
#if AddSystUnc: l.AddEntry(summed_MC_hist,"stat. + syst.","f")
#else: l.AddEntry(summed_MC_hist,"MC stat. unc.","f")
l.SetBorderSize(0)
l.SetTextSize(0.05)
l.Draw("same")


#########
# TEXT
#########
int_lumi=41.5
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

latex_prefit = ROOT.TLatex()
latex_prefit.SetTextFont(42)
latex_prefit.SetTextSize(0.06)
latex_prefit.SetTextAlign(11)
latex_prefit.DrawLatexNDC(0.15,0.92,"prefit")

latex_lepton_category = ROOT.TLatex()
latex_lepton_category.SetTextFont(42)
latex_lepton_category.SetTextSize(0.06)
latex_lepton_category.SetTextAlign(11)
latex_lepton_category.DrawLatexNDC(0.19,0.75,"dilepton channel")


#
# Calculate Chi2
#
# chi2_pre = 0
# for ibin in range(h_data.GetNbinsX()):
#     print ibin
#     data_yield = h_data.GetBinContent(ibin+1)
#     MC_yield = summed_MC_hist.GetBinContent(ibin+1)
#     unc = h_data.GetBinError(ibin+1) # needs to be changed with systematics!
    #chi2_pre += float((data_yield-MC_yield)**2)/float(unc**2)



downpad_pre_ttbj.cd()
ROOT.gPad.SetMargin(0.15,0.05,0.4,0.01)
#ratio hist
h_data.GetXaxis().SetTitle("bin number")
ratio_hist_ttbj = h_data.Clone()
ratio_hist_ttbj.Divide(summed_MC_hist)
ratio_hist_ttbj.SetMarkerStyle(20)
ratio_hist_ttbj.Draw("pe1x0")
ratio_hist_ttbj.GetYaxis().SetRangeUser(0.3,2.1)
ratio_hist_ttbj.GetYaxis().SetNdivisions(4)
ratio_hist_ttbj.GetYaxis().SetLabelSize(0.14)
ratio_hist_ttbj.GetYaxis().SetLabelOffset(0.01)
ratio_hist_ttbj.GetYaxis().SetTitle("#frac{syst.}{nom.}")
ratio_hist_ttbj.GetYaxis().SetTitleSize(0.16)
ratio_hist_ttbj.GetYaxis().CenterTitle()
ratio_hist_ttbj.GetYaxis().SetTitleOffset(0.4)
ratio_hist_ttbj.GetXaxis().SetTitleSize(0.19)
ratio_hist_ttbj.GetXaxis().SetTitleOffset(0.9)
ratio_hist_ttbj.GetXaxis().SetLabelSize(0.14)

MC_ratio_hist_ttbj = summed_MC_hist.Clone()
MC_ratio_hist_ttbj.Divide(summed_MC_hist)
MC_ratio_hist_ttbj.Draw("same E2")


#Redraw ratio_hist_ttbj
ratio_hist_ttbj.Draw("same pe1x0")



#
# Systematics
#
graph_x = array("d",[1]*summed_MC_hist.GetNbinsX())
graph_y = array("d",[1]*summed_MC_hist.GetNbinsX())
graph_exl = array("d",[0]*summed_MC_hist.GetNbinsX())
graph_exh = array("d",[0]*summed_MC_hist.GetNbinsX())
graph_eyl = array("d",[0]*summed_MC_hist.GetNbinsX())
graph_eyh = array("d",[0]*summed_MC_hist.GetNbinsX())

# stat. unc.
for ibin in range(summed_MC_hist.GetNbinsX()):
    graph_eyh[ibin] = summed_MC_hist.GetBinError(ibin+1)
    graph_eyl[ibin] = summed_MC_hist.GetBinError(ibin+1)
    graph_exl[ibin] = summed_MC_hist.GetBinCenter(ibin+1)-summed_MC_hist.GetXaxis().GetBinLowEdge(ibin+1)
    graph_exh[ibin] = summed_MC_hist.GetXaxis().GetBinLowEdge(ibin+2) - summed_MC_hist.GetBinCenter(ibin+1)
    graph_x[ibin] = summed_MC_hist.GetBinCenter(ibin+1)
    graph_y[ibin] = summed_MC_hist.GetBinContent(ibin+1)


# syst. unc.
syst_dict = {}
syst_list = set([i.GetName().split("_")[-1][:-2] for i in f_.GetListOfKeys() if "Up" in i.GetName()])
for syst in syst_list:
    syst_dict[syst+"Up"]={}
    syst_dict[syst+"Up"]["h_ttbj"] = f_.Get("h_ttbj_"+syst+"Up")
    syst_dict[syst+"Up"]["h_ttbj"] = f_.Get("h_ttbj_"+syst+"Up")
    syst_dict[syst+"Up"]["h_ttcc"] = f_.Get("h_ttcc_"+syst+"Up")
    syst_dict[syst+"Up"]["h_ttcj"] = f_.Get("h_ttcj_"+syst+"Up")
    syst_dict[syst+"Up"]["h_ttjj"] = f_.Get("h_ttjj_"+syst+"Up")
    syst_dict[syst+"Up"]["h_ttother"] = f_.Get("h_ttother_"+syst+"Up")
    syst_dict[syst+"Up"]["h_bkg"] = f_.Get("h_bkg_"+syst+"Up")
    syst_dict[syst+"Down"]={}
    syst_dict[syst+"Down"]["h_ttbj"] = f_.Get("h_ttbj_"+syst+"Down")
    syst_dict[syst+"Down"]["h_ttbj"] = f_.Get("h_ttbj_"+syst+"Down")
    syst_dict[syst+"Down"]["h_ttcc"] = f_.Get("h_ttcc_"+syst+"Down")
    syst_dict[syst+"Down"]["h_ttcj"] = f_.Get("h_ttcj_"+syst+"Down")
    syst_dict[syst+"Down"]["h_ttjj"] = f_.Get("h_ttjj_"+syst+"Down")
    syst_dict[syst+"Down"]["h_ttother"] = f_.Get("h_ttother_"+syst+"Down")
    syst_dict[syst+"Down"]["h_bkg"] = f_.Get("h_bkg_"+syst+"Down")
    
    temp_summed_hist_Up = syst_dict[syst+"Up"]["h_ttbj"].Clone()
    temp_summed_hist_Up.Add(syst_dict[syst+"Up"]["h_ttbj"])
    temp_summed_hist_Up.Add(syst_dict[syst+"Up"]["h_ttcc"])
    temp_summed_hist_Up.Add(syst_dict[syst+"Up"]["h_ttcj"])
    temp_summed_hist_Up.Add(syst_dict[syst+"Up"]["h_ttjj"])
    temp_summed_hist_Up.Add(syst_dict[syst+"Up"]["h_ttother"])
    temp_summed_hist_Up.Add(syst_dict[syst+"Up"]["h_bkg"])
    temp_summed_hist_Up.Add(summed_MC_hist,-1)
    for ibin in range(summed_MC_hist.GetNbinsX()):
        this_error = temp_summed_hist_Up.GetBinContent(ibin+1)
        if this_error >= 0: graph_eyh[ibin] = sqrt(graph_eyh[ibin]**2 + (this_error)**2)
        if this_error < 0: graph_eyl[ibin] = sqrt(graph_eyl[ibin]**2 + (this_error)**2)
    
    temp_summed_hist_Down = syst_dict[syst+"Down"]["h_ttbj"].Clone()
    temp_summed_hist_Down.Add(syst_dict[syst+"Down"]["h_ttbj"])
    temp_summed_hist_Down.Add(syst_dict[syst+"Down"]["h_ttcc"])
    temp_summed_hist_Down.Add(syst_dict[syst+"Down"]["h_ttcj"])
    temp_summed_hist_Down.Add(syst_dict[syst+"Down"]["h_ttjj"])
    temp_summed_hist_Down.Add(syst_dict[syst+"Down"]["h_ttother"])
    temp_summed_hist_Down.Add(syst_dict[syst+"Down"]["h_bkg"])
    temp_summed_hist_Down.Add(summed_MC_hist,-1)
    for ibin in range(summed_MC_hist.GetNbinsX()):
        this_error = temp_summed_hist_Down.GetBinContent(ibin+1)
        if this_error >= 0: graph_eyh[ibin] = sqrt(graph_eyh[ibin]**2 + (this_error)**2)
        if this_error < 0: graph_eyl[ibin] = sqrt(graph_eyl[ibin]**2 + (this_error)**2)

# add ttbar normalization by hand
syst_dict["ttbarNorm"+"Up"]={}
syst_dict["ttbarNorm"+"Up"]["h_ttbj"] = h_ttbj.Clone()
syst_dict["ttbarNorm"+"Up"]["h_ttbj"].Scale(1.048)
syst_dict["ttbarNorm"+"Up"]["h_ttbj"] = h_ttbj.Clone()
syst_dict["ttbarNorm"+"Up"]["h_ttbj"].Scale(1.048)
syst_dict["ttbarNorm"+"Up"]["h_ttcc"] = h_ttcc.Clone()
syst_dict["ttbarNorm"+"Up"]["h_ttcc"].Scale(1.048)
syst_dict["ttbarNorm"+"Up"]["h_ttcj"] = h_ttcj.Clone()
syst_dict["ttbarNorm"+"Up"]["h_ttcj"].Scale(1.048)
syst_dict["ttbarNorm"+"Up"]["h_ttjj"] = h_ttjj.Clone()
syst_dict["ttbarNorm"+"Up"]["h_ttjj"].Scale(1.048)
syst_dict["ttbarNorm"+"Up"]["h_ttother"] = h_ttother.Clone()
syst_dict["ttbarNorm"+"Up"]["h_ttother"].Scale(1.048)
syst_dict["ttbarNorm"+"Up"]["h_bkg"] = h_bkg.Clone()
syst_dict["ttbarNorm"+"Up"]["h_bkg"].Scale(1.3)
syst_dict["ttbarNorm"+"Down"]={}
syst_dict["ttbarNorm"+"Down"]["h_ttbj"] = h_ttbj.Clone()
syst_dict["ttbarNorm"+"Down"]["h_ttbj"].Scale(0.939)
syst_dict["ttbarNorm"+"Down"]["h_ttbj"] = h_ttbj.Clone()
syst_dict["ttbarNorm"+"Down"]["h_ttbj"].Scale(0.939)
syst_dict["ttbarNorm"+"Down"]["h_ttcc"] = h_ttcc.Clone()
syst_dict["ttbarNorm"+"Down"]["h_ttcc"].Scale(0.939)
syst_dict["ttbarNorm"+"Down"]["h_ttcj"] = h_ttcj.Clone()
syst_dict["ttbarNorm"+"Down"]["h_ttcj"].Scale(0.939)
syst_dict["ttbarNorm"+"Down"]["h_ttjj"] = h_ttjj.Clone()
syst_dict["ttbarNorm"+"Down"]["h_ttjj"].Scale(0.939)
syst_dict["ttbarNorm"+"Down"]["h_ttother"] = h_ttother.Clone()
syst_dict["ttbarNorm"+"Down"]["h_ttother"].Scale(0.939)
syst_dict["ttbarNorm"+"Down"]["h_bkg"] = h_bkg.Clone()
syst_dict["ttbarNorm"+"Down"]["h_bkg"].Scale(0.7)

temp_summed_hist_Up = syst_dict["ttbarNorm"+"Up"]["h_ttbj"].Clone()
temp_summed_hist_Up.Add(syst_dict["ttbarNorm"+"Up"]["h_ttbj"])
temp_summed_hist_Up.Add(syst_dict["ttbarNorm"+"Up"]["h_ttcc"])
temp_summed_hist_Up.Add(syst_dict["ttbarNorm"+"Up"]["h_ttcj"])
temp_summed_hist_Up.Add(syst_dict["ttbarNorm"+"Up"]["h_ttjj"])
temp_summed_hist_Up.Add(syst_dict["ttbarNorm"+"Up"]["h_ttother"])
temp_summed_hist_Up.Add(syst_dict["ttbarNorm"+"Up"]["h_bkg"])
temp_summed_hist_Up.Add(summed_MC_hist,-1)
for ibin in range(summed_MC_hist.GetNbinsX()):
    this_error = temp_summed_hist_Up.GetBinContent(ibin+1)
    #print this_error, graph_eyh[ibin]
    if this_error >= 0: graph_eyh[ibin] = sqrt(graph_eyh[ibin]**2 + (this_error)**2)
    if this_error < 0: graph_eyl[ibin] = sqrt(graph_eyl[ibin]**2 + (this_error)**2)

temp_summed_hist_Down = syst_dict["ttbarNorm"+"Down"]["h_ttbj"].Clone()
temp_summed_hist_Down.Add(syst_dict["ttbarNorm"+"Down"]["h_ttbj"])
temp_summed_hist_Down.Add(syst_dict["ttbarNorm"+"Down"]["h_ttcc"])
temp_summed_hist_Down.Add(syst_dict["ttbarNorm"+"Down"]["h_ttcj"])
temp_summed_hist_Down.Add(syst_dict["ttbarNorm"+"Down"]["h_ttjj"])
temp_summed_hist_Down.Add(syst_dict["ttbarNorm"+"Down"]["h_ttother"])
temp_summed_hist_Down.Add(syst_dict["ttbarNorm"+"Down"]["h_bkg"])
temp_summed_hist_Down.Add(summed_MC_hist,-1)
for ibin in range(summed_MC_hist.GetNbinsX()):
    this_error = temp_summed_hist_Down.GetBinContent(ibin+1)
    if this_error >= 0: graph_eyh[ibin] = sqrt(graph_eyh[ibin]**2 + (this_error)**2)
    if this_error < 0: graph_eyl[ibin] = sqrt(graph_eyl[ibin]**2 + (this_error)**2)

                       

ratio_graph_x = graph_x
ratio_graph_y = array("d",[1]*summed_MC_hist.GetNbinsX())
ratio_graph_exl = graph_exl
ratio_graph_exh = graph_exh
ratio_graph_eyl = array("d",[0]*summed_MC_hist.GetNbinsX())
ratio_graph_eyh = array("d",[0]*summed_MC_hist.GetNbinsX())
#print graph_y
for ibin in range(summed_MC_hist.GetNbinsX()):
    ratio_graph_eyh[ibin] = float(graph_eyh[ibin])/float(graph_y[ibin])
    ratio_graph_eyl[ibin] = float(graph_eyl[ibin])/float(graph_y[ibin])
    ratio_graph_x[ibin] = summed_MC_hist.GetBinCenter(ibin+1)

ratio_assymGraph = ROOT.TGraphAsymmErrors(len(ratio_graph_x),ratio_graph_x,ratio_graph_y,ratio_graph_exl,ratio_graph_exh,ratio_graph_eyl,ratio_graph_eyh)
ratio_assymGraph.SetFillColor(13)
ratio_assymGraph.SetFillStyle(3244)
ratio_assymGraph.SetLineWidth(0)
ratio_assymGraph.Draw("2")

ratio_hist_ttbj.Draw("same pe1x0")

l_rat = ROOT.TLegend(0.2,0.79,0.54,0.97)
#l_rat.SetNColumns(2)
entries_dict={}
l_rat.AddEntry(ratio_assymGraph,"stat. #oplus syst.","f")
l_rat.SetBorderSize(0)
l_rat.SetFillStyle(0)
l_rat.SetTextSize(0.18)
l_rat.Draw("same")


xmin = 0
xmax = h_data.GetNbinsX()
line3 = ROOT.TLine()
line3.SetLineColor(1)
line3.SetLineStyle(2)
line3.SetLineWidth(2)
line3.DrawLine(xmin, 1, xmax, 1)
line3.SetLineWidth(1)
line3.DrawLine(xmin, 0.75, xmax, 0.75)
line3.DrawLine(xmin, 1.25, xmax, 1.25)





c_pre.SaveAs("./Prefit.pdf")
c_pre.SaveAs("./Prefit.png")
c_pre.SaveAs("./Prefit.C")










#
#
# POSTFIT
#
#
# Fb = 1.445
# FbUp = Fb+0.174
# FbDown = Fb-0.149
# Fc = 1.498
# FcUp = Fc+0.219
# FcDown = Fc-0.191
# Fl = 0.766
# FlUp =Fl+0.082 
# FlDown =Fl-0.071 
Fb = 1.156
FbUp = Fb+0.158
FbDown = Fb-0.137
Fc = 1.751
FcUp = Fc+0.267
FcDown = Fc-0.235
Fl = 0.713
FlUp =Fl+0.083 
FlDown =Fl-0.072 

#For systematics
h_ttbjUp = h_ttbj.Clone()
h_ttbjUp.Scale(FbUp)
h_ttbjDown = h_ttbj.Clone()
h_ttbjDown.Scale(FbDown)
h_ttbjUp = h_ttbj.Clone()
h_ttbjUp.Scale(FbUp)
h_ttbjDown = h_ttbj.Clone()
h_ttbjDown.Scale(FbDown)
h_ttccUp = h_ttcc.Clone()
h_ttccUp.Scale(FcUp)
h_ttccDown = h_ttcc.Clone()
h_ttccDown.Scale(FcDown)
h_ttcjUp = h_ttcj.Clone()
h_ttcjUp.Scale(FcUp)
h_ttcjDown = h_ttcj.Clone()
h_ttcjDown.Scale(FcDown)
h_ttjjUp = h_ttjj.Clone()
h_ttjjUp.Scale(FlUp)
h_ttjjDown = h_ttjj.Clone()
h_ttjjDown.Scale(FlDown)
h_ttotherUp = h_ttother.Clone()
h_ttotherUp.Scale(FlUp)
h_ttotherDown = h_ttother.Clone()
h_ttotherDown.Scale(FlDown)

h_ttbj.Scale(Fb)
h_ttbj.Scale(Fb)
h_ttcc.Scale(Fc)
h_ttcj.Scale(Fc)
h_ttjj.Scale(Fl)
h_ttother.Scale(Fl)


mg_post = ROOT.THStack()
mg_post.Add(h_ttcc)
mg_post.Add(h_ttcj)
mg_post.Add(h_ttbj)
mg_post.Add(h_ttbj)
mg_post.Add(h_ttjj)
mg_post.Add(h_ttother)
mg_post.Add(h_bkg)
summed_MC_hist_post = h_ttcc.Clone()
summed_MC_hist_post.Add(h_ttcj)
summed_MC_hist_post.Add(h_ttbj)
summed_MC_hist_post.Add(h_ttbj)
summed_MC_hist_post.Add(h_ttjj)
summed_MC_hist_post.Add(h_ttother)
summed_MC_hist_post.Add(h_bkg)
summed_MC_hist_post.SetFillStyle(3244)
summed_MC_hist_post.SetFillColor(13)
summed_MC_hist_post.SetLineWidth(0)

c_post = ROOT.TCanvas("c_post","c_post",800,700)
c_post.cd()
uppad_post = ROOT.TPad("u_post","u_post",0.,0.25,1.,1.)
downpad_post = ROOT.TPad("d_post","d_post",0.,0.0,1.,0.25)
uppad_post.Draw()
downpad_post.Draw()

uppad_post.cd()
ROOT.gPad.SetLogy(1)
ROOT.gPad.SetMargin(0.15,0.05,0.01,0.1)
mg_post.Draw("hist")
mg_post.GetHistogram().SetLineWidth(0)

mg_post.GetYaxis().SetTitle("Events")
mg_post.GetYaxis().SetLabelSize(0.05)
mg_post.GetYaxis().SetLabelOffset(0.01)
mg_post.GetYaxis().SetTitleSize(0.06)
mg_post.GetYaxis().SetTitleOffset(1.2)
mg_post.GetXaxis().SetTitleSize(0.0)
mg_post.GetXaxis().SetLabelSize(0.0)
mg_post.SetMinimum(1)
mg_post.SetMaximum(2*summed_MC_hist_post.GetBinContent(summed_MC_hist_post.GetMaximumBin())**2)

h_data.Draw("epx0 same")



ROOT.gPad.RedrawAxis()
# line = ROOT.TLine()
# line.DrawLine(h_data.GetNbinsX(), ROOT.gPad.GetUymin(), h_data.GetNbinsX(), ROOT.gPad.GetUymax())

#############
# LEGEND
#############
l.Draw("same")


#########
# TEXT
#########

latex.DrawLatexNDC(0.94,0.94,lumi+" fb^{-1}, "+year)
latex_cms.DrawLatexNDC(0.19,0.83,"#bf{CMS} #it{Preliminary}")

latex_postfit = ROOT.TLatex()
latex_postfit.SetTextFont(42)
latex_postfit.SetTextSize(0.06)
latex_postfit.SetTextAlign(11)
latex_postfit.DrawLatexNDC(0.15,0.92,"Postfit")

latex_lepton_category.DrawLatexNDC(0.19,0.75,"dilepton channel")

latex_fit = ROOT.TLatex()
latex_fit.SetTextFont(42)
latex_fit.SetTextSize(0.05)
latex_fit.SetTextAlign(11)
latex_fit.DrawLatexNDC(0.25,0.68,"#alpha_{c} = %.3f ^{+%.3f}_{-%.3f}"%(Fc,abs(Fc-FcUp),abs(Fc-FcDown)))
latex_fit.DrawLatexNDC(0.25,0.6,"#alpha_{b} = %.3f ^{+%.3f}_{-%.3f}"%(Fb,abs(Fb-FbUp),abs(Fb-FbDown)))
latex_fit.DrawLatexNDC(0.25,0.52,"#alpha_{l}  = %.3f ^{+%.3f}_{-%.3f}"%(Fl,abs(Fl-FlUp),abs(Fl-FlDown)))


downpad_post.cd()
ROOT.gPad.SetMargin(0.15,0.05,0.4,0.01)
#ratio hist
h_data.GetXaxis().SetTitle("bin number")
ratio_hist_ttbj_post = h_data.Clone()
ratio_hist_ttbj_post.Divide(summed_MC_hist_post)
ratio_hist_ttbj_post.SetMarkerStyle(20)
ratio_hist_ttbj_post.Draw("pe1x0")
ratio_hist_ttbj_post.GetYaxis().SetRangeUser(0.3,2.1)
ratio_hist_ttbj_post.GetYaxis().SetNdivisions(4)
ratio_hist_ttbj_post.GetYaxis().SetLabelSize(0.14)
ratio_hist_ttbj_post.GetYaxis().SetLabelOffset(0.01)
ratio_hist_ttbj_post.GetYaxis().SetTitle("#frac{syst.}{nom.}")
ratio_hist_ttbj_post.GetYaxis().SetTitleSize(0.16)
ratio_hist_ttbj_post.GetYaxis().CenterTitle()
ratio_hist_ttbj_post.GetYaxis().SetTitleOffset(0.4)
ratio_hist_ttbj_post.GetXaxis().SetTitleSize(0.19)
ratio_hist_ttbj_post.GetXaxis().SetTitleOffset(0.9)
ratio_hist_ttbj_post.GetXaxis().SetLabelSize(0.14)

MC_ratio_hist_ttbj_post = summed_MC_hist_post.Clone()
MC_ratio_hist_ttbj_post.Divide(summed_MC_hist_post)
MC_ratio_hist_ttbj_post.Draw("same E2")


#Redraw ratio_hist_ttbj_post
ratio_hist_ttbj_post.Draw("same pe1x0")




#
# Systematics
#
graph_x = array("d",[1]*summed_MC_hist.GetNbinsX())
graph_y = array("d",[1]*summed_MC_hist.GetNbinsX())
graph_exl = array("d",[0]*summed_MC_hist.GetNbinsX())
graph_exh = array("d",[0]*summed_MC_hist.GetNbinsX())
graph_eyl = array("d",[0]*summed_MC_hist.GetNbinsX())
graph_eyh = array("d",[0]*summed_MC_hist.GetNbinsX())

# stat. unc.
for ibin in range(summed_MC_hist_post.GetNbinsX()):
    graph_eyh[ibin] = summed_MC_hist_post.GetBinError(ibin+1)
    graph_eyl[ibin] = summed_MC_hist_post.GetBinError(ibin+1)
    graph_exl[ibin] = summed_MC_hist_post.GetBinCenter(ibin+1)-summed_MC_hist_post.GetXaxis().GetBinLowEdge(ibin+1)
    graph_exh[ibin] = summed_MC_hist_post.GetXaxis().GetBinLowEdge(ibin+2) - summed_MC_hist_post.GetBinCenter(ibin+1)
    graph_x[ibin] = summed_MC_hist_post.GetBinCenter(ibin+1)
    graph_y[ibin] = summed_MC_hist_post.GetBinContent(ibin+1)


# syst. unc.
syst_dict = {}

# add ttbar normalization by hand
syst_dict["fit"+"Up"]={}
syst_dict["fit"+"Up"]["h_ttbj"] = h_ttbjUp
syst_dict["fit"+"Up"]["h_ttbj"] = h_ttbjUp
syst_dict["fit"+"Up"]["h_ttcc"] = h_ttccUp
syst_dict["fit"+"Up"]["h_ttcj"] = h_ttcjUp
syst_dict["fit"+"Up"]["h_ttjj"] = h_ttjjUp
syst_dict["fit"+"Up"]["h_ttother"] = h_ttotherUp
syst_dict["fit"+"Up"]["h_bkg"] = h_bkg
syst_dict["fit"+"Down"]={}
syst_dict["fit"+"Down"]["h_ttbj"] = h_ttbjDown
syst_dict["fit"+"Down"]["h_ttbj"] = h_ttbjDown
syst_dict["fit"+"Down"]["h_ttcc"] = h_ttccDown
syst_dict["fit"+"Down"]["h_ttcj"] = h_ttcjDown
syst_dict["fit"+"Down"]["h_ttjj"] = h_ttjjDown
syst_dict["fit"+"Down"]["h_ttother"] = h_ttotherDown
syst_dict["fit"+"Down"]["h_bkg"] = h_bkg

temp_summed_hist_Up = syst_dict["fit"+"Up"]["h_ttbj"].Clone()
temp_summed_hist_Up.Add(syst_dict["fit"+"Up"]["h_ttbj"])
temp_summed_hist_Up.Add(syst_dict["fit"+"Up"]["h_ttcc"])
temp_summed_hist_Up.Add(syst_dict["fit"+"Up"]["h_ttcj"])
temp_summed_hist_Up.Add(syst_dict["fit"+"Up"]["h_ttjj"])
temp_summed_hist_Up.Add(syst_dict["fit"+"Up"]["h_ttother"])
temp_summed_hist_Up.Add(syst_dict["fit"+"Up"]["h_bkg"])
temp_summed_hist_Up.Add(summed_MC_hist_post,-1)
for ibin in range(summed_MC_hist_post.GetNbinsX()):
    this_error = temp_summed_hist_Up.GetBinContent(ibin+1)
    #print this_error, graph_eyh[ibin]
    if this_error >= 0: graph_eyh[ibin] = sqrt(graph_eyh[ibin]**2 + (this_error)**2)
    if this_error < 0: graph_eyl[ibin] = sqrt(graph_eyl[ibin]**2 + (this_error)**2)

temp_summed_hist_Down = syst_dict["fit"+"Down"]["h_ttbj"].Clone()
temp_summed_hist_Down.Add(syst_dict["fit"+"Down"]["h_ttbj"])
temp_summed_hist_Down.Add(syst_dict["fit"+"Down"]["h_ttcc"])
temp_summed_hist_Down.Add(syst_dict["fit"+"Down"]["h_ttcj"])
temp_summed_hist_Down.Add(syst_dict["fit"+"Down"]["h_ttjj"])
temp_summed_hist_Down.Add(syst_dict["fit"+"Down"]["h_ttother"])
temp_summed_hist_Down.Add(syst_dict["fit"+"Down"]["h_bkg"])
temp_summed_hist_Down.Add(summed_MC_hist_post,-1)
for ibin in range(summed_MC_hist_post.GetNbinsX()):
    this_error = temp_summed_hist_Down.GetBinContent(ibin+1)
    if this_error >= 0: graph_eyh[ibin] = sqrt(graph_eyh[ibin]**2 + (this_error)**2)
    if this_error < 0: graph_eyl[ibin] = sqrt(graph_eyl[ibin]**2 + (this_error)**2)

                       

ratio_graph_x = graph_x
ratio_graph_y = array("d",[1]*summed_MC_hist_post.GetNbinsX())
ratio_graph_exl = graph_exl
ratio_graph_exh = graph_exh
ratio_graph_eyl = array("d",[0]*summed_MC_hist_post.GetNbinsX())
ratio_graph_eyh = array("d",[0]*summed_MC_hist_post.GetNbinsX())
#print graph_y
for ibin in range(summed_MC_hist_post.GetNbinsX()):
    ratio_graph_eyh[ibin] = float(graph_eyh[ibin])/float(graph_y[ibin])
    ratio_graph_eyl[ibin] = float(graph_eyl[ibin])/float(graph_y[ibin])
    ratio_graph_x[ibin] = summed_MC_hist_post.GetBinCenter(ibin+1)

ratio_assymGraph = ROOT.TGraphAsymmErrors(len(ratio_graph_x),ratio_graph_x,ratio_graph_y,ratio_graph_exl,ratio_graph_exh,ratio_graph_eyl,ratio_graph_eyh)
ratio_assymGraph.SetFillColor(13)
ratio_assymGraph.SetFillStyle(3244)
ratio_assymGraph.SetLineWidth(0)
ratio_assymGraph.Draw("2")

ratio_hist_ttbj_post.Draw("same pe1x0")

# l_rat = ROOT.TLegend(0.2,0.79,0.54,0.97)
# #l_rat.SetNColumns(2)
# entries_dict={}
# l_rat.AddEntry(ratio_assymGraph,"stat. + syst.","f")
# l_rat.SetBorderSize(0)
# l_rat.SetFillStyle(0)
# l_rat.SetTextSize(0.18)
l_rat.Draw("same")




xmin = 0
xmax = h_data.GetNbinsX()
line3 = ROOT.TLine()
line3.SetLineColor(1)
line3.SetLineStyle(2)
line3.SetLineWidth(2)
line3.DrawLine(xmin, 1, xmax, 1)
line3.SetLineWidth(1)
line3.DrawLine(xmin, 0.75, xmax, 0.75)
line3.DrawLine(xmin, 1.25, xmax, 1.25)

print h_data.Integral() , summed_MC_hist_post.Integral()

c_post.SaveAs("./Postfit.pdf")
c_post.SaveAs("./Postfit.png")
c_post.SaveAs("./Postfit.C")

f_.Close()
"""