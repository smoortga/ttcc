import ROOT
import os
import sys
from argparse import ArgumentParser

ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetOptStat(0)

parser = ArgumentParser()
parser.add_argument('--infile', default="FILL",help='input file')
parser.add_argument('--outdir', default=os.getcwd(),help='name of output directory')
parser.add_argument('--cat', default="inclusive",help='ttbar category')
args = parser.parse_args()

f_ = ROOT.TFile(args.infile)
correct_tree = f_.Get("tree_correct")
flipped_tree = f_.Get("tree_flipped")
wrong_tree = f_.Get("tree_wrong")

def Plot1D(var,x_name,y_name,nbins,xmin,xmax,logy=1,overflow=1,category="inclusive"):
    
    if category == "inclusive": 
        ttbar_cat_sel = ""
        cat_text = "#it{t#bar{t} + jets (inclusive)}"
    elif category == "ttbb": 
        ttbar_cat_sel = "event_Category == 0"
        cat_text = "#it{t#bar{t} + bb }"
    elif category == "ttbj":
        ttbar_cat_sel = "event_Category == 1"
        cat_text = "#it{t#bar{t} + bj }"
    elif category == "ttcc":
        ttbar_cat_sel = "event_Category == 2"
        cat_text = "#it{t#bar{t} + cc }"
    elif category == "ttcj":
        ttbar_cat_sel = "event_Category == 3"
        cat_text = "#it{t#bar{t} + cj }"
    elif category == "ttjj":
        ttbar_cat_sel = "event_Category == 4"
        cat_text = "#it{t#bar{t} + jj }"
    elif category == "ttother":
        ttbar_cat_sel = "event_Category == -1"
        cat_text = "#it{t#bar{t} + other }"
    else: 
        print "NOT A PROPER EVENT CATEGORY: %s"%args.cat
        sys.exit(1)
    
    binwidth = float(xmax-xmin)/nbins
    if "[" in x_name: units_x = x_name.split("[")[1].split("]")[0]
    else: units_x = ""
    
    h_correct = ROOT.TH1D("h_correct",";%s;%s / %.2f %s"%(x_name,y_name,binwidth,units_x),nbins,xmin,xmax)
    correct_tree.Draw(var+">>h_correct",ttbar_cat_sel)
    if overflow: h_correct.GetXaxis().SetRange(1,h_correct.GetNbinsX()+1)
    h_correct.Scale(1./h_correct.Integral())
    h_correct.SetLineWidth(3)
    h_correct.SetLineColor(2)
    
    h_flipped = ROOT.TH1D("h_flipped",";%s;%s / %.2f %s"%(x_name,y_name,binwidth,units_x),nbins,xmin,xmax)
    flipped_tree.Draw(var+">>h_flipped",ttbar_cat_sel)
    if overflow: h_flipped.GetXaxis().SetRange(1,h_flipped.GetNbinsX()+1)
    h_flipped.Scale(1./h_flipped.Integral())
    h_flipped.SetLineWidth(2)
    h_flipped.SetLineStyle(2)
    h_flipped.SetLineColor(4)
    h_flipped.SetMarkerStyle(34)
    h_flipped.SetMarkerColor(4)
    h_flipped.SetMarkerSize(1.6)
    
    h_wrong = ROOT.TH1D("h_wrong",";%s;%s / %.2f %s"%(x_name,y_name,binwidth,units_x),nbins,xmin,xmax)
    wrong_tree.Draw(var+">>h_wrong",ttbar_cat_sel)
    if overflow: h_wrong.GetXaxis().SetRange(1,h_wrong.GetNbinsX()+1)
    h_wrong.Scale(1./h_wrong.Integral())
    h_wrong.SetLineWidth(0)
    h_wrong.SetFillColor(33)
    
    c = ROOT.TCanvas("c","c",800,700)
    c.cd()
    ROOT.gPad.SetLogy(logy)
    ROOT.gPad.SetMargin(0.15,0.05,0.15,0.1)
    
    ROOT.TGaxis.SetMaxDigits(3)
    
    max_bin_content = 0
    if h_correct.GetBinContent(h_correct.GetMaximumBin()) > max_bin_content: max_bin_content = h_correct.GetBinContent(h_correct.GetMaximumBin())
    if h_wrong.GetBinContent(h_wrong.GetMaximumBin()) > max_bin_content: max_bin_content = h_wrong.GetBinContent(h_wrong.GetMaximumBin())

    if (logy): 
        h_wrong.SetMinimum(0.0001)
        h_wrong.SetMaximum(10000)
    else:
        h_wrong.SetMinimum(0)
        h_wrong.SetMaximum(1.5*max_bin_content)
    h_wrong.GetYaxis().SetLabelSize(0.05)
    h_wrong.GetYaxis().SetLabelOffset(0.01)
    h_wrong.GetYaxis().SetTitleSize(0.055)
    h_wrong.GetYaxis().SetTitleOffset(1.25)
    h_wrong.GetXaxis().SetTitleSize(0.055)
    h_wrong.GetXaxis().SetTitleOffset(1.1)
    h_wrong.GetXaxis().SetLabelSize(0.05)
    
    h_wrong.Draw("")    
    h_correct.Draw("same")
    h_flipped.Draw("same p")
    
    
    ROOT.gPad.RedrawAxis()
    #line = ROOT.TLine()
    #if overflow: line.DrawLine(xmax+binwidth, ROOT.gPad.GetUymin(), xmax+binwidth, ROOT.gPad.GetUymax())
    #else:line.DrawLine(xmax, ROOT.gPad.GetUymin(), xmax, ROOT.gPad.GetUymax())
    
    
    # TEXT
    year = "2017"
    latex = ROOT.TLatex()
    latex.SetTextFont(42)
    latex.SetTextSize(0.05)
    latex.SetTextAlign(32)
    latex.DrawLatexNDC(0.94,0.94,year + ", 94X")
    
    latex_cms = ROOT.TLatex()
    latex_cms.SetTextFont(42)
    latex_cms.SetTextSize(0.045)
    latex_cms.SetTextAlign(11)
    latex_cms.DrawLatexNDC(0.19,0.83,"#bf{CMS} #it{Simulation}")
    
    latex_sample = ROOT.TLatex()
    latex_sample.SetTextFont(42)
    latex_sample.SetTextSize(0.045)
    latex_sample.SetTextAlign(11)
    latex_sample.DrawLatexNDC(0.19,0.77,cat_text)
    
    #Legend
    l = ROOT.TLegend(0.5,0.75,0.94,0.89)
    l.SetBorderSize(0)
    l.SetTextSize(0.045)
    l.AddEntry(h_correct,"correct combinations","l")
    l.AddEntry(h_flipped,"flipped combinations","p")
    l.AddEntry(h_wrong,"wrong combinations","f")
    l.Draw("same")
    
    if not os.path.isdir(args.outdir): os.mkdir(args.outdir)
    
    if (logy): 
        c.SaveAs(args.outdir+"/"+var+"_%s_Log.pdf"%category)
        c.SaveAs(args.outdir+"/"+var+"_%s_Log.png"%category)
        c.SaveAs(args.outdir+"/"+var+"_%s_Log.C"%category)
    else: 
        c.SaveAs(args.outdir+"/"+var+"_%s_Linear.pdf"%category)
        c.SaveAs(args.outdir+"/"+var+"_%s_Linear.png"%category)
        c.SaveAs(args.outdir+"/"+var+"_%s_Linear.C"%category)
    
