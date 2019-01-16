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

mg = ROOT.THStack()
mg.Add(h_ttcc)
mg.Add(h_ttcj)
mg.Add(h_ttbb)
mg.Add(h_ttbj)
mg.Add(h_ttjj)
mg.Add(h_ttother)
mg.Add(h_bkg)
summed_MC_hist = h_ttcc.Clone()
summed_MC_hist.Add(h_ttcj)
summed_MC_hist.Add(h_ttbb)
summed_MC_hist.Add(h_ttbj)
summed_MC_hist.Add(h_ttjj)
summed_MC_hist.Add(h_ttother)
summed_MC_hist.Add(h_bkg)
summed_MC_hist.SetFillStyle(3244)
summed_MC_hist.SetFillColor(13)
summed_MC_hist.SetLineWidth(0)

c_pre = ROOT.TCanvas("c_pre","c_pre",800,700)
c_pre.cd()
uppad_pre = ROOT.TPad("u_pre","u_pre",0.,0.25,1.,1.)
downpad_pre = ROOT.TPad("d_pre","d_pre",0.,0.0,1.,0.25)
uppad_pre.Draw()
downpad_pre.Draw()

uppad_pre.cd()
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
l.AddEntry(h_ttbb,"t#bar{t}b#bar{b}","f")
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



downpad_pre.cd()
ROOT.gPad.SetMargin(0.15,0.05,0.4,0.01)
#ratio hist
h_data.GetXaxis().SetTitle("bin number")
ratio_hist = h_data.Clone()
ratio_hist.Divide(summed_MC_hist)
ratio_hist.SetMarkerStyle(20)
ratio_hist.Draw("pe1x0")
ratio_hist.GetYaxis().SetRangeUser(0.3,2.1)
ratio_hist.GetYaxis().SetNdivisions(4)
ratio_hist.GetYaxis().SetLabelSize(0.14)
ratio_hist.GetYaxis().SetLabelOffset(0.01)
ratio_hist.GetYaxis().SetTitle("#frac{data}{MC}")
ratio_hist.GetYaxis().SetTitleSize(0.16)
ratio_hist.GetYaxis().CenterTitle()
ratio_hist.GetYaxis().SetTitleOffset(0.4)
ratio_hist.GetXaxis().SetTitleSize(0.19)
ratio_hist.GetXaxis().SetTitleOffset(0.9)
ratio_hist.GetXaxis().SetLabelSize(0.14)

MC_ratio_hist = summed_MC_hist.Clone()
MC_ratio_hist.Divide(summed_MC_hist)
MC_ratio_hist.Draw("same E2")


