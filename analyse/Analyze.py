from Helper import *
from argparse import ArgumentParser
import time
import multiprocessing
import thread
import subprocess

def Analyze(infile, outfile):

    infile_ = TFile(infile)
    intree_ = infile_.Get("tree")
    
    ofile_ = TFile(outfile,"RECREATE")
    otree_ = intree_.CloneTree(0)
    
    # **************************** add extra branches to output****************************
    dict_variableName_Leaves = {}
    dict_variableName_Leaves.update({"DileptonInvariantMass": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"DileptonDeltaR": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"hadronFlavour_addJet1": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"hadronFlavour_addJet2": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"partonFlavour_addJet1": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"partonFlavour_addJet2": [array('i', [0]),"I"]})
    dict_variableName_Leaves.update({"CSVv2_addJet1": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"CSVv2_addJet2": [array('d', [0]),"D"]})
    dict_variableName_Leaves.update({"event_Category": [array('i', [0]),"I"]})
    #weights
    dict_variableName_Leaves.update({"weight_btag_iterativefit": [array('d', [0]),"D"]})
    
    for name,arr in dict_variableName_Leaves.iteritems():
        otree_.Branch(name,arr[0],name+"/"+arr[1])
    #****************************************************************************************
    
    nEntries = intree_.GetEntries()
    #nEntries = 1000
    
    print "Processing File %s, containing %i events"%(infile,nEntries)
    
    v_el = ROOT.std.vector( Electron )()
    v_mu = ROOT.std.vector( Muon )()
    v_jet = ROOT.std.vector( Jet )()
    v_trig = ROOT.std.vector( Trigger )()
    
    # ***************** Start event loop ********************
    for evt in range(nEntries):
        if (evt % int(nEntries/10.) == 0): print"%s: Processing event %i/%i (%.1f %%)"%(infile.split("/")[-1],evt,nEntries,100*float(evt)/float(nEntries))
        intree_.GetEntry(evt)
        
        v_el = intree_.Electrons
        v_mu = intree_.Muons
        v_jet = intree_.Jets
        v_trig = intree_.Trigger
        
        # ***************** Trigger ********************
        passAnyTrigger = False
        #iTrig = Trigger()
        for trig in v_trig:
             if trig.Pass(): passAnyTrigger = True
        if not passAnyTrigger: continue
        # *******************************************************
        
        
        # ***************** Leading Electron ********************
        leading_elec = Electron()
        n_isolated_electrons = 0
        for el in v_el:
            if (el.isMedium() and el.relIso() < 0.077 and abs(el.Eta()) < 1.48 and el.Pt() > leading_elec.Pt()): 
                n_isolated_electrons = n_isolated_electrons + 1
                leading_elec = el
            elif (el.isMedium() and el.relIso() < 0.068 and abs(el.Eta()) >= 1.48 and el.Pt() > leading_elec.Pt()): 
                n_isolated_electrons = n_isolated_electrons + 1
                leading_elec = el
        # *******************************************************
        
        # ***************** Leading Muon ********************
        leading_muon = Muon()
        n_isolated_muons = 0
        for mu in v_mu:
             if (mu.isTight() and mu.relIso() < 0.15 and mu.Pt() > leading_muon.Pt()): 
                n_isolated_muons = n_isolated_muons + 1
                leading_muon = mu
        # *******************************************************
        
        
        if (n_isolated_electrons == 1 and n_isolated_muons == 1):
            mll = DileptonIvariantMass(leading_elec,leading_muon)
            if not (mll>12.): continue 
            dict_variableName_Leaves["DileptonInvariantMass"][0][0] = DileptonIvariantMass(leading_elec,leading_muon)#DiLeptonIvariantMass(leading_elec.p4(),leading_muon.p4())
            dict_variableName_Leaves["DileptonDeltaR"][0][0] = DileptonDeltaR(leading_elec,leading_muon)
        else: 
            continue        
        
        # Require OS leptons
        if leading_elec.Charge()*leading_muon.Charge() >= 0: continue
        
        # REMOVE THIS LATER
        #if v_mu.size() > 1 or v_el.size()> 1: continue
        
        # ***************** Jets ********************
        # event category based on jet content
        
        if (not intree_.is_data):
            cat = -1
            if len([j for j in v_jet if j.HadronFlavour() == 5]) >= 4: cat = 0 #ttbb
            elif len([j for j in v_jet if j.HadronFlavour() == 5]) >= 3 and len([j for j in v_jet if j.HadronFlavour() == 4]) >= 1: cat = 1 #ttbc
            elif len([j for j in v_jet if j.HadronFlavour() == 5]) >= 3 and len([j for j in v_jet if j.HadronFlavour() == 4]) < 1: cat = 2 #ttbj
            elif len([j for j in v_jet if j.HadronFlavour() == 5]) >= 2 and len([j for j in v_jet if j.HadronFlavour() == 4]) >= 2: cat = 3 #ttcc
            elif len([j for j in v_jet if j.HadronFlavour() == 5]) >= 2 and len([j for j in v_jet if j.HadronFlavour() == 4]) >= 1: cat = 4 #ttcj
            elif len([j for j in v_jet if j.HadronFlavour() == 5]) >= 2: cat = 5
        
        jclf = JetsClassifier(v_jet)
        jclf.Clean(leading_elec,leading_muon)
        
        jclf.OrderCSVv2()
        
        if not jclf.IsValid(): continue # at least 4 valid jets found with valid CSVv2 values
        
        if not (isCSVv2M(jclf.jets_dict_["leading_top_bjet"][0]) and isCSVv2M(jclf.jets_dict_["subleading_top_bjet"][0])): continue
        
        # https://twiki.cern.ch/twiki/bin/view/CMS/BTagSFMethods
        if (not intree_.is_data): dict_variableName_Leaves["weight_btag_iterativefit"][0][0] = jclf.LeadingTopJet().SfIterativeFitCentral()*jclf.SubLeadingTopJet().SfIterativeFitCentral()*jclf.LeadingAddJet().SfIterativeFitCentral()*jclf.SubLeadingAddJet().SfIterativeFitCentral()
        else: dict_variableName_Leaves["weight_btag_iterativefit"][0][0] = 1.
        
        
        # if (jclf.LeadingTopJet().SfIterativeFitCentral()*jclf.SubLeadingTopJet().SfIterativeFitCentral()*jclf.LeadingAddJet().SfIterativeFitCentral()*jclf.SubLeadingAddJet().SfIterativeFitCentral() == 0):