def main():

    
    
    Plot1D("pT_topb","p_{T}(b_{top}) [GeV]","Entries (norm.)",20,0,300,logy=0,overflow=1,category=args.cat)
    Plot1D("pT_antitopb","p_{T}(#bar{b}_{top}) [GeV]","Entries (norm.)",20,0,300,logy=0,overflow=1,category=args.cat)
    Plot1D("pT_addlead","p_{T}(j_{add}^{1}) [GeV]","Entries (norm.)",20,0,400,logy=0,overflow=1,category=args.cat)
    Plot1D("pT_addsublead","p_{T}(j_{add}^{2}) [GeV]","Entries (norm.)",20,0,200,logy=0,overflow=1,category=args.cat)
    Plot1D("Eta_topb","#eta(b_{top})","Entries (norm.)",20,-3.0,3.0,logy=0,overflow=0,category=args.cat)
    Plot1D("Eta_antitopb","#eta(#bar{b}_{top})","Entries (norm.)",20,-3.0,3.0,logy=0,overflow=0,category=args.cat)
    Plot1D("Eta_addlead","#eta(j_{add}^{1})","Entries (norm.)",20,-3.0,3.0,logy=0,overflow=0,category=args.cat)
    Plot1D("Eta_addsublead","#eta(j_{add}^{2})","Entries (norm.)",20,-3.0,3.0,logy=0,overflow=0,category=args.cat)
    # Plot1D("Phi_topb","#phi(b_{top})","Entries (norm.)",20,-3.2,3.2,logy=0,overflow=0,category=args.cat)
#     Plot1D("Phi_antitopb","#phi(#bar{b}_{top})","Entries (norm.)",20,-3.2,3.2,logy=0,overflow=0,category=args.cat)
#     Plot1D("Phi_addlead","#phi(j_{add}^{1})","Entries (norm.)",20,-3.2,3.2,logy=0,overflow=0,category=args.cat)
#     Plot1D("Phi_addsublead","#phi(j_{add}^{2})","Entries (norm.)",20,-3.2,3.2,logy=0,overflow=0,category=args.cat)
    # Plot1D("CSVv2_topb","CSVv2 discriminator b_{top}","Entries (norm.)",20,0,1,logy=0,overflow=0,category=args.cat)