#Redraw ratio_hist
ratio_hist.Draw("same pe1x0")



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
    syst_dict[syst+"Up"]["h_ttbb"] = f_.Get("h_ttbb_"+syst+"Up")
    syst_dict[syst+"Up"]["h_ttbj"] = f_.Get("h_ttbj_"+syst+"Up")
    syst_dict[syst+"Up"]["h_ttcc"] = f_.Get("h_ttcc_"+syst+"Up")
    syst_dict[syst+"Up"]["h_ttcj"] = f_.Get("h_ttcj_"+syst+"Up")
    syst_dict[syst+"Up"]["h_ttjj"] = f_.Get("h_ttjj_"+syst+"Up")
    syst_dict[syst+"Up"]["h_ttother"] = f_.Get("h_ttother_"+syst+"Up")
    syst_dict[syst+"Up"]["h_bkg"] = f_.Get("h_bkg_"+syst+"Up")
    syst_dict[syst+"Down"]={}
    syst_dict[syst+"Down"]["h_ttbb"] = f_.Get("h_ttbb_"+syst+"Down")
    syst_dict[syst+"Down"]["h_ttbj"] = f_.Get("h_ttbj_"+syst+"Down")
    syst_dict[syst+"Down"]["h_ttcc"] = f_.Get("h_ttcc_"+syst+"Down")
    syst_dict[syst+"Down"]["h_ttcj"] = f_.Get("h_ttcj_"+syst+"Down")
    syst_dict[syst+"Down"]["h_ttjj"] = f_.Get("h_ttjj_"+syst+"Down")
    syst_dict[syst+"Down"]["h_ttother"] = f_.Get("h_ttother_"+syst+"Down")
    if not (syst == "muR" or syst == "muF"): syst_dict[syst+"Down"]["h_bkg"] = f_.Get("h_bkg_"+syst+"Down")
    
    temp_summed_hist_Up = syst_dict[syst+"Up"]["h_ttbb"].Clone()
    temp_summed_hist_Up.Add(syst_dict[syst+"Up"]["h_ttbj"])
    temp_summed_hist_Up.Add(syst_dict[syst+"Up"]["h_ttcc"])
    temp_summed_hist_Up.Add(syst_dict[syst+"Up"]["h_ttcj"])
    temp_summed_hist_Up.Add(syst_dict[syst+"Up"]["h_ttjj"])
    temp_summed_hist_Up.Add(syst_dict[syst+"Up"]["h_ttother"])
    if not (syst == "muR" or syst == "muF"): temp_summed_hist_Up.Add(syst_dict[syst+"Up"]["h_bkg"])
    else: temp_summed_hist_Up.Add(h_bkg)
    temp_summed_hist_Up.Add(summed_MC_hist,-1)
    for ibin in range(summed_MC_hist.GetNbinsX()):
        this_error = temp_summed_hist_Up.GetBinContent(ibin+1)
        if this_error >= 0: graph_eyh[ibin] = sqrt(graph_eyh[ibin]**2 + (this_error)**2)
        if this_error < 0: graph_eyl[ibin] = sqrt(graph_eyl[ibin]**2 + (this_error)**2)
    
    temp_summed_hist_Down = syst_dict[syst+"Down"]["h_ttbb"].Clone()
    temp_summed_hist_Down.Add(syst_dict[syst+"Down"]["h_ttbj"])
    temp_summed_hist_Down.Add(syst_dict[syst+"Down"]["h_ttcc"])
    temp_summed_hist_Down.Add(syst_dict[syst+"Down"]["h_ttcj"])
    temp_summed_hist_Down.Add(syst_dict[syst+"Down"]["h_ttjj"])
    temp_summed_hist_Down.Add(syst_dict[syst+"Down"]["h_ttother"])
    if not (syst == "muR" or syst == "muF"): temp_summed_hist_Down.Add(syst_dict[syst+"Down"]["h_bkg"])
    else: temp_summed_hist_Down.Add(h_bkg)
    temp_summed_hist_Down.Add(summed_MC_hist,-1)
    for ibin in range(summed_MC_hist.GetNbinsX()):
        this_error = temp_summed_hist_Down.GetBinContent(ibin+1)
        if this_error >= 0: graph_eyh[ibin] = sqrt(graph_eyh[ibin]**2 + (this_error)**2)
        if this_error < 0: graph_eyl[ibin] = sqrt(graph_eyl[ibin]**2 + (this_error)**2)

# add ttbar normalization by hand
syst_dict["ttbarNorm"+"Up"]={}
syst_dict["ttbarNorm"+"Up"]["h_ttbb"] = h_ttbb.Clone()
syst_dict["ttbarNorm"+"Up"]["h_ttbb"].Scale(1.048)
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
syst_dict["ttbarNorm"+"Down"]["h_ttbb"] = h_ttbb.Clone()
syst_dict["ttbarNorm"+"Down"]["h_ttbb"].Scale(0.939)
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

temp_summed_hist_Up = syst_dict["ttbarNorm"+"Up"]["h_ttbb"].Clone()
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

temp_summed_hist_Down = syst_dict["ttbarNorm"+"Down"]["h_ttbb"].Clone()
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

ratio_hist.Draw("same pe1x0")

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


###
#
# Chi2
#
###
chi2_pre = 0
for ibin in range(ratio_hist.GetNbinsX()):
    value = ratio_hist.GetBinContent(ibin+1)
    error = (ratio_graph_eyh[ibin] + ratio_graph_eyl[ibin])/2.
    chi2_pre += ((value - 1)**2) / (error**2)
print "Chi2/ndof Prefit: ", chi2_pre/float(ratio_hist.GetNbinsX())
    


c_pre.SaveAs("./Prefit.pdf")
c_pre.SaveAs("./Prefit.png")
c_pre.SaveAs("./Prefit.C")










#
#
# POSTFIT
#
#
# Fb = 1.161
# FbUp = Fb+0.213
# FbDown = Fb-0.178
# Fc = 1.775 
# FcUp = Fc+0.329
# FcDown = Fc-0.275
# Fl = 0.719
# FlUp =Fl+0.117 
# FlDown =Fl-0.100

#    Fb :    +1.254   -0.155/+0.168 (68%)
#    Fc :    +1.676   -0.200/+0.202 (68%)
#    Fl :    +0.705   -0.027/+0.027 (68%)

