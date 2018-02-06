import os
import time
from argparse import ArgumentParser
import ROOT
from ROOT import gSystem, TFile
gSystem.Load('../objects/Electron_C')
gSystem.Load('../objects/Muon_C')
gSystem.Load('../objects/Jet_C')
gSystem.Load('../objects/MissingEnergy_C')
gSystem.Load('../objects/Trigger_C')
from ROOT import Electron, Muon, Jet, MissingEnergy, Trigger
from array import array
from math import sqrt, pow

def DileptonIvariantMass(lepton_1, lepton_2):
    total_p4 = lepton_1.p4() + lepton_2.p4()
    return total_p4.M()

def DileptonDeltaR(lepton1, lepton2):
    return sqrt(pow(lepton1.Phi()-lepton2.Phi(),2) + pow(lepton1.Eta()-lepton2.Eta(),2))

def DeltaR(obj1,obj2):
    return sqrt(pow(obj1.Phi()-obj2.Phi(),2) + pow(obj1.Eta()-obj2.Eta(),2))

def isCSVv2M(jet):
    return jet.CSVv2() > 0.8484

def isCSVv2T(jet):
    return jet.CSVv2() > 0.9535 








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
    
    def Clean(self, electron, muon):
        for idx,jet in enumerate(self.v_jet_):
            #electrons
            if DeltaR(jet,electron) < 0.5: 
                self.bad_indices.append(idx)
                continue
            #if idx in self.bad_indices: continue
            #muons
            if DeltaR(jet,muon) < 0.5: 
                self.bad_indices.append(idx)
                continue
            # take tight jetIds
            if not jet.IsTightJetID(): 
                self.bad_indices.append(idx)
                continue
            if jet.CSVv2() < 0:
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
    
    def IsValid(self):
        alljetsfilled = self.jets_dict_["leading_top_bjet"][1] and self.jets_dict_["subleading_top_bjet"][1] and self.jets_dict_["leading_add_jet"][1] and self.jets_dict_["subleading_add_jet"][1]
        validCSVv2Values = self.jets_dict_["leading_top_bjet"][0].CSVv2() > -1 and self.jets_dict_["subleading_top_bjet"][0].CSVv2() > -1 and self.jets_dict_["leading_add_jet"][0].CSVv2() > -1 and self.jets_dict_["subleading_add_jet"][0].CSVv2() > -1
        return alljetsfilled and validCSVv2Values
