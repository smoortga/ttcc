import ROOT
import os
import sys
from argparse import ArgumentParser
from array import array
from xsec import xsec_table, color_table, legend_array
from math import sqrt
from collections import OrderedDict

ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetOptStat(0)




#syst_list=["weight_btag_iterativefit_JesUp","weight_btag_iterativefit_JesDown","weight_btag_iterativefit_HfUp","weight_btag_iterativefit_HfDown","weight_btag_iterativefit_Hfstats1Up","weight_btag_iterativefit_Hfstats1Down","weight_btag_iterativefit_Hfstats2Up","weight_btag_iterativefit_Hfstats2Down","weight_btag_iterativefit_Lfstats1Up","weight_btag_iterativefit_Lfstats1Down","weight_btag_iterativefit_Lfstats2Up","weight_btag_iterativefit_Lfstats2Down","weight_btag_iterativefit_Cferr1Up","weight_btag_iterativefit_Cferr1Down","weight_btag_iterativefit_Cferr2Up","weight_btag_iterativefit_Cferr2Down"]
syst_list=["weight_ctag_iterativefit_Up","weight_ctag_iterativefit_Down"]

def make_display_dict(ttbarnames = ["TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS","TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8","TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8"]):
    display_dict_ = {
     3:    {"legend":"t#bar{t}b#bar{b}",
             "tag":"ttbb",
             "samples":ttbarnames,
             "color":ROOT.kRed+3,
             "category":0
             },
     # 2:    {"legend":"t#bar{t}bc",
    #             "samples":ttbarnames,
    #             "color":ROOT.kOrange+6,
    #             "category":1
    #             },
     4:    {"legend":"t#bar{t}bj",
             "tag":"ttbj",
             "samples":ttbarnames,
             "color":ROOT.kRed+2,
             "category":1
             },
     1:    {"legend":"t#bar{t}c#bar{c}",
             "tag":"ttcc",
             "samples":ttbarnames,
             "color":ROOT.kOrange-2,
             "category":2
             },
     2:    {"legend":"t#bar{t}cj",
             "tag":"ttcj",
             "samples":ttbarnames,
             "color":ROOT.kOrange-7,
             "category":3
             },
     5:    {"legend":"t#bar{t}jj",
             "tag":"ttjj",
             "samples":ttbarnames,
             "color":ROOT.kRed-7,
             "category":4
             },
      6:    {"legend":"t#bar{t} + Other",
              "samples":ttbarnames,
              "tag":"ttother",
              "color":ROOT.kOrange+6,
              "category":-1
              },


     7:    {"legend":"Backgrounds",
             "tag":"bkg",
             "samples":["ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8","ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8","ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8","ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8","ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8"
                         ,"DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8","WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8","WZZ_TuneCP5_13TeV-amcatnlo-pythia8","WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8","ZZZ_TuneCP5_13TeV-amcatnlo-pythia8","WW_TuneCP5_13TeV-pythia8","WZ_TuneCP5_13TeV-pythia8","ZZ_TuneCP5_13TeV-pythia8"
                         ,"WW_TuneCP5_13TeV-pythia8","WZ_TuneCP5_13TeV-pythia8","ZZ_TuneCP5_13TeV-pythia8"
                         ], #"DYJetsToLL_M-5to50_TuneCP5_13TeV-madgraphMLM-pythia8","ttHJetTobb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8","ttHJetToNonbb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8"
             "color":ROOT.kCyan+1,
             "category":-1
             },

    #  6:    {"legend":"Single top",
    #             "tag":"singletop",
    #             "samples":["ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8","ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8","ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8","ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8","ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8"], 
    #             "color":ROOT.kCyan+1,
    #             "category":-1
    #             },
    #     7:    {"legend":"Z + jets",
    #             "tag":"zjets",
    #             "samples":["DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8","DYJetsToLL_M-5to50_TuneCP5_13TeV-madgraphMLM-pythia8"],#,"DYJetsToLL_M-4to50_HT-70to100_TuneCP5_13TeV-madgraphMLM-pythia8","DYJetsToLL_M-4to50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8","DYJetsToLL_M-4to50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8","DYJetsToLL_M-4to50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8","DYJetsToLL_M-4to50_HT-600toInf_TuneCP5_13TeV-madgraphMLM-pythia8"],#,"DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8_ext"],#,"DYJetsToLL_M-4to50_HT-70to100_TuneCP5_13TeV-madgraphMLM-pythia8","DYJetsToLL_M-4to50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8","DYJetsToLL_M-4to50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8","DYJetsToLL_M-4to50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8","DYJetsToLL_M-4to50_HT-600toInf_TuneCP5_13TeV-madgraphMLM-pythia8"],
    #             "color":ROOT.kBlue,
    #             "category":-1
    #             },
    #    #  1:    {"legend":"Diboson",
    # #             "samples":["WW_TuneCP5_13TeV-pythia8","WZ_TuneCP5_13TeV-pythia8","ZZ_TuneCP5_13TeV-pythia8"],
    # #             "color":402,
    # #             "category":-1
    # #             },           
    #     8:    {"legend":"Rare",
    #             "tag":"rare",
    #             "samples":["WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8","WZZ_TuneCP5_13TeV-amcatnlo-pythia8","WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8","ZZZ_TuneCP5_13TeV-amcatnlo-pythia8","WW_TuneCP5_13TeV-pythia8","WZ_TuneCP5_13TeV-pythia8","ZZ_TuneCP5_13TeV-pythia8","ttHJetTobb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8","ttHJetToNonbb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8","WW_TuneCP5_13TeV-pythia8","WZ_TuneCP5_13TeV-pythia8","ZZ_TuneCP5_13TeV-pythia8"],
    #             "color":1,
    #             "category":-1
    #             },
     # 9:    {"legend":"W + jets",
    #             "samples":["WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8"],
    #             "color":ROOT.kMagenta+1,
    #             "category":-1
    #             },
     # 9:    {"legend":"t#bar{t}V",
    #             "samples":["ttZJets_13TeV_madgraphMLM","ttWJets_13TeV_madgraphMLM"],
    #             "color":ROOT.kMagenta+1,
    #             "category":-1
    #             },
    #     10:    {"legend":"ttH (h #rightarrow b#bar{b})",
    #             "samples":["ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8"],
    #             "color":1,
    #             "category":-1
    #             },
     -1:    {"legend":"data",
             "tag":"data_obs",
             "samples":["DoubleMuon_Run2017E_31Mar2018_v1_MINIAOD","DoubleEG_Run2017B_31Mar2018_v1_MINIAOD","MuonEG_Run2017C_31Mar2018_v1_MINIAOD","MuonEG_Run2017E_31Mar2018_v1_MINIAOD",
                         "DoubleMuon_Run2017F_31Mar2018_v1_MINIAOD","DoubleMuon_Run2017C_31Mar2018_v1_MINIAOD","MuonEG_Run2017F_31Mar2018_v1_MINIAOD","DoubleEG_Run2017D_31Mar2018_v1_MINIAOD",
                         "DoubleMuon_Run2017D_31Mar2018_v1_MINIAOD","DoubleEG_Run2017C_31Mar2018_v1_MINIAOD","MuonEG_Run2017B_31Mar2018_v1_MINIAOD","DoubleMuon_Run2017B_31Mar2018_v1_MINIAOD",
                         "DoubleEG_Run2017F_31Mar2018_v1_MINIAOD","DoubleEG_Run2017E_31Mar2018_v1_MINIAOD","MuonEG_Run2017D_31Mar2018_v1_MINIAOD"
                         ],
             "color":1,
             "category":-1
             }
    }

    return display_dict_



