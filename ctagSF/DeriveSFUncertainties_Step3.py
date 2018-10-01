import ROOT
import os
import sys
from argparse import ArgumentParser
from math import sqrt
import pickle
import numpy as np
from scipy.optimize import fmin,fminbound,minimize,brentq,ridder,fsolve
from copy import deepcopy
from binning import *
from array import array

ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetOptStat(0)

parser = ArgumentParser()
parser.add_argument('--indir', default="FILL",help='input directory that contains all the Histograms with syst variations')
args = parser.parse_args()

basedir = args.indir
subdirs = [i for i in os.listdir(basedir) if os.path.isdir(basedir+"/"+i)]
centraldir = [i for i in subdirs if "central" in i][0]
systdirs = [i for i in subdirs if not "central" in i]


SFb_histUp = ROOT.TH2D("SFb_hist_Up",";CvsL;CvsB;|SFb - SFb_Up|",nbins_CvsL_jet1,array("d",custom_bins_CvsL_jet1),nbins_CvsB_jet1,array("d",custom_bins_CvsB_jet1))
SFc_histUp = ROOT.TH2D("SFc_hist_Up",";CvsL;CvsB;|SFc - SFc_Up|",nbins_CvsL_jet2,array("d",custom_bins_CvsL_jet2),nbins_CvsB_jet2,array("d",custom_bins_CvsB_jet2))
SFl_histUp = ROOT.TH2D("SFl_hist_Up",";CvsL;CvsB;|SFl - SFl_Up|",nbins_CvsL_jet3,array("d",custom_bins_CvsL_jet3),nbins_CvsB_jet3,array("d",custom_bins_CvsB_jet3))
SFb_histDown = ROOT.TH2D("SFb_hist_Down",";CvsL;CvsB;|SFb - SFb_Down|",nbins_CvsL_jet1,array("d",custom_bins_CvsL_jet1),nbins_CvsB_jet1,array("d",custom_bins_CvsB_jet1))
SFc_histDown = ROOT.TH2D("SFc_hist_Down",";CvsL;CvsB;|SFc - SFc_Down|",nbins_CvsL_jet2,array("d",custom_bins_CvsL_jet2),nbins_CvsB_jet2,array("d",custom_bins_CvsB_jet2))
SFl_histDown = ROOT.TH2D("SFl_hist_Down",";CvsL;CvsB;|SFl - SFl_Down|",nbins_CvsL_jet3,array("d",custom_bins_CvsL_jet3),nbins_CvsB_jet3,array("d",custom_bins_CvsB_jet3))

central_SF_file = ROOT.TFile(basedir+"/"+centraldir+"/DeepCSV_cTag_SFs_94X.root","update")
SFb_histCentral = central_SF_file.Get("SFb_hist_central")
SFc_histCentral = central_SF_file.Get("SFc_hist_central")
SFl_histCentral = central_SF_file.Get("SFl_hist_central")

for systdir in systdirs:
    currentdir = basedir + "/" + systdir
    tmp_file_ = ROOT.TFile(currentdir+"/DeepCSV_cTag_SFs_94X.root")
    tmp_SFb_hist = tmp_file_.Get("SFb_hist_"+systdir)
    tmp_SFc_hist = tmp_file_.Get("SFc_hist_"+systdir)
    tmp_SFl_hist = tmp_file_.Get("SFl_hist_"+systdir)
    
    diff_SFb = tmp_SFb_hist.Clone()
    diff_SFc = tmp_SFc_hist.Clone()
    diff_SFl = tmp_SFl_hist.Clone()
    
    diff_SFb.Add(SFb_histCentral,-1)
    diff_SFc.Add(SFc_histCentral,-1)
    diff_SFl.Add(SFl_histCentral,-1)
    
    for binx in range(diff_SFb.GetNbinsX()):
        for biny in range(diff_SFb.GetNbinsY()):
            if diff_SFb.GetBinContent(binx+1,biny+1) > 0: 
                old_bin_content_SFbUp = SFb_histUp.GetBinContent(binx+1,biny+1)
                new_bin_content_SFbUp = sqrt(old_bin_content_SFbUp**2 + diff_SFb.GetBinContent(binx+1,biny+1)**2)
                SFb_histUp.SetBinContent(binx+1,biny+1,new_bin_content_SFbUp)
            elif diff_SFb.GetBinContent(binx+1,biny+1) < 0: 
                old_bin_content_SFbDown = SFb_histDown.GetBinContent(binx+1,biny+1)
                new_bin_content_SFbDown = sqrt(old_bin_content_SFbDown**2 + diff_SFb.GetBinContent(binx+1,biny+1)**2)
                SFb_histDown.SetBinContent(binx+1,biny+1,new_bin_content_SFbDown)
            
            if diff_SFc.GetBinContent(binx+1,biny+1) > 0: 
                old_bin_content_SFcUp = SFc_histUp.GetBinContent(binx+1,biny+1)
                new_bin_content_SFcUp = sqrt(old_bin_content_SFcUp**2 + diff_SFc.GetBinContent(binx+1,biny+1)**2)
                SFc_histUp.SetBinContent(binx+1,biny+1,new_bin_content_SFcUp)
            elif diff_SFc.GetBinContent(binx+1,biny+1) < 0: 
                old_bin_content_SFcDown = SFc_histDown.GetBinContent(binx+1,biny+1)
                new_bin_content_SFcDown = sqrt(old_bin_content_SFcDown**2 + diff_SFc.GetBinContent(binx+1,biny+1)**2)
                SFc_histDown.SetBinContent(binx+1,biny+1,new_bin_content_SFcDown)
            
            if diff_SFl.GetBinContent(binx+1,biny+1) > 0: 
                old_bin_content_SFlUp = SFl_histUp.GetBinContent(binx+1,biny+1)
                new_bin_content_SFlUp = sqrt(old_bin_content_SFlUp**2 + diff_SFl.GetBinContent(binx+1,biny+1)**2)
                SFl_histUp.SetBinContent(binx+1,biny+1,new_bin_content_SFlUp)
            elif diff_SFl.GetBinContent(binx+1,biny+1) < 0: 
                old_bin_content_SFlDown = SFl_histDown.GetBinContent(binx+1,biny+1)
                new_bin_content_SFlDown = sqrt(old_bin_content_SFlDown**2 + diff_SFl.GetBinContent(binx+1,biny+1)**2)
                SFl_histDown.SetBinContent(binx+1,biny+1,new_bin_content_SFlDown)
    


