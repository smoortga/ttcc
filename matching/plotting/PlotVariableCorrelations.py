import ROOT
import os
import sys
from argparse import ArgumentParser
import pickle
from itertools import combinations

ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetOptStat(0)

parser = ArgumentParser()
parser.add_argument('--infile', default="FILL",help='input file')
parser.add_argument('--variables', default="FILL",help='variables.pkl file')
parser.add_argument('--outdir', default=os.getcwd(),help='name of output directory')
parser.add_argument('--cat', default="inclusive",help='ttbar category')
parser.add_argument('--perm', default="correct",help='permutation category: flipped, correct or wrong')
args = parser.parse_args()

f_ = ROOT.TFile(args.infile)
tree = f_.Get("tree_%s"%args.perm)


def Plot2D(varx,vary,x_name,y_name,nbinsx,xmin,xmax,nbinsy,ymin,ymax,logy=1,overflow=1,category="inclusive"):
    
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
    
#     binwidth = float(xmax-xmin)/nbins
#     if "[" in x_name: units_x = x_name.split("[")[1].split("]")[0]
#     else: units_x = ""
    
    h_perm = ROOT.TH2D("h_perm",";%s;%s"%(x_name,y_name),nbinsx,xmin,xmax,nbinsy,ymin,ymax)
    tree.Draw(vary+":"+varx+">>h_perm",ttbar_cat_sel)
    if overflow: 
        h_perm.GetXaxis().SetRange(1,h_perm.GetNbinsX()+1)
        h_perm.GetYaxis().SetRange(1,h_perm.GetNbinsY()+1)
    h_perm.Scale(1./h_perm.Integral())
    # h_perm.SetLineWidth(3)
#     h_perm.SetLineColor(2)
    
    c = ROOT.TCanvas("c","c",800,700)
    c.cd()
    ROOT.gPad.SetLogz(logy)
    ROOT.gPad.SetMargin(0.15,0.15,0.15,0.1)
    
    ROOT.TGaxis.SetMaxDigits(3)
    
   #  max_bin_content = 0
#     if h_correct.GetBinContent(h_correct.GetMaximumBin()) > max_bin_content: max_bin_content = h_correct.GetBinContent(h_correct.GetMaximumBin())
#     if h_wrong.GetBinContent(h_wrong.GetMaximumBin()) > max_bin_content: max_bin_content = h_wrong.GetBinContent(h_wrong.GetMaximumBin())
# 
#     if (logy): 
#         h_wrong.SetMinimum(0.0001)
#         h_wrong.SetMaximum(10000)
#     else:
#         h_wrong.SetMinimum(0)
#         h_wrong.SetMaximum(1.5*max_bin_content)
    h_perm.GetYaxis().SetLabelSize(0.05)
    h_perm.GetYaxis().SetLabelOffset(0.01)
    h_perm.GetYaxis().SetTitleSize(0.055)
    h_perm.GetYaxis().SetTitleOffset(1.25)
    h_perm.GetXaxis().SetTitleSize(0.055)
    h_perm.GetXaxis().SetTitleOffset(1.1)
    h_perm.GetXaxis().SetLabelSize(0.05)
    #h_perm.GetZaxis().SetTitleSize(0.055)
    h_perm.GetZaxis().SetTitleOffset(1.1)
    h_perm.GetZaxis().SetLabelSize(0.05)
    
    h_perm.Draw("COLZ")    
    
    
    #ROOT.gPad.RedrawAxis()
    #line = ROOT.TLine()
    #if overflow: line.DrawLine(xmax+binwidth, ROOT.gPad.GetUymin(), xmax+binwidth, ROOT.gPad.GetUymax())
    #else:line.DrawLine(xmax, ROOT.gPad.GetUymin(), xmax, ROOT.gPad.GetUymax())
    
    
    # TEXT
    year = "2017"
    latex = ROOT.TLatex()
    latex.SetTextFont(42)
    latex.SetTextSize(0.05)
    latex.SetTextAlign(32)
    latex.DrawLatexNDC(0.84,0.94,year + ", 94X")
    
    latex_cms = ROOT.TLatex()
    latex_cms.SetTextFont(42)
    latex_cms.SetTextSize(0.05)
    latex_cms.SetTextAlign(12)
    latex_cms.DrawLatexNDC(0.15,0.94,"#bf{CMS} #it{Simulation}")
    
    corr = h_perm.GetCorrelationFactor()
    latex_corr = ROOT.TLatex()
    latex_corr.SetTextFont(42)
    latex_corr.SetTextSize(0.05)
    latex_corr.SetTextAlign(12)
    latex_corr.DrawLatexNDC(0.19,0.8,"#rho = %.3f"%corr)
    
  #   latex_sample = ROOT.TLatex()