def ExtractNBins(dict):
    nglobalbins = 0
    for jet,hist_2d_dict in dict.iteritems():
        nbins_tmp = 1
        for hist,bins in hist_2d_dict.iteritems():
            nbins_tmp*=len(bins)-1
        nglobalbins += nbins_tmp
    return nglobalbins


def FillMCHistogram_MCStat(entry_dict,hist_dict,indir,total_nbins,weights_to_apply, tag_to_vary, MC_stat_variation ,normalization = -1,postfix=""):
    final_hist_tmp_ = ROOT.TH1D("h_"+entry_dict["tag"]+postfix,"",total_nbins,0,total_nbins)
    final_hist_tmp_.Sumw2()
    
    iBin = 1 #counter while running over all available bins
    for jet,hist_2d_dict in hist_dict.iteritems():
        var_names = hist_2d_dict.keys()
        binnings = hist_2d_dict.values()
        hist2d_ = ROOT.TH2D("hist2d_"+entry_dict["tag"]+"_"+jet,"",len(binnings[0])-1,array("d",binnings[0]),len(binnings[1])-1,array("d",binnings[1]))
        hist2d_.Sumw2()
        for f in entry_dict["samples"]:
            full_path = indir + "/" + f + ".root"
            if not os.path.isfile(full_path): continue
            f_ = ROOT.TFile(full_path)
            n_original_h = f_.Get("hweight")
            n_original = n_original_h.GetBinContent(1)
            f_.Close()
            hist2d_tmp_ = ROOT.TH2D("hist2d_tmp_"+entry_dict["tag"]+"_"+jet+"_"+f,"",len(binnings[0])-1,array("d",binnings[0]),len(binnings[1])-1,array("d",binnings[1]))
            hist2d_tmp_.Sumw2()
            t_ = ROOT.TChain("tree")
            t_.Add(full_path)
            t_.Draw(var_names[1]+":"+var_names[0]+">> hist2d_tmp_"+entry_dict["tag"]+"_"+jet+"_"+f,weights_to_apply+"*(event_Category_VisiblePS == %s)"%entry_dict["category"])#*(mc_pu_trueNumInt>0)
            t_.GetEntry(1)
            if t_.is_data == 1:
                print "WARNING, found MC samples with is_data==1! (%s)"%f
                continue
        
            if tag_to_vary == entry_dict["tag"]:
                if MC_stat_variation == "Up":
                    for binX in range(hist2d_.GetNbinsX()):
                         for binY in range(hist2d_.GetNbinsY()):
                            err = hist2d_tmp_.GetBinError(binX+1,binY+1)
                            cont = hist2d_tmp_.GetBinContent(binX+1,binY+1)
                            hist2d_tmp_.SetBinContent(binX+1,binY+1,cont+err)          
                elif MC_stat_variation == "Down":
                    for binX in range(hist2d_.GetNbinsX()):
                         for binY in range(hist2d_.GetNbinsY()):
                            err = hist2d_tmp_.GetBinError(binX+1,binY+1)
                            cont = hist2d_tmp_.GetBinContent(binX+1,binY+1)
                            hist2d_tmp_.SetBinContent(binX+1,binY+1,cont-err)
                else: 
                    print "Error: did not recognize MC variation %s (should be Up or Down)"%str(MC_stat_variation)
        
            xsec = xsec_table[f]*1000 #[fb]
            int_lumi=41.527 #[fb^-1	]35.921875594646 #27.271
            scale = float(xsec*int_lumi)/float(n_original)
            hist2d_.Add(hist2d_tmp_,scale)
        
        # Now run over all the bins and add them to the final histogram
        for binX in range(hist2d_.GetNbinsX()):
            for binY in range(hist2d_.GetNbinsY()):
                content = hist2d_.GetBinContent(binX+1,binY+1)
                err = hist2d_.GetBinError(binX+1,binY+1)
                final_hist_tmp_.SetBinContent(iBin,content)
                final_hist_tmp_.SetBinError(iBin,err)
                iBin += 1    

    if not (normalization == -1): final_hist_tmp_.Scale(normalization/final_hist_tmp_.Integral())  
    return final_hist_tmp_
    
def FillMCHistogram(entry_dict,hist_dict,indir,total_nbins,weights_to_apply, normalization = -1,postfix=""):
    final_hist_tmp_ = ROOT.TH1D("h_"+entry_dict["tag"]+postfix,"",total_nbins,0,total_nbins)
    final_hist_tmp_.Sumw2()
    
     #counter while running over all available bins
    for jet,hist_2d_dict in hist_dict.iteritems():
        var_names = hist_2d_dict.keys()
        binnings = hist_2d_dict.values()
        # hist2d_ = ROOT.TH2D("hist2d_"+entry_dict["tag"]+"_"+jet,"",len(binnings[0])-1,array("d",binnings[0]),len(binnings[1])-1,array("d",binnings[1]))
#         hist2d_.Sumw2()
        hist1d_ = ROOT.TH1D("hist1d_"+entry_dict["tag"]+"_"+jet,"",total_nbins,0,total_nbins)
        hist1d_.Sumw2()
        for f in entry_dict["samples"]:
            full_path = indir + "/" + f + ".root"
            if not os.path.isfile(full_path): continue
            f_ = ROOT.TFile(full_path)
            n_original_h = f_.Get("hweight")
            n_original = n_original_h.GetBinContent(1)
            f_.Close()
            hist2d_tmp_ = ROOT.TH2D("hist2d_tmp_"+entry_dict["tag"]+"_"+jet+"_"+f,"",len(binnings[0])-1,array("d",binnings[0]),len(binnings[1])-1,array("d",binnings[1]))
            hist2d_tmp_.Sumw2()
            hist1d_tmp_ = ROOT.TH1D("hist1d_tmp_"+entry_dict["tag"]+"_"+jet+"_"+f,"",total_nbins,0,total_nbins)
            hist1d_tmp_.Sumw2()
            t_ = ROOT.TChain("tree")
            t_.Add(full_path)
            t_.Draw(var_names[1]+":"+var_names[0]+">> hist2d_tmp_"+entry_dict["tag"]+"_"+jet+"_"+f,weights_to_apply+"*(event_Category_VisiblePS == %s)"%entry_dict["category"])#*(mc_pu_trueNumInt>0)
            #t_.Draw(var_names[1]+":"+var_names[0]+">> hist2d_tmp_"+entry_dict["tag"]+"_"+jet+"_"+f,"(event_Category == %s)"%entry_dict["category"])#*(mc_pu_trueNumInt>0)
            #print hist2d_tmp_.Integral()
            #print [i for i in hist2d_tmp_.GetSumw2()]
            #print entry_dict["tag"],hist2d_tmp_.Integral()
            t_.GetEntry(1)
            if t_.is_data == 1:
                print "WARNING, found MC samples with is_data==1! (%s)"%f
                continue
            xsec = xsec_table[f]*1000 #[fb]
            int_lumi=41.527 #[fb^-1	]35.921875594646 #27.271
            scale = float(xsec*int_lumi)/float(n_original)
            #hist2d_.Add(hist2d_tmp_,scale)
        
            iBin = 1
            for binX in range(hist2d_tmp_.GetNbinsX()):
                for binY in range(hist2d_tmp_.GetNbinsY()):
                    content = hist2d_tmp_.GetBinContent(binX+1,binY+1)
                    err = hist2d_tmp_.GetBinError(binX+1,binY+1)
                    #print binX+1,binY+1,content,err,content**2/err**2
                    hist1d_tmp_.SetBinContent(iBin,content)
                    hist1d_tmp_.SetBinError(iBin,err)
                    iBin += 1
        
            final_hist_tmp_.Add(hist1d_tmp_,scale)
    
        print entry_dict["tag"]
        for binX in range(final_hist_tmp_.GetNbinsX()):
            for binY in range(final_hist_tmp_.GetNbinsY()):
                content = final_hist_tmp_.GetBinContent(binX+1,binY+1)
                err = final_hist_tmp_.GetBinError(binX+1,binY+1) 
                #print binX+1,binY+1,content,err,content**2/err**2
        
        # Now run over all the bins and add them to the final histogram
        # for binX in range(hist2d_.GetNbinsX()):
