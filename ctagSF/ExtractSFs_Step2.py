import ROOT
import os
import sys
from argparse import ArgumentParser
from math import sqrt
import pickle
import numpy as np
from scipy.optimize import fmin,fminbound,minimize,brentq,ridder,fsolve
from copy import deepcopy
from binning import *
from array import array
import matplotlib.pyplot as plt

ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetOptStat(0)

parser = ArgumentParser()
parser.add_argument('--indir', default="FILL",help='input directory that contains all the Histograms with syst variations')
#parser.add_argument('--NormalizeMCToData', default=True,help='Normalize Data-to-MC')
parser.add_argument('--NormalizeMCToData', action='store_true', help='skip new features')
args = parser.parse_args()

basedir = args.indir
subdirs = [i for i in os.listdir(basedir) if os.path.isdir(basedir+"/"+i)]


#****************************************************
#
# DERIVE TOTAL UNCERTAINTY FROM TEMPLATES TO BE USED IN CHI2 CALCULATION
#
#****************************************************

syst_dirs = [i for i in subdirs if not "central" in i]
central_dir = [i for i in subdirs if "central" in i]

histo_dict_uncPositive = {}
histo_dict_uncPositive["jet1"] = {
    "b" : ROOT.TH2D("b1_uncPositive",";DeepCSV CvsL first jet;DeepCSV CvsB first jet;Events",nbins_CvsL_jet1,array("d",custom_bins_CvsL_jet1),nbins_CvsB_jet1,array("d",custom_bins_CvsB_jet1)),
    "c" : ROOT.TH2D("c1_uncPositive",";DeepCSV CvsL first jet;DeepCSV CvsB first jet;Events",nbins_CvsL_jet1,array("d",custom_bins_CvsL_jet1),nbins_CvsB_jet1,array("d",custom_bins_CvsB_jet1)),
    "l" : ROOT.TH2D("l1_uncPositive",";DeepCSV CvsL first jet;DeepCSV CvsB first jet;Events",nbins_CvsL_jet1,array("d",custom_bins_CvsL_jet1),nbins_CvsB_jet1,array("d",custom_bins_CvsB_jet1)),
}
histo_dict_uncPositive["jet2"] = {
    "b" : ROOT.TH2D("b2_uncPositive",";DeepCSV CvsL second jet;DeepCSV CvsB second jet;Events",nbins_CvsL_jet2,array("d",custom_bins_CvsL_jet2),nbins_CvsB_jet2,array("d",custom_bins_CvsB_jet2)),
    "c" : ROOT.TH2D("c2_uncPositive",";DeepCSV CvsL second jet;DeepCSV CvsB second jet;Events",nbins_CvsL_jet2,array("d",custom_bins_CvsL_jet2),nbins_CvsB_jet2,array("d",custom_bins_CvsB_jet2)),
    "l" : ROOT.TH2D("l2_uncPositive",";DeepCSV CvsL second jet;DeepCSV CvsB second jet;Events",nbins_CvsL_jet2,array("d",custom_bins_CvsL_jet2),nbins_CvsB_jet2,array("d",custom_bins_CvsB_jet2)),
}
histo_dict_uncPositive["jet3"] = {
    "b" : ROOT.TH2D("b3_uncPositive",";DeepCSV CvsL third jet;DeepCSV CvsB third jet;Events",nbins_CvsL_jet3,array("d",custom_bins_CvsL_jet3),nbins_CvsB_jet3,array("d",custom_bins_CvsB_jet3)),
    "c" : ROOT.TH2D("c3_uncPositive",";DeepCSV CvsL third jet;DeepCSV CvsB third jet;Events",nbins_CvsL_jet3,array("d",custom_bins_CvsL_jet3),nbins_CvsB_jet3,array("d",custom_bins_CvsB_jet3)),
    "l" : ROOT.TH2D("l3_uncPositive",";DeepCSV CvsL third jet;DeepCSV CvsB third jet;Events",nbins_CvsL_jet3,array("d",custom_bins_CvsL_jet3),nbins_CvsB_jet3,array("d",custom_bins_CvsB_jet3)),
}

