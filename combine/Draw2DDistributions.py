import ROOT
import os
import sys
from argparse import ArgumentParser
from array import array

def main():

    parser = ArgumentParser()
    parser.add_argument('--indir', default="FILL",help='input directory that contains all the samples')
    #parser.add_argument('--outdfile', default=os.getcwd(),help='name of output directory')
    args = parser.parse_args()

    ROOT.gROOT.SetBatch(1)
    ROOT.gStyle.SetOptStat(0)

    
	
    #binsx = [ 0.,0.25,0.4,0.5,0.7,0.8,0.9,1.0]
    #binsy = [ 0.,0.2,0.3,0.4,0.45,0.5,0.6,1.0,1.15]
    binsx = [ 0.  ,  0.05,  0.1 ,  0.15,  0.2 ,  0.25,  0.3 ,  0.35,  0.4 ,
        0.45,  0.5 ,  0.55,  0.6 ,  0.65,  0.7 ,  0.75,  0.8 ,  0.85,
        0.9 ,  0.95, 1.]
    binsy = [ 0.  ,  0.05,  0.1 ,  0.15,  0.2 ,  0.25,  0.3 ,  0.35,  0.4 ,
        0.45,  0.5 ,  0.55,  0.6 ,  0.65,  0.7 ,  0.75,  0.8 ,  0.85,
        0.9 ,  0.95, 1., 1.1]
    
    
    #************************************
    #
    # SIMULATION
    #
    #************************************
    
    

    weights_to_apply = "weight_bjets_ctag_iterativefit*weight_cjets_ctag_iterativefit*weight_udsgjets_ctag_iterativefit*weight_bcjets_btag_DeepCSVMedium*weight_udsgjets_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
    infile = ROOT.TFile(args.indir + "/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS.root")
    intree = infile.Get("tree")

    
    c = ROOT.TCanvas("c","c",1600,800)
    c.cd()
    c.SetMargin(0.0,0.09,0.105,0.01)
    #c.SetFillStyle(4000)
    hist_ttbb_dummy = ROOT.TH2D("hist_ttbb_dummy","",len(binsx)-1,array("d",binsx),len(binsy)-1,array("d",binsy))
    intree.Draw("ttHF_selector_NN_CvsB:ttHF_selector_NN_CvsL >> hist_ttbb_dummy",weights_to_apply+"*(event_Category_VisiblePS == 0)")
    hist_ttbb_dummy.Scale(1./hist_ttbb_dummy.Integral())
    hist_ttbb_dummy.GetZaxis().SetRangeUser(0,0.22)
    hist_ttbb_dummy.GetZaxis().SetLabelSize(0.04)
    hist_ttbb_dummy.GetZaxis().SetLabelOffset(0.00)
    hist_ttbb_dummy.Draw("COLZ")
    ROOT.gPad.SetLogz(1)
	
    pad0 = ROOT.TPad("pad0","pad0",0.0,0.,0.915,1.)
    pad0.Draw()
	
	
    
    #
    # ttbb
    #
    pad1 = ROOT.TPad("pad1","pad1",0.0,0.57,0.35,0.99)
    pad1.Draw()
    pad1.cd()
    ROOT.gPad.SetMargin(0.228,0.02,0.03,0)
    hist_ttbb = ROOT.TH2D("hist_ttbb","",len(binsx)-1,array("d",binsx),len(binsy)-1,array("d",binsy))
    intree.Draw("ttHF_selector_NN_CvsB:ttHF_selector_NN_CvsL >> hist_ttbb",weights_to_apply+"*(event_Category_VisiblePS == 0)")
    hist_ttbb.Scale(1./hist_ttbb.Integral())
    hist_ttbb.GetYaxis().SetTitle("#Delta_{b}^{c}")
    hist_ttbb.GetYaxis().CenterTitle()
    hist_ttbb.GetYaxis().SetTitleSize(0.11)
    hist_ttbb.GetYaxis().SetTitleOffset(0.8)
    hist_ttbb.GetYaxis().SetLabelSize(0.075)
    hist_ttbb.GetYaxis().SetLabelOffset(2*hist_ttbb.GetYaxis().GetLabelOffset())
    hist_ttbb.GetXaxis().SetLabelSize(0)
    hist_ttbb.GetZaxis().SetRangeUser(0,0.23)
    ROOT.gPad.SetLogz(1)
    hist_ttbb.Draw("COL")
    latex_ttbb = ROOT.TLatex()
    latex_ttbb.SetTextFont(42)
    latex_ttbb.SetTextSize(0.09)
    latex_ttbb.SetTextAlign(32)
    latex_ttbb.DrawLatexNDC(0.94,0.94,"t#bar{t}b#bar{b}")
    latex_ttbb.SetTextAlign(12)
    latex_ttbb.DrawLatexNDC(0.228 + 0.04,0.94,"#bf{CMS} #it{Simulation}")
    
    
    
    
    #
    # ttbj
    #
    c.cd()
    pad2 = ROOT.TPad("pad2","pad2",0.0,0.0,0.35,0.55)
    pad2.Draw()
    pad2.cd()
    ROOT.gPad.SetMargin(0.228,0.02,0.1818+0.03,0)
    hist_ttbL = ROOT.TH2D("hist_ttbL","",len(binsx)-1,array("d",binsx),len(binsy)-1,array("d",binsy))
    intree.Draw("ttHF_selector_NN_CvsB:ttHF_selector_NN_CvsL >> hist_ttbL",weights_to_apply+"*(event_Category_VisiblePS == 1)")
    hist_ttbL.Scale(1./hist_ttbL.Integral())
    hist_ttbL.GetYaxis().SetTitle("#Delta_{b}^{c}")
    hist_ttbL.GetYaxis().CenterTitle()
    hist_ttbL.GetYaxis().SetTitleSize(0.085)
    hist_ttbL.GetYaxis().SetTitleOffset(1.)
    hist_ttbL.GetYaxis().SetLabelSize(0.06)
    hist_ttbL.GetYaxis().SetLabelOffset(2*hist_ttbL.GetYaxis().GetLabelOffset())
    hist_ttbL.GetXaxis().SetTitle("#Delta_{L}^{c}")
    hist_ttbL.GetXaxis().CenterTitle()
    hist_ttbL.GetXaxis().SetTitleSize(0.08)
    hist_ttbL.GetXaxis().SetTitleOffset(1)
    hist_ttbL.GetXaxis().SetLabelSize(0.06)
    hist_ttbL.GetXaxis().SetLabelOffset(2*hist_ttbL.GetXaxis().GetLabelOffset())
    hist_ttbL.GetZaxis().SetRangeUser(0,0.23)
    ROOT.gPad.SetLogz(1)
    hist_ttbL.Draw("COL")
    latex_ttbL = ROOT.TLatex()
    latex_ttbL.SetTextFont(42)
    latex_ttbL.SetTextSize(0.07)
    latex_ttbL.SetTextAlign(32)
    latex_ttbL.DrawLatexNDC(0.94,0.94,"t#bar{t}bL")
    latex_ttbL.SetTextAlign(12)
    latex_ttbL.DrawLatexNDC(0.228 + 0.04,0.94,"#bf{CMS} #it{Simulation}")
    
    #
    # ttcc
    #
    c.cd()
    pad3 = ROOT.TPad("pad3","pad3",0.36,0.57,0.63,0.99)
    pad3.Draw()
    pad3.cd()
    ROOT.gPad.SetMargin(0.02,0.02,0.03,0)
    hist_ttcc = ROOT.TH2D("hist_ttcc","",len(binsx)-1,array("d",binsx),len(binsy)-1,array("d",binsy))
    intree.Draw("ttHF_selector_NN_CvsB:ttHF_selector_NN_CvsL >> hist_ttcc",weights_to_apply+"*(event_Category_VisiblePS == 2)")
    hist_ttcc.Scale(1./hist_ttcc.Integral())
    hist_ttcc.GetYaxis().SetLabelSize(0)
    hist_ttcc.GetXaxis().SetLabelSize(0)
    hist_ttcc.GetZaxis().SetRangeUser(0,0.23)
    ROOT.gPad.SetLogz(1)
    hist_ttcc.Draw("COL")
    latex_ttcc = ROOT.TLatex()
    latex_ttcc.SetTextFont(42)
    latex_ttcc.SetTextSize(0.09)
    latex_ttcc.SetTextAlign(32)
    latex_ttcc.DrawLatexNDC(0.94,0.94,"t#bar{t}c#bar{c}")
    latex_ttcc.SetTextAlign(12)
    latex_ttcc.DrawLatexNDC(0.065,0.94,"#bf{CMS} #it{Simulation}")
    
    #
    # ttcL
    #
    c.cd()
    pad4 = ROOT.TPad("pad4","pad4",0.36,0,0.63,0.55)
    pad4.Draw()
    pad4.cd()
    ROOT.gPad.SetMargin(0.02,0.02,0.1818+0.03,0)
    hist_ttcL = ROOT.TH2D("hist_ttcL","",len(binsx)-1,array("d",binsx),len(binsy)-1,array("d",binsy))
    intree.Draw("ttHF_selector_NN_CvsB:ttHF_selector_NN_CvsL >> hist_ttcL",weights_to_apply+"*(event_Category_VisiblePS == 3)")
    hist_ttcL.Scale(1./hist_ttcL.Integral())
    hist_ttcL.GetYaxis().SetLabelSize(0)
    hist_ttcL.GetXaxis().SetTitle("#Delta_{L}^{c}")
    hist_ttcL.GetXaxis().CenterTitle()
    hist_ttcL.GetXaxis().SetTitleSize(0.08)
    hist_ttcL.GetXaxis().SetTitleOffset(1)
    hist_ttcL.GetXaxis().SetLabelSize(0.06)
    hist_ttcL.GetXaxis().SetLabelOffset(2*hist_ttcL.GetXaxis().GetLabelOffset())
    hist_ttcL.GetZaxis().SetRangeUser(0,0.23)
    ROOT.gPad.SetLogz(1)
    hist_ttcL.Draw("COL")
    latex_ttcL = ROOT.TLatex()
    latex_ttcL.SetTextFont(42)
    latex_ttcL.SetTextSize(0.07)
    latex_ttcL.SetTextAlign(32)
    latex_ttcL.DrawLatexNDC(0.94,0.94,"t#bar{t}cL")
    latex_ttcL.SetTextAlign(12)
    latex_ttcL.DrawLatexNDC(0.065,0.94,"#bf{CMS} #it{Simulation}")

    #
    # ttLF
    #
    c.cd()
    pad5 = ROOT.TPad("pad5","pad5",0.64,0.57,0.91,0.99)
    pad5.Draw()
    pad5.cd()
    ROOT.gPad.SetMargin(0.02,0.02,0.03,0)
    hist_ttLF = ROOT.TH2D("hist_ttLF","",len(binsx)-1,array("d",binsx),len(binsy)-1,array("d",binsy))
    intree.Draw("ttHF_selector_NN_CvsB:ttHF_selector_NN_CvsL >> hist_ttLF",weights_to_apply+"*(event_Category_VisiblePS == 4)")
    hist_ttLF.Scale(1./hist_ttLF.Integral())
    hist_ttLF.GetYaxis().SetLabelSize(0)
    hist_ttLF.GetXaxis().SetLabelSize(0)
    hist_ttLF.GetZaxis().SetRangeUser(0,0.23)
    ROOT.gPad.SetLogz(1)
    hist_ttLF.Draw("COL")
    latex_ttLF = ROOT.TLatex()
    latex_ttLF.SetTextFont(42)
    latex_ttLF.SetTextSize(0.09)
    latex_ttLF.SetTextAlign(32)
    latex_ttLF.DrawLatexNDC(0.94,0.94,"t#bar{t}LF")
    latex_ttLF.SetTextAlign(12)
    latex_ttLF.DrawLatexNDC(0.065,0.94,"#bf{CMS} #it{Simulation}")
    
    #
    # ttcL
    #
    c.cd()
    pad6 = ROOT.TPad("pad6","pad6",0.64,0,0.91,0.55)
    pad6.Draw()
    pad6.cd()
    ROOT.gPad.SetMargin(0.02,0.02,0.1818+0.03,0)
    hist_ttother = ROOT.TH2D("hist_ttother","",len(binsx)-1,array("d",binsx),len(binsy)-1,array("d",binsy))
    intree.Draw("ttHF_selector_NN_CvsB:ttHF_selector_NN_CvsL >> hist_ttother",weights_to_apply+"*(event_Category_VisiblePS == -1)")
    hist_ttother.Scale(1./hist_ttother.Integral())
    hist_ttother.GetYaxis().SetLabelSize(0)
    hist_ttother.GetXaxis().SetTitle("#Delta_{L}^{c}")
    hist_ttother.GetXaxis().CenterTitle()
    hist_ttother.GetXaxis().SetTitleSize(0.08)
    hist_ttother.GetXaxis().SetTitleOffset(1)
    hist_ttother.GetXaxis().SetLabelSize(0.06)
    hist_ttother.GetXaxis().SetLabelOffset(2*hist_ttother.GetXaxis().GetLabelOffset())
    hist_ttother.GetZaxis().SetRangeUser(0,0.23)
    ROOT.gPad.SetLogz(1)
    hist_ttother.Draw("COL")
    latex_ttother = ROOT.TLatex()
    latex_ttother.SetTextFont(42)
    latex_ttother.SetTextSize(0.07)
    latex_ttother.SetTextAlign(32)
    latex_ttother.DrawLatexNDC(0.94,0.94,"t#bar{t} others")
    latex_ttother.SetTextAlign(12)
    latex_ttother.DrawLatexNDC(0.065,0.94,"#bf{CMS} #it{Simulation}")
    
    #
    # Draw Colorbar
    #
    #c.cd()
#    pad7 = ROOT.TPad("pad7","pad7",0.92,0.02,0.99,0.99)
#    pad7.Draw()
#    pad7.cd()
#    hist_ttbb = ROOT.TH2D("hist_ttbb","",len(binsx)-1,array("d",binsx),len(binsy)-1,array("d",binsy))
#    intree.Draw("ttHF_selector_NN_CvsB:ttHF_selector_NN_CvsL >> hist_ttbb",weights_to_apply+"*(event_Category_VisiblePS == 0)")
#    palette = hist_ttbb.GetListOfFunctions().FindObject("palette")
#    #palette.SetY2NDC(0.7)
#    palette.Paint()



    c.cd()
    c.SaveAs("ttHFDistributions2D.pdf")
    c.SaveAs("ttHFDistributions2D.png")
    c.SaveAs("ttHFDistributions2D.C")
    
    #infile.Close()
    
    
    #************************************
    #
    # DATA
    #
    #************************************


if __name__ == "__main__":
    main()
