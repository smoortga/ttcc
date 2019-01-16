import root_numpy as rootnp
import matplotlib.pyplot as plt
import sys
import ROOT
import os
from argparse import ArgumentParser
from array import array
from math import *
from sklearn.metrics import roc_curve,roc_auc_score
import numpy as np
import random

ROOT.gROOT.SetBatch(1)

parser = ArgumentParser()
parser.add_argument('--infile', default = "/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/analyse/SELECTED_NewElectronIDv2_MC_VisiblePS_WithttHFSelectior/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS.root", help='path to the training file')#TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8.root", help='path to the training file')
args = parser.parse_args()

variables = { # name: [leg,color,style]
    
    1:{
        "name": "DeepCSVcTagCvsL_addJet1",
        "opt":["c-tag CvsL add. jet 1",ROOT.kGreen+2,1]
        },
    
    2:{
        "name":"DeepCSVcTagCvsL_addJet2",
        "opt":["c-tag CvsL add. jet 2",ROOT.kGreen+2,2]
        },
        
    3:{
        "name": "DeepCSVcTagCvsB_addJet1",
        "opt":["c-tag CvsB add. jet 1",4,1]
        },
    
    4:{
        "name":"DeepCSVcTagCvsB_addJet2",
        "opt":["c-tag CvsB add. jet 2",4,2],
        },
    
    5:{
        "name": "TopMatching_NN_best_value",
        "opt":["matching NN output",6,1]
        },
    
    6:{
        "name":"DeltaR_addJets",
        "opt":["#Delta R (add. jets)",7,1]
        },
        
    7:{
        "name": "ttHF_selector_NN_CvsL",
        "opt":["#Delta_{L}^{c}",2,1]
        },
    
    8:{
        "name":"ttHF_selector_NN_CvsB",
        "opt":["#Delta_{b}^{c}",2,2],
        }
}



#
# ttcc vs ttbb
#
roc_ttcc_vs_ttbb_dict = {}
mg_ttcc_vs_ttbb = ROOT.TMultiGraph("mg_ttcc_vs_ttbb","")
l_ttcc_vs_ttbb = ROOT.TLegend(0.56,0.15,0.99,0.97)
l_ttcc_vs_ttbb.SetBorderSize(0)
for idx, item_dict in variables.iteritems():
    var = item_dict["name"]
    opt = item_dict["opt"]
    X_ttcc = rootnp.root2array(args.infile,"tree",var,"event_Category_VisiblePS == 2")
    #X_ttcc = rootnp.rec2array(X_ttcc)
    Y_ttcc = np.ones(len(X_ttcc))
    X_ttbb = rootnp.root2array(args.infile,"tree",var,"event_Category_VisiblePS == 0")
    #X_ttbb = rootnp.rec2array(X_ttbb)
    Y_ttbb = np.zeros(len(X_ttbb))
    X = np.concatenate((X_ttcc,X_ttbb))
    Y = np.concatenate((Y_ttcc,Y_ttbb))
    fpr, tpr, thres = roc_curve( Y,X)
    random_indices = np.sort([np.where(fpr==i)[0][0] for i in random.sample(fpr, 200)])
    fpr = fpr[random_indices] 
    tpr = tpr[random_indices] 
    auc = 1.-roc_auc_score( Y,X)
    if auc > 0.5:
        # Other side of the diagonal
        fpr = np.asarray([1.-i for i in fpr])
        tpr = np.asarray([1.-i for i in tpr])
        auc = 1.-auc
    roc_ttcc_vs_ttbb_dict[var] = ROOT.TGraph(len(fpr),tpr,fpr)
    roc_ttcc_vs_ttbb_dict[var].SetLineColor(opt[1])
    roc_ttcc_vs_ttbb_dict[var].SetLineStyle(opt[2])
    roc_ttcc_vs_ttbb_dict[var].SetLineWidth(2)
    mg_ttcc_vs_ttbb.Add(roc_ttcc_vs_ttbb_dict[var])
    l_ttcc_vs_ttbb.AddEntry(roc_ttcc_vs_ttbb_dict[var],opt[0] + " (AUC=%.2f)"%auc,"l")
    