histo_dict_uncNegative = {}
histo_dict_uncNegative["jet1"] = {
    "b" : ROOT.TH2D("b1_uncNegative",";DeepCSV CvsL first jet;DeepCSV CvsB first jet;Events",nbins_CvsL_jet1,array("d",custom_bins_CvsL_jet1),nbins_CvsB_jet1,array("d",custom_bins_CvsB_jet1)),
    "c" : ROOT.TH2D("c1_uncNegative",";DeepCSV CvsL first jet;DeepCSV CvsB first jet;Events",nbins_CvsL_jet1,array("d",custom_bins_CvsL_jet1),nbins_CvsB_jet1,array("d",custom_bins_CvsB_jet1)),
    "l" : ROOT.TH2D("l1_uncNegative",";DeepCSV CvsL first jet;DeepCSV CvsB first jet;Events",nbins_CvsL_jet1,array("d",custom_bins_CvsL_jet1),nbins_CvsB_jet1,array("d",custom_bins_CvsB_jet1)),
}
histo_dict_uncNegative["jet2"] = {
    "b" : ROOT.TH2D("b2_uncNegative",";DeepCSV CvsL second jet;DeepCSV CvsB second jet;Events",nbins_CvsL_jet2,array("d",custom_bins_CvsL_jet2),nbins_CvsB_jet2,array("d",custom_bins_CvsB_jet2)),
    "c" : ROOT.TH2D("c2_uncNegative",";DeepCSV CvsL second jet;DeepCSV CvsB second jet;Events",nbins_CvsL_jet2,array("d",custom_bins_CvsL_jet2),nbins_CvsB_jet2,array("d",custom_bins_CvsB_jet2)),
    "l" : ROOT.TH2D("l2_uncNegative",";DeepCSV CvsL second jet;DeepCSV CvsB second jet;Events",nbins_CvsL_jet2,array("d",custom_bins_CvsL_jet2),nbins_CvsB_jet2,array("d",custom_bins_CvsB_jet2)),
}
histo_dict_uncNegative["jet3"] = {
    "b" : ROOT.TH2D("b3_uncNegative",";DeepCSV CvsL third jet;DeepCSV CvsB third jet;Events",nbins_CvsL_jet3,array("d",custom_bins_CvsL_jet3),nbins_CvsB_jet3,array("d",custom_bins_CvsB_jet3)),
    "c" : ROOT.TH2D("c3_uncNegative",";DeepCSV CvsL third jet;DeepCSV CvsB third jet;Events",nbins_CvsL_jet3,array("d",custom_bins_CvsL_jet3),nbins_CvsB_jet3,array("d",custom_bins_CvsB_jet3)),
    "l" : ROOT.TH2D("l3_uncNegative",";DeepCSV CvsL third jet;DeepCSV CvsB third jet;Events",nbins_CvsL_jet3,array("d",custom_bins_CvsL_jet3),nbins_CvsB_jet3,array("d",custom_bins_CvsB_jet3)),
}

histo_dict_uncTotal = {}
histo_dict_uncTotal["jet1"] = {
    "b" : ROOT.TH2D("b1_uncTotal",";DeepCSV CvsL first jet;DeepCSV CvsB first jet;Events",nbins_CvsL_jet1,array("d",custom_bins_CvsL_jet1),nbins_CvsB_jet1,array("d",custom_bins_CvsB_jet1)),
    "c" : ROOT.TH2D("c1_uncTotal",";DeepCSV CvsL first jet;DeepCSV CvsB first jet;Events",nbins_CvsL_jet1,array("d",custom_bins_CvsL_jet1),nbins_CvsB_jet1,array("d",custom_bins_CvsB_jet1)),
    "l" : ROOT.TH2D("l1_uncTotal",";DeepCSV CvsL first jet;DeepCSV CvsB first jet;Events",nbins_CvsL_jet1,array("d",custom_bins_CvsL_jet1),nbins_CvsB_jet1,array("d",custom_bins_CvsB_jet1)),
}
histo_dict_uncTotal["jet2"] = {
    "b" : ROOT.TH2D("b2_uncTotal",";DeepCSV CvsL second jet;DeepCSV CvsB second jet;Events",nbins_CvsL_jet2,array("d",custom_bins_CvsL_jet2),nbins_CvsB_jet2,array("d",custom_bins_CvsB_jet2)),
    "c" : ROOT.TH2D("c2_uncTotal",";DeepCSV CvsL second jet;DeepCSV CvsB second jet;Events",nbins_CvsL_jet2,array("d",custom_bins_CvsL_jet2),nbins_CvsB_jet2,array("d",custom_bins_CvsB_jet2)),
    "l" : ROOT.TH2D("l2_uncTotal",";DeepCSV CvsL second jet;DeepCSV CvsB second jet;Events",nbins_CvsL_jet2,array("d",custom_bins_CvsL_jet2),nbins_CvsB_jet2,array("d",custom_bins_CvsB_jet2)),
}
histo_dict_uncTotal["jet3"] = {
    "b" : ROOT.TH2D("b3_uncTotal",";DeepCSV CvsL third jet;DeepCSV CvsB third jet;Events",nbins_CvsL_jet3,array("d",custom_bins_CvsL_jet3),nbins_CvsB_jet3,array("d",custom_bins_CvsB_jet3)),
    "c" : ROOT.TH2D("c3_uncTotal",";DeepCSV CvsL third jet;DeepCSV CvsB third jet;Events",nbins_CvsL_jet3,array("d",custom_bins_CvsL_jet3),nbins_CvsB_jet3,array("d",custom_bins_CvsB_jet3)),
    "l" : ROOT.TH2D("l3_uncTotal",";DeepCSV CvsL third jet;DeepCSV CvsB third jet;Events",nbins_CvsL_jet3,array("d",custom_bins_CvsL_jet3),nbins_CvsB_jet3,array("d",custom_bins_CvsB_jet3)),
}