#             for binY in range(hist2d_.GetNbinsY()):
#                 content = hist2d_.GetBinContent(binX+1,binY+1)
#                 err = hist2d_.GetBinError(binX+1,binY+1)
#                 final_hist_tmp_.SetBinContent(iBin,content)
#                 final_hist_tmp_.SetBinError(iBin,err)
#                 iBin += 1    


    if not (normalization == -1): final_hist_tmp_.Scale(normalization/final_hist_tmp_.Integral())  
    return final_hist_tmp_


def FillDataHistogram(entry_dict,hist_dict,indir,total_nbins):
    final_hist_tmp_ = ROOT.TH1D("h_"+entry_dict["tag"],"",total_nbins,0,total_nbins)
    #final_hist_tmp_.Sumw2()

    iBin = 1 #counter while running over all available bins
    for jet,hist_2d_dict in hist_dict.iteritems():
        var_names = hist_2d_dict.keys()
        binnings = hist_2d_dict.values()
        hist2d_ = ROOT.TH2D("hist2d_"+entry_dict["tag"]+"_"+jet,"",len(binnings[0])-1,array("d",binnings[0]),len(binnings[1])-1,array("d",binnings[1]))
        hist2d_.Sumw2()
        for f in entry_dict["samples"]:
            full_path = indir + "/" + f + ".root"
            if not os.path.isfile(full_path): 
                print "ERROR: could not find %s, continue without"%full_path
                continue
            hist2d_tmp_ = ROOT.TH2D("hist2d_tmp_"+entry_dict["tag"]+"_"+jet+"_"+f,"",len(binnings[0])-1,array("d",binnings[0]),len(binnings[1])-1,array("d",binnings[1]))
            hist2d_tmp_.Sumw2()
            t_ = ROOT.TChain("tree")
            t_.Add(full_path)
            t_.Draw(var_names[1]+":"+var_names[0]+">> hist2d_tmp_"+entry_dict["tag"]+"_"+jet+"_"+f)#*(mc_pu_trueNumInt>0)
            t_.GetEntry(1)
            if not t_.is_data == 1:
                print "WARNING, found Data samples with is_data!=1! (%s)"%f
                continue
            hist2d_.Add(hist2d_tmp_)
        
        # Now run over all the bins and add them to the final histogram
        for binX in range(hist2d_.GetNbinsX()):
            for binY in range(hist2d_.GetNbinsY()):
                content = hist2d_.GetBinContent(binX+1,binY+1)
                err = hist2d_.GetBinError(binX+1,binY+1)
                final_hist_tmp_.SetBinContent(iBin,content)
                final_hist_tmp_.SetBinError(iBin,err)
                iBin += 1 

    return final_hist_tmp_

