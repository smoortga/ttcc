import os
import time
from argparse import ArgumentParser
import ROOT
from ROOT import gSystem, TFile
gSystem.Load('../objects/Electron_C')
gSystem.Load('../objects/Muon_C')
gSystem.Load('../objects/Jet_C')
gSystem.Load('../objects/GenJet_C')
gSystem.Load('../objects/MissingEnergy_C')
gSystem.Load('../objects/Trigger_C')
gSystem.Load('../objects/Truth_C')
from ROOT import Electron, Muon, Jet, MissingEnergy, Trigger, Truth
from array import array
from math import sqrt, pow, pi
from itertools import permutations
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler
from keras.objectives import mean_squared_error


def make_loss_D(c):
    def loss_D(y_true, y_pred):
        return c * mean_squared_error(y_pred, y_true)
    return loss_D


def IvariantMass(part_1, part_2):
    total_p4 = part_1.p4() + part_2.p4()
    return total_p4.M()

def IvariantMass_3particles(part_1, part_2, part_3):
    total_p4 = part_1.p4() + part_2.p4() + part_3.p4()
    return total_p4.M()

def DileptonIvariantMass(lepton_1, lepton_2):
    total_p4 = lepton_1.p4() + lepton_2.p4()
    return total_p4.M()

def DileptonDeltaR(lepton1, lepton2):
    return sqrt(pow(lepton1.Phi()-lepton2.Phi(),2) + pow(lepton1.Eta()-lepton2.Eta(),2))

def DeltaPhi(phi1,phi2):
    dphi = abs(phi1-phi2)
    if dphi > pi: dphi = 2*pi - dphi
    return dphi

def DeltaR(obj1,obj2):
    return sqrt(pow(DeltaPhi(obj1.Phi(),obj2.Phi()),2) + pow(obj1.Eta()-obj2.Eta(),2))

#https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation
def isCSVv2L(jet):
    return jet.CSVv2() > 0.5803  

def isCSVv2M(jet):
    return jet.CSVv2() > 0.8838

def isCSVv2T(jet):
    return jet.CSVv2() > 0.9693  

def isDeepCSVBDiscrL(jet):
    return jet.DeepCSVBDiscr() > 0.1522 

def isDeepCSVBDiscrM(jet):
    return jet.DeepCSVBDiscr() > 0.4941

def isDeepCSVBDiscrT(jet):
    return jet.DeepCSVBDiscr() > 0.8001 

def iscTaggerL(jet):
    return jet.CTagCvsL() > -0.53 and jet.CTagCvsB() > -0.26

def iscTaggerM(jet):
    return jet.CTagCvsL() > 0.07 and jet.CTagCvsB() > -0.10

def iscTaggerT(jet):
    return jet.CTagCvsL() > 0.87 and jet.CTagCvsB() > -0.3

def isDeepCSVcTaggerL(jet):
    return jet.DeepCSVCvsL() > 0.05 and jet.DeepCSVCvsB() > 0.33 

def isDeepCSVcTaggerM(jet):
    return jet.DeepCSVCvsL() > 0.15 and jet.DeepCSVCvsB() > 0.28 

def isDeepCSVcTaggerT(jet):
    return jet.DeepCSVCvsL() > 0.8  and jet.DeepCSVCvsB() > 0.1



def getcTagSF(jet,histogram):
    CvsL = jet.DeepCSVCvsL()
    CvsB = jet.DeepCSVCvsB()
    binx = histogram.GetXaxis().FindBin(CvsL)
    biny = histogram.GetYaxis().FindBin(CvsB)
    SF = histogram.GetBinContent(binx,biny)
    return SF


