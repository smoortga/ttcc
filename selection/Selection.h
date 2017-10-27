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


void Selection(TString infilename, TString outfilename);

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


#endif