ROOT.gStyle.SetPaintTextFormat("4.3f")

cSFb = ROOT.TCanvas("cSFb","cSFb",1800,1200)
cSFb.Divide(3,2)
cSFb.cd(1)
ROOT.gPad.SetMargin(0.15,0.15,0.15,0.1)
SFb_histUp.SetMarkerSize(1.5)
SFb_histUp.SetMarkerColor(0)
SFb_histUp.GetXaxis().CenterTitle()
SFb_histUp.GetXaxis().SetTitleSize(0.05)
SFb_histUp.GetXaxis().SetTitleOffset(1.2)
SFb_histUp.GetYaxis().CenterTitle()
SFb_histUp.GetYaxis().SetTitleSize(0.05)
SFb_histUp.GetYaxis().SetTitleOffset(1.2)
SFb_histUp.GetZaxis().SetRangeUser(0.,2.)
SFb_histUp.GetZaxis().CenterTitle()
SFb_histUp.GetZaxis().SetTitleSize(0.05)
SFb_histUp.GetZaxis().SetTitleOffset(1.2)
SFb_histUp.Draw("COLZ TEXT")
cSFb.cd(2)
ROOT.gPad.SetMargin(0.15,0.15,0.15,0.1)
SFc_histUp.SetMarkerSize(1.5)
SFc_histUp.SetMarkerColor(0)
SFc_histUp.GetXaxis().CenterTitle()
SFc_histUp.GetXaxis().SetTitleSize(0.05)
SFc_histUp.GetXaxis().SetTitleOffset(1.2)
SFc_histUp.GetYaxis().CenterTitle()
SFc_histUp.GetYaxis().SetTitleSize(0.05)
SFc_histUp.GetYaxis().SetTitleOffset(1.2)
SFc_histUp.GetZaxis().SetRangeUser(0.,2.)
SFc_histUp.GetZaxis().CenterTitle()
SFc_histUp.GetZaxis().SetTitleSize(0.05)
SFc_histUp.GetZaxis().SetTitleOffset(1.2)
SFc_histUp.Draw("COLZ TEXT")
cSFb.cd(3)
ROOT.gPad.SetMargin(0.15,0.15,0.15,0.1)
SFl_histUp.SetMarkerSize(1.5)
SFl_histUp.SetMarkerColor(0)
SFl_histUp.GetXaxis().CenterTitle()
SFl_histUp.GetXaxis().SetTitleSize(0.05)
SFl_histUp.GetXaxis().SetTitleOffset(1.2)
SFl_histUp.GetYaxis().CenterTitle()
SFl_histUp.GetYaxis().SetTitleSize(0.05)
SFl_histUp.GetYaxis().SetTitleOffset(1.2)
SFl_histUp.GetZaxis().SetRangeUser(0.,2.)
SFl_histUp.GetZaxis().CenterTitle()
SFl_histUp.GetZaxis().SetTitleSize(0.05)
SFl_histUp.GetZaxis().SetTitleOffset(1.2)
SFl_histUp.Draw("COLZ TEXT")
cSFb.cd(4)
ROOT.gPad.SetMargin(0.15,0.15,0.15,0.1)
SFb_histDown.SetMarkerSize(1.5)
SFb_histDown.SetMarkerColor(0)
SFb_histDown.GetXaxis().CenterTitle()
SFb_histDown.GetXaxis().SetTitleSize(0.05)
SFb_histDown.GetXaxis().SetTitleOffset(1.2)
SFb_histDown.GetYaxis().CenterTitle()
SFb_histDown.GetYaxis().SetTitleSize(0.05)
SFb_histDown.GetYaxis().SetTitleOffset(1.2)
SFb_histDown.GetZaxis().SetRangeUser(0.,2.)
SFb_histDown.GetZaxis().CenterTitle()
SFb_histDown.GetZaxis().SetTitleSize(0.05)
SFb_histDown.GetZaxis().SetTitleOffset(1.2)
SFb_histDown.Draw("COLZ TEXT")
cSFb.cd(5)
ROOT.gPad.SetMargin(0.15,0.15,0.15,0.1)
SFc_histDown.SetMarkerSize(1.5)
SFc_histDown.SetMarkerColor(0)
SFc_histDown.GetXaxis().CenterTitle()
SFc_histDown.GetXaxis().SetTitleSize(0.05)
SFc_histDown.GetXaxis().SetTitleOffset(1.2)
SFc_histDown.GetYaxis().CenterTitle()
SFc_histDown.GetYaxis().SetTitleSize(0.05)
SFc_histDown.GetYaxis().SetTitleOffset(1.2)
SFc_histDown.GetZaxis().SetRangeUser(0.,2.)
SFc_histDown.GetZaxis().CenterTitle()
SFc_histDown.GetZaxis().SetTitleSize(0.05)
SFc_histDown.GetZaxis().SetTitleOffset(1.2)
SFc_histDown.Draw("COLZ TEXT")
cSFb.cd(6)
ROOT.gPad.SetMargin(0.15,0.15,0.15,0.1)
SFl_histDown.SetMarkerSize(1.5)
SFl_histDown.SetMarkerColor(0)
SFl_histDown.GetXaxis().CenterTitle()
SFl_histDown.GetXaxis().SetTitleSize(0.05)
SFl_histDown.GetXaxis().SetTitleOffset(1.2)
SFl_histDown.GetYaxis().CenterTitle()
SFl_histDown.GetYaxis().SetTitleSize(0.05)
SFl_histDown.GetYaxis().SetTitleOffset(1.2)
SFl_histDown.GetZaxis().SetRangeUser(0.,2.)
SFl_histDown.GetZaxis().CenterTitle()
SFl_histDown.GetZaxis().SetTitleSize(0.05)
SFl_histDown.GetZaxis().SetTitleOffset(1.2)
SFl_histDown.Draw("COLZ TEXT")
cSFb.SaveAs(basedir+"/"+centraldir+"/SFs_cTag_UpDown_relative.png")
cSFb.SaveAs(basedir+"/"+centraldir+"/SFs_cTag_UpDown_relative.pdf")