#     latex_sample.SetTextFont(42)
#     latex_sample.SetTextSize(0.045)
#     latex_sample.SetTextAlign(11)
#     latex_sample.DrawLatexNDC(0.19,0.77,cat_text)
#     
    #Legend
#     l = ROOT.TLegend(0.5,0.75,0.94,0.89)
#     l.SetBorderSize(0)
#     l.SetTextSize(0.045)
#     l.AddEntry(h_correct,"correct combinations","l")
#     l.AddEntry(h_flipped,"flipped combinations","p")
#     l.AddEntry(h_wrong,"wrong combinations","f")
#     l.Draw("same")
    
    if not os.path.isdir(args.outdir): os.mkdir(args.outdir)
    
    if (logy): 
        c.SaveAs(args.outdir+"/"+varx+"_"+vary+"_%s_%s_Log.pdf"%(category,args.perm))
        c.SaveAs(args.outdir+"/"+varx+"_"+vary+"_%s_%s_Log.png"%(category,args.perm))
        c.SaveAs(args.outdir+"/"+varx+"_"+vary+"_%s_%s_Log.C"%(category,args.perm))
    else: 
        c.SaveAs(args.outdir+"/"+varx+"_"+vary+"_%s_%s_Linear.pdf"%(category,args.perm))
        c.SaveAs(args.outdir+"/"+varx+"_"+vary+"_%s_%s_Linear.png"%(category,args.perm))
        c.SaveAs(args.outdir+"/"+varx+"_"+vary+"_%s_%s_Linear.C"%(category,args.perm))
    
def main():
    
    var_dict = {}
    var_dict["pT"] = [20,0,400]
    var_dict["Eta"] = [20,-3.0,3.0]
    var_dict["DeepCSV"] = [20,0,1]
    var_dict["DeltaR"] = [20,0,5]
    var_dict["minv"] = [20,0,500]
    
    
    variables = pickle.load(open(args.variables,"rb"))
    perm = [i for i in combinations(variables,2)]
    for p in perm:
        if "pT" in p[0]: 
            nbinx = var_dict["pT"][0]
            xmin = var_dict["pT"][1]
            xmax = var_dict["pT"][2]
        elif "Eta" in p[0]: 
            nbinx = var_dict["Eta"][0]
            xmin = var_dict["Eta"][1]
            xmax = var_dict["Eta"][2]
        elif "DeepCSV" in p[0]: 
            nbinx = var_dict["DeepCSV"][0]
            xmin = var_dict["DeepCSV"][1]
            xmax = var_dict["DeepCSV"][2]
        elif "DeltaR" in p[0]: 
            nbinx = var_dict["DeltaR"][0]
            xmin = var_dict["DeltaR"][1]
            xmax = var_dict["DeltaR"][2]
        elif "minv" in p[0]: 
            nbinx = var_dict["minv"][0]
            xmin = var_dict["minv"][1]
            xmax = var_dict["minv"][2]
        
        if "pT" in p[1]: 
            nbiny = var_dict["pT"][0]
            ymin = var_dict["pT"][1]
            ymax = var_dict["pT"][2]
        elif "Eta" in p[1]: 
            nbiny = var_dict["Eta"][0]
            ymin = var_dict["Eta"][1]
            ymax = var_dict["Eta"][2]
        elif "DeepCSV" in p[1]: 
            nbiny = var_dict["DeepCSV"][0]
            ymin = var_dict["DeepCSV"][1]
            ymax = var_dict["DeepCSV"][2]
        elif "DeltaR" in p[1]: 
            nbiny = var_dict["DeltaR"][0]
            ymin = var_dict["DeltaR"][1]
            ymax = var_dict["DeltaR"][2]
        elif "minv" in p[1]: 
            nbiny = var_dict["minv"][0]
            ymin = var_dict["minv"][1]
            ymax = var_dict["minv"][2]
    
        Plot2D(p[0],p[1],p[0],p[1],nbinx,xmin,xmax,nbiny,ymin,ymax,logy=1,overflow=1,category=args.cat)
    # Plot1D("pT_antitopb","p_{T}(#bar{b}_{top}) [GeV]","Entries (norm.)",20,0,300,logy=0,overflow=1,category=args.cat)