def MakeRoot1D(hist_dict,indir,outfile,options_dict,ttbarnames = ["TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS","TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8","TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8"],standardpostfix="",norm_dict={}):

    #*************************************************************
    #
    # Prepare the output file to store all histograms
    #
    #*************************************************************

    if os.path.isfile(outfile):
        print "WARNING, file %s EXISTS!!!! APPENDING TO THIS FILE"%outfile
        outf_ = ROOT.TFile(outfile,"update")
    else: 
        outf_ = ROOT.TFile(outfile,"recreate")

    #*************************************************************
    #
    # Process MC
    #
    #*************************************************************
    display_dict = make_display_dict(ttbarnames)
    for idx,entry_dict in display_dict.iteritems():
        if entry_dict["legend"]=="data": continue
        # create for this "sample" one big histogram
        # The exact binning spacing is not important for the final histogram
        # you just need to know for each bin the measured number of events in data and the expectations from MC
        # therefore we will create a histogram that unfolds the 2D distributions into a long 1D histogram with uniform spacing
        # if more than 1 jet is fitted, just concatenate the histograms
        
        total_yield_nominal = norm_dict[entry_dict["tag"]]
        
        total_nbins=ExtractNBins(hist_dict)
        weights_to_apply = "weight_ctag_iterativefit*weight_bcjets_btag_DeepCSVMedium*weight_udsgjets_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
        final_hist_tmp_ = FillMCHistogram(entry_dict,hist_dict,indir,total_nbins,weights_to_apply, normalization = total_yield_nominal, postfix = standardpostfix)
        outf_.cd()
        final_hist_tmp_.Write()

        


        # MC stat for each subsample:
        # ttbb Up
        # weights_to_apply = "weight_ctag_iterativefit*weight_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
        #         final_hist_tmp_ = FillMCHistogram_MCStat(entry_dict,hist_dict,indir,total_nbins,weights_to_apply,"ttbb","Up" , normalization = 1,postfix=standardpostfix+"_ttbbMCStatUp")
        #         outf_.cd()
        #         final_hist_tmp_.Write()
        #         # ttbb Down
        #         weights_to_apply = "weight_ctag_iterativefit*weight_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
        #         final_hist_tmp_ = FillMCHistogram_MCStat(entry_dict,hist_dict,indir,total_nbins,weights_to_apply,"ttbb","Down" , normalization = 1,postfix=standardpostfix+"_ttbbMCStatDown")
        #         outf_.cd()
        #         final_hist_tmp_.Write()
        #         
        #         # ttbj Up
        #         weights_to_apply = "weight_ctag_iterativefit*weight_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
        #         final_hist_tmp_ = FillMCHistogram_MCStat(entry_dict,hist_dict,indir,total_nbins,weights_to_apply,"ttbj","Up" , normalization = 1,postfix=standardpostfix+"_ttbjMCStatUp")
        #         outf_.cd()
        #         final_hist_tmp_.Write()
        #         # ttbj Down
        #         weights_to_apply = "weight_ctag_iterativefit*weight_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
        #         final_hist_tmp_ = FillMCHistogram_MCStat(entry_dict,hist_dict,indir,total_nbins,weights_to_apply,"ttbj","Down" , normalization = 1,postfix=standardpostfix+"_ttbjMCStatDown")
        #         outf_.cd()
        #         final_hist_tmp_.Write()
        #         
        #         # ttcc Up
        #         weights_to_apply = "weight_ctag_iterativefit*weight_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
        #         final_hist_tmp_ = FillMCHistogram_MCStat(entry_dict,hist_dict,indir,total_nbins,weights_to_apply,"ttcc","Up" , normalization = 1,postfix=standardpostfix+"_ttccMCStatUp")
        #         outf_.cd()
        #         final_hist_tmp_.Write()
        #         # ttcc Down
        #         weights_to_apply = "weight_ctag_iterativefit*weight_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
        #         final_hist_tmp_ = FillMCHistogram_MCStat(entry_dict,hist_dict,indir,total_nbins,weights_to_apply,"ttcc","Down" , normalization = 1,postfix=standardpostfix+"_ttccMCStatDown")
        #         outf_.cd()
        #         final_hist_tmp_.Write()
        #         
        #         # ttcj Up
        #         weights_to_apply = "weight_ctag_iterativefit*weight_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
        #         final_hist_tmp_ = FillMCHistogram_MCStat(entry_dict,hist_dict,indir,total_nbins,weights_to_apply,"ttcj","Up" , normalization = 1,postfix=standardpostfix+"_ttcjMCStatUp")
        #         outf_.cd()
        #         final_hist_tmp_.Write()
        #         # ttcj Down
        #         weights_to_apply = "weight_ctag_iterativefit*weight_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
        #         final_hist_tmp_ = FillMCHistogram_MCStat(entry_dict,hist_dict,indir,total_nbins,weights_to_apply,"ttcj","Down" , normalization = 1,postfix=standardpostfix+"_ttcjMCStatDown")
        #         outf_.cd()
        #         final_hist_tmp_.Write()
        #         
        #         # ttjj Up
        #         weights_to_apply = "weight_ctag_iterativefit*weight_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
        #         final_hist_tmp_ = FillMCHistogram_MCStat(entry_dict,hist_dict,indir,total_nbins,weights_to_apply,"ttjj","Up" , normalization = 1,postfix=standardpostfix+"_ttjjMCStatUp")
        #         outf_.cd()
        #         final_hist_tmp_.Write()
        #         # ttjj Down
        #         weights_to_apply = "weight_ctag_iterativefit*weight_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
        #         final_hist_tmp_ = FillMCHistogram_MCStat(entry_dict,hist_dict,indir,total_nbins,weights_to_apply,"ttjj","Down" , normalization = 1,postfix=standardpostfix+"_ttjjMCStatDown")
        #         outf_.cd()
        #         final_hist_tmp_.Write()
        #         
        #         # zjets Up
        #         weights_to_apply = "weight_ctag_iterativefit*weight_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
        #         final_hist_tmp_ = FillMCHistogram_MCStat(entry_dict,hist_dict,indir,total_nbins,weights_to_apply,"zjets","Up" , normalization = 1,postfix=standardpostfix+"_zjetsMCStatUp")
        #         outf_.cd()
        #         final_hist_tmp_.Write()
        #         # zjets Down
        #         weights_to_apply = "weight_ctag_iterativefit*weight_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
        #         final_hist_tmp_ = FillMCHistogram_MCStat(entry_dict,hist_dict,indir,total_nbins,weights_to_apply,"zjets","Down" , normalization = 1,postfix=standardpostfix+"_zjetsMCStatDown")
        #         outf_.cd()
        #         final_hist_tmp_.Write()
        #         
        #         # singletop Up
        #         weights_to_apply = "weight_ctag_iterativefit*weight_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
        #         final_hist_tmp_ = FillMCHistogram_MCStat(entry_dict,hist_dict,indir,total_nbins,weights_to_apply,"singletop","Up" , normalization = 1,postfix=standardpostfix+"_singletopMCStatUp")
        #         outf_.cd()
        #         final_hist_tmp_.Write()
        #         # singletop Down
        #         weights_to_apply = "weight_ctag_iterativefit*weight_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
        #         final_hist_tmp_ = FillMCHistogram_MCStat(entry_dict,hist_dict,indir,total_nbins,weights_to_apply,"singletop","Down" , normalization = 1,postfix=standardpostfix+"_singletopMCStatDown")
        #         outf_.cd()
        #         final_hist_tmp_.Write()
        #         
        #         # rare Up
        #         weights_to_apply = "weight_ctag_iterativefit*weight_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
        #         final_hist_tmp_ = FillMCHistogram_MCStat(entry_dict,hist_dict,indir,total_nbins,weights_to_apply,"rare","Up" , normalization = 1,postfix=standardpostfix+"_rareMCStatUp")
        #         outf_.cd()
        #         final_hist_tmp_.Write()
        #         # rare Down
        #         weights_to_apply = "weight_ctag_iterativefit*weight_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
        #         final_hist_tmp_ = FillMCHistogram_MCStat(entry_dict,hist_dict,indir,total_nbins,weights_to_apply,"rare","Down" , normalization = 1,postfix=standardpostfix+"_rareMCStatDown")
        #         outf_.cd()
        #         final_hist_tmp_.Write()


        if options_dict["cTagCalib"] == True:
            # Ctag Total systematic Up
            # weights_to_apply = "weight_ctag_iterativefit_Up*weight_bcjets_btag_DeepCSVMedium*weight_udsgjets_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
# 			final_hist_tmp_ = FillMCHistogram(entry_dict,hist_dict,indir,total_nbins,weights_to_apply, normalization = total_yield_nominal, postfix=standardpostfix+"_cTagCalibUp")
# 			outf_.cd()
# 			final_hist_tmp_.Write()
# 			# Ctag Total systematic Down
# 			weights_to_apply = "weight_ctag_iterativefit_Down*weight_bcjets_btag_DeepCSVMedium*weight_udsgjets_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
# 			final_hist_tmp_ = FillMCHistogram(entry_dict,hist_dict,indir,total_nbins,weights_to_apply, normalization = total_yield_nominal, postfix=standardpostfix+"_cTagCalibDown")
# 			outf_.cd()
# 			final_hist_tmp_.Write()
            # Ctag JES systematic Up
            weights_to_apply = "weight_ctag_iterativefit_JESUp*weight_bcjets_btag_DeepCSVMedium*weight_udsgjets_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
            final_hist_tmp_ = FillMCHistogram(entry_dict,hist_dict,indir,total_nbins,weights_to_apply, normalization = total_yield_nominal, postfix=standardpostfix+"_cTagCalibJESUp")
            outf_.cd()
            final_hist_tmp_.Write()
            # Ctag JES systematic Down
            weights_to_apply = "weight_ctag_iterativefit_JESDown*weight_bcjets_btag_DeepCSVMedium*weight_udsgjets_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
            final_hist_tmp_ = FillMCHistogram(entry_dict,hist_dict,indir,total_nbins,weights_to_apply, normalization = total_yield_nominal, postfix=standardpostfix+"_cTagCalibJESDown")
            outf_.cd()
            final_hist_tmp_.Write()
            # Ctag JER systematic Up
            weights_to_apply = "weight_ctag_iterativefit_JERUp*weight_bcjets_btag_DeepCSVMedium*weight_udsgjets_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
            final_hist_tmp_ = FillMCHistogram(entry_dict,hist_dict,indir,total_nbins,weights_to_apply, normalization = total_yield_nominal, postfix=standardpostfix+"_cTagCalibJERUp")
            outf_.cd()
            final_hist_tmp_.Write()
            # Ctag JER systematic Down
            weights_to_apply = "weight_ctag_iterativefit_JERDown*weight_bcjets_btag_DeepCSVMedium*weight_udsgjets_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
            final_hist_tmp_ = FillMCHistogram(entry_dict,hist_dict,indir,total_nbins,weights_to_apply, normalization = total_yield_nominal, postfix=standardpostfix+"_cTagCalibJERDown")
            outf_.cd()
            final_hist_tmp_.Write()
            # Ctag PU systematic Up
