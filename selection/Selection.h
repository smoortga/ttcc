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
#include <sstream>
#include <TLegend.h>
#include <TString.h>
#include <vector>
#include <map>
#include <dirent.h>
#include <sys/stat.h>
#include "Converter.h"
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/ini_parser.hpp>


void Selection(std::string infilename, std::string outfilename, Int_t nevents = -1);

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


std::vector<std::string> split(const std::string &s, char delim) {
  std::stringstream ss(s);
  std::string item;
  std::vector<std::string> elems;
  while (std::getline(ss, item, delim)) {
    elems.push_back(item);
  }
  return elems;
}

std::string GetOutputFileName(std::string output){
    std::vector<std::string> sample_name_v = split(output, '/');
    for (std::vector<std::string>::iterator it = sample_name_v.begin(); it != sample_name_v.end(); it++){
        TString buffer(*it);
        if (buffer.EndsWith(".root")) return split(*it, '.')[0];
    }
    return "NOTFOUND";
}




#endif
