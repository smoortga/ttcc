from ROOT import TFile, TTree, TChain, TCanvas, TH1D, TLegend, gROOT, gStyle, TPad, gPad, TGraph, TMultiGraph, TLatex
import sys
import ROOT
import os
import time
from argparse import ArgumentParser
from array import array
from math import *
import numpy as np
from collections import Counter
import root_numpy as rootnp
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.utils import np_utils
from keras.callbacks import EarlyStopping, ModelCheckpoint, LearningRateScheduler
from keras.optimizers import SGD,Adam
from keras.regularizers import l1, l2
from numpy.lib.recfunctions import stack_arrays
from sklearn.preprocessing import StandardScaler
from keras.models import load_model
from sklearn.metrics import roc_curve,roc_auc_score
from sklearn.cross_validation import train_test_split
import pickle
from rootpy.plotting import Hist

parser = ArgumentParser()
parser.add_argument('--trainingdir', default = "", help='path to training directory')
parser.add_argument('--outdir', default = "DecisionBoundaryPlot", help='output directory')
args = parser.parse_args()

model = load_model(args.trainingdir+"/model_checkpoint_save.hdf5")
scaler = pickle.load(open(args.trainingdir+"/scaler.pkl","rb"))
input_variables = pickle.load(open(args.trainingdir+"/variables.pkl","rb"))

x_min=0
x_max=1
step=0.05

CvsL1,CvsB1,CvsL2,CvsB2 = np.meshgrid(np.arange(x_min, x_max, step),np.arange(x_min, x_max, step),np.arange(x_min, x_max, step),np.arange(x_min, x_max, step)) 
X = np.c_[CvsL1.ravel(), CvsB1.ravel(), CvsL2.ravel(), CvsB2.ravel()]
XX = scaler.transform(X)
Y = model.predict(XX)
#print Y



# First Additional Jet
CvsL1_ = X[:,0]
CvsB1_ = X[:,1]
output_dict={}
for i in range(len(CvsL1_)):
    if not CvsL1_[i] in output_dict.keys():
        output_dict[CvsL1_[i]]={}
        output_dict[CvsL1_[i]][CvsB1_[i]] = Y[i][0]+Y[i][1]
    elif not CvsB1_[i] in output_dict[CvsL1_[i]].keys():
        output_dict[CvsL1_[i]][CvsB1_[i]] = Y[i][0]+Y[i][1]
    else:
        output_dict[CvsL1_[i]][CvsB1_[i]] = (output_dict[CvsL1_[i]][CvsB1_[i]]+(Y[i][0]+Y[i][1]))/2.

xx, yy = np.meshgrid(np.arange(x_min, x_max, step),
                         np.arange(x_min, x_max, step))

zz = np.asarray([output_dict[i][j] for i,j in zip(xx.ravel(), yy.ravel())])
CS = plt.contourf(xx, yy, zz.reshape(xx.shape),15, linewidth=5,cmap=plt.cm.plasma_r,alpha=0.5)
CS2 = plt.contour(xx, yy, zz.reshape(xx.shape),15, linewidth=5,colors="k")#cmap=plt.cm.plasma_r)
plt.clabel(CS2, inline=1, fontsize=20)
plt.xlabel('DeepCSV CvsL first add. jet',size=20)
plt.ylabel('DeepCSV CvsB first add. jet',size=20)
if not os.path.isdir(args.outdir): os.mkdir(args.outdir)
plt.savefig(args.outdir+"/ContourFirstAddJet.pdf")

plt.clf()



# Second Additional Jet
CvsL2_ = X[:,2]
CvsB2_ = X[:,3]
output_dict={}
for i in range(len(CvsL2_)):
    if not CvsL2_[i] in output_dict.keys():
        output_dict[CvsL2_[i]]={}
        output_dict[CvsL2_[i]][CvsB2_[i]] = Y[i][0]+Y[i][1]
    elif not CvsB2_[i] in output_dict[CvsL2_[i]].keys():
        output_dict[CvsL2_[i]][CvsB2_[i]] = Y[i][0]+Y[i][1]
    else:
        output_dict[CvsL2_[i]][CvsB2_[i]] = (output_dict[CvsL2_[i]][CvsB2_[i]]+(Y[i][0]+Y[i][1]))/2.

xx, yy = np.meshgrid(np.arange(x_min, x_max, step),
                         np.arange(x_min, x_max, step))

zz = np.asarray([output_dict[i][j] for i,j in zip(xx.ravel(), yy.ravel())])

CS = plt.contourf(xx, yy, zz.reshape(xx.shape),15, linewidth=5,cmap=plt.cm.plasma_r,alpha=0.5)
CS2 = plt.contour(xx, yy, zz.reshape(xx.shape),15, linewidth=5,colors="k")#cmap=plt.cm.plasma_r)
plt.clabel(CS2, inline=1, fontsize=20)
plt.xlabel('DeepCSV CvsL second add. jet',size=20)
plt.ylabel('DeepCSV CvsB second add. jet',size=20)
plt.savefig(args.outdir+"/ContourSecondAddJet.pdf")




