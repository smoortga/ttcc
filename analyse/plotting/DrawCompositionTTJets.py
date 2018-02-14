import os
import ROOT
from ROOT import gSystem, TFile, TCanvas, TH1D, TLegend, gROOT, gStyle, TH2D, gPad
gSystem.Load('../../objects/Electron_C')
gSystem.Load('../../objects/Muon_C')
gSystem.Load('../../objects/Jet_C')
gSystem.Load('../../objects/MissingEnergy_C')
gSystem.Load('../../objects/Trigger_C')
from ROOT import Electron, Muon, Jet, MissingEnergy, Trigger
gROOT.SetBatch(True)
gStyle.SetOptStat(0)
#gStyle.SetPaintTextFormat(".2f %%")
gStyle.SetPaintTextFormat(".2f")


def main():

    CatHist = TH1D("hist","",7,-1.5,5.5)
    FlavHist = TH2D("flav",";add1 hadron flavour; add2 hadron flavour",6,-0.5,5.5,6,-0.5,5.5)

    workingdir = os.getcwd()
    infile = TFile("/user/smoortga/Analysis/NTupler/CMSSW_8_0_25/src/FlatTree/FlatTreeAnalyzer/ttcc/analyse/SELECTED_SelectionFromPaper_emu/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8.root")
    intree = infile.Get("tree")
    
    hweight = infile.Get("hweight")
    orig_nevents = hweight.GetEntries()
    xsec = 831*1000 #[fb]
    int_lumi = 2.3 #[fb-1]
    expected_nevents = xsec*int_lumi
    factor = float(expected_nevents)/float(orig_nevents)
    print factor
    #factor = factor*24/63.

    if not os.path.isdir(workingdir+"/output"): os.mkdir(workingdir+"/output")
    
    nEvents = intree.GetEntries()
    for evt in range(nEvents):
        intree.GetEntry(evt)
        
        FlavHist.Fill(intree.hadronFlavour_addJet1,intree.hadronFlavour_addJet2,factor)
        
        category_bin = -1
        
        #ttbb
        # if (intree.hadronFlavour_addJet1 == 5 and intree.hadronFlavour_addJet2 == 5): category_bin=1
#         #ttbc
#         elif (intree.hadronFlavour_addJet1 == 5 and intree.hadronFlavour_addJet2 == 4): category_bin=2
#         elif (intree.hadronFlavour_addJet1 == 4 and intree.hadronFlavour_addJet2 == 5): category_bin=2
#         #ttbj
#         elif (intree.hadronFlavour_addJet1 == 5 and intree.hadronFlavour_addJet2 == 0): category_bin=3
#         elif (intree.hadronFlavour_addJet1 == 0 and intree.hadronFlavour_addJet2 == 5): category_bin=3
#         #ttcc
#         elif (intree.hadronFlavour_addJet1 == 4 and intree.hadronFlavour_addJet2 == 4): category_bin=4
#         #ttcj
#         elif (intree.hadronFlavour_addJet1 == 4 and intree.hadronFlavour_addJet2 == 0): category_bin=5
#         elif (intree.hadronFlavour_addJet1 == 0 and intree.hadronFlavour_addJet2 == 4): category_bin=5
#         #ttjj
#         elif (intree.hadronFlavour_addJet1 == 0 and intree.hadronFlavour_addJet2 == 0): category_bin=6
        
        #print intree.hadronFlavour_addJet1, intree.hadronFlavour_addJet2, category_bin
        #CatHist.Fill(category_bin-1,factor)
        CatHist.Fill(intree.event_Category,factor)
    
    CatHistNorm=CatHist.Clone()
    CatHistNorm.Scale(100./CatHist.Integral())
    CatHistNorm.SetLineWidth(0)
    CatHistNorm.SetFillColor(0)
    c1 = TCanvas("c1","c1",1500,800)
    c1.Divide(2,1)
    c1.cd(1)
    gPad.SetLogy(1)
    CatHist.SetTitle("")
    CatHist.SetFillColor(2)
    CatHist.SetLineColor(2)
    CatHist.SetBarWidth(0.2)
    CatHist.SetBarOffset(0.1)
    #CatHist.Scale(100./CatHist.Integral())
    CatHist.GetXaxis().SetBinLabel(1,"other")
    CatHist.GetXaxis().SetBinLabel(2,"ttbb")
    CatHist.GetXaxis().SetBinLabel(3,"ttbc")
    CatHist.GetXaxis().SetBinLabel(4,"ttbj")
    CatHist.GetXaxis().SetBinLabel(5,"ttcc")
    CatHist.GetXaxis().SetBinLabel(6,"ttcj")
    CatHist.GetXaxis().SetBinLabel(7,"ttjj")
    CatHist.GetXaxis().SetLabelSize(0.06)
    #CatHist.GetYaxis().SetTitle("Percentage of events [%]")
    CatHist.GetYaxis().SetTitle("# events (2.3 fb-1)")
    CatHist.GetYaxis().SetTitleOffset(1.3)
    #CatHist.GetYaxis().SetRangeUser(0.1,500)
    
    CatHist.Draw("barTEXT")
    #CatHistNorm.Draw("TEXT")
    
    c1.cd(2)
    FlavHist.Draw("colzTEXT")

    c1.SaveAs(workingdir+"/output/categories.png")
    c1.SaveAs(workingdir+"/output/categories.pdf")
    
    
    
    
if __name__ == "__main__":
	main()