#             weights_to_apply = "weight_ctag_iterativefit_PUUp*weight_bcjets_btag_DeepCSVMedium*weight_udsgjets_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
#             final_hist_tmp_ = FillMCHistogram(entry_dict,hist_dict,indir,total_nbins,weights_to_apply, normalization = total_yield_nominal, postfix=standardpostfix+"_cTagCalibPUUp")
#             outf_.cd()
#             final_hist_tmp_.Write()
#             Ctag PU systematic Down
#             weights_to_apply = "weight_ctag_iterativefit_PUDown*weight_bcjets_btag_DeepCSVMedium*weight_udsgjets_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
#             final_hist_tmp_ = FillMCHistogram(entry_dict,hist_dict,indir,total_nbins,weights_to_apply, normalization = total_yield_nominal, postfix=standardpostfix+"_cTagCalibPUDown")
#             outf_.cd()
#             final_hist_tmp_.Write()
            # Ctag btag systematic Up
            weights_to_apply = "weight_ctag_iterativefit_btagUp*weight_bcjets_btag_DeepCSVMedium*weight_udsgjets_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
            final_hist_tmp_ = FillMCHistogram(entry_dict,hist_dict,indir,total_nbins,weights_to_apply, normalization = total_yield_nominal, postfix=standardpostfix+"_cTagCalibbtagUp")
            outf_.cd()
            final_hist_tmp_.Write()
            # Ctag btag systematic Down
            weights_to_apply = "weight_ctag_iterativefit_btagDown*weight_bcjets_btag_DeepCSVMedium*weight_udsgjets_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
            final_hist_tmp_ = FillMCHistogram(entry_dict,hist_dict,indir,total_nbins,weights_to_apply, normalization = total_yield_nominal, postfix=standardpostfix+"_cTagCalibbtagDown")
            outf_.cd()
            final_hist_tmp_.Write()
            # Ctag Tune systematic Up
            weights_to_apply = "weight_ctag_iterativefit_TuneUp*weight_bcjets_btag_DeepCSVMedium*weight_udsgjets_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
            final_hist_tmp_ = FillMCHistogram(entry_dict,hist_dict,indir,total_nbins,weights_to_apply, normalization = total_yield_nominal, postfix=standardpostfix+"_cTagCalibTuneUp")
            outf_.cd()
            final_hist_tmp_.Write()
            # Ctag Tune systematic Down
            weights_to_apply = "weight_ctag_iterativefit_TuneDown*weight_bcjets_btag_DeepCSVMedium*weight_udsgjets_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
            final_hist_tmp_ = FillMCHistogram(entry_dict,hist_dict,indir,total_nbins,weights_to_apply, normalization = total_yield_nominal, postfix=standardpostfix+"_cTagCalibTuneDown")
            outf_.cd()
            final_hist_tmp_.Write()
            # Ctag hdamp systematic Up
            weights_to_apply = "weight_ctag_iterativefit_hdampUp*weight_bcjets_btag_DeepCSVMedium*weight_udsgjets_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
            final_hist_tmp_ = FillMCHistogram(entry_dict,hist_dict,indir,total_nbins,weights_to_apply, normalization = total_yield_nominal, postfix=standardpostfix+"_cTagCalibhdampUp")
            outf_.cd()
            final_hist_tmp_.Write()
            # Ctag hdamp systematic Down
            weights_to_apply = "weight_ctag_iterativefit_hdampDown*weight_bcjets_btag_DeepCSVMedium*weight_udsgjets_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
            final_hist_tmp_ = FillMCHistogram(entry_dict,hist_dict,indir,total_nbins,weights_to_apply, normalization = total_yield_nominal, postfix=standardpostfix+"_cTagCalibhdampDown")
            outf_.cd()
            final_hist_tmp_.Write()
            # Ctag muR systematic Up
            weights_to_apply = "weight_ctag_iterativefit_muRUp*weight_bcjets_btag_DeepCSVMedium*weight_udsgjets_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
            final_hist_tmp_ = FillMCHistogram(entry_dict,hist_dict,indir,total_nbins,weights_to_apply, normalization = total_yield_nominal, postfix=standardpostfix+"_cTagCalibmuRUp")
            outf_.cd()
            final_hist_tmp_.Write()
            # Ctag muR systematic Down
            weights_to_apply = "weight_ctag_iterativefit_muRDown*weight_bcjets_btag_DeepCSVMedium*weight_udsgjets_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
            final_hist_tmp_ = FillMCHistogram(entry_dict,hist_dict,indir,total_nbins,weights_to_apply, normalization = total_yield_nominal, postfix=standardpostfix+"_cTagCalibmuRDown")
            outf_.cd()
            final_hist_tmp_.Write()
            # Ctag muF systematic Up
            weights_to_apply = "weight_ctag_iterativefit_muFUp*weight_bcjets_btag_DeepCSVMedium*weight_udsgjets_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
            final_hist_tmp_ = FillMCHistogram(entry_dict,hist_dict,indir,total_nbins,weights_to_apply, normalization = total_yield_nominal, postfix=standardpostfix+"_cTagCalibmuFUp")
            outf_.cd()
            final_hist_tmp_.Write()
            # Ctag muF systematic Down
            weights_to_apply = "weight_ctag_iterativefit_muFDown*weight_bcjets_btag_DeepCSVMedium*weight_udsgjets_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
            final_hist_tmp_ = FillMCHistogram(entry_dict,hist_dict,indir,total_nbins,weights_to_apply, normalization = total_yield_nominal, postfix=standardpostfix+"_cTagCalibmuFDown")
            outf_.cd()
            final_hist_tmp_.Write()
        

        if options_dict["bTagCalibHF"] == True:
            # btag (Medium) systematic Up
            weights_to_apply = "weight_ctag_iterativefit*weight_bcjets_btag_DeepCSVMediumUp*weight_udsgjets_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
            final_hist_tmp_ = FillMCHistogram(entry_dict,hist_dict,indir,total_nbins,weights_to_apply, normalization = total_yield_nominal, postfix=standardpostfix+"_bTagCalibHFUp")
            outf_.cd()
            final_hist_tmp_.Write()
            # btag (Medium) systematic Down
            weights_to_apply = "weight_ctag_iterativefit*weight_bcjets_btag_DeepCSVMediumDown*weight_udsgjets_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
            final_hist_tmp_ = FillMCHistogram(entry_dict,hist_dict,indir,total_nbins,weights_to_apply, normalization = total_yield_nominal, postfix=standardpostfix+"_bTagCalibHFDown")
            outf_.cd()
            final_hist_tmp_.Write()
    
        if options_dict["bTagCalibLF"] == True:
            # btag (Medium) systematic Up
            weights_to_apply = "weight_ctag_iterativefit*weight_bcjets_btag_DeepCSVMedium*weight_udsgjets_btag_DeepCSVMediumUp*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
            final_hist_tmp_ = FillMCHistogram(entry_dict,hist_dict,indir,total_nbins,weights_to_apply, normalization = total_yield_nominal, postfix=standardpostfix+"_bTagCalibLFUp")
            outf_.cd()
            final_hist_tmp_.Write()
            # btag (Medium) systematic Down
            weights_to_apply = "weight_ctag_iterativefit*weight_bcjets_btag_DeepCSVMedium*weight_udsgjets_btag_DeepCSVMediumDown*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
            final_hist_tmp_ = FillMCHistogram(entry_dict,hist_dict,indir,total_nbins,weights_to_apply, normalization = total_yield_nominal, postfix=standardpostfix+"_bTagCalibLFDown")
            outf_.cd()
            final_hist_tmp_.Write()

        if options_dict["PU"] == True:
            # PU up
            weights_to_apply = "weight_ctag_iterativefit_PUUp*weight_bcjets_btag_DeepCSVMedium*weight_udsgjets_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight_up"
            final_hist_tmp_ = FillMCHistogram(entry_dict,hist_dict,indir,total_nbins,weights_to_apply, normalization = total_yield_nominal, postfix=standardpostfix+"_puUp")
            outf_.cd()
            final_hist_tmp_.Write()
            # PU down
            weights_to_apply = "weight_ctag_iterativefit_PUDown*weight_bcjets_btag_DeepCSVMedium*weight_udsgjets_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight_down"
            final_hist_tmp_ = FillMCHistogram(entry_dict,hist_dict,indir,total_nbins,weights_to_apply, normalization = total_yield_nominal, postfix=standardpostfix+"_puDown")
            outf_.cd()
            final_hist_tmp_.Write()

        if options_dict["muF"] == True and not (entry_dict["tag"] == "bkg"):
            # muF Up (2)
            weights_to_apply = "weight_ctag_iterativefit*weight_bcjets_btag_DeepCSVMedium*weight_udsgjets_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*weight_scale_muF2*pu_weight"
            final_hist_tmp_ = FillMCHistogram(entry_dict,hist_dict,indir,total_nbins,weights_to_apply, normalization = total_yield_nominal, postfix=standardpostfix+"_muFUp")
            outf_.cd()
            final_hist_tmp_.Write()
            # muF Down (0.5)
            weights_to_apply = "weight_ctag_iterativefit*weight_bcjets_btag_DeepCSVMedium*weight_udsgjets_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*weight_scale_muF0p5*pu_weight"
            final_hist_tmp_ = FillMCHistogram(entry_dict,hist_dict,indir,total_nbins,weights_to_apply, normalization = total_yield_nominal, postfix=standardpostfix+"_muFDown")
            outf_.cd()
            final_hist_tmp_.Write()

        if options_dict["muR"] == True and not (entry_dict["tag"] == "bkg"):
            # muR Up (2)
            weights_to_apply = "weight_ctag_iterativefit*weight_bcjets_btag_DeepCSVMedium*weight_udsgjets_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*weight_scale_muR2*pu_weight"
            final_hist_tmp_ = FillMCHistogram(entry_dict,hist_dict,indir,total_nbins,weights_to_apply, normalization = total_yield_nominal, postfix=standardpostfix+"_muRDown")
            outf_.cd()
            final_hist_tmp_.Write()
            # muR Down (0.5)
            weights_to_apply = "weight_ctag_iterativefit*weight_bcjets_btag_DeepCSVMedium*weight_udsgjets_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*weight_scale_muR0p5*pu_weight"
            final_hist_tmp_ = FillMCHistogram(entry_dict,hist_dict,indir,total_nbins,weights_to_apply, normalization = total_yield_nominal, postfix=standardpostfix+"_muRUp")
            outf_.cd()
            final_hist_tmp_.Write()

        if options_dict["ElectronID"] == True:
            # electron ID Up
            weights_to_apply = "weight_ctag_iterativefit*weight_bcjets_btag_DeepCSVMedium*weight_udsgjets_btag_DeepCSVMedium*weight_electron_id_Up*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
            final_hist_tmp_ = FillMCHistogram(entry_dict,hist_dict,indir,total_nbins,weights_to_apply, normalization = total_yield_nominal, postfix=standardpostfix+"_ElectronIDUp")
            outf_.cd()
            final_hist_tmp_.Write()
            # electron ID Down
            weights_to_apply = "weight_ctag_iterativefit*weight_bcjets_btag_DeepCSVMedium*weight_udsgjets_btag_DeepCSVMedium*weight_electron_id_Down*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
            final_hist_tmp_ = FillMCHistogram(entry_dict,hist_dict,indir,total_nbins,weights_to_apply, normalization = total_yield_nominal, postfix=standardpostfix+"_ElectronIDDown")
            outf_.cd()
            final_hist_tmp_.Write()

        if options_dict["ElectronReco"] == True:
            # electron Reconstruction Up
            weights_to_apply = "weight_ctag_iterativefit*weight_bcjets_btag_DeepCSVMedium*weight_udsgjets_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco_Up*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
            final_hist_tmp_ = FillMCHistogram(entry_dict,hist_dict,indir,total_nbins,weights_to_apply, normalization = total_yield_nominal, postfix=standardpostfix+"_ElectronRecoUp")
            outf_.cd()
            final_hist_tmp_.Write()
            # electron Reconstruction Down
            weights_to_apply = "weight_ctag_iterativefit*weight_bcjets_btag_DeepCSVMedium*weight_udsgjets_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco_Down*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
            final_hist_tmp_ = FillMCHistogram(entry_dict,hist_dict,indir,total_nbins,weights_to_apply, normalization = total_yield_nominal, postfix=standardpostfix+"_ElectronRecoDown")
            outf_.cd()
            final_hist_tmp_.Write()

        if options_dict["MuonID"] == True:
            # muon ID Up
            weights_to_apply = "weight_ctag_iterativefit*weight_bcjets_btag_DeepCSVMedium*weight_udsgjets_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id_Up*weight_muon_iso*mc_weight*pu_weight"
            final_hist_tmp_ = FillMCHistogram(entry_dict,hist_dict,indir,total_nbins,weights_to_apply, normalization = total_yield_nominal, postfix=standardpostfix+"_MuonIDUp")
            outf_.cd()
            final_hist_tmp_.Write()
            # muon ID Down
            weights_to_apply = "weight_ctag_iterativefit*weight_bcjets_btag_DeepCSVMedium*weight_udsgjets_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id_Down*weight_muon_iso*mc_weight*pu_weight"
            final_hist_tmp_ = FillMCHistogram(entry_dict,hist_dict,indir,total_nbins,weights_to_apply, normalization = total_yield_nominal, postfix=standardpostfix+"_MuonIDDown")
            outf_.cd()
            final_hist_tmp_.Write()

        if options_dict["MuonIso"] == True:
            # muon Isolation Up
            weights_to_apply = "weight_ctag_iterativefit*weight_bcjets_btag_DeepCSVMedium*weight_udsgjets_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso_Up*mc_weight*pu_weight"
            final_hist_tmp_ = FillMCHistogram(entry_dict,hist_dict,indir,total_nbins,weights_to_apply, normalization = total_yield_nominal, postfix=standardpostfix+"_MuonIsoUp")
            outf_.cd()
            final_hist_tmp_.Write()
            # muon Isolation Down
            weights_to_apply = "weight_ctag_iterativefit*weight_bcjets_btag_DeepCSVMedium*weight_udsgjets_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso_Down*mc_weight*pu_weight"
            final_hist_tmp_ = FillMCHistogram(entry_dict,hist_dict,indir,total_nbins,weights_to_apply, normalization = total_yield_nominal, postfix=standardpostfix+"_MuonIsoDown")
            outf_.cd()
            final_hist_tmp_.Write()
    
    

    #*************************************************************
    #
    # Process Data
    #
    #*************************************************************
    if options_dict["doData"] == True:
        for idx,entry_dict in display_dict.iteritems():
            if not entry_dict["legend"]=="data": continue

            total_nbins=ExtractNBins(hist_dict)
            final_hist_tmp_ = FillDataHistogram(entry_dict,hist_dict,indir,total_nbins)
            outf_.cd()
            final_hist_tmp_.Write()

        outf_.Close()




