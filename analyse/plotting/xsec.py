xsec_table = {
    "ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4":38.09,
    "ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4":38.09,
    "ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1":3.36 ,
    "ST_t-channel_top_4f_inclusiveDecays_TuneCUETP8M2T4_13TeV-powhegV2-madspin":44.33,
    "ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1":26.38 , 
    "WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":61526.7,
    "DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8":6025.2,
    "DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8": 18610,
    "TT_TuneCUETP8M2T4_13TeV-powheg-pythia8": 831.76,
    "ttZJets_13TeV_madgraphMLM":0.7826,
    "ttWJets_13TeV_madgraphMLM":0.6105,
    "ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8": 0.103    
}

color_table = {
    "ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4":433,#kCyan+1
    "ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4":433,#kCyan+1
    "ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1":433,#kCyan+1
    "ST_t-channel_top_4f_inclusiveDecays_TuneCUETP8M2T4_13TeV-powhegV2-madspin":433,#kCyan+1
    "ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1":433,#kCyan+1 
    "WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":418,#kGreen+2
    "DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8":600, #kBlue
    "DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8": 600, #kBlue
    "TT_TuneCUETP8M2T4_13TeV-powheg-pythia8": 633,#kRed+1
    "ttZJets_13TeV_madgraphMLM":617, #kMagenta+1,
    "ttWJets_13TeV_madgraphMLM":920, #kGrey
    "ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8": 1 #kBlack    
}

legend_array = [
	["t#bar{t}",color_table["TT_TuneCUETP8M2T4_13TeV-powheg-pythia8"]],
	["Single top",color_table["ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4"]],
	["W + jets",color_table["WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"]],
	["Z + jets",color_table["DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8"]],
	["ttZ",color_table["ttZJets_13TeV_madgraphMLM"]],
	["ttZ",color_table["ttWJets_13TeV_madgraphMLM"]],
	["ttH (h #rightarrow b#bar{b})",color_table["ttHTobb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8"]]
]