#     Plot1D("CSVv2_antitopb","CSVv2 discriminator #bar{b}_{top}","Entries (norm.)",20,0,1,logy=0,overflow=0,category=args.cat)
#     Plot1D("CSVv2_addlead","CSVv2 discriminator j_{add}^{1}","Entries (norm.)",20,0,1,logy=0,overflow=0,category=args.cat)
#     Plot1D("CSVv2_addsublead","CSVv2 discriminator j_{add}^{2}","Entries (norm.)",20,0,1,logy=0,overflow=0,category=args.cat)
    Plot1D("DeepCSVBDiscr_topb","DeepCSVBDiscr discriminator b_{top}","Entries (norm.)",20,0,1,logy=0,overflow=0,category=args.cat)
    Plot1D("DeepCSVBDiscr_antitopb","DeepCSVBDiscr discriminator #bar{b}_{top}","Entries (norm.)",20,0,1,logy=0,overflow=0,category=args.cat)
    Plot1D("DeepCSVBDiscr_addlead","DeepCSVBDiscr discriminator j_{add}^{1}","Entries (norm.)",20,0,1,logy=0,overflow=0,category=args.cat)
    Plot1D("DeepCSVBDiscr_addsublead","DeepCSVBDiscr discriminator j_{add}^{2}","Entries (norm.)",20,0,1,logy=0,overflow=0,category=args.cat)
    Plot1D("DeepCSVCvsL_topb","DeepCSVCvsL discriminator b_{top}","Entries (norm.)",20,0,1,logy=0,overflow=0,category=args.cat)
    Plot1D("DeepCSVCvsL_antitopb","DeepCSVCvsL discriminator #bar{b}_{top}","Entries (norm.)",20,0,1,logy=0,overflow=0,category=args.cat)
    Plot1D("DeepCSVCvsL_addlead","DeepCSVCvsL discriminator j_{add}^{1}","Entries (norm.)",20,0,1,logy=0,overflow=0,category=args.cat)
    Plot1D("DeepCSVCvsL_addsublead","DeepCSVCvsL discriminator j_{add}^{2}","Entries (norm.)",20,0,1,logy=0,overflow=0,category=args.cat)
    Plot1D("DeepCSVCvsB_topb","DeepCSVCvsB discriminator b_{top}","Entries (norm.)",20,0,1,logy=0,overflow=0,category=args.cat)
    Plot1D("DeepCSVCvsB_antitopb","DeepCSVCvsB discriminator #bar{b}_{top}","Entries (norm.)",20,0,1,logy=0,overflow=0,category=args.cat)
    Plot1D("DeepCSVCvsB_addlead","DeepCSVCvsB discriminator j_{add}^{1}","Entries (norm.)",20,0,1,logy=0,overflow=0,category=args.cat)
    Plot1D("DeepCSVCvsB_addsublead","DeepCSVCvsB discriminator j_{add}^{2}","Entries (norm.)",20,0,1,logy=0,overflow=0,category=args.cat)
    Plot1D("DeltaR_topb_leppos","#DeltaR(b_{top},l^{+})","Entries (norm.)",20,0,5,logy=0,overflow=1,category=args.cat)
    Plot1D("DeltaR_antitopb_lepneg","#DeltaR(#bar{b}_{top},l^{-})","Entries (norm.)",20,0,5,logy=0,overflow=1,category=args.cat)
    Plot1D("DeltaR_adds","#DeltaR(j_{add}^{1},j_{add}^{2})","Entries (norm.)",20,0,5,logy=0,overflow=1,category=args.cat)
    Plot1D("minv_topb_leppos","m_{inv}(b_{top},l^{+}) [GeV]","Entries (norm.)",20,0,400,logy=0,overflow=1,category=args.cat)
    Plot1D("minv_antitopb_lepneg","m_{inv}(#bar{b}_{top},l^{-}) [GeV]","Entries (norm.)",20,0,400,logy=0,overflow=1,category=args.cat)
    Plot1D("minv_adds","m_{inv}(j_{add}^{1},j_{add}^{2}) [GeV]","Entries (norm.)",20,0,500,logy=0,overflow=1,category=args.cat)
    # Plot1D("CSVv2_addJet2","CSVv2 Discriminator second add. jet","Jets (norm.)",10,0,1,logy=1,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     Plot1D("DeepCSVBDiscr_addJet1","DeepCSV BDiscriminator first add. jet","Jets (norm.)",10,0,1,logy=1,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     Plot1D("DeepCSVBDiscr_addJet2","DeepCSV BDiscriminator second add. jet","Jets (norm.)",10,0,1,logy=1,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)


if __name__ == "__main__":
    main()