def main():

    # 
    # HOW TO CALCULATE LUMI
    #    https://cms-service-lumi.web.cern.ch/cms-service-lumi/brilwsdoc.html
    # 
    # export PATH=$HOME/.local/bin:/afs/cern.ch/cms/lumi/brilconda-1.1.7/bin:$PATH
    # 
    # brilcalc lumi --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -i ./Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt
    #


    parser = ArgumentParser()
    parser.add_argument('--indir', default="FILL",help='input directory that contains all the samples')
    parser.add_argument('--outdir', default=os.getcwd(),help='name of output directory')
    parser.add_argument('--outfile', default="testCombineOutput.root",help='name of output root file to be used with combine')
    args = parser.parse_args()

    #weight_string = "weight_btag_iterativefit*weight_electron_id*weight_electron_reco*weight_electron_trig*weight_muon_id*weight_muon_iso*weight_muon_trig*pu_weight*mc_weight"
    # weight_string = "weight_btag_iterativefit*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight"#*pu_weight"
#     weight_string_withcTagWeights = "weight_btag_iterativefit*weight_ctag_iterativefit*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight"#*pu_weight"
#     weight_string_noPUweights = "weight_btag_iterativefit*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight"
#     weights_string_noBtagWeights = "weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*pu_weight*mc_weight"
#     
#     no_weights = "1"
#     lepton_channel="inclusive"#"mumu"#"elmu","inclusive","elel"
#     

    #custom_bins_CvsL = [ 0.,0.075,0.1,0.125,0.15,0.2,0.25,0.3,0.35,0.45,0.6,0.8,1.0]
    #custom_bins_CvsB = [ 0.,0.2,0.35,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,1.0]
    #custom_bins_CvsL = [ 0.,0.3,0.5,0.7,1.0]
    #custom_bins_CvsB = [ 0.,0.3,0.5,0.7,1.0]
    #custom_bins_CvsL = [ 0.,0.25,0.4,0.5,0.7,0.8,0.9,1.0]
    #custom_bins_CvsB = [ 0.,0.2,0.3,0.4,0.45,0.5,0.6,1.0]

    #custom_bins_CvsL = [ 0.,0.25,0.4,0.6,0.8,1.0]
    #custom_bins_CvsB = [ 0.,0.25,0.4,0.5,0.55,1.0]
    custom_bins_CvsL = [ 0.,0.25,0.4,0.55,0.7,1.0]
    custom_bins_CvsB = [ 0.,0.25,0.4,0.5,0.55,1.0]

    charm_histo_dict = OrderedDict()
    charm_histo_dict["addJet1"] = OrderedDict()
    charm_histo_dict["addJet1"]["ttHF_selector_NN_CvsL"]=custom_bins_CvsL
    charm_histo_dict["addJet1"]["ttHF_selector_NN_CvsB"]=custom_bins_CvsB
    # charm_histo_dict["addJet2"] = OrderedDict()
