import ROOT
import os
import sys
from argparse import ArgumentParser
from array import array

parser = ArgumentParser()
parser.add_argument('--infile', default="FILL",help='input root file to be used with combine')
parser.add_argument('--outfile', default=os.getcwd()+"/card.txt",help='name of output card (.txt format)')
args = parser.parse_args()

f_ = ROOT.TFile(args.infile)
card_ = open(args.outfile,"wb")

hist_list = [i.GetName() for i in f_.GetListOfKeys()]
print "Found the following histograms: "
for i in hist_list:
    print " ",i
processes = set([i.split("_")[1] for i in hist_list if not "data_obs" in i])
rates = [(f_.Get(i)).Integral() for i in ["h_"+j for j in processes]]
print "Found the following unique processes: "
for idx,i in enumerate(processes):
    print " ",i," : ",rates[idx]," events"
all_systematics = set([i.split("_")[2].replace("Up","").replace("Down","") for i in hist_list if len(i.split("_")) > 2 and not "data_obs" in i])
print "Found the following unique systematicss: "
for i in all_systematics:
    print " ",i

card_.write("imax * # number of channels \n")
card_.write("jmax * # number of backgrounds \n")
card_.write("kmax * # number of nuisance parameters \n")
card_.write("--------------- \n")
card_.write("bin incl \n")
card_.write("observation %i \n"%(f_.Get("h_data_obs")).Integral())
card_.write("--------------- \n")
card_.write("shapes * * %s h_$PROCESS h_$PROCESS_$SYSTEMATIC \n"%args.infile)
card_.write("--------------- \n")
card_.write("bin " + "incl "*len(processes)+"\n")
card_.write("process "+' '.join(processes)+" \n")
card_.write("process "+' '.join([str(i) for i in range(len(processes))])+" \n")
card_.write("rate  "+' '.join([str(round(i,2)) for i in rates])+" \n")
card_.write("--------------- \n")
for sys in all_systematics:
    card_.write(sys + " " + "shape" + " " + "1 "*len(processes) + "\n")
card_.write("--------------- \n")



card_.close()
f_.Close()
print ""
print "******* Summary of the output card *******"
os.system("cat %s"%args.outfile)