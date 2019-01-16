from argparse import ArgumentParser
import sys
import os
import time
import ROOT

def main():
    
    ROOT.gROOT.SetBatch(1)
    ROOT.gStyle.SetOptStat(0)
    
    parser = ArgumentParser()
    parser.add_argument('--prefile', default="FILLMEPLEASE",help='directory name where to find histogram before any selection')
    parser.add_argument('--postfile', default="FILLMEPLEASE",help='name of input file after the selection')
    args = parser.parse_args()
    

    pre_file = ROOT.TFile(args.prefile)
    pre_hist = pre_file.Get("hist_vis")
    pre_weight_hist = pre_file.Get("hweight")
    
    lumi=41.5
    xsec_dilep = 88.29*1000 #[fb]
    number_original_pre = pre_weight_hist.GetBinContent(1)
    print "# original pre: ", number_original_pre
    
    n_ttother_pre = float(pre_hist.GetBinContent(1)*lumi*xsec_dilep)/float(number_original_pre)
    n_ttbb_pre = float(pre_hist.GetBinContent(2)*lumi*xsec_dilep)/float(number_original_pre)
    n_ttbL_pre = float(pre_hist.GetBinContent(3)*lumi*xsec_dilep)/float(number_original_pre)
    n_ttcc_pre = float(pre_hist.GetBinContent(4)*lumi*xsec_dilep)/float(number_original_pre)
    n_ttcL_pre = float(pre_hist.GetBinContent(5)*lumi*xsec_dilep)/float(number_original_pre)
    n_ttLF_pre = float(pre_hist.GetBinContent(6)*lumi*xsec_dilep)/float(number_original_pre)
    
    print "**************** PRE SELECTION ***********************"
    print " - - - - Lumi: %.2f fb-1, xsec (tt dilepton): %.2f fb - - - - "%(lumi,xsec_dilep)
    print "--> tt+bb: ", n_ttbb_pre
    print "--> tt+bL: ", n_ttbL_pre
    print "--> tt+cc: ", n_ttcc_pre
    print "--> tt+cL: ", n_ttcL_pre
    print "--> tt+LF: ", n_ttLF_pre
    print "--> tt+jj: ", n_ttbb_pre + n_ttbL_pre + n_ttcc_pre + n_ttcL_pre + n_ttLF_pre
    print "--> tt+other: ", n_ttother_pre
    print "******************************************************"
    
    
    
    final_category_dict = {
        "ttbb":0,
        "ttbL":1,
        "ttcc":2,
        "ttcL":3,
        "ttLF":4,
        "ttother":-1,
    }
    
    post_selection_yields_dict = {
        "ttbb":0,
        "ttbL":0,
        "ttcc":0,
        "ttcL":0,
        "ttLF":0,
        "ttother":0,
    }
    
    post_file = ROOT.TFile(args.postfile)
    post_weight_hist = post_file.Get("hweight")
    number_original_post = post_weight_hist.GetBinContent(1)
    print "# original post: ", number_original_post
    post_tree = post_file.Get("tree")
    
    weights_to_apply_tmp = "weight_ctag_iterativefit*weight_btag_DeepCSVMedium*weight_electron_id*weight_electron_reco*weight_muon_id*weight_muon_iso*mc_weight*pu_weight"
    for cat,number in final_category_dict.iteritems():
        hist_tmp = ROOT.TH1D("h_"+cat,";;",1,-99999,999999)
        post_tree.Draw("is_data>>h_"+cat,weights_to_apply_tmp+"*(event_Category_VisiblePS == %s)*(mc_pu_trueNumInt>10 && mc_pu_trueNumInt<70)"%str(number))
        post_selection_yields_dict[cat] = float(hist_tmp.Integral()*lumi*xsec_dilep)/float(number_original_post)
       
        #post_selection_yields_dict[cat] = float(post_tree.GetEntries(weights_to_apply_tmp+"*(event_Category_VisiblePS == %s)"%str(number))*lumi*xsec_dilep)/number_original_post
    
    print "**************** POST SELECTION ***********************"
    print " - - - - Lumi: %.2f fb-1, xsec (tt dilepton): %.2f fb - - - - "%(lumi,xsec_dilep)
    print "--> tt+bb: ", post_selection_yields_dict["ttbb"]
    print "--> tt+bL: ", post_selection_yields_dict["ttbL"]
    print "--> tt+cc: ", post_selection_yields_dict["ttcc"]
    print "--> tt+cL: ", post_selection_yields_dict["ttcL"]
    print "--> tt+LF: ", post_selection_yields_dict["ttLF"]
    print "--> tt+jj: ", post_selection_yields_dict["ttbb"] + post_selection_yields_dict["ttbL"] + post_selection_yields_dict["ttcc"] + post_selection_yields_dict["ttcL"] + post_selection_yields_dict["ttLF"]
    print "--> tt+other: ", post_selection_yields_dict["ttother"]
    print "******************************************************"
    
    
    print "**************** EFFICIENCIES VISIBLE PS ***********************"
    print " - - - - Lumi: %.2f fb-1, xsec (tt dilepton): %.2f fb - - - - "%(lumi,xsec_dilep)
    print "--> tt+bb: ", 100*post_selection_yields_dict["ttbb"]/n_ttbb_pre, " %"
    print "--> tt+bL: ", 100*post_selection_yields_dict["ttbL"]/n_ttbL_pre, " %"
    print "--> tt+cc: ", 100*post_selection_yields_dict["ttcc"]/n_ttcc_pre, " %"
    print "--> tt+cL: ", 100*post_selection_yields_dict["ttcL"]/n_ttcL_pre, " %"
    print "--> tt+LF: ", 100*post_selection_yields_dict["ttLF"]/n_ttLF_pre, " %"
    print "--> tt+jj: ", 100*(post_selection_yields_dict["ttbb"] + post_selection_yields_dict["ttbL"] + post_selection_yields_dict["ttcc"] + post_selection_yields_dict["ttcL"] + post_selection_yields_dict["ttLF"])/(n_ttbb_pre + n_ttbL_pre + n_ttcc_pre + n_ttcL_pre + n_ttLF_pre), " %"
    print "--> tt+other: ", 100*post_selection_yields_dict["ttother"]/n_ttother_pre, " %"
    print "******************************************************"
    
    
    
    
    
if __name__ == "__main__":
	main()