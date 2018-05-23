import os
from ROOT import *

indir = "/pnfs/iihe/cms/store/user/smoortga/Analysis/FlatTree/Test2017Analysis_MC/"

samples = os.listdir(indir)


output_for_filenames = []
output_for_nevents = []

outfile = open("sampelist.txt","w")

for sample in samples:
    printname = indir+sample
    printname = printname+"/"+os.listdir(printname)[0]
    printname = printname+"/"+os.listdir(printname)[0]
    printname = printname+"/"+os.listdir(printname)[0]
    #printname = printname+"/"+os.listdir(printname)[0]
    #print 'superTree->Add("'+printname+'/J*.root");'
    
    # now try to figure out how many events are in each pthat bin
    print '"'+printname+'/":["./SelectedSamples/'+printname.split("/")[10]+'.root",args.nevents]'
    #print ""
    
    outfile.write('"'+printname+'/":["./SelectedSamples/'+printname.split("/")[10]+'.root",args.nevents],\n')

outfile.close()