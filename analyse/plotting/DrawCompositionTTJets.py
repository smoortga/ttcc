import os
import ROOT
from ROOT import gSystem, TFile, TCanvas, TH1D, TLegend, gROOT, gStyle, TH2D, gPad, TLegend,TPad
gSystem.Load('../../objects/Electron_C')
gSystem.Load('../../objects/Muon_C')
gSystem.Load('../../objects/Jet_C')
gSystem.Load('../../objects/MissingEnergy_C')
gSystem.Load('../../objects/Trigger_C')
gSystem.Load('../../objects/Truth_C')
from ROOT import Electron, Muon, Jet, MissingEnergy, Trigger
gROOT.SetBatch(True)
gStyle.SetOptStat(0)
#gStyle.SetPaintTextFormat(".2f %%")
gStyle.SetPaintTextFormat(".2f")


def main():

    CatHist_elel = TH1D("hist_elel","",6,-1.5,4.5)
    CatHist_mumu = TH1D("hist_mumu","",6,-1.5,4.5)
    CatHist_elmu = TH1D("hist_elmu","",6,-1.5,4.5)
    CatHist_incl = TH1D("hist_incl","",6,-1.5,4.5)

    workingdir = os.getcwd()
    infile = TFile("/user/smoortga/Analysis/NTupler/CMSSW_8_0_25/src/FlatTree/FlatTreeAnalyzer/ttcc/analyse/SELECTED_Full2016_WithDeepCSV_LeptonTriggerSF_10042018/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8.root")
    intree = infile.Get("tree")
    
    hweight = infile.Get("hweight")
    orig_nevents = hweight.GetBinContent(1)
    xsec = 831*1000 #[fb]
    int_lumi = 27.3#27.3 #[fb-1]
    expected_nevents = xsec*int_lumi
    factor = float(expected_nevents)/float(orig_nevents)
    print factor
    #factor = factor*24/63.

    if not os.path.isdir(workingdir+"/inclusive"): os.mkdir(workingdir+"/inclusive")
    
    nEvents = intree.GetEntries()
    for evt in range(nEvents):
        intree.GetEntry(evt)
        
        weight = intree.weight_btag_iterativefit*intree.weight_electron_id*intree.weight_electron_reco*intree.weight_electron_trig*intree.weight_muon_id*intree.weight_muon_iso*intree.weight_muon_trig*intree.pu_weight
        

        lept_channel = intree.lepton_Category
        if lept_channel == 0: # elel
            CatHist_elel.Fill(intree.event_Category,factor*weight)
        if lept_channel == 1: # mumu
            CatHist_mumu.Fill(intree.event_Category,factor*weight)
        if lept_channel == 2: # elmu
            CatHist_elmu.Fill(intree.event_Category,factor*weight)
        
        CatHist_incl.Fill(intree.event_Category,factor*weight)
    
#     CatHistNorm=CatHist.Clone()
#     CatHistNorm.Scale(100./CatHist.Integral())
#     CatHistNorm.SetLineWidth(0)
#     CatHistNorm.SetFillColor(0)
    c1 = TCanvas("c1","c1",1200,800)
    leftpad = TPad("u","u",0.,0.,0.7,1.)
    rightpad = TPad("d","d",0.7,0.0,1.,1.)
    leftpad.Draw()
    rightpad.Draw()

    leftpad.cd()
    gPad.SetLogy(1)
    gPad.SetMargin(0.15,0.05,0.1,0.1)
    CatHist_elmu.SetTitle("")
    CatHist_elmu.SetFillColor(2)
    CatHist_elmu.SetLineColor(2)
    CatHist_elmu.SetLineWidth(0)
    CatHist_elmu.SetBarWidth(0.2)
    CatHist_elmu.SetBarOffset(0.1)
    CatHist_elmu.SetMarkerStyle(0)
    #CatHist_elmu.Scale(100./CatHist_elmu.Integral())
    CatHist_elmu.GetXaxis().SetBinLabel(1,"other")
    CatHist_elmu.GetXaxis().SetBinLabel(2,"ttbb")
    #CatHist_elmu.GetXaxis().SetBinLabel(3,"ttbc")
    CatHist_elmu.GetXaxis().SetBinLabel(3,"ttbj")
    CatHist_elmu.GetXaxis().SetBinLabel(4,"ttcc")
    CatHist_elmu.GetXaxis().SetBinLabel(5,"ttcj")
    CatHist_elmu.GetXaxis().SetBinLabel(6,"ttjj")
    CatHist_elmu.GetXaxis().SetLabelSize(0.06)
    #CatHist_elmu.GetYaxis().SetTitle("Percentage of events [%]")
    CatHist_elmu.GetYaxis().SetTitle("# events (%.1f fb-1)"%int_lumi)
    CatHist_elmu.GetYaxis().SetTitleOffset(1.4)
    CatHist_elmu.GetYaxis().SetTitleSize(0.05)
    CatHist_elmu.GetYaxis().SetRangeUser(1,500000)
    #CatHist_elmu.GetYaxis().SetRangeUser(0.1,500)
    CatHist_elmu.Draw("barTEXT")
    #CatHist_elmuNorm.Draw("TEXT")
    
    CatHist_elel.SetTitle("")
    CatHist_elel.SetFillColor(4)
    CatHist_elel.SetLineColor(4)
    CatHist_elel.SetLineWidth(0)
    CatHist_elel.SetBarWidth(0.2)
    CatHist_elel.SetBarOffset(0.3)
    CatHist_elel.SetMarkerStyle(0)
    CatHist_elel.Draw("barTEXT same")  
    
    CatHist_mumu.SetTitle("")
    CatHist_mumu.SetFillColor(3)
    CatHist_mumu.SetLineColor(3)
    CatHist_mumu.SetLineWidth(0)
    CatHist_mumu.SetBarWidth(0.2)
    CatHist_mumu.SetBarOffset(0.5)
    CatHist_mumu.SetMarkerStyle(0)
    CatHist_mumu.Draw("barTEXT same")   
    
    CatHist_incl.SetTitle("")
    CatHist_incl.SetFillColor(14)
    CatHist_incl.SetLineColor(14)
    CatHist_incl.SetLineWidth(0)
    CatHist_incl.SetBarWidth(0.2)
    CatHist_incl.SetBarOffset(0.7)
    CatHist_incl.SetMarkerStyle(0)
    CatHist_incl.Draw("barTEXT same")  
    
    
    l_1 = TLegend(0.18,0.7,0.5,0.89)
    l_1.SetFillStyle(0)
    l_1.SetBorderSize(0)
    l_1.AddEntry(CatHist_elmu,"e^{#pm}#mu^{#mp} channel","f")
    l_1.AddEntry(CatHist_elel,"e^{+}e^{-} channel","f")
    l_1.AddEntry(CatHist_mumu,"#mu^{+}#mu^{-} channel","f")
    l_1.AddEntry(CatHist_incl,"inclusive","f")
    l_1.Draw("same")
      
    #c1.cd(2)
    #FlavHist.Draw("colzTEXT")

    c1.SaveAs(workingdir+"/inclusive/categories.png")
    c1.SaveAs(workingdir+"/inclusive/categories.pdf")
    
    
    
    
if __name__ == "__main__":
	main()