# SFb_hist = ROOT.TH2D("SFb_hist",";CvsL;CvsB;SFb",nbins_CvsL_jet1,array("d",custom_bins_CvsL_jet1),nbins_CvsB_jet1,array("d",custom_bins_CvsB_jet1))
# SFc_hist = ROOT.TH2D("SFc_hist",";CvsL;CvsB;SFc",nbins_CvsL_jet2,array("d",custom_bins_CvsL_jet2),nbins_CvsB_jet2,array("d",custom_bins_CvsB_jet2))
# SFl_hist = ROOT.TH2D("SFl_hist",";CvsL;CvsB;SFl",nbins_CvsL_jet3,array("d",custom_bins_CvsL_jet3),nbins_CvsB_jet3,array("d",custom_bins_CvsB_jet3))


central_MC_histo_dict = pickle.load(open(basedir+"/"+central_dir[0]+"/MC_histograms2D.pkl","rb"))

# First initialize the Up and Down systematics histos with statistical uncertainties
for jet, flavor_dict in histo_dict_uncPositive.iteritems():
        for flav, hist in flavor_dict.iteritems():
            for binx in range(hist.GetNbinsX()):
                for biny in range(hist.GetNbinsY()):
                    if central_MC_histo_dict[jet][flav].GetBinContent(binx+1,biny+1) >= 0 :
                        stat_unc = sqrt(central_MC_histo_dict[jet][flav].GetBinContent(binx+1,biny+1))
                    else: 
                        stat_unc = 1
                    histo_dict_uncPositive[jet][flav].SetBinContent(binx+1,biny+1,stat_unc)
                    histo_dict_uncNegative[jet][flav].SetBinContent(binx+1,biny+1,stat_unc)


for systdir in syst_dirs:
    print "Processing: %s"%systdir
    dict_tmp  = pickle.load(open(basedir+"/"+systdir+"/MC_histograms2D.pkl","rb"))
    for jet, flavor_dict in dict_tmp.iteritems():
        for flav, hist in flavor_dict.iteritems():
            syst_histo = hist
            central_histo = central_MC_histo_dict[jet][flav]
            diff_hist = syst_histo.Clone()
            diff_hist.Add(central_histo,-1)
            for binx in range(diff_hist.GetNbinsX()):
                for biny in range(diff_hist.GetNbinsY()):
                    if diff_hist.GetBinContent(binx+1,biny+1) > 0: 
                        old_unc = histo_dict_uncPositive[jet][flav].GetBinContent(binx+1,biny+1)
                        histo_dict_uncPositive[jet][flav].SetBinContent(binx+1,biny+1,sqrt(old_unc**2 + diff_hist.GetBinContent(binx+1,biny+1)**2))
                    elif diff_hist.GetBinContent(binx+1,biny+1) < 0: 
                        old_unc = histo_dict_uncNegative[jet][flav].GetBinContent(binx+1,biny+1)
                        histo_dict_uncNegative[jet][flav].SetBinContent(binx+1,biny+1,sqrt(old_unc**2 + diff_hist.GetBinContent(binx+1,biny+1)**2))

# Take a per-bin uncertainty, calculated as the average between the Up and Down total systematic                           
for jet, flavor_dict in histo_dict_uncTotal.iteritems():
    for flav, hist in flavor_dict.iteritems(): 
        for binx in range(hist.GetNbinsX()):
            for biny in range(hist.GetNbinsY()):
                Positive_content = histo_dict_uncPositive[jet][flav].GetBinContent(binx+1,biny+1)
                Negative_content = histo_dict_uncNegative[jet][flav].GetBinContent(binx+1,biny+1)
                #print Positive_content,Negative_content
                hist.SetBinContent(binx+1,biny+1,np.mean([Positive_content,Negative_content]))    
                if central_MC_histo_dict[jet][flav].GetBinContent(binx+1,biny+1) != 0: print  binx+1,biny+1, np.mean([Positive_content,Negative_content])/float(central_MC_histo_dict[jet][flav].GetBinContent(binx+1,biny+1))


#****************************************************
#
# For each of the systematics, do the entire SF calculation
#
#****************************************************