Fb = 1.254
FbUp = Fb+0.168
FbDown = Fb-0.155
Fc = 1.676 
FcUp = Fc+0.200
FcDown = Fc-0.202
Fl = 0.705
FlUp =Fl+0.027
FlDown =Fl-0.027

#For systematics
h_ttbbUp = h_ttbb.Clone()
h_ttbbUp.Scale(FbUp)
h_ttbbDown = h_ttbb.Clone()
h_ttbbDown.Scale(FbDown)
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

h_ttbb.Scale(Fb)
h_ttbj.Scale(Fb)
h_ttcc.Scale(Fc)
h_ttcj.Scale(Fc)
h_ttjj.Scale(Fl)
h_ttother.Scale(Fl)


mg_post = ROOT.THStack()
mg_post.Add(h_ttcc)
mg_post.Add(h_ttcj)
mg_post.Add(h_ttbb)
mg_post.Add(h_ttbj)
mg_post.Add(h_ttjj)
mg_post.Add(h_ttother)
mg_post.Add(h_bkg)
summed_MC_hist_post = h_ttcc.Clone()
summed_MC_hist_post.Add(h_ttcj)
summed_MC_hist_post.Add(h_ttbb)
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
ratio_hist_post = h_data.Clone()
ratio_hist_post.Divide(summed_MC_hist_post)
ratio_hist_post.SetMarkerStyle(20)
ratio_hist_post.Draw("pe1x0")
ratio_hist_post.GetYaxis().SetRangeUser(0.3,2.1)
ratio_hist_post.GetYaxis().SetNdivisions(4)
ratio_hist_post.GetYaxis().SetLabelSize(0.14)
ratio_hist_post.GetYaxis().SetLabelOffset(0.01)
ratio_hist_post.GetYaxis().SetTitle("#frac{data}{MC}")
ratio_hist_post.GetYaxis().SetTitleSize(0.16)
ratio_hist_post.GetYaxis().CenterTitle()
ratio_hist_post.GetYaxis().SetTitleOffset(0.4)
ratio_hist_post.GetXaxis().SetTitleSize(0.19)
ratio_hist_post.GetXaxis().SetTitleOffset(0.9)
ratio_hist_post.GetXaxis().SetLabelSize(0.14)

MC_ratio_hist_post = summed_MC_hist_post.Clone()
MC_ratio_hist_post.Divide(summed_MC_hist_post)
MC_ratio_hist_post.Draw("same E2")


#Redraw ratio_hist_post
ratio_hist_post.Draw("same pe1x0")




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
syst_dict["fit"+"Up"]["h_ttbb"] = h_ttbbUp
syst_dict["fit"+"Up"]["h_ttbj"] = h_ttbjUp
syst_dict["fit"+"Up"]["h_ttcc"] = h_ttccUp
syst_dict["fit"+"Up"]["h_ttcj"] = h_ttcjUp
syst_dict["fit"+"Up"]["h_ttjj"] = h_ttjjUp
syst_dict["fit"+"Up"]["h_ttother"] = h_ttotherUp
syst_dict["fit"+"Up"]["h_bkg"] = h_bkg
syst_dict["fit"+"Down"]={}
syst_dict["fit"+"Down"]["h_ttbb"] = h_ttbbDown
syst_dict["fit"+"Down"]["h_ttbj"] = h_ttbjDown
syst_dict["fit"+"Down"]["h_ttcc"] = h_ttccDown
syst_dict["fit"+"Down"]["h_ttcj"] = h_ttcjDown
syst_dict["fit"+"Down"]["h_ttjj"] = h_ttjjDown
syst_dict["fit"+"Down"]["h_ttother"] = h_ttotherDown
syst_dict["fit"+"Down"]["h_bkg"] = h_bkg

temp_summed_hist_Up = syst_dict["fit"+"Up"]["h_ttbb"].Clone()
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

temp_summed_hist_Down = syst_dict["fit"+"Down"]["h_ttbb"].Clone()
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

ratio_hist_post.Draw("same pe1x0")

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

###
#
# Chi2
#
###
chi2_post = 0
for ibin in range(ratio_hist_post.GetNbinsX()):
    value = ratio_hist_post.GetBinContent(ibin+1)
    error = (ratio_graph_eyh[ibin] + ratio_graph_eyl[ibin])/2.
    chi2_post += ((value - 1)**2) / (error**2)
print "Chi2/ndof Postfit: ", chi2_post/float(ratio_hist.GetNbinsX())

c_post.SaveAs("./Postfit.pdf")
c_post.SaveAs("./Postfit.png")
c_post.SaveAs("./Postfit.C")

f_.Close()
