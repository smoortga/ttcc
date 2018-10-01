import ROOT
import os
import sys
from argparse import ArgumentParser
from array import array
from xsec import xsec_table
import numpy as np
from math import sqrt
import pickle


def PlotDataMCPerJetFlavour(histo_dict,datahisto_dict):
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