for directory in [i for i in subdirs]:
    current_dir=basedir+"/"+directory
    histo_dict = pickle.load(open(current_dir+"/MC_histograms2D.pkl","rb"))
    datahisto_dict = pickle.load(open(current_dir+"/Data_histograms2D.pkl","rb"))
    
    for jet,flav_dict in histo_dict.iteritems():
            for flav,hist in flav_dict.iteritems():
                print hist.Integral()
    
    if args.NormalizeMCToData:
        scale = float(datahisto_dict["jet1"].Integral()) / float(histo_dict["jet1"]["b"].Integral() + histo_dict["jet1"]["c"].Integral() + histo_dict["jet1"]["l"].Integral())
        print "Renomalize MC to data with scaleing factor: %.3f"%scale
        for jet,flav_dict in histo_dict.iteritems():
            for flav,hist in flav_dict.iteritems():
                hist.Scale(scale)
    
    for jet,flav_dict in histo_dict.iteritems():
            for flav,hist in flav_dict.iteritems():
                print hist.Integral()
    
    
    convergence_dict = {}
    SFb_hist = ROOT.TH2D("SFb_hist_"+directory,";CvsL;CvsB;SFb",nbins_CvsL_jet1,array("d",custom_bins_CvsL_jet1),nbins_CvsB_jet1,array("d",custom_bins_CvsB_jet1))
    SFc_hist = ROOT.TH2D("SFc_hist_"+directory,";CvsL;CvsB;SFc",nbins_CvsL_jet2,array("d",custom_bins_CvsL_jet2),nbins_CvsB_jet2,array("d",custom_bins_CvsB_jet2))
    SFl_hist = ROOT.TH2D("SFl_hist_"+directory,";CvsL;CvsB;SFl",nbins_CvsL_jet3,array("d",custom_bins_CvsL_jet3),nbins_CvsB_jet3,array("d",custom_bins_CvsB_jet3))
    
    fit_unc_dict = {}
    
    for binx in range(histo_dict["jet1"]["b"].GetNbinsX()):
        for biny in range(histo_dict["jet1"]["b"].GetNbinsY()):
        
            convergence_dict[(binx,biny)] = {"SFb":[],"SFc":[],"SFl":[]}
        
            print binx+1,biny+1#,histo_dict["jet1"]["b"].GetBinContent(binx+1,biny+1)
            N_MC_b1 = histo_dict["jet1"]["b"].GetBinContent(binx+1,biny+1)
            N_MC_c1 = histo_dict["jet1"]["c"].GetBinContent(binx+1,biny+1)
            N_MC_l1 = histo_dict["jet1"]["l"].GetBinContent(binx+1,biny+1)
            N_MC_b2 = histo_dict["jet2"]["b"].GetBinContent(binx+1,biny+1)
            N_MC_c2 = histo_dict["jet2"]["c"].GetBinContent(binx+1,biny+1)
            N_MC_l2 = histo_dict["jet2"]["l"].GetBinContent(binx+1,biny+1)
            N_MC_b3 = histo_dict["jet3"]["b"].GetBinContent(binx+1,biny+1)
            N_MC_c3 = histo_dict["jet3"]["c"].GetBinContent(binx+1,biny+1)
            N_MC_l3 = histo_dict["jet3"]["l"].GetBinContent(binx+1,biny+1)
            N_Data_1 = datahisto_dict["jet1"].GetBinContent(binx+1,biny+1)
            N_Data_2 = datahisto_dict["jet2"].GetBinContent(binx+1,biny+1)
            N_Data_3 = datahisto_dict["jet3"].GetBinContent(binx+1,biny+1)
            print "Jet1: Fraction of (b,c,l): (%.3f,%.3f,%.3f)"%(N_MC_b1/(N_MC_b1+N_MC_c1+N_MC_l1),N_MC_c1/(N_MC_b1+N_MC_c1+N_MC_l1),N_MC_l1/(N_MC_b1+N_MC_c1+N_MC_l1))
            print "Jet2: Fraction of (b,c,l): (%.3f,%.3f,%.3f)"%(N_MC_b2/(N_MC_b2+N_MC_c2+N_MC_l2),N_MC_c2/(N_MC_b2+N_MC_c2+N_MC_l2),N_MC_l2/(N_MC_b2+N_MC_c2+N_MC_l2))
            print "Jet3: Fraction of (b,c,l): (%.3f,%.3f,%.3f)"%(N_MC_b3/(N_MC_b3+N_MC_c3+N_MC_l3),N_MC_c3/(N_MC_b3+N_MC_c3+N_MC_l3),N_MC_l3/(N_MC_b3+N_MC_c3+N_MC_l3))
            
            # uncertainty on this bin
            Total_Unc_b1 = histo_dict_uncTotal["jet1"]["b"].GetBinContent(binx+1,biny+1)
            Total_Unc_b2 = histo_dict_uncTotal["jet2"]["b"].GetBinContent(binx+1,biny+1)
            Total_Unc_b3 = histo_dict_uncTotal["jet3"]["b"].GetBinContent(binx+1,biny+1)
            Total_Unc_c1 = histo_dict_uncTotal["jet1"]["c"].GetBinContent(binx+1,biny+1)
            Total_Unc_c2 = histo_dict_uncTotal["jet2"]["c"].GetBinContent(binx+1,biny+1)
            Total_Unc_c3 = histo_dict_uncTotal["jet3"]["c"].GetBinContent(binx+1,biny+1)
            Total_Unc_l1 = histo_dict_uncTotal["jet1"]["l"].GetBinContent(binx+1,biny+1)
            Total_Unc_l2 = histo_dict_uncTotal["jet2"]["l"].GetBinContent(binx+1,biny+1)
            Total_Unc_l3 = histo_dict_uncTotal["jet3"]["l"].GetBinContent(binx+1,biny+1)
            
            inital_guess = np.average([float(N_Data_1)/float(N_MC_b1+N_MC_c1+ N_MC_l1), float(N_Data_2)/float(N_MC_b2+N_MC_c2+ N_MC_l2), float(N_Data_3)/float(N_MC_b3+N_MC_c3+ N_MC_l3)],weights=np.asarray([N_Data_1,N_Data_2,N_Data_3]))
            SFs_result = np.asarray([inital_guess,inital_guess,inital_guess])
        
            convergence_dict[(binx,biny)]["SFb"].append(SFs_result[0])
            convergence_dict[(binx,biny)]["SFc"].append(SFs_result[1])
            convergence_dict[(binx,biny)]["SFl"].append(SFs_result[2])
        
        
            def chi2_b(SFs):
                N_Data_b1 = N_Data_1 - SFs_result[1]*N_MC_c1 - SFs_result[2]*N_MC_l1
                if N_Data_b1<=0: N_Data_b1 = 1
                #return float(pow(SFs[0]*N_MC_b1 -(N_Data_b1) ,2))/float(Total_Unc_b1**2)#  +  frac_b2*float(pow(SFs[0]*N_MC_b2 -(N_Data_b2) ,2))/float(N_Data_b2) +  frac_b3*float(pow(SFs[0]*N_MC_b3 -(N_Data_b3),2))/float(N_Data_b3)
                return float(pow(SFs[0]*N_MC_b1 -(N_Data_b1) ,2))/float(N_Data_1)
                
            def chi2_c(SFs):
                N_Data_c2 = N_Data_2 - SFs_result[0]*N_MC_b2 - SFs_result[2]*N_MC_l2
                if N_Data_c2<=0: N_Data_c2 = 1
                #return float(pow(SFs[1]*N_MC_c2 -(N_Data_c2) ,2))/float(Total_Unc_c2**2)# +  frac_c3*float(pow(SFs[1]*N_MC_c3 -(N_Data_c3) ,2))/float(N_Data_c3)
                return float(pow(SFs[1]*N_MC_c2 -(N_Data_c2) ,2))/float(N_Data_2)
                
            def chi2_l(SFs):
                N_Data_l3 = N_Data_3 - SFs_result[0]*N_MC_b3 - SFs_result[1]*N_MC_c3
                if N_Data_l3<=0: N_Data_l3 = 1
                #return float(pow(SFs[2]*N_MC_l3 -(N_Data_l3) ,2))/float(Total_Unc_l3**2)
                return float(pow(SFs[2]*N_MC_l3 -(N_Data_l3) ,2))/float(N_Data_3)
        
            def chi2(SFs):
    #             return chi2_b(SFs) + chi2_l(SFs)
                return float(pow(SFs[0]*N_MC_b1 + SFs[1]*N_MC_c1 + SFs[2]*N_MC_l1 - N_Data_1,2))/float(N_Data_1)  +  float(pow(SFs[0]*N_MC_b2 + SFs[1]*N_MC_c2 + SFs[2]*N_MC_l2 - N_Data_2,2))/float(N_Data_2)  +  float(pow(SFs[0]*N_MC_b3 + SFs[1]*N_MC_c3 + SFs[2]*N_MC_l3 - N_Data_3,2))/float(N_Data_3) 
                #return float(pow(SFs[0]*N_MC_b1 + SFs[1]*N_MC_c1 + SFs[2]*N_MC_l1 - N_Data_1,2))/float(Total_Unc_b1**2)  +  float(pow(SFs[0]*N_MC_b2 + SFs[1]*N_MC_c2 + SFs[2]*N_MC_l2 - N_Data_2,2))/float(Total_Unc_c2**2)  +  float(pow(SFs[0]*N_MC_b3 + SFs[1]*N_MC_c3 + SFs[2]*N_MC_l3 - N_Data_3,2))/float(Total_Unc_l3**2) 
        
        
            print N_MC_b1,N_MC_c1, N_MC_l1,N_MC_b1+N_MC_c1+ N_MC_l1, N_Data_1
            print N_MC_b2,N_MC_c2, N_MC_l2,N_MC_b2+N_MC_c2+ N_MC_l2, N_Data_2
            print N_MC_b3,N_MC_c3, N_MC_l3,N_MC_b3+N_MC_c3+ N_MC_l3, N_Data_3
        
            print SFs_result
        
            improved = True
            i = 0
            max_niter = 2000
            verbose=False
            while improved:
                if verbose: print "Starting Iter %i"%i
                if verbose: print "INITIAL SFs: ",SFs_result
                if verbose: print "INITIAL Chi2: ",chi2_b(SFs_result),chi2_c(SFs_result),chi2_l(SFs_result)
                previous_SF = deepcopy(SFs_result)
                previous_chi2_b = chi2_b(SFs_result)
                previous_chi2_c = chi2_c(SFs_result)
                previous_chi2_l = chi2_l(SFs_result)
            
                #
                # First optimize SFl
                #
                improved_l = True
                if verbose: print " PROCESSING FLAVOUR: UDSG"
                minimizedSFl = minimize(chi2_l,SFs_result, bounds=np.c_[SFs_result-0.01, SFs_result+0.01])
                if verbose: print "MINIMIZED SF:", minimizedSFl.x
                SFs_result=minimizedSFl.x
                if verbose: print "MINIMIZED CHI2: ", chi2_b(SFs_result),chi2_c(SFs_result),chi2_l(SFs_result)
                if i != 0 and chi2_b(SFs_result)+chi2_c(SFs_result)+chi2_l(SFs_result)  >= previous_chi2_b +previous_chi2_c +previous_chi2_l:
                   SFs_result = previous_SF
                   if verbose: print "TOTAL CHI2 DID NOT IMPROVE!!!"
                   improved_l = False
                else:
                    previous_SF = deepcopy(SFs_result)

                convergence_dict[(binx,biny)]["SFl"].append(SFs_result[2])

                #
                # Then optimize SFb
                #
                improved_b = True
                if verbose: print " PROCESSING FLAVOUR: B"
                minimizedSFb = minimize(chi2_b,SFs_result, bounds=np.c_[SFs_result-0.01, SFs_result+0.01])
                #print minimizedSFb
                if verbose: print "MINIMIZED SF:", minimizedSFb.x
                SFs_result=minimizedSFb.x
                if verbose: print "MINIMIZED CHI2: ", chi2_b(SFs_result),chi2_c(SFs_result),chi2_l(SFs_result)
                if i != 0 and chi2_b(SFs_result)+chi2_c(SFs_result)+chi2_l(SFs_result)  >= previous_chi2_b +previous_chi2_c +previous_chi2_l:
                    SFs_result = previous_SF
                    if verbose: print "TOTAL CHI2 DID NOT IMPROVE!!!"
                    improved_b = False
                else:
                    previous_SF = deepcopy(SFs_result)


                previous_chi2_b = chi2_b(SFs_result)
                previous_chi2_c = chi2_c(SFs_result)
                previous_chi2_l = chi2_l(SFs_result)
            
                convergence_dict[(binx,biny)]["SFb"].append(SFs_result[0])

                #
                # Finally optimize SFc
                #
                improved_c = True
                if verbose: print " PROCESSING FLAVOUR: C"
                minimizedSFc = minimize(chi2_c,SFs_result, bounds=np.c_[SFs_result-0.01, SFs_result+0.01])
                if verbose: print "MINIMIZED SF:", minimizedSFc.x
                SFs_result=minimizedSFc.x
                if verbose: print "MINIMIZED CHI2: ", chi2_b(SFs_result),chi2_c(SFs_result),chi2_l(SFs_result)
                if i != 0 and chi2_b(SFs_result)+chi2_c(SFs_result)+chi2_l(SFs_result)  >= previous_chi2_b +previous_chi2_c +previous_chi2_l:
                    SFs_result = previous_SF
                    if verbose: print "TOTAL CHI2 DID NOT IMPROVE!!!"
                    improved_c = False
                else:
                    previous_SF = deepcopy(SFs_result)

                previous_chi2_b = chi2_b(SFs_result)
                previous_chi2_c = chi2_c(SFs_result)
                previous_chi2_l = chi2_l(SFs_result)
            
                convergence_dict[(binx,biny)]["SFc"].append(SFs_result[1])

            

                if verbose: print "Ending Iter %i"%i,SFs_result, "chi2 = ", chi2_b(SFs_result)+chi2_c(SFs_result)+chi2_l(SFs_result)
                if verbose: print ""
                # if i != 0 and chi2_b(SFs_result[0])+chi2_c(SFs_result[1])+chi2_l(SFs_result[2])  > previous_chi2_b +previous_chi2_c +previous_chi2_l:
    #                 SFs_result = previous_SF
    #                 break

                i+=1
                if i > max_niter: break
                if not improved_b and not improved_c and not improved_l:
                    improved = False
           
            
            print "DONE in %i iterations"%i    
        
            print "FINAL ", SFs_result, "Chi2: ",chi2_b(SFs_result),chi2_c(SFs_result),chi2_l(SFs_result)
            print "Jet1: Corrected # MC: ", SFs_result[0]*N_MC_b1+SFs_result[1]*N_MC_c1+SFs_result[2]*N_MC_l1, "# Data: ", N_Data_1
            print "Jet2: Corrected # MC: ", SFs_result[0]*N_MC_b2+SFs_result[1]*N_MC_c2+SFs_result[2]*N_MC_l2, "# Data: ", N_Data_2
            print "Jet3: Corrected # MC: ", SFs_result[0]*N_MC_b3+SFs_result[1]*N_MC_c3+SFs_result[2]*N_MC_l3, "# Data: ", N_Data_3
            

            
            xvalues_SFb = np.arange(SFs_result[0]-1,SFs_result[0]+1,0.001)
            yvalues_SFb = np.asarray([chi2(np.asarray([i,SFs_result[1],SFs_result[2]])) - chi2(SFs_result) - 1  for i in xvalues_SFb])
            # plt.plot(xvalues_SFb,yvalues_SFb)