#             print jclf.LeadingTopJet().SfIterativeFitCentral(),jclf.SubLeadingTopJet().SfIterativeFitCentral(),jclf.LeadingAddJet().SfIterativeFitCentral(),jclf.SubLeadingAddJet().SfIterativeFitCentral()
#             print jclf.LeadingTopJet().CSVv2(),jclf.SubLeadingTopJet().CSVv2(),jclf.LeadingAddJet().CSVv2(),jclf.SubLeadingAddJet().CSVv2()
#             print ""
        #print jclf.LeadingTopJet().GenJetID(), jclf.SubLeadingTopJet().GenJetID(), jclf.LeadingAddJet().GenJetID(), jclf.SubLeadingAddJet().GenJetID()
        
        dict_variableName_Leaves["CSVv2_addJet1"][0][0] = jclf.jets_dict_["leading_add_jet"][0].CSVv2()
        dict_variableName_Leaves["CSVv2_addJet2"][0][0] = jclf.jets_dict_["subleading_add_jet"][0].CSVv2()
        
        if (not intree_.is_data):
            dict_variableName_Leaves["hadronFlavour_addJet1"][0][0] = jclf.jets_dict_["leading_add_jet"][0].HadronFlavour()
            dict_variableName_Leaves["hadronFlavour_addJet2"][0][0] = jclf.jets_dict_["subleading_add_jet"][0].HadronFlavour()
            dict_variableName_Leaves["partonFlavour_addJet1"][0][0] = jclf.jets_dict_["leading_add_jet"][0].PartonFlavour()
            dict_variableName_Leaves["partonFlavour_addJet2"][0][0] = jclf.jets_dict_["subleading_add_jet"][0].PartonFlavour()
            dict_variableName_Leaves["event_Category"][0][0] = cat
        else:
            dict_variableName_Leaves["hadronFlavour_addJet1"][0][0] = -999
            dict_variableName_Leaves["hadronFlavour_addJet2"][0][0] = -999
            dict_variableName_Leaves["partonFlavour_addJet1"][0][0] = -999
            dict_variableName_Leaves["partonFlavour_addJet2"][0][0] = -999
            dict_variableName_Leaves["event_Category"][0][0] = -999

    



        otree_.Fill()

        v_el.clear()
        v_mu.clear()
    # ***************** end of  event loop ********************
    
    print "%s: Selected %i/%i (%.3f%%) of events"%(infile.split("/")[-1],otree_.GetEntries(),nEntries,100*float(otree_.GetEntries())/float(nEntries))
    
    hcount = infile_.Get("hcount")
    hweight = infile_.Get("hweight")
    
    
    ofile_.cd()
    hcount.Write()
    hweight.Write()
    otree_.Write()
    
    ofile_.Close()
    infile_.Close()
    
    
    
    
    