#     charm_histo_dict["addJet2"]["DeepCSVcTagCvsL_addJet2"]=custom_bins_CvsL
#     charm_histo_dict["addJet2"]["DeepCSVcTagCvsB_addJet2"]=custom_bins_CvsB
    
    
    #
    # DERIVE NORMALIZATIONS OF NOMINAL SAMPLES
    #
    nominal_yields_dict = {}
    display_dict = make_display_dict(ttbarnames = ["TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS","TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS","TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS"])
    for idx,entry_dict in display_dict.iteritems():
        if entry_dict["legend"]=="data": continue
        total_nbins=ExtractNBins(charm_histo_dict)
        weights_to_apply = "weight_ctag_iterativefit*weight_bcjets_btag_DeepCSVMedium*weight_udsgjets_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
        final_hist_tmp_ = FillMCHistogram(entry_dict,charm_histo_dict,args.indir,total_nbins,weights_to_apply, normalization = -1, postfix = "")
        total_yield_nominal = final_hist_tmp_.Integral()
        print entry_dict["tag"], total_yield_nominal
        nominal_yields_dict[entry_dict["tag"]] = total_yield_nominal
    
    
    

    #print charm_histo_dict["DeepCSVcTagCvsL_addJet1"][-1]
    options_dict={
        "cTagCalib":True,
        "bTagCalibHF":True,
        "bTagCalibLF":True,
        "PU":True,
        "muF":True,
        "muR":True,
        "ElectronID":True,
        "ElectronReco":True,
        "MuonID":True,
        "MuonIso":True,
        "doData":True,
    }

    MakeRoot1D(charm_histo_dict,args.indir,args.outdir+"/"+args.outfile,options_dict,ttbarnames = ["TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS","TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS","TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS"],standardpostfix="",norm_dict = nominal_yields_dict)



    # For JES and JER, hdamp, TuneCP5,... use different ttbar files
    options_dict={
        "cTagCalib":False,
        "bTagCalibHF":False,
        "bTagCalibLF":False,
        "PU":False,
        "muF":False,
        "muR":False,
        "ElectronID":False,
        "ElectronReco":False,
        "MuonID":False,
        "MuonIso":False,
        "doData":False,
    }

    #JES
    MakeRoot1D(charm_histo_dict,args.indir,args.outdir+"/"+args.outfile,options_dict,ttbarnames = ["TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS_JESUp","TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS_JESUp","TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS_JESUp"],standardpostfix="_JESUp",norm_dict = nominal_yields_dict)
    MakeRoot1D(charm_histo_dict,args.indir,args.outdir+"/"+args.outfile,options_dict,ttbarnames = ["TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS_JESDown","TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS_JESDown","TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS_JESDown"],standardpostfix="_JESDown",norm_dict = nominal_yields_dict)
    #JER
    MakeRoot1D(charm_histo_dict,args.indir,args.outdir+"/"+args.outfile,options_dict,ttbarnames = ["TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS_JERUp","TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS_JERUp","TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS_JERUp"],standardpostfix="_JERUp",norm_dict = nominal_yields_dict)
    MakeRoot1D(charm_histo_dict,args.indir,args.outdir+"/"+args.outfile,options_dict,ttbarnames = ["TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS_JERDown","TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS_JERDown","TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS_JERDown"],standardpostfix="_JERDown",norm_dict = nominal_yields_dict)

    #hdamp
    MakeRoot1D(charm_histo_dict,args.indir,args.outdir+"/"+args.outfile,options_dict,ttbarnames = ["TTTo2L2Nu_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS","TTToSemiLeptonic_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS","TTToHadronic_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS"],standardpostfix="_hdampDown",norm_dict = nominal_yields_dict)
    MakeRoot1D(charm_histo_dict,args.indir,args.outdir+"/"+args.outfile,options_dict,ttbarnames = ["TTTo2L2Nu_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS","TTToSemiLeptonic_hdampUp_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS","TTToHadronic_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS"],standardpostfix="_hdampUp",norm_dict = nominal_yields_dict)

    #Tune (UE)
    MakeRoot1D(charm_histo_dict,args.indir,args.outdir+"/"+args.outfile,options_dict,ttbarnames = ["TTTo2L2Nu_TuneCP5down_PSweights_13TeV-powheg-pythia8_VisiblePS","TTToSemiLeptonic_TuneCP5down_PSweights_13TeV-powheg-pythia8_VisiblePS","TTToHadronic_TuneCP5down_PSweights_13TeV-powheg-pythia8_VisiblePS"],standardpostfix="_TuneCP5Down",norm_dict = nominal_yields_dict)
    MakeRoot1D(charm_histo_dict,args.indir,args.outdir+"/"+args.outfile,options_dict,ttbarnames = ["TTTo2L2Nu_TuneCP5up_PSweights_13TeV-powheg-pythia8_VisiblePS","TTToSemiLeptonic_TuneCP5up_PSweights_13TeV-powheg-pythia8_VisiblePS","TTToHadronic_TuneCP5up_PSweights_13TeV-powheg-pythia8_VisiblePS"],standardpostfix="_TuneCP5Up",norm_dict = nominal_yields_dict)






    # custom_bins_DeepCSVBdiscr = [ 0.,0.025,0.05,0.1,0.15,0.2,0.25,0.35,0.45,0.6,0.8,1.0]