#             plt.plot(xvalues_SFb,np.zeros(len(xvalues_SFb)))
#             plt.show()
            ysign_SFb = np.sign(yvalues_SFb)
            signchange_SFb = ((np.roll(ysign_SFb, 1) - ysign_SFb) != 0).astype(int)
            print xvalues_SFb[signchange_SFb == 1]
            if len(xvalues_SFb[signchange_SFb == 1]) == 2: fit_unc_SFb = (xvalues_SFb[signchange_SFb == 1][1] - xvalues_SFb[signchange_SFb == 1][0])/2.
            else: fit_unc_SFb = 1.
            
            xvalues_SFc = np.arange(SFs_result[1]-1,SFs_result[1]+1,0.001)
            yvalues_SFc = np.asarray([chi2(np.asarray([SFs_result[0],i,SFs_result[2]])) - chi2(SFs_result) - 1 for i in xvalues_SFc])
            ysign_SFc = np.sign(yvalues_SFc)
            signchange_SFc = ((np.roll(ysign_SFc, 1) - ysign_SFc) != 0).astype(int)
            if len(xvalues_SFc[signchange_SFc == 1]) == 2: fit_unc_SFc = (xvalues_SFc[signchange_SFc == 1][1] - xvalues_SFc[signchange_SFc == 1][0])/2.
            else: fit_unc_SFc = 1.
            
            xvalues_SFl = np.arange(SFs_result[2]-1,SFs_result[2]+1,0.001)
            yvalues_SFl = np.asarray([chi2(np.asarray([SFs_result[0],SFs_result[1],i])) - chi2(SFs_result) - 1 for i in xvalues_SFl])
            ysign_SFl = np.sign(yvalues_SFl)
            signchange_SFl = ((np.roll(ysign_SFl, 1) - ysign_SFl) != 0).astype(int)
            if len(xvalues_SFl[signchange_SFl == 1]) == 2: fit_unc_SFl = (xvalues_SFl[signchange_SFl == 1][1] - xvalues_SFl[signchange_SFl == 1][0])/2.
            else: fit_unc_SFl = 1.
            
            print "SFb = ",SFs_result[0], " +- ", fit_unc_SFb
            print "SFc = ",SFs_result[1], " +- ", fit_unc_SFc
            print "SFl = ",SFs_result[2], " +- ", fit_unc_SFl
            # print "SFb = ",SFs_result[0], " +- ", sqrt(result.hess_inv[0][0])