c_ttcc_vs_ttbb = ROOT.TCanvas("c_ttcc_vs_ttbb","c_ttcc_vs_ttbb",1000,550)
ROOT.gPad.SetMargin(0.1,0.45,0.15,0.02)
mg_ttcc_vs_ttbb.Draw("AL")
mg_ttcc_vs_ttbb.GetXaxis().SetRangeUser(0.,1.)
#mg_ttcc_vs_ttbb.GetXaxis().SetNdivisions(405)
mg_ttcc_vs_ttbb.GetXaxis().SetTitle("t#bar{t}c#bar{c} efficiency")
mg_ttcc_vs_ttbb.GetXaxis().SetTitleSize(0.055)
mg_ttcc_vs_ttbb.GetXaxis().SetTitleOffset(1.)
mg_ttcc_vs_ttbb.GetXaxis().CenterTitle()
mg_ttcc_vs_ttbb.GetYaxis().SetNdivisions(405)
mg_ttcc_vs_ttbb.GetYaxis().SetTitle("t#bar{t}b#bar{b} efficiency")
mg_ttcc_vs_ttbb.GetYaxis().SetTitleSize(0.055)
mg_ttcc_vs_ttbb.GetYaxis().SetTitleOffset(0.95)
mg_ttcc_vs_ttbb.GetYaxis().CenterTitle()
mg_ttcc_vs_ttbb.SetMinimum(0.0)
mg_ttcc_vs_ttbb.SetMaximum(1.0)
l_ttcc_vs_ttbb.Draw("same")
latex_cms = ROOT.TLatex()
latex_cms.SetTextFont(42)
latex_cms.SetTextSize(0.055)
latex_cms.SetTextAlign(11)
latex_cms.DrawLatexNDC(0.13,0.92,"#bf{CMS} #it{Simulation}")
c_ttcc_vs_ttbb.SaveAs("./ROCs_ttcc_vs_ttbb.pdf")

#
# ttcc vs ttLF
#
roc_ttcc_vs_ttlf_dict = {}
mg_ttcc_vs_ttlf = ROOT.TMultiGraph("mg_ttcc_vs_ttlf","")
l_ttcc_vs_ttlf = ROOT.TLegend(0.56,0.15,0.99,0.97)
l_ttcc_vs_ttlf.SetBorderSize(0)
for idx, item_dict in variables.iteritems():
    var = item_dict["name"]
    opt = item_dict["opt"]
    X_ttcc = rootnp.root2array(args.infile,"tree",var,"event_Category_VisiblePS == 2")
    #X_ttcc = rootnp.rec2array(X_ttcc)
    Y_ttcc = np.ones(len(X_ttcc))
    X_ttlf = rootnp.root2array(args.infile,"tree",var,"event_Category_VisiblePS == 4")
    #X_ttlf = rootnp.rec2array(X_ttlf)
    Y_ttlf = np.zeros(len(X_ttlf))
    X = np.concatenate((X_ttcc,X_ttlf))
    Y = np.concatenate((Y_ttcc,Y_ttlf))
    fpr, tpr, thres = roc_curve( Y,X)
    random_indices = np.sort([np.where(fpr==i)[0][0] for i in random.sample(fpr, 200)])
    fpr = fpr[random_indices] 
    tpr = tpr[random_indices] 
    auc = 1.-roc_auc_score( Y,X)
    if auc > 0.5:
        # Other side of the diagonal
        fpr = np.asarray([1.-i for i in fpr])
        tpr = np.asarray([1.-i for i in tpr])
        auc = 1.-auc
    roc_ttcc_vs_ttlf_dict[var] = ROOT.TGraph(len(fpr),tpr,fpr)
    roc_ttcc_vs_ttlf_dict[var].SetLineColor(opt[1])
    roc_ttcc_vs_ttlf_dict[var].SetLineStyle(opt[2])
    roc_ttcc_vs_ttlf_dict[var].SetLineWidth(2)
    mg_ttcc_vs_ttlf.Add(roc_ttcc_vs_ttlf_dict[var])
    l_ttcc_vs_ttlf.AddEntry(roc_ttcc_vs_ttlf_dict[var],opt[0] + " (AUC=%.2f)"%auc,"l")
    
