import ROOT
import os
import sys
from argparse import ArgumentParser
from array import array

parser = ArgumentParser()
parser.add_argument('--infile', default="FILL",help='input root file to be used with combine')
parser.add_argument('--outfile', default=os.getcwd()+"/card.txt",help='name of output card (.txt format)')
args = parser.parse_args()

process_number_dict = {
	"ttbb":"-4",
	"ttbj":"-3",
	"ttcc":"-2",
	"ttcj":"-1",
	"ttjj":"0",
	"ttother":"1",
	"bkg":"2",
	"singletop":"3",
	"zjets":"4",
	"rare":"5"
}

process_order = ["ttbb","ttbj","ttcc", "ttcj", "ttjj","ttother","bkg"]#"singletop","zjets","rare"]

f_ = ROOT.TFile(args.infile)
card_ = open(args.outfile,"wb")



hist_list = [i.GetName() for i in f_.GetListOfKeys()]
print "Found the following histograms: "
for i in hist_list:
    print " ",i
processes = set([i.split("_")[1] for i in hist_list if not "data_obs" in i])
rates = [(f_.Get(i)).Integral() for i in ["h_"+j for j in process_order]]
print "Found the following unique processes: "
for idx,i in enumerate(process_order):
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
card_.write("bin " + "incl "*len(process_order)+"\n")
card_.write("process "+' '.join(process_order)+" \n")
card_.write("process "+' '.join([process_number_dict[i] for i in process_order])+" \n")
card_.write("rate  "+' '.join([str(round(i,2)) for i in rates])+" \n")
card_.write("--------------- \n")
for sys in all_systematics:
    if "MCStat" in sys:
        continue
        tag = sys.split("MCStat")[0]
        binary_string = " ".join([str(int(i == tag)).replace("0","-") for i in process_order])
        card_.write(sys + " " + "shape" + " " + binary_string + "\n")
    
    elif "cTagCalib" in sys:
        card_.write(sys + " " + "shape" + " " + "1 "*len(processes) + "\n") 
    # elif "muR" in sys:
#         binary_string = " ".join([(str(int("tt" in i)*1.11)).replace("0.0","-") for i in process_order])#.replace("0","-")
#         card_.write("muR " + "lnN" + " " + binary_string + "\n")
#     elif "muF" in sys:
#         binary_string = " ".join([(str(int("tt" in i)*1.04)).replace("0.0","-") for i in process_order])#.replace("0","-")
#         card_.write("muF " + "lnN" + " " + binary_string + "\n")    
    elif "hdamp" in sys or "JES" in sys or "JER" in sys or "Tune" in sys or "muR" in sys or "muF" in sys:# These are only on the ttbar samples
		binary_string = " ".join([str(int("tt" in i)).replace("0","-") for i in process_order])
		card_.write(sys + " " + "shape" + " " + binary_string + "\n")
    else:
        card_.write(sys + " " + "shape" + " " + "1 "*len(processes) + "\n")
card_.write("lumi lnN "+" ".join(["1.023"]*len(process_order))+"\n")
#binary_string = " ".join([(str(int("tt" in i)*0.939) + "/" + str(int("tt" in i)*1.048)).replace("0.0/0.0","-") for i in process_order])#.replace("0","-")
# card_.write("ttbarNorm " + "lnN" + " " + binary_string + "\n")	
binary_string = " ".join([(str(int(not "tt" in i)*0.7) + "/" + str(int(not "tt" in i)*1.3)).replace("0.0/0.0","-") for i in process_order])#.replace("0","-")
card_.write("bkgNorm " + "lnN" + " " + binary_string + "\n")		
card_.write("--------------- \n")
card_.write("* autoMCStats 10 1 \n")




card_.close()
f_.Close()
print ""
print "******* Summary of the output card *******"
os.system("cat %s"%args.outfile)