#             print "SFc = ",SFs_result[1], " +- ", sqrt(result.hess_inv[1][1])
#             print "SFl = ",SFs_result[2], " +- ", sqrt(result.hess_inv[2][2])
            
            fit_unc_dict[(binx+1,biny+1)] = [fit_unc_SFb,fit_unc_SFc,fit_unc_SFl]
            
            print "FINAL CHI2: ",chi2(SFs_result)
            #sys.exit(1)
            
            SFb_hist.SetBinContent(binx+1,biny+1,histo_dict["jet1"]["b"].GetBinContent(binx+1,biny+1)*SFs_result[0])
            SFc_hist.SetBinContent(binx+1,biny+1,histo_dict["jet2"]["c"].GetBinContent(binx+1,biny+1)*SFs_result[1])
            SFl_hist.SetBinContent(binx+1,biny+1,histo_dict["jet3"]["l"].GetBinContent(binx+1,biny+1)*SFs_result[2])
        
        
        
            # uncertainties
            # def unc_b(SFb):
    #             return chi2_b([SFb,SFs_result[1],SFs_result[2]]) - chi2_b(SFs_result) - 1
    #         zeros_b_low = fsolve(unc_b,SFs_result[0]-0.5)
    #         zeros_b_high = fsolve(unc_b,SFs_result[0]+0.5)
    #         print "unc SFb = ",SFs_result[0], "- ", SFs_result[0]-zeros_b_low[0]," + ", zeros_b_high[0]-SFs_result[0]
    #         
            print ""
            print "********************"
            print ""

    SFb_hist.Divide(histo_dict["jet1"]["b"])
    SFc_hist.Divide(histo_dict["jet2"]["c"])
    SFl_hist.Divide(histo_dict["jet3"]["l"])
    
    
     # Add fit uncertainty
    for binx in range(histo_dict["jet1"]["b"].GetNbinsX()):
        for biny in range(histo_dict["jet1"]["b"].GetNbinsY()):
            SFb_hist.SetBinError(binx+1,biny+1,sqrt(SFb_hist.GetBinError(binx+1,biny+1)**2 + fit_unc_dict[(binx+1,biny+1)][0]**2))
            SFc_hist.SetBinError(binx+1,biny+1,sqrt(SFc_hist.GetBinError(binx+1,biny+1)**2 + fit_unc_dict[(binx+1,biny+1)][1]**2))
            SFl_hist.SetBinError(binx+1,biny+1,sqrt(SFl_hist.GetBinError(binx+1,biny+1)**2 + fit_unc_dict[(binx+1,biny+1)][2]**2))


    ROOT.gStyle.SetPaintTextFormat("4.3f")

    cSFb = ROOT.TCanvas("cSFb","cSFb",1800,600)
    cSFb.Divide(3)
    cSFb.cd(1)
    ROOT.gPad.SetMargin(0.15,0.15,0.15,0.1)
    SFb_hist.SetMarkerSize(1.5)
    SFb_hist.GetXaxis().CenterTitle()
    SFb_hist.GetXaxis().SetTitleSize(0.05)
    SFb_hist.GetXaxis().SetTitleOffset(1.2)
    SFb_hist.GetYaxis().CenterTitle()
    SFb_hist.GetYaxis().SetTitleSize(0.05)
    SFb_hist.GetYaxis().SetTitleOffset(1.2)
    SFb_hist.GetZaxis().SetRangeUser(0.,2.)
    SFb_hist.GetZaxis().CenterTitle()
    SFb_hist.GetZaxis().SetTitleSize(0.05)
    SFb_hist.GetZaxis().SetTitleOffset(1.2)
    SFb_hist.Draw("COLZ TEXT E")
    cSFb.cd(2)
    ROOT.gPad.SetMargin(0.15,0.15,0.15,0.1)
    SFc_hist.SetMarkerSize(1.5)
    SFc_hist.GetXaxis().CenterTitle()
    SFc_hist.GetXaxis().SetTitleSize(0.05)
    SFc_hist.GetXaxis().SetTitleOffset(1.2)
    SFc_hist.GetYaxis().CenterTitle()
    SFc_hist.GetYaxis().SetTitleSize(0.05)
    SFc_hist.GetYaxis().SetTitleOffset(1.2)
    SFc_hist.GetZaxis().SetRangeUser(0.,2.)
    SFc_hist.GetZaxis().CenterTitle()
    SFc_hist.GetZaxis().SetTitleSize(0.05)
    SFc_hist.GetZaxis().SetTitleOffset(1.2)
    SFc_hist.Draw("COLZ TEXT E")
    cSFb.cd(3)
    ROOT.gPad.SetMargin(0.15,0.15,0.15,0.1)
    SFl_hist.SetMarkerSize(1.5)
    SFl_hist.GetXaxis().CenterTitle()
    SFl_hist.GetXaxis().SetTitleSize(0.05)
    SFl_hist.GetXaxis().SetTitleOffset(1.2)
    SFl_hist.GetYaxis().CenterTitle()
    SFl_hist.GetYaxis().SetTitleSize(0.05)
    SFl_hist.GetYaxis().SetTitleOffset(1.2)
    SFl_hist.GetZaxis().SetRangeUser(0.,2.)
    SFl_hist.GetZaxis().CenterTitle()
    SFl_hist.GetZaxis().SetTitleSize(0.05)
    SFl_hist.GetZaxis().SetTitleOffset(1.2)
    SFl_hist.Draw("COLZ TEXT E")
    cSFb.SaveAs(current_dir+"/SFs_cTag.png")
    cSFb.SaveAs(current_dir+"/SFs_cTag.pdf")

    outf = ROOT.TFile(current_dir+"/DeepCSV_cTag_SFs_94X.root","RECREATE")
    outf.cd()
    SFl_hist.Write()
    SFb_hist.Write()
    SFc_hist.Write()
    outf.Close()


    if not os.path.isdir(current_dir+"/convergencePlots"): os.mkdir(current_dir+"/convergencePlots")

    for (binx,biny), SF_dict in convergence_dict.iteritems():
        cc = ROOT.TCanvas("cc","cc",800,400)
        niter = np.array([float(i) for i in range(len(SF_dict["SFb"]))])
        SFb_list = np.array(SF_dict["SFb"])
        SFc_list = np.array(SF_dict["SFc"])
        SFl_list = np.array(SF_dict["SFl"])
        graph_b = ROOT.TGraph(len(niter),niter,SFb_list)
        graph_c = ROOT.TGraph(len(niter),niter,SFc_list)
        graph_l = ROOT.TGraph(len(niter),niter,SFl_list)
        mg = ROOT.TMultiGraph()
        mg.Add(graph_b)
        mg.Add(graph_c)
        mg.Add(graph_l)
   
        cc.cd()
        ROOT.gPad.SetMargin(0.12,0.25,0.15,0.1)
        mg.Draw("AL")
        graph_b.SetLineColor(2)
        graph_b.SetLineWidth(2)
        graph_c.SetLineColor(3)
        graph_c.SetLineWidth(2)
        graph_l.SetLineColor(4)
        graph_l.SetLineWidth(2)
        mg.GetXaxis().SetTitle("iteration")
        mg.GetXaxis().SetTitleSize(0.07)
        mg.GetXaxis().SetTitleOffset(0.95)
        mg.GetXaxis().SetLabelSize(0.06)
        mg.GetYaxis().SetTitle("SF")
        mg.GetYaxis().SetTitleSize(0.07)
        mg.GetYaxis().SetTitleOffset(0.9)
        mg.GetYaxis().SetLabelSize(0.06)
        mg.GetYaxis().CenterTitle()
        l = ROOT.TLegend(0.76,0.15,0.95,0.7)
        l.SetBorderSize(0)
        #l.SetHeader("bin_CvsL: "+str(binx+1)+", bin_CvsB: "+str(biny+1))
        l.AddEntry(graph_b,"b jets","l")
        l.AddEntry(graph_c,"c jets","l")
        l.AddEntry(graph_l,"l jets","l")
        l.Draw("same")
        latex = ROOT.TLatex()
        latex.SetTextFont(42)
        latex.SetTextSize(0.07)
        latex.DrawLatexNDC(0.77,0.83,"bin CvsL: "+str(binx+1))
        latex.DrawLatexNDC(0.77,0.73,"bin CvsB: "+str(biny+1))
        cc.Update()
        cc.SaveAs(current_dir+"/convergencePlots/convergence_binx_"+str(binx)+"_biny_"+str(biny)+".pdf")
        del graph_b
        del graph_c
        del graph_l
        del mg                
                