def GetBTagEff(jet,btageffhistofile,WP):
    if not (WP == "loose" or WP == "medium" or WP == "tight"):
        print "ERROR: WP '%s' not known!"%WP
        return 0.
    pt_ = jet.Pt()
    eta_ = abs(jet.Eta())
    flav_ = abs(jet.HadronFlavour())
    
    if flav_ == 5:
        incl_histo = btageffhistofile.Get("hist_DeepCSV_total_bjets")
        tagged_histo = btageffhistofile.Get("hist_DeepCSV_btagged_%s_bjets"%WP)
    elif flav_ == 4:
        incl_histo = btageffhistofile.Get("hist_DeepCSV_total_cjets")
        tagged_histo = btageffhistofile.Get("hist_DeepCSV_btagged_%s_cjets"%WP)
    elif flav_ == 0:
        incl_histo = btageffhistofile.Get("hist_DeepCSV_total_ljets")
        tagged_histo = btageffhistofile.Get("hist_DeepCSV_btagged_%s_ljets"%WP)
    
    max_pt = incl_histo.GetXaxis().GetXmax()
    min_pt = incl_histo.GetXaxis().GetXmin()
    max_eta = incl_histo.GetYaxis().GetXmax()
    min_eta = incl_histo.GetYaxis().GetXmin()
    if pt_ > max_pt: pt = max_pt - 0.1
    if pt_ < min_pt: pt = min_pt + 0.1
    if eta_ > max_eta: eta = max_eta - 0.1
    if eta_ < min_eta: eta = min_eta + 0.1
    
    n_total = incl_histo.GetBinContent(incl_histo.FindBin(pt_,eta_))
    n_tagged = tagged_histo.GetBinContent(tagged_histo.FindBin(pt_,eta_))
    return float(n_tagged)/float(n_total)
    


class JetsClassifier:
    def __init__(self, jet_collection,isdata=False):
            #assert(jet_collection.size() >= 4)
            self.v_jet_ = jet_collection
            self.isdata_ = isdata

            self.jets_dict_ = { # name : [object, is_filled]
                    "leading_top_bjet"      : [Jet(),False],
                    "subleading_top_bjet"   : [Jet(),False],
                    "leading_add_jet"       : [Jet(),False],
                    "subleading_add_jet"    : [Jet(),False]
            }
            self.bad_indices = []
    
    def LeadingTopJet(self):
        if (self.jets_dict_["leading_top_bjet"][1]): return self.jets_dict_["leading_top_bjet"][0]
        else: 
            print "leading_top_bjet NOT FOUND, check IsValid() of your JetClassifier!"
            return Jet()
    
    def SubLeadingTopJet(self):
        if (self.jets_dict_["subleading_top_bjet"][1]): return self.jets_dict_["subleading_top_bjet"][0]
        else: 
            print "subleading_top_bjet NOT FOUND, check IsValid() of your JetClassifier!"
            return Jet()
    
    def LeadingAddJet(self):
        if (self.jets_dict_["leading_add_jet"][1]): return self.jets_dict_["leading_add_jet"][0]
        else: 
            print "leading_add_jet NOT FOUND, check IsValid() of your JetClassifier!"
            return Jet()
    
    def SubLeadingAddJet(self):
        if (self.jets_dict_["subleading_add_jet"][1]): return self.jets_dict_["subleading_add_jet"][0]
        else: 
            print "subleading_add_jet NOT FOUND, check IsValid() of your JetClassifier!"
            return Jet()
    
    def Clean(self, first_lepton, second_lepton):
        for idx,jet in enumerate(self.v_jet_):
            #first_leptons
            if DeltaR(jet,first_lepton) < 0.5: 
                self.bad_indices.append(idx)
                continue
            #if idx in self.bad_indices: continue
            #second_leptons
            if DeltaR(jet,second_lepton) < 0.5: 
                self.bad_indices.append(idx)
                continue
            # take tight jetIds
            if not jet.IsTightJetID(): 
                self.bad_indices.append(idx)
                continue
            if jet.CSVv2() < 0:
                self.bad_indices.append(idx)
                continue
            if jet.DeepCSVBDiscr() < 0:
                self.bad_indices.append(idx)
                continue
        for index in sorted(self.bad_indices,reverse=True):
            self.v_jet_.erase( self.v_jet_.begin() + index)
        
            
    def OrderCSVv2(self): 
        # order and save CSVv2 value and index
        CSV_values = [(idx,jet.CSVv2()) for idx, jet in enumerate(self.v_jet_)]
        sorted_values = sorted(CSV_values, key=lambda x: x[1], reverse=True)
        if len(sorted_values)>0: self.jets_dict_["leading_top_bjet"] = [self.v_jet_[sorted_values[0][0]],True]
        if len(sorted_values)>1: self.jets_dict_["subleading_top_bjet"] = [self.v_jet_[sorted_values[1][0]],True]
        if len(sorted_values)>2: self.jets_dict_["leading_add_jet"] = [self.v_jet_[sorted_values[2][0]],True]
        if len(sorted_values)>3: self.jets_dict_["subleading_add_jet"] = [self.v_jet_[sorted_values[3][0]],True]
    
    def OrderDeepCSV(self): 
        # order and save CSVv2 value and index
        DeepCSV_values = [(idx,jet.DeepCSVBDiscr()) for idx, jet in enumerate(self.v_jet_)]
        sorted_values = sorted(DeepCSV_values, key=lambda x: x[1], reverse=True)
        if len(sorted_values)>0: self.jets_dict_["leading_top_bjet"] = [self.v_jet_[sorted_values[0][0]],True]
        if len(sorted_values)>1: self.jets_dict_["subleading_top_bjet"] = [self.v_jet_[sorted_values[1][0]],True]
        if len(sorted_values)>2: self.jets_dict_["leading_add_jet"] = [self.v_jet_[sorted_values[2][0]],True]
        if len(sorted_values)>3: self.jets_dict_["subleading_add_jet"] = [self.v_jet_[sorted_values[3][0]],True]
    
    def OrderTopMatchingNN(self,model,scaler,variables,lepton):
         
        #
        #   Fills the jets_dict_ according to highest Neural Network output
        #   The non-top jets are ranked according to DeepCSVCvsL and the two highest are chosen
        #
        #   Return value: highest NN output or -999 in case no proper permutation of jets was found
        #
        
        if len(self.v_jet_)<4:
            return -1
        
        best_perm_val = -999
        best_perm = (-1,-1,-1,-1)
        perm = [i for i in permutations(range(len(self.v_jet_)),4)]
        dict_inputs = {}
        for p in perm:

            perm_lept_bjet = self.v_jet_.at(p[0])
            perm_hadr_bjet = self.v_jet_.at(p[1])
            if not (isDeepCSVBDiscrT(perm_lept_bjet)) :continue #and not (isDeepCSVBDiscrT(perm_hadr_bjet)): continue
            perm_W1_jet = self.v_jet_.at(p[2])
            perm_W2_jet = self.v_jet_.at(p[3])
            dict_inputs["pT_leptb"] = perm_lept_bjet.Pt()
            dict_inputs["pT_hadrb"] = perm_hadr_bjet.Pt()
            dict_inputs["pT_W1"] = perm_W1_jet.Pt()
            dict_inputs["pT_W2"] = perm_W2_jet.Pt()
            dict_inputs["Eta_leptb"] = perm_lept_bjet.Eta()
            dict_inputs["Eta_hadrb"] = perm_hadr_bjet.Eta()
            dict_inputs["Eta_W1"] = perm_W1_jet.Eta()
            dict_inputs["Eta_W2"] = perm_W2_jet.Eta()
            # dict_inputs["DeepCSVBDiscr_W1"] = perm_W1_jet.DeepCSVBDiscr()
