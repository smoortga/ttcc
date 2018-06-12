xsec_table = {
    "ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8":38.09,
    "ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8":38.09,
    "ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8":3.36 ,
    "ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8":44.33,
    "ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8":26.38 , 
    "WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8":50260.0,
    "DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8":5941.0,
    "DYJetsToLL_M-4to50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8": 18610,#CHECK THIS AGAIN!
    "TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8": 831.76,#831.76,
    #"TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8": 88.29
    #"ttZJets_13TeV_madgraphMLM":0.7826,
    #"ttWJets_13TeV_madgraphMLM":0.6105,
    #"ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8": 0.103    
}

color_table = {
    "ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8":433,#kCyan+1
    "ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8":433,#kCyan+1
    "ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8":433,#kCyan+1
    "ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8":433,#kCyan+1
    "ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8":433,#kCyan+1 
    "WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8":418,#kGreen+2
    "DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8":600, #kBlue
    "DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8": 600, #kBlue
    "TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8": 633,#kRed+1
    #"ttZJets_13TeV_madgraphMLM":617, #kMagenta+1,
    #"ttWJets_13TeV_madgraphMLM":617, #kMagenta+1
    #"ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8": 1 #kBlack    
}

legend_array = [
	["t#bar{t}",color_table["TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8"]],
	["Single top",color_table["ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8"]],
	["W + jets",color_table["WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8"]],
	["Z + jets",color_table["DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8"]],
	#["t#bar{t}V",color_table["ttZJets_13TeV_madgraphMLM"]]
	#["ttZ",color_table["ttWJets_13TeV_madgraphMLM"]],
	#["ttH (h #rightarrow b#bar{b})",color_table["ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8"]]
]