c_ttcc_vs_ttlf = ROOT.TCanvas("c_ttcc_vs_ttlf","c_ttcc_vs_ttlf",1000,550)
ROOT.gPad.SetMargin(0.1,0.45,0.15,0.02)
mg_ttcc_vs_ttlf.Draw("AL")
mg_ttcc_vs_ttlf.GetXaxis().SetRangeUser(0.,1.)
#mg_ttcc_vs_ttlf.GetXaxis().SetNdivisions(405)
mg_ttcc_vs_ttlf.GetXaxis().SetTitle("t#bar{t}c#bar{c} efficiency")
mg_ttcc_vs_ttlf.GetXaxis().SetTitleSize(0.055)
mg_ttcc_vs_ttlf.GetXaxis().SetTitleOffset(1.)
mg_ttcc_vs_ttlf.GetXaxis().CenterTitle()
mg_ttcc_vs_ttlf.GetYaxis().SetNdivisions(405)
mg_ttcc_vs_ttlf.GetYaxis().SetTitle("t#bar{t}LF efficiency")
mg_ttcc_vs_ttlf.GetYaxis().SetTitleSize(0.055)
mg_ttcc_vs_ttlf.GetYaxis().SetTitleOffset(0.95)
mg_ttcc_vs_ttlf.GetYaxis().CenterTitle()
mg_ttcc_vs_ttlf.SetMinimum(0.0)
mg_ttcc_vs_ttlf.SetMaximum(1.0)
l_ttcc_vs_ttlf.Draw("same")
latex_cms.DrawLatexNDC(0.13,0.92,"#bf{CMS} #it{Simulation}")
c_ttcc_vs_ttlf.SaveAs("./ROCs_ttcc_vs_ttlf.pdf")



# roc_ttcc_vs_ttlf_dict = {}
# mg_ttcc_vs_ttlf = ROOT.TMultiGraph("mg_ttcc_vs_ttlf","")
# for idx, item_dict in variables.iteritems():
#     var = item_dict["name"]
#     opt = item_dict["opt"]
#     X_ttcc = rootnp.root2array(args.infile,"tree",var,"event_Category_VisiblePS == 2")
#     #X_ttcc = rootnp.rec2array(X_ttcc)
#     Y_ttcc = np.ones(len(X_ttcc))
#     X_ttlf = rootnp.root2array(args.infile,"tree",var,"event_Category_VisiblePS == 4")
#     #X_ttlf = rootnp.rec2array(X_ttlf)
#     Y_ttlf = np.zeros(len(X_ttlf))
#     X = np.concatenate((X_ttcc,X_ttlf))
#     Y = np.concatenate((Y_ttcc,Y_ttlf))
#     fpr, tpr, thres = roc_curve( Y,X)
#     random_indices = np.sort([np.where(fpr==i)[0][0] for i in random.sample(fpr, 200)])
#     fpr = fpr[random_indices] 
#     tpr = tpr[random_indices] 
#     auc = 1.-roc_auc_score( Y,X)
#     if auc > 0.5:
#         # Other side of the diagonal
#         fpr = np.asarray([1.-i for i in fpr])
#         tpr = np.asarray([1.-i for i in tpr])
#     roc_ttcc_vs_ttlf_dict[var] = ROOT.TGraph(len(fpr),tpr,fpr)
#     roc_ttcc_vs_ttlf_dict[var].SetLineColor(opt[1])
#     roc_ttcc_vs_ttlf_dict[var].SetLineStyle(opt[2])
#     roc_ttcc_vs_ttlf_dict[var].SetLineWidth(2)
#     mg_ttcc_vs_ttlf.Add(roc_ttcc_vs_ttlf_dict[var])
#     
# c_ttcc_vs_ttlf = ROOT.TCanvas("c_ttcc_vs_ttlf","c_ttcc_vs_ttlf",900,600)
# ROOT.gPad.SetMargin(0.15,0.35,0.15,0.1)
# mg_ttcc_vs_ttlf.Draw("AL")
# c_ttcc_vs_ttlf.SaveAs("./ROCs_ttcc_vs_ttlf.pdf")
    
    