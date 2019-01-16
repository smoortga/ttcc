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



def getFullPSCategory(genttXID,v_truth):
    """
    Full PS: 
        top and anti-top found
        categorization based on additional jets:
            cat = 0: ttbb (ttXID = 53,54,55)
            cat = 1: ttbL (ttXID = 51,52)
            cat = 2: ttcc (ttXID = 43,44,45)
            cat = 3: ttcL (ttXID = 41,42)
            cat = 4: ttLL (ttXID = 0)
            cat = -1: ttOther (top and anti-top were not found in truth info (should never happen really...))
    """
    top_found = False
    antitop_found = False
    ##
    #
    # Leptons
    #
    ##
    for tr in v_truth:
        if tr.LabelName() == "top":
            top_found = True
        elif tr.LabelName() == "antitop":
            antitop_found = True
    
    if not top_found or not antitop_found: return -1

    ##
    #
    # Jets
    #
    ##
    id = int(str(genttXID)[-2:])
    if (id == 53 or id == 54 or id == 55): return 0 #ttbb
    elif (id == 51 or id == 52): return 1 #ttbL
    elif (id == 43 or id == 44 or id == 45): return 2 #ttcc
    elif (id == 41 or id == 42): return 3 #ttcL
    elif (id == 0): return 4 #ttLF
    
    else:
        print "WARNING: Did not find suitable ttX category! Check This!!"
        return -1


def getVisiblePSCategory(genttXID,v_truth):
    """
    Visible PS: 
        two (truth) leptons form top and antitop decay found with pT > 30 GeV and abs(Eta) < 2.4
        two b-jets from top decays found (ttXID starts with 2)
        categorization based on additional jets:
            cat = 0: ttbb (ttXID = 53,54,55)
            cat = 1: ttbL (ttXID = 51,52)
            cat = 2: ttcc (ttXID = 43,44,45)
            cat = 3: ttcL (ttXID = 41,42)
            cat = 4: ttLL (ttXID = 0)
            cat = -1: ttOther (ttxID does not start with 2 or leptons not found)
    """
    top_lepton_found = False
    antitop_lepton_found = False
    ##
    #
    # Leptons
    #
    ##
    for tr in v_truth:
        if tr.LabelName() == "top_lep":
            if tr.Pt() > 25 and abs(tr.Eta()) < 2.4: top_lepton_found = True
        elif tr.LabelName() == "antitop_lep":
            if tr.Pt() > 25 and abs(tr.Eta()) < 2.4: antitop_lepton_found = True
    
    if not top_lepton_found or not antitop_lepton_found: return -1

    ##
    #
    # Jets
    #
    ##
    id = int(str(genttXID)[-2:])
    # The visible phase space requires the two b jets form the top decay to be within the acceptance
    # therefore, genTTX_id has to start with 2! (if it starts with 1 or 0[only two numbers long] it is not in Visible PS)
    if len(str(genttXID)) < 3: 
        return -1 # this means no b-jets from top decay are within acceptance
    elif int(str(genttXID)[0]) == 1: 
        return -1 # this means only 1 bjet from top decay was within acceptance
    #print "genTTXid = ",genttXID
    elif int(str(genttXID)[0]) == 2: # two b-jets form top decay are within acceptance!
        if (id == 53 or id == 54 or id == 55): return 0 #ttbb
        elif (id == 51 or id == 52): return 1 #ttbL
        elif (id == 43 or id == 44 or id == 45): return 2 #ttcc
        elif (id == 41 or id == 42): return 3 #ttcL
        elif (id == 0): return 4 #ttLF
        else: 
            print "WARNING: Did not find suitable ttX category! Check This!!"
            return -1
    
    else:
        print "WARNING: Did not find suitable ttX category! Check This!!"
        return -1


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
    if pt_ > max_pt: pt_ = max_pt - 0.1
    if pt_ < min_pt: pt_ = min_pt + 0.1
    if eta_ > max_eta: eta_ = max_eta - 0.1
    if eta_ < min_eta: eta_ = min_eta + 0.1
    
    
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
    
    def OrderTopMatchingNN(self,model,scaler,variables,pos_lepton,neg_lepton):
         
        #
        #   Fills the jets_dict_ according to highest Neural Network output
        #   The non-top jets are ranked according to DeepCSVCvsL and the two highest are chosen
        #
        #   Return value: highest NN output or -1 in case no proper permutation of jets was found
        #
        
        if len(self.v_jet_)<4:
            return -1
        
        best_perm_val = -999
        best_perm = (-1,-1,-1,-1)
        perm = [i for i in permutations(range(len(self.v_jet_)),4)]
        dict_inputs = {}
        for p in perm:

            perm_top_bjet = self.v_jet_.at(p[0])
            perm_antitop_bjet = self.v_jet_.at(p[1])
            if not isDeepCSVBDiscrM(perm_top_bjet) or not isDeepCSVBDiscrM(perm_antitop_bjet): continue
            if not (perm_top_bjet.Pt()>30 and perm_antitop_bjet.Pt() > 30): continue
            perm_addjet_lead = self.v_jet_.at(p[2])
            perm_addjet_sublead = self.v_jet_.at(p[3])
            #fill variables
            dict_inputs["pT_topb"] = perm_top_bjet.Pt()
            dict_inputs["pT_antitopb"] = perm_antitop_bjet.Pt()
            dict_inputs["pT_addlead"] = perm_addjet_lead.Pt()
            dict_inputs["pT_addsublead"] = perm_addjet_sublead.Pt()
            dict_inputs["Eta_topb"] = perm_top_bjet.Eta()
            dict_inputs["Eta_antitopb"] = perm_antitop_bjet.Eta()
            dict_inputs["Eta_addlead"] = perm_addjet_lead.Eta()
            dict_inputs["Eta_addsublead"] = perm_addjet_sublead.Eta()
            # dict_inputs["Phi_topb"] = perm_top_bjet.Phi()
