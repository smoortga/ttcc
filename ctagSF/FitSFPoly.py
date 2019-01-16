import ROOT
import os
import sys
from argparse import ArgumentParser
from math import sqrt
import numpy as np
#from scipy.optimize import fmin,fminbound,minimize,brentq,ridder,fsolve
from binning import *
from array import array
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetOptStat(0)

parser = ArgumentParser()
parser.add_argument('--indir', default="FILL",help='input directory that contains all the Histograms with syst variations')
#parser.add_argument('--ApplyBiasUnc', action='store_true', help='Apply the bias Unc')
args = parser.parse_args()

basedir = args.indir
subdirs = [i for i in os.listdir(basedir) if os.path.isdir(basedir+"/"+i)]
centraldir = [i for i in subdirs if "central" in i][0]
systdirs = [i for i in subdirs if not "central" in i and not "Bias" in i]
biasdirs = [i for i in subdirs if "Bias" in i]


x = custom_bins_CvsL_jet1
x = [x[idx] + (x[idx+1]-x[idx])/2. for idx in range(len(x)-1)] #Get bin centers
y = custom_bins_CvsB_jet1
y = [y[idx] + (y[idx+1]-y[idx])/2. for idx in range(len(y)-1)]
X, Y = np.meshgrid(x, y, copy=False)
print X,Y
Z = X**2 + Y**2 #Just dummy as container!!
print Z

central_SF_file = ROOT.TFile(basedir+"/"+centraldir+"/DeepCSV_cTag_SFs_94X.root","update")
histos_names = [i.GetName() for i in central_SF_file.GetListOfKeys()]
print histos_names

results_dict = {
    "central":{"SFb":{},"SFc":{},"SFl":{}},
    "Up": {"SFb":{},"SFc":{},"SFl":{}},
    "Down":{"SFb":{},"SFc":{},"SFl":{}}
}

for hist_name in histos_names:
    print hist_name
    if not("central" in hist_name or "_Down" in hist_name or "_Up" in hist_name): continue
    flav = hist_name.split("_")[0]
    syst = hist_name.split("_")[-1]
    hist_ = central_SF_file.Get(hist_name)
    for binx in range(hist_.GetNbinsX()):
        for biny in range(hist_.GetNbinsY()):
            Z[binx][biny] = hist_.GetBinContent(binx+1,biny+1)
    print Z
    X_ = X.flatten()
    Y_ = Y.flatten()

    A = np.array([X_*0+1, X_, Y_, X_**2, Y_**2, X_*Y_, X_**2*Y_,X_*Y_**2, X_**3, Y_**3]).T
    B = Z.flatten()
    coeff, r, rank, s = np.linalg.lstsq(A, B)
    print coeff
    
    xx = np.arange(0,1,0.1)
    yy = np.arange(0,1,0.1)
    XX, YY = np.meshgrid(xx, yy, copy=False)
    XX_ = XX.flatten()
    YY_ = YY.flatten()
    ZZ = np.dot(np.c_[np.ones(XX_.shape), XX_, YY_, XX_**2, YY_**2, XX_*YY_, XX_**2*YY_,XX_*YY_**2, XX_**3, YY_**3], coeff).reshape(XX.shape)
    
    results_dict[syst][flav]["values"] = Z
    results_dict[syst][flav]["smooth"] = ZZ
    
    # fig = plt.figure()
#     ax = fig.add_subplot(111, projection='3d')
#     ax.plot_surface(XX, YY, ZZ, rstride=1, cstride=1, alpha=0.3)
#     ax.scatter(X, Y, Z, c='r')
#     plt.xlabel('X')
#     plt.ylabel('Y')
#     plt.show()
#     plt.clf()

for fl in ["SFb","SFc","SFl"]:
    print fl 
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(XX, YY, results_dict["Up"][fl]["smooth"], rstride=1, cstride=1, alpha=0.3)
    ax.plot_surface(XX, YY, results_dict["Down"][fl]["smooth"], rstride=1, cstride=1, alpha=0.3)
    ax.scatter(X, Y, results_dict["central"][fl]["values"], c='r')
    #ax.scatter(X, Y, results_dict["Up"][fl]["values"], c='g')
    #ax.scatter(X, Y, results_dict["Down"][fl]["values"], c='b')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()
  
    plt.clf()


                