def main():

    parser = ArgumentParser()
    #parser.add_argument('--nevents', type=int, default=-1,help='number of events for each sample')
    parser.add_argument('--tag', default=time.strftime("%a%d%b%Y_%Hh%Mm%Ss"),help='name of output directory')
    parser.add_argument('--ncpu', type=int, default=-1,help='number of CPU to use in parallel')
    args = parser.parse_args()

    workingdir = os.getcwd()

    if not os.path.isdir(workingdir+"/SELECTED_"+args.tag): os.mkdir(workingdir+"/SELECTED_"+args.tag)
    
    indir="/user/smoortga//Analysis/NTupler/CMSSW_8_0_25/src/FlatTree/FlatTreeAnalyzer/ttcc/selection/OUTPUT_TEST_JEC_22022018/SelectedSamples/"
    #filelist = [f for f in os.listdir(indir) if ".root" in f]
    filelist = [f for f in os.listdir(indir)]# if "MuonEG_Run2016C_23Sep2016_v1_MINIAOD.root" in f or "TT_TuneCUETP8M2T4_13TeV-powheg-pythia8.root" in f]
    
    if (args.ncpu < 0 or args.ncpu > multiprocessing.cpu_count()): parallelProcesses = multiprocessing.cpu_count()
    else: parallelProcesses = args.ncpu
    p = multiprocessing.Pool(parallelProcesses)
    print "Using %i parallel processes (%i in total)" %(parallelProcesses,len(filelist))
    
    for f in filelist:
        #Analyze(indir+f,workingdir+"/SELECTED_"+args.tag+"/"+f)
        p.apply_async(Analyze, args = (indir+f,workingdir+"/SELECTED_"+args.tag+"/"+f,))
        
    p.close()
    p.join()
    
    #Analyze(indir+"TT_TuneCUETP8M2T4_13TeV-powheg-pythia8.root",workingdir+"/SELECTED_"+args.tag+"/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8.root")

if __name__ == "__main__":
	main()





# v = ROOT.std.vector( Electron )()
# v.push_back(object)
# v.push_back(object)
# 
# f = TFile("test.root", "recreate")
# mytree = TTree("mytree", "testing tree appending")
# mytree.Branch("electron", v) 
# mytree.Fill()  
# 
# f.WriteTObject(mytree)
# f.Close()
# 
# f = TFile("test.root")
# t = f.Get("mytree")
# nEntries = t.GetEntries()
# print nEntries
# for i in range(nEntries):
#     t.GetEntry(i)
#     el_collection = t.electron
#     print el_collection.size()
#     for el in el_collection:
#         print el.Pt()
#         el.setp4()
# 