#     Plot1D("pT_addlead","p_{T}(j_{add}^{1}) [GeV]","Entries (norm.)",20,0,400,logy=0,overflow=1,category=args.cat)
#     Plot1D("pT_addsublead","p_{T}(j_{add}^{2}) [GeV]","Entries (norm.)",20,0,200,logy=0,overflow=1,category=args.cat)
#     Plot1D("Eta_topb","#eta(b_{top})","Entries (norm.)",20,-3.0,3.0,logy=0,overflow=0,category=args.cat)
#     Plot1D("Eta_antitopb","#eta(#bar{b}_{top})","Entries (norm.)",20,-3.0,3.0,logy=0,overflow=0,category=args.cat)
#     Plot1D("Eta_addlead","#eta(j_{add}^{1})","Entries (norm.)",20,-3.0,3.0,logy=0,overflow=0,category=args.cat)
#     Plot1D("Eta_addsublead","#eta(j_{add}^{2})","Entries (norm.)",20,-3.0,3.0,logy=0,overflow=0,category=args.cat)
#     Plot1D("Phi_topb","#phi(b_{top})","Entries (norm.)",20,-3.2,3.2,logy=0,overflow=0,category=args.cat)
#     Plot1D("Phi_antitopb","#phi(#bar{b}_{top})","Entries (norm.)",20,-3.2,3.2,logy=0,overflow=0,category=args.cat)
#     Plot1D("Phi_addlead","#phi(j_{add}^{1})","Entries (norm.)",20,-3.2,3.2,logy=0,overflow=0,category=args.cat)
#     Plot1D("Phi_addsublead","#phi(j_{add}^{2})","Entries (norm.)",20,-3.2,3.2,logy=0,overflow=0,category=args.cat)
#     Plot1D("CSVv2_topb","CSVv2 discriminator b_{top}","Entries (norm.)",20,0,1,logy=0,overflow=0,category=args.cat)
#     Plot1D("CSVv2_antitopb","CSVv2 discriminator #bar{b}_{top}","Entries (norm.)",20,0,1,logy=0,overflow=0,category=args.cat)
#     Plot1D("CSVv2_addlead","CSVv2 discriminator j_{add}^{1}","Entries (norm.)",20,0,1,logy=0,overflow=0,category=args.cat)
#     Plot1D("CSVv2_addsublead","CSVv2 discriminator j_{add}^{2}","Entries (norm.)",20,0,1,logy=0,overflow=0,category=args.cat)
#     Plot1D("DeepCSVBDiscr_topb","DeepCSVBDiscr discriminator b_{top}","Entries (norm.)",20,0,1,logy=0,overflow=0,category=args.cat)
#     Plot1D("DeepCSVBDiscr_antitopb","DeepCSVBDiscr discriminator #bar{b}_{top}","Entries (norm.)",20,0,1,logy=0,overflow=0,category=args.cat)
#     Plot1D("DeepCSVBDiscr_addlead","DeepCSVBDiscr discriminator j_{add}^{1}","Entries (norm.)",20,0,1,logy=0,overflow=0,category=args.cat)
#     Plot1D("DeepCSVBDiscr_addsublead","DeepCSVBDiscr discriminator j_{add}^{2}","Entries (norm.)",20,0,1,logy=0,overflow=0,category=args.cat)
#     Plot1D("DeepCSVCvsL_topb","DeepCSVCvsL discriminator b_{top}","Entries (norm.)",20,0,1,logy=0,overflow=0,category=args.cat)
#     Plot1D("DeepCSVCvsL_antitopb","DeepCSVCvsL discriminator #bar{b}_{top}","Entries (norm.)",20,0,1,logy=0,overflow=0,category=args.cat)
#     Plot1D("DeepCSVCvsL_addlead","DeepCSVCvsL discriminator j_{add}^{1}","Entries (norm.)",20,0,1,logy=0,overflow=0,category=args.cat)
#     Plot1D("DeepCSVCvsL_addsublead","DeepCSVCvsL discriminator j_{add}^{2}","Entries (norm.)",20,0,1,logy=0,overflow=0,category=args.cat)
#     Plot1D("DeepCSVCvsB_topb","DeepCSVCvsB discriminator b_{top}","Entries (norm.)",20,0,1,logy=0,overflow=0,category=args.cat)
#     Plot1D("DeepCSVCvsB_antitopb","DeepCSVCvsB discriminator #bar{b}_{top}","Entries (norm.)",20,0,1,logy=0,overflow=0,category=args.cat)
#     Plot1D("DeepCSVCvsB_addlead","DeepCSVCvsB discriminator j_{add}^{1}","Entries (norm.)",20,0,1,logy=0,overflow=0,category=args.cat)
#     Plot1D("DeepCSVCvsB_addsublead","DeepCSVCvsB discriminator j_{add}^{2}","Entries (norm.)",20,0,1,logy=0,overflow=0,category=args.cat)
#     Plot1D("DeltaR_topb_leppos","#DeltaR(b_{top},l^{+})","Entries (norm.)",20,0,5,logy=0,overflow=1,category=args.cat)
#     Plot1D("DeltaR_antitopb_lepneg","#DeltaR(#bar{b}_{top},l^{-})","Entries (norm.)",20,0,5,logy=0,overflow=1,category=args.cat)
#     Plot1D("DeltaR_adds","#DeltaR(j_{add}^{1},j_{add}^{2})","Entries (norm.)",20,0,5,logy=0,overflow=1,category=args.cat)
#     Plot1D("minv_topb_leppos","m_{inv}(b_{top},l^{+}) [GeV]","Entries (norm.)",20,0,400,logy=0,overflow=1,category=args.cat)
#     Plot1D("minv_antitopb_lepneg","m_{inv}(#bar{b}_{top},l^{-}) [GeV]","Entries (norm.)",20,0,400,logy=0,overflow=1,category=args.cat)
#     Plot1D("minv_adds","m_{inv}(j_{add}^{1},j_{add}^{2}) [GeV]","Entries (norm.)",20,0,500,logy=0,overflow=1,category=args.cat)
    # Plot1D("CSVv2_addJet2","CSVv2 Discriminator second add. jet","Jets (norm.)",10,0,1,logy=1,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     Plot1D("DeepCSVBDiscr_addJet1","DeepCSV BDiscriminator first add. jet","Jets (norm.)",10,0,1,logy=1,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     Plot1D("DeepCSVBDiscr_addJet2","DeepCSV BDiscriminator second add. jet","Jets (norm.)",10,0,1,logy=1,overflow=0,weights_to_apply=weight_string,lepton_category=lepton_channel)


if __name__ == "__main__":
    main()