#             dict_inputs["DeepCSVBDiscr_W2"] = perm_W2_jet.DeepCSVBDiscr()
#             dict_inputs["DeepCSVBDiscr_hadrb"] = perm_hadr_bjet.DeepCSVBDiscr()
#             dict_inputs["DeepCSVBDiscr_leptb"] = perm_lept_bjet.DeepCSVBDiscr()
#             dict_inputs["DeepCSVCvsL_leptb"] = perm_lept_bjet.DeepCSVCvsL()
#             dict_inputs["DeepCSVCvsL_hadrb"] = perm_hadr_bjet.DeepCSVCvsL()
#             dict_inputs["DeepCSVCvsL_W1"] = perm_W1_jet.DeepCSVCvsL()
#             dict_inputs["DeepCSVCvsL_W2"] =  perm_W2_jet.DeepCSVCvsL()
#             dict_inputs["DeepCSVCvsB_leptb"] = perm_lept_bjet.DeepCSVCvsB()
#             dict_inputs["DeepCSVCvsB_hadrb"] = perm_hadr_bjet.DeepCSVCvsB()
#             dict_inputs["DeepCSVCvsB_W1"] = perm_W1_jet.DeepCSVCvsB()
#             dict_inputs["DeepCSVCvsB_W2"] = perm_W2_jet.DeepCSVCvsB()
            dict_inputs["DeltaR_leptb_lep"] = DeltaR(perm_lept_bjet,lepton)
            dict_inputs["DeltaR_hadrb_lep"] = DeltaR(perm_hadr_bjet,lepton)
            dict_inputs["DeltaR_Wjets"] = DeltaR(perm_W1_jet,perm_W2_jet)
            dict_inputs["minv_leptb_lep"] = IvariantMass(perm_lept_bjet,lepton)
            dict_inputs["minv_hadrb_lep"] = IvariantMass(perm_hadr_bjet,lepton)
            dict_inputs["minv_Wjets"] = IvariantMass(perm_W1_jet,perm_W2_jet)
            dict_inputs["minv_Wjets_leptb"] = IvariantMass_3particles(perm_W1_jet,perm_W2_jet,perm_lept_bjet)
            dict_inputs["minv_Wjets_hadrb"] = IvariantMass_3particles(perm_W1_jet,perm_W2_jet,perm_hadr_bjet)
            
            if np.isnan(dict_inputs.values()).any():
                print "WARNING: nan value encountered in NN inputs. Matching failed!"
                return -999

            X = np.ndarray(shape=(1,len(variables)), dtype=float, order='F')
            for idx,var in enumerate(variables):
                X[0,idx] =  dict_inputs[var]
            X = scaler.transform(X)

            pred = model.predict(np.asarray(X))
            discr = pred[:,1]
            #discr = max(pred[:,1]/(pred[:,0]+pred[:,1]),pred[:,2]/(pred[:,0]+pred[:,2]))
            
            #print p,discr
            if discr > best_perm_val:
                best_perm = p
                best_perm_val=discr
        
        if best_perm[0] == -1 or best_perm[1] == -1 or best_perm[2] == -1 or best_perm[3] == -1:
            return -999
        
        self.jets_dict_["leading_top_bjet"] = [self.v_jet_.at(best_perm[0]),True]
        self.jets_dict_["subleading_top_bjet"] = [self.v_jet_.at(best_perm[1]),True]
        #print "top bjet hadronFlavour: ", self.jets_dict_["leading_top_bjet"][0].HadronFlavour(), self.jets_dict_["leading_top_bjet"][0].DeepCSVBDiscr()
        #print "antitop bjet hadronFlavour: ", self.jets_dict_["subleading_top_bjet"][0].HadronFlavour(), self.jets_dict_["subleading_top_bjet"][0].DeepCSVBDiscr()
        #print "best perm value: ", best_perm_val
        # remaining_indices = range(len(self.v_jet_))
