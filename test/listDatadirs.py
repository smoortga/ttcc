import os
from ROOT import *

indir = "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_SingleLeptonData_WithgenTTXJets/"

if indir.endswith("/"): indir = indir[:-1]

samples = os.listdir(indir)


output_for_filenames = []
output_for_nevents = []

outfile = open("data_sampelist.txt","w")

for sample in samples:
	printname = indir+"/"+sample
	subsamples = os.listdir(printname)
	savename = printname
	for subs in subsamples:
		printname=savename
		printname = printname+"/"+subs
		printname = printname+"/"+os.listdir(printname)[0]
		printname = printname+"/"+os.listdir(printname)[0]
		
		print '"'+printname+'/":["'+printname.split("/")[10]+'_'+printname.split("/")[11]+'.root",args.nevents],'
		#print ""
    
		outfile.write('"'+printname+'/":["./SelectedSamples/'+printname.split("/")[10]+'_'+printname.split("/")[11]+'.root"args.nevents],\n')

outfile.close()
