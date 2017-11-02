#ifndef __SELECTION_H__
#define __SELECTION_H__

#include <TCanvas.h>
#include <TSystem.h>
#include <TH1.h>
#include <TFile.h>
#include <TTree.h>
#include <TChain.h>
#include "TLorentzVector.h"
#include <iostream>
#include <TMath.h>
#include <math.h> 
#include <TLegend.h>
#include <TString.h>
#include <vector>
#include <map>
#include <dirent.h>
#include <sys/stat.h>
#include "Converter.h"
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/ini_parser.hpp>


void Selection(TString infilename, TString outfilename, Int_t nevents = -1);

// https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation80XReReco
bool TightBTag(float discr){
    return discr>0.9535;
}
bool MediumBTag(float discr){
    return discr>0.8484;
}

vector<TString> listfiles(TString indir){
    DIR *dir;
    struct dirent *ent;
    vector<TString> filenames;
    if ((dir = opendir (indir)) != NULL) {
      /* print all the files and directories within directory */
      while ((ent = readdir (dir)) != NULL) {
        TString name = ent->d_name;
        if (name.BeginsWith("output_")){
            filenames.push_back(name);
        }
      }
      closedir (dir);
    }
    return filenames;
}


bool DirExists(TString indir){
    DIR *dir;
    return ((dir = opendir (indir)) != NULL);
}


// int nmuon_min = -1;
// int nmuon_max = 9999;
// float muon_pt_min = -1;
// float muon_pt_max = 9999;
// float muon_abseta_min = -1;
// float muon_abseta_max = 9999;
// int nelectron_min = -1;
// int nelectron_max = 9999;
// float electron_pt_min = -1;
// float electron_pt_max = 9999;
// float electron_abseta_min = -1;
// float electron_abseta_max = 9999;
// int njet_min = -1;
// int njet_max = 9999;
// float jet_pt_min = -1;
// float jet_pt_max = 9999;
// float jet_abseta_min = -1;
// float jet_abseta_max = 9999;
// 
// void readConfig(std::string config_file)
// {
//     boost::property_tree::ptree ptree;
//     boost::property_tree::ini_parser::read_ini(config_file, ptree);
//     nmuon_min = ptree.get<int>("muon.n_min");
//     nmuon_max = ptree.get<int>("muon.n_max");
//     muon_pt_min = ptree.get<float>("muon.pt_min");
//     muon_pt_max = ptree.get<float>("muon.pt_max");
//     muon_abseta_min = ptree.get<float>("muon.abseta_min");
//     muon_abseta_max = ptree.get<float>("muon.abseta_max");
//     
//     nelectron_min = ptree.get<int>("electron.n_min");
//     nelectron_max = ptree.get<int>("electron.n_max");
//     electron_pt_min = ptree.get<float>("electron.pt_min");
//     electron_pt_max = ptree.get<float>("electron.pt_max");
//     electron_abseta_min = ptree.get<float>("electron.abseta_min");
//     electron_abseta_max = ptree.get<float>("electron.abseta_max");
//     
//     njet_min = ptree.get<int>("jet.n_min");
//     njet_max = ptree.get<int>("jet.n_max");
//     jet_pt_min = ptree.get<float>("jet.pt_min");
//     jet_pt_max = ptree.get<float>("jet.pt_max");
//     jet_abseta_min = ptree.get<float>("jet.abseta_min");
//     jet_abseta_max = ptree.get<float>("jet.abseta_max");
//     
// }




#endif
