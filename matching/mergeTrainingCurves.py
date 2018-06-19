from ROOT import TFile, TTree, TChain, TCanvas, TH1D, TLegend, gROOT, gStyle, TPad, gPad, TGraph, TMultiGraph, TLatex
import sys
import os
import pickle
from argparse import ArgumentParser
from array import array
from math import *
import numpy as np

def drawTrainingCurve(input,output):
    hist = pickle.load(open(input,"rb"))
    tr_acc = hist["acc"]
    tr_loss = hist["loss"]
    val_acc = hist["val_acc"]
    val_loss = hist["val_loss"]
    epochs = range(len(tr_acc))
    
    c = TCanvas("c","c",800,500)
    #c.SetFillStyle(4000)
    #c.SetFrameFillStyle(4000)
    gStyle.SetOptStat(0)
    uppad = TPad("u","u",0.,0.55,1.,1.)
    downpad = TPad("d","d",0.,0.,1.,0.55)
    uppad.Draw()
    #uppad.SetFillStyle(4000)
    #uppad.SetFrameFillStyle(4000)
    downpad.Draw()
    #downpad.SetFillStyle(4000)
    #downpad.SetFrameFillStyle(4000)
    uppad.cd()
    gPad.SetMargin(0.15,0.05,0.02,0.15)
    gPad.SetGrid(1,1)
    gStyle.SetGridColor(13)
    
    gr_acc_train = TGraph(len(epochs),array('d',epochs),array('d',tr_acc))
    gr_acc_train.SetLineColor(2)
    gr_acc_train.SetLineWidth(2)
    gr_acc_test = TGraph(len(epochs),array('d',epochs),array('d',val_acc))
    gr_acc_test.SetLineColor(4)
    gr_acc_test.SetLineWidth(2)
    
    mgup = TMultiGraph("mgup",";number of epochs;accuracy")
    mgup.Add(gr_acc_train,"l")
    mgup.Add(gr_acc_test,"l")
    mgup.Draw("AL")
    mgup.GetXaxis().SetRangeUser(min(epochs),max(epochs))
    mgup.GetXaxis().SetLabelSize(0)
    mgup.GetYaxis().CenterTitle()
    mgup.GetYaxis().SetTitleSize(0.12)
    mgup.GetYaxis().SetTitleOffset(0.5)
    mgup.GetYaxis().SetLabelSize(0.105)
    mgup.GetYaxis().SetNdivisions(8)
    
    l = TLegend(0.6,0.15,0.88,0.6)
    l.SetTextSize(0.14)
    l.AddEntry(gr_acc_train,"training","l")
    l.AddEntry(gr_acc_test,"validation","l")
    l.Draw("same")
    
    downpad.cd()
    gPad.SetMargin(0.15,0.05,0.25,0.02)
    gPad.SetGrid(1,1)
    gStyle.SetGridColor(13)
    
    gr_loss_train = TGraph(len(epochs),array('d',epochs),array('d',tr_loss))
    gr_loss_train.SetLineColor(2)
    gr_loss_train.SetLineWidth(2)
    gr_loss_test = TGraph(len(epochs),array('d',epochs),array('d',val_loss))
    gr_loss_test.SetLineColor(4)
    gr_loss_test.SetLineWidth(2)
    
    mgdown = TMultiGraph("mgdown",";number of epochs;loss")
    mgdown.Add(gr_loss_train,"l")
    mgdown.Add(gr_loss_test,"l")
    mgdown.Draw("AL")
    mgdown.GetXaxis().SetRangeUser(min(epochs),max(epochs))
    mgdown.GetXaxis().SetLabelSize(0.085)
    mgdown.GetXaxis().SetTitleSize(0.11)
    mgdown.GetXaxis().SetTitleOffset(0.9)
    mgdown.GetXaxis().CenterTitle()
    mgdown.GetYaxis().CenterTitle()
    mgdown.GetYaxis().SetTitleSize(0.11)
    mgdown.GetYaxis().SetTitleOffset(0.55)
    mgdown.GetYaxis().SetLabelSize(0.085)
    mgdown.GetYaxis().SetNdivisions(8)
    
    c.SaveAs(output)

def main():
    
    gROOT.SetBatch(1)
    
    parser = ArgumentParser()
    parser.add_argument('--indir', default = os.getcwd(), help='directory where the training acc_and_loss.pkl files are located')
    args = parser.parse_args()
    
    files = [i for i in os.listdir(args.indir) if "loss_and_acc" in i]
    f1_name = 'loss_and_acc_phase1.pkl'
    f2_name = 'loss_and_acc_phase2.pkl'
    f3_name = 'loss_and_acc_contd.pkl'
    f4_name = 'loss_and_acc_contd2.pkl'
    f1 = pickle.load(open(args.indir+"/"+f1_name,"rb"))
    if f2_name in files: f2 = pickle.load(open(args.indir+"/"+f2_name,"rb"))
    if f3_name in files: f3 = pickle.load(open(args.indir+"/"+f3_name,"rb"))
    if f4_name in files: f4 = pickle.load(open(args.indir+"/"+f4_name,"rb"))
    
    if f2_name in files: f1['acc'] += f2['acc']
    if f3_name in files: f1['acc'] += f3['acc']
    if f4_name in files: f1['acc'] += f4['acc']
    if f2_name in files: f1['loss'] += f2['loss']
    if f3_name in files: f1['loss'] += f3['loss']
    if f4_name in files: f1['loss'] += f4['loss']
    if f2_name in files: f1['val_acc'] += f2['val_acc']
    if f3_name in files: f1['val_acc'] += f3['val_acc']
    if f4_name in files: f1['val_acc'] += f4['val_acc']
    if f2_name in files: f1['val_loss'] += f2['val_loss']
    if f3_name in files: f1['val_loss'] += f3['val_loss']
    if f4_name in files: f1['val_loss'] += f4['val_loss']
    
    pickle.dump(f1,open(args.indir+"/loss_and_acc_merged.pkl","wb"))
    drawTrainingCurve(args.indir+"/loss_and_acc_merged.pkl",args.indir+"/training_curve_merged.pdf")

if __name__ == "__main__":
    main()