#             dict_inputs["Phi_antitopb"] = perm_antitop_bjet.Phi()
#             dict_inputs["Phi_addlead"] = perm_addjet_lead.Phi()
#             dict_inputs["Phi_addsublead"] = perm_addjet_sublead.Phi()
            # dict_inputs["CSVv2_topb"] = perm_top_bjet.CSVv2()
#             dict_inputs["CSVv2_antitopb"] = perm_antitop_bjet.CSVv2()
#             dict_inputs["CSVv2_addlead"] = perm_addjet_lead.CSVv2()
#             dict_inputs["CSVv2_addsublead"] = perm_addjet_sublead.CSVv2()
            dict_inputs["DeepCSVBDiscr_topb"] = perm_top_bjet.DeepCSVBDiscr()
            dict_inputs["DeepCSVBDiscr_antitopb"] = perm_antitop_bjet.DeepCSVBDiscr()
            dict_inputs["DeepCSVBDiscr_addlead"] = perm_addjet_lead.DeepCSVBDiscr()
            dict_inputs["DeepCSVBDiscr_addsublead"] = perm_addjet_sublead.DeepCSVBDiscr()
            dict_inputs["DeepCSVCvsL_topb"] = perm_top_bjet.DeepCSVCvsL()
            dict_inputs["DeepCSVCvsL_antitopb"] = perm_antitop_bjet.DeepCSVCvsL()
            dict_inputs["DeepCSVCvsL_addlead"] = perm_addjet_lead.DeepCSVCvsL()
            dict_inputs["DeepCSVCvsL_addsublead"] =  perm_addjet_sublead.DeepCSVCvsL()
            dict_inputs["DeepCSVCvsB_topb"] = perm_top_bjet.DeepCSVCvsB()
            dict_inputs["DeepCSVCvsB_antitopb"] = perm_antitop_bjet.DeepCSVCvsB()
            dict_inputs["DeepCSVCvsB_addlead"] = perm_addjet_lead.DeepCSVCvsB()
            dict_inputs["DeepCSVCvsB_addsublead"] = perm_addjet_sublead.DeepCSVCvsB()
            dict_inputs["DeltaR_topb_leppos"] = DeltaR(perm_top_bjet,pos_lepton)
            dict_inputs["DeltaR_antitopb_lepneg"] = DeltaR(perm_antitop_bjet,neg_lepton)
            dict_inputs["DeltaR_adds"] = DeltaR(perm_addjet_lead,perm_addjet_sublead)
            dict_inputs["minv_topb_leppos"] = IvariantMass(perm_top_bjet,pos_lepton)
            dict_inputs["minv_antitopb_lepneg"] = IvariantMass(perm_antitop_bjet,neg_lepton)
            dict_inputs["minv_adds"] = IvariantMass(perm_addjet_lead,perm_addjet_sublead)
            
            if np.isnan(dict_inputs.values()).any():
                print "WARNING: nan value encountered in NN inputs. Matching failed!"
                return -999

            X = np.ndarray(shape=(1,len(variables)), dtype=float, order='F')
            for idx,var in enumerate(variables):
                X[0,idx] =  dict_inputs[var]
            X = scaler.transform(X)

            pred = model.predict(np.asarray(X))
            discr = max(pred[:,1]/(pred[:,0]+pred[:,1]),pred[:,2]/(pred[:,0]+pred[:,2]))

            if discr > best_perm_val:
                best_perm = p
                best_perm_val=discr
        
        if best_perm[0] == -1 or best_perm[1] == -1 or best_perm[2] == -1 or best_perm[3] == -1:
            return -1
        
        self.jets_dict_["leading_top_bjet"] = [self.v_jet_.at(best_perm[0]),True]
        self.jets_dict_["subleading_top_bjet"] = [self.v_jet_.at(best_perm[1]),True]
        #print "top bjet hadronFlavour: ", self.jets_dict_["leading_top_bjet"][0].HadronFlavour()
        #print "antitop bjet hadronFlavour: ", self.jets_dict_["subleading_top_bjet"][0].HadronFlavour()
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