# Save absolute values of up-down w.r.t. central in histograms
SFb_histUp_absolute = SFb_histUp.Clone()
SFb_histUp_absolute.Add(SFb_histCentral)
SFc_histUp_absolute = SFc_histUp.Clone()
SFc_histUp_absolute.Add(SFc_histCentral)
SFl_histUp_absolute = SFl_histUp.Clone()
SFl_histUp_absolute.Add(SFl_histCentral)
#outfileUp = ROOT.TFile(basedir+"/"+centraldir+"/DeepCSV_cTag_SFs_Up_94X.root","RECREATE")
#outfileUp.cd()
central_SF_file.cd()
SFb_histUp_absolute.Write()
SFc_histUp_absolute.Write()
SFl_histUp_absolute.Write()
#outfileUp.Close()

#
# NOTE: SF down variations have a lower bound at 0!! This needs te be checked
#
SFb_histDown_absolute = SFb_histDown.Clone()
SFb_histDown_absolute.Add(SFb_histCentral,-1)
SFb_histDown_absolute.Scale(-1)
for binx in range(SFb_histDown_absolute.GetNbinsX()):
    for biny in range(SFb_histDown_absolute.GetNbinsY()):
        if SFb_histDown_absolute.GetBinContent(binx+1,biny+1) < 0: SFb_histDown_absolute.SetBinContent(binx+1,biny+1,0.0)
        
SFc_histDown_absolute = SFc_histDown.Clone()
SFc_histDown_absolute.Add(SFc_histCentral,-1)
SFc_histDown_absolute.Scale(-1)
for binx in range(SFc_histDown_absolute.GetNbinsX()):
    for biny in range(SFc_histDown_absolute.GetNbinsY()):
        if SFc_histDown_absolute.GetBinContent(binx+1,biny+1) < 0: SFc_histDown_absolute.SetBinContent(binx+1,biny+1,0.0)
        
SFl_histDown_absolute = SFl_histDown.Clone()
SFl_histDown_absolute.Add(SFl_histCentral,-1)
SFl_histDown_absolute.Scale(-1)
for binx in range(SFl_histDown_absolute.GetNbinsX()):
    for biny in range(SFl_histDown_absolute.GetNbinsY()):
        if SFl_histDown_absolute.GetBinContent(binx+1,biny+1) < 0: SFl_histDown_absolute.SetBinContent(binx+1,biny+1,0.0)
        
#outfileDown = ROOT.TFile(basedir+"/"+centraldir+"/DeepCSV_cTag_SFs_Down_94X.root","RECREATE")
#outfileDown.cd()
central_SF_file.cd()
SFb_histDown_absolute.Write()
SFc_histDown_absolute.Write()
SFl_histDown_absolute.Write()
#outfileDown.Close()
central_SF_file.Close()
                