#         remaining_indices.remove(best_perm[0])
#         remaining_indices.remove(best_perm[1])
#         remaining_jets = [self.v_jet_.at(ij) for ij in remaining_indices]
#         ptsorted_remaining_jets = sorted(remaining_jets, key=lambda x: x.DeepCSVBDiscr(), reverse=True)
        #print "***********"
        #print [jj.DeepCSVBDiscr() for jj in remaining_jets]
        #print [jj.HadronFlavour() for jj in remaining_jets]
        #print [jj.DeepCSVBDiscr() for jj in ptsorted_remaining_jets]
        #print [jj.HadronFlavour() for jj in ptsorted_remaining_jets]
        #print "***********"
        self.jets_dict_["leading_add_jet"] = [self.v_jet_.at(best_perm[2]),True]
        self.jets_dict_["subleading_add_jet"] = [self.v_jet_.at(best_perm[3]),True]
        
        return best_perm_val
        
    
    def IsValid(self):
        alljetsfilled = self.jets_dict_["leading_top_bjet"][1] and self.jets_dict_["subleading_top_bjet"][1] and self.jets_dict_["leading_add_jet"][1] and self.jets_dict_["subleading_add_jet"][1]
        #validCSVv2Values = self.jets_dict_["leading_top_bjet"][0].CSVv2() > -1 and self.jets_dict_["subleading_top_bjet"][0].CSVv2() > -1 and self.jets_dict_["leading_add_jet"][0].CSVv2() > -1 and self.jets_dict_["subleading_add_jet"][0].CSVv2() > -1
        validDeepCSVValues = self.jets_dict_["leading_top_bjet"][0].DeepCSVBDiscr() > -1 and self.jets_dict_["subleading_top_bjet"][0].DeepCSVBDiscr() > -1 and self.jets_dict_["leading_add_jet"][0].DeepCSVBDiscr() > -1 and self.jets_dict_["subleading_add_jet"][0].DeepCSVBDiscr() > -1
        return alljetsfilled and validDeepCSVValues
    
    def validJets(self):
        return self.v_jet_