#     Plot1D("DeepCSVBDiscr_addJet1","DeepCSVBDiscr Discriminator first add. jet","Events",len(custom_bins_DeepCSVBdiscr)-1,min(custom_bins_DeepCSVBdiscr),max(custom_bins_DeepCSVBdiscr),use_custom_bins = 1,custom_bins =custom_bins_DeepCSVBdiscr,logy=1,overflow=0,underflow=1,weights_to_apply=weight_string,lepton_category=lepton_channel)#,AddSystUnc = True)
#     Plot1D("DeepCSVBDiscr_addJet2","DeepCSVBDiscr Discriminator second add. jet","Events",len(custom_bins_DeepCSVBdiscr)-1,min(custom_bins_DeepCSVBdiscr),max(custom_bins_DeepCSVBdiscr),use_custom_bins = 1,custom_bins =custom_bins_DeepCSVBdiscr,logy=1,overflow=0,underflow=1,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     Plot1D("DeepCSVBDiscr_addJet1","DeepCSVBDiscr Discriminator first add. jet (w. cTag weights)","Events",len(custom_bins_DeepCSVBdiscr)-1,min(custom_bins_DeepCSVBdiscr),max(custom_bins_DeepCSVBdiscr),use_custom_bins = 1,custom_bins =custom_bins_DeepCSVBdiscr,logy=1,overflow=0,underflow=1,weights_to_apply=weight_string_withcTagWeights,lepton_category=lepton_channel,suffix="_WithcTagWeights")#,AddSystUnc = True)
#     Plot1D("DeepCSVBDiscr_addJet2","DeepCSVBDiscr Discriminator second add. jet (w. cTag weights)","Events",len(custom_bins_DeepCSVBdiscr)-1,min(custom_bins_DeepCSVBdiscr),max(custom_bins_DeepCSVBdiscr),use_custom_bins = 1,custom_bins =custom_bins_DeepCSVBdiscr,logy=1,overflow=0,underflow=1,weights_to_apply=weight_string_withcTagWeights,lepton_category=lepton_channel,suffix="_WithcTagWeights")#,AddSystUnc = True)

    # Plot1D("DeepCSVcTagCvsL_addJet1","DeepCSV CvsL Discriminator first add. jet","Events",len(custom_bins_CvsL)-1,min(custom_bins_CvsL),max(custom_bins_CvsL),use_custom_bins = 1,custom_bins =custom_bins_CvsL,logy=1,overflow=0,underflow=1,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     Plot1D("DeepCSVcTagCvsL_addJet2","DeepCSV CvsL Discriminator second add. jet","Events",len(custom_bins_CvsL)-1,min(custom_bins_CvsL),max(custom_bins_CvsL),use_custom_bins = 1,custom_bins =custom_bins_CvsL,logy=1,overflow=0,underflow=1,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     
#     
#     Plot1D("DeepCSVcTagCvsB_addJet1","DeepCSV CvsB Discriminator first add. jet","Events",len(custom_bins_CvsB)-1,min(custom_bins_CvsB),max(custom_bins_CvsB),use_custom_bins = 1,custom_bins =custom_bins_CvsB,logy=1,overflow=0,underflow=1,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     Plot1D("DeepCSVcTagCvsB_addJet2","DeepCSV CvsB Discriminator second add. jet","Events",len(custom_bins_CvsB)-1,min(custom_bins_CvsB),max(custom_bins_CvsB),use_custom_bins = 1,custom_bins =custom_bins_CvsB,logy=1,overflow=0,underflow=1,weights_to_apply=weight_string,lepton_category=lepton_channel)
#     Plot1D("DeepCSVcTagCvsB_addJet1","DeepCSV CvsB Discriminator first add. jet (w. cTag weights)","Events",len(custom_bins_CvsB)-1,min(custom_bins_CvsB),max(custom_bins_CvsB),use_custom_bins = 1,custom_bins =custom_bins_CvsB,logy=1,overflow=0,underflow=1,weights_to_apply=weight_string_withcTagWeights,lepton_category=lepton_channel,suffix="_WithcTagWeights")#,AddSystUnc = True)
#     Plot1D("DeepCSVcTagCvsB_addJet2","DeepCSV CvsB Discriminator second add. jet (w. cTag weights)","Events",len(custom_bins_CvsB)-1,min(custom_bins_CvsB),max(custom_bins_CvsB),use_custom_bins = 1,custom_bins =custom_bins_CvsB,logy=1,overflow=0,underflow=1,weights_to_apply=weight_string_withcTagWeights,lepton_category=lepton_channel,suffix="_WithcTagWeights")#,AddSystUnc = True)


if __name__ == "__main__":
    main()
