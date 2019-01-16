from ROOT import TFile, TTree, TChain, TCanvas, TH1D, TLegend, gROOT, gStyle, TPad, gPad, TGraph, TMultiGraph, TLatex
import sys
import ROOT
import os
import time
from argparse import ArgumentParser
from array import array
from math import *
import numpy as np
from collections import Counter
import root_numpy as rootnp
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.utils import np_utils
from keras.callbacks import EarlyStopping, ModelCheckpoint, LearningRateScheduler
from keras.optimizers import SGD,Adam
from keras.regularizers import l1, l2
from numpy.lib.recfunctions import stack_arrays
from sklearn.preprocessing import StandardScaler
from keras.models import load_model
from sklearn.metrics import roc_curve,roc_auc_score
from sklearn.cross_validation import train_test_split
import pickle
from rootpy.plotting import Hist


def makeROC(fpr, tpr, thresholds,AUC,outfile,signal_label, background_label):
	
    c = TCanvas("c","c",700,600)
    gPad.SetMargin(0.15,0.07,0.15,0.05)
    gPad.SetLogy(0)
    gPad.SetGrid(1,1)
    gStyle.SetGridColor(15)

    roc = TGraph(len(fpr),tpr,fpr)

    roc.SetLineColor(2)
    roc.SetLineWidth(2)
    roc.SetTitle(";Signal efficiency (%s); Background efficiency (%s)"%(signal_label, background_label))
    roc.GetXaxis().SetTitleOffset(1.4)
    roc.GetXaxis().SetTitleSize(0.045)
    roc.GetYaxis().SetTitleOffset(1.4)
    roc.GetYaxis().SetTitleSize(0.045)
    roc.GetXaxis().SetRangeUser(0,1)
    roc.GetYaxis().SetRangeUser(0.000,1)
    roc.Draw("AL")

    latex = TLatex()
    latex.SetTextFont(42)
    latex.SetTextSize(0.05)
    latex.DrawLatexNDC(0.2,0.88,'AUC = %.3f'%AUC)
	
    c.SaveAs(outfile)

def makeDiscr(train_discr_dict,discr_dict,outfile,xtitle="discriminator",logy=1):
    c = ROOT.TCanvas("c","c",800,500)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gPad.SetMargin(0.15,0.1,0.2,0.1)
    if logy: ROOT.gPad.SetLogy(1)
    #ROOT.gPad.SetGrid(1,1)
    ROOT.gStyle.SetGridColor(17)
    l = TLegend(0.17,0.75,0.88,0.88)
    l.SetTextSize(0.055)
    l.SetBorderSize(0)
    l.SetFillStyle(0)
    l.SetNColumns(3)
    
    colors = [2,1,4,6,7]
    counter = 0
    for leg,discr in train_discr_dict:
        a = Hist(30, 0, 1)
        #fill_hist_with_ndarray(a, discr)
        a.fill_array(discr)
        a.SetLineColor(colors[counter])
        a.SetLineWidth(2)
        a.GetXaxis().SetTitle(xtitle)
        a.GetXaxis().SetLabelSize(0.05)
        a.GetXaxis().SetTitleSize(0.06)
        a.GetXaxis().SetTitleOffset(1.45)
        a.GetYaxis().SetTitle("a.u.")
        #a.GetYaxis().SetTickSize(0)
        #a.GetYaxis().SetLabelSize(0)
        a.GetYaxis().SetTitleSize(0.06)
        a.GetYaxis().SetTitleOffset(0.9)
        a.Scale(1./a.Integral())
        if logy: a.GetYaxis().SetRangeUser(0.00001,100)
        else: a.GetYaxis().SetRangeUser(0,0.9)
        if counter == 0: a.draw("hist")
        else: a.draw("same hist")  
        l.AddEntry(a,leg,"l")
        counter += 1
        
    counter = 0
    for leg,discr in discr_dict:
        a = Hist(30, 0, 1)
        #fill_hist_with_ndarray(a, discr)
        a.fill_array(discr)
        a.SetLineColor(colors[counter])
        a.SetMarkerColor(colors[counter])
        a.SetMarkerStyle(34)
        a.SetMarkerSize(1.8)
        a.SetLineWidth(2)
        a.GetXaxis().SetTitle(xtitle)
        a.GetXaxis().SetLabelSize(0.05)
        a.GetXaxis().SetTitleSize(0.06)
        a.GetXaxis().SetTitleOffset(1.45)
        a.GetYaxis().SetTitle("a.u.")
        #a.GetYaxis().SetTickSize(0)
        #a.GetYaxis().SetLabelSize(0)
        a.GetYaxis().SetTitleSize(0.06)
        a.GetYaxis().SetTitleOffset(0.9)
        a.Scale(1./a.Integral())
        if logy: a.GetYaxis().SetRangeUser(0.00001,100)
        else: a.GetYaxis().SetRangeUser(0,0.4)
        a.draw("same p X0")
        l.AddEntry(a,leg,"p")
        counter += 1
        
    # counter = 0
#     for leg,discr in train_discr_dict.iteritems():
#         d = Hist(30, 0, 1)
#         d.fill_array(discr)
#         d.SetLineColor(colors[counter])
#         d.SetLineWidth(2)
#         l.AddEntry(d,leg,"l")
#         
#         b = Hist(30, 0, 1)
#         d.fill_array(discr_dict[leg.split(" ")[0] + " test"])
#         b.SetLineColor(colors[counter])
#         b.SetMarkerColor(colors[counter])
#         b.SetMarkerStyle(34)
#         b.SetMarkerSize(1.8)
#         b.SetLineWidth(2)
#         l.AddEntry(b,leg,"p")
#         counter += 1
        
    l.Draw("same") 
    
    c.SaveAs(outfile)

def drawTrainingCurve(input,output):
    hist = pickle.load(open(input,"rb"))
    tr_acc = hist["acc"]
    tr_loss = hist["loss"]
    val_acc = hist["val_acc"]
    val_loss = hist["val_loss"]
    epochs = range(len(tr_acc))
    
    c = TCanvas("c","c",800,500)
    #c.SetFillStyle(4000)
    #c.SetFrameFillStyle(4000)
    gStyle.SetOptStat(0)
    uppad = TPad("u","u",0.,0.55,1.,1.)
    downpad = TPad("d","d",0.,0.,1.,0.55)
    uppad.Draw()
    #uppad.SetFillStyle(4000)
    #uppad.SetFrameFillStyle(4000)
    downpad.Draw()
    #downpad.SetFillStyle(4000)
    #downpad.SetFrameFillStyle(4000)
    uppad.cd()
    gPad.SetMargin(0.15,0.05,0.02,0.15)
    gPad.SetGrid(1,1)
    gStyle.SetGridColor(13)
    
    gr_acc_train = TGraph(len(epochs),array('d',epochs),array('d',tr_acc))
    gr_acc_train.SetLineColor(2)
    gr_acc_train.SetLineWidth(2)
    gr_acc_test = TGraph(len(epochs),array('d',epochs),array('d',val_acc))
    gr_acc_test.SetLineColor(4)
    gr_acc_test.SetLineWidth(2)
    
    mgup = TMultiGraph("mgup",";number of epochs;accuracy")
    mgup.Add(gr_acc_train,"l")
    mgup.Add(gr_acc_test,"l")
    mgup.Draw("AL")
    mgup.GetXaxis().SetRangeUser(min(epochs),max(epochs))
    mgup.GetXaxis().SetLabelSize(0)
    mgup.GetYaxis().CenterTitle()
    mgup.GetYaxis().SetTitleSize(0.12)
    mgup.GetYaxis().SetTitleOffset(0.5)
    mgup.GetYaxis().SetLabelSize(0.105)
    mgup.GetYaxis().SetNdivisions(8)
    
    l = TLegend(0.6,0.15,0.88,0.6)
    l.SetTextSize(0.14)
    l.AddEntry(gr_acc_train,"training","l")
    l.AddEntry(gr_acc_test,"validation","l")
    l.Draw("same")
    
    downpad.cd()
    gPad.SetMargin(0.15,0.05,0.25,0.02)
    gPad.SetGrid(1,1)
    gStyle.SetGridColor(13)
    
    gr_loss_train = TGraph(len(epochs),array('d',epochs),array('d',tr_loss))
    gr_loss_train.SetLineColor(2)
    gr_loss_train.SetLineWidth(2)
    gr_loss_test = TGraph(len(epochs),array('d',epochs),array('d',val_loss))
    gr_loss_test.SetLineColor(4)
    gr_loss_test.SetLineWidth(2)
    
    mgdown = TMultiGraph("mgdown",";number of epochs;loss")
    mgdown.Add(gr_loss_train,"l")
    mgdown.Add(gr_loss_test,"l")
    mgdown.Draw("AL")
    mgdown.GetXaxis().SetRangeUser(min(epochs),max(epochs))
    mgdown.GetXaxis().SetLabelSize(0.085)
    mgdown.GetXaxis().SetTitleSize(0.11)
    mgdown.GetXaxis().SetTitleOffset(0.9)
    mgdown.GetXaxis().CenterTitle()
    mgdown.GetYaxis().CenterTitle()
    mgdown.GetYaxis().SetTitleSize(0.11)
    mgdown.GetYaxis().SetTitleOffset(0.55)
    mgdown.GetYaxis().SetLabelSize(0.085)
    mgdown.GetYaxis().SetNdivisions(8)
    
    c.SaveAs(output)
    

def make_model(input_dim, nb_classes, nb_hidden_layers = 1, nb_neurons = 30,momentum_sgd = 0.8, init_learning_rate_sgd = 0.001, dropout =0.1,nb_epoch = 100, batch_size=128):
    #batch_size = 128
    #nb_epoch = args.n_epochs

    #prepare the optimizer 
    decay_sgd = init_learning_rate_sgd/float(5*nb_epoch) if nb_epoch !=0 else 0.0001
    sgd = SGD(lr=init_learning_rate_sgd, decay=decay_sgd, momentum=momentum_sgd, nesterov=True)


    model = Sequential()
    model.add(Dense(nb_neurons ,input_shape= input_dim))
    model.add(Activation('relu'))
    for x in range ( nb_hidden_layers ):
            model.add(Dense(nb_neurons))
            model.add(Activation('relu'))
            model.add(Dropout(dropout))
    # model.add(Dense(nb_neurons))
#     model.add(Activation('relu'))
    #model.add(Dropout(dropout))
    model.add(Dense(nb_classes))
    model.add(Activation('softmax'))

    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
 
    return model
    
def main():
    
    gROOT.SetBatch(1)

    parser = ArgumentParser()
    parser.add_argument('--nepoch', type=int, default=20,help='number of epochs to run the training for')
    parser.add_argument('--TrainingFile', default = "", help='path to training')
    #parser.add_argument('--initepoch', type=int, default=1,help='starting epoch when using an existing training')
    parser.add_argument('--infile', default = "/user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/analyse/SELECTED_NewElectronIDv2_MC_VisiblePS_WithttHFSelectior_smearedjets_trial2/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_VisiblePS.root", help='path to the training file')#TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8.root", help='path to the training file')
    parser.add_argument('--tag', default=time.strftime("%a%d%b%Y_%Hh%Mm%Ss"),help='name of output directory')
    parser.add_argument('--skipEvery', type=int, default=1,help='ignore one entry every')
    parser.add_argument('--verbose', type=int, default=1,help='verbosity of training')
    args = parser.parse_args()
    
    
    from keras import backend as K
    #K.set_session(K.tf.Session(config=K.tf.ConfigProto(intra_op_parallelism_threads = 4, inter_op_parallelism_threads = 4)))
    
    
    nb_classes =5
    
    print "******** READING INPUT FILES ************"
    
    f_ = TFile(args.infile)
    tree = f_.Get("tree")

    # branchnames = [i.GetName() for i in correct_tree.GetListOfBranches()]
#     branchnames = sorted(branchnames)
#     for i in branchnames:
#         print '"'+i+'",'
#     sys.exit(1)
    
    variables = [
    "Pt_addJet1",
    #"Eta_addJet1",
    "DeepCSVcTagCvsL_addJet1",
    "DeepCSVcTagCvsB_addJet1",
    "Pt_addJet2",
    #"Eta_addJet2",
    "DeepCSVcTagCvsL_addJet2",
    "DeepCSVcTagCvsB_addJet2",
    "TopMatching_NN_best_value",
    "DeltaR_addJets",
    #"Minv_addJets"
    ]
    
    if not os.path.isdir(os.getcwd() + "/"+args.tag): os.mkdir(os.getcwd() + "/"+args.tag)
    pickle.dump(variables,open(os.getcwd() + "/"+args.tag+"/variables.pkl",'wb'))
    
    extra_selection = ""# "*(n_DeepCSVcTagger_L_Additional_ctagged>1)"
    
    weights = ["weight_bjets_ctag_iterativefit","weight_cjets_ctag_iterativefit","weight_udsgjets_ctag_iterativefit","weight_bcjets_btag_DeepCSVMedium","weight_udsgjets_btag_DeepCSVMedium","weight_electron_id","weight_electron_reco","weight_muon_id","weight_muon_iso","mc_weight","pu_weight"]
    
    X_ttbb = rootnp.tree2array(tree,variables,"event_Category_VisiblePS==0"+extra_selection,step=args.skipEvery)
    X_ttbb = rootnp.rec2array(X_ttbb)
    weight_ttbb = rootnp.tree2array(tree,weights,"event_Category_VisiblePS==0"+extra_selection,step=args.skipEvery)
    weight_ttbb = rootnp.rec2array(weight_ttbb)
    weight_ttbb = np.asarray([reduce(lambda x, y: x*y, sublist) for sublist in weight_ttbb])
    
    X_ttbL = rootnp.tree2array(tree,variables,"event_Category_VisiblePS==1"+extra_selection,step=args.skipEvery)
    X_ttbL = rootnp.rec2array(X_ttbL)
    weight_ttbL = rootnp.tree2array(tree,weights,"event_Category_VisiblePS==1"+extra_selection,step=args.skipEvery)
    weight_ttbL = rootnp.rec2array(weight_ttbL)
    weight_ttbL = np.asarray([reduce(lambda x, y: x*y, sublist) for sublist in weight_ttbL])
    
    X_ttcc = rootnp.tree2array(tree,variables,"event_Category_VisiblePS==2"+extra_selection,step=args.skipEvery)
    X_ttcc = rootnp.rec2array(X_ttcc)
    weight_ttcc = rootnp.tree2array(tree,weights,"event_Category_VisiblePS==2"+extra_selection,step=args.skipEvery)
    weight_ttcc = rootnp.rec2array(weight_ttcc)
    weight_ttcc = np.asarray([reduce(lambda x, y: x*y, sublist) for sublist in weight_ttcc])
    
    X_ttcL = rootnp.tree2array(tree,variables,"event_Category_VisiblePS==3"+extra_selection,step=args.skipEvery)
    X_ttcL = rootnp.rec2array(X_ttcL)
    weight_ttcL = rootnp.tree2array(tree,weights,"event_Category_VisiblePS==3"+extra_selection,step=args.skipEvery)
    weight_ttcL = rootnp.rec2array(weight_ttcL)
    weight_ttcL = np.asarray([reduce(lambda x, y: x*y, sublist) for sublist in weight_ttcL])
    
    X_ttLL = rootnp.tree2array(tree,variables,"event_Category_VisiblePS==4"+extra_selection,step=args.skipEvery)
    X_ttLL = rootnp.rec2array(X_ttLL)
    weight_ttLL = rootnp.tree2array(tree,weights,"event_Category_VisiblePS==4"+extra_selection,step=args.skipEvery)
    weight_ttLL = rootnp.rec2array(weight_ttLL)
    weight_ttLL = np.asarray([reduce(lambda x, y: x*y, sublist) for sublist in weight_ttLL])
    

    total = len(X_ttbb)+len(X_ttbL)+len(X_ttcc)+len(X_ttcL)+len(X_ttLL)
    weight_ttbb = weight_ttbb*float(total)/float(len(X_ttbb))
    weight_ttbL = weight_ttbL*float(total)/float(len(X_ttbL))
    weight_ttcc = weight_ttcc*float(total)/float(len(X_ttcc))
    weight_ttcL = weight_ttcL*float(total)/float(len(X_ttcL))
    weight_ttLL = weight_ttLL*float(total)/float(len(X_ttLL))
    
    
    X = np.concatenate((X_ttbb,X_ttbL,X_ttcc,X_ttcL,X_ttLL))
    weight = np.concatenate((weight_ttbb,weight_ttbL,weight_ttcc,weight_ttcL,weight_ttLL))
    #wtotal = np.asarray([i*j for i,j in zip(w,wbtag)])
    y = np.concatenate(( np.full(len(X_ttbb),2),np.full(len(X_ttbL),3),np.full(len(X_ttcc),0),np.full(len(X_ttcL),1),np.full(len(X_ttLL),4) )) # ttbb= 2, ttbL=3, ttcc=0, ttcL=1, ttLL=4
    Y = np_utils.to_categorical(y.astype(int), nb_classes)
    
    print "******** SCALING INPUTS ************"
    
    scaler = StandardScaler()
    scaler.fit(X)
    if not os.path.isdir(os.getcwd() + "/"+args.tag): os.mkdir(os.getcwd() + "/"+args.tag)
    print "storing output in %s"%(os.getcwd() + "/"+args.tag)
    pickle.dump(scaler,open(os.getcwd() + "/"+args.tag+"/scaler.pkl",'wb'))
    X = scaler.transform(X)
    
    X_train, X_test , y_train, y_test, Y_train, Y_test, weight_train, weight_test = train_test_split(X, y, Y, weight, test_size=0.2)
    
    #print "%i training correct events, %i training flipped events and %i training background events"%(len(X_train[y_train==1]),len(X_train[y_train==2]),len(X_train[y_train==0]))
    
    
    print "******** BUILDING/TRAINING MODEL ************"
    if args.TrainingFile == "":
        model = make_model(X_train.shape[1:],nb_classes, nb_epoch = args.nepoch)
        print model.summary()
        
        if args.nepoch>0:
            batch_size = 128
            if not os.path.isdir(os.getcwd() + "/"+args.tag): os.mkdir(os.getcwd() + "/"+args.tag)
            train_history = model.fit(X_train, Y_train, batch_size=batch_size, nb_epoch=args.nepoch, validation_data=(X_test, Y_test), callbacks = [ModelCheckpoint(os.getcwd() + "/"+args.tag+"/model_checkpoint_save.hdf5")], shuffle=True,verbose=args.verbose, sample_weight = weight_train)
            pickle.dump(train_history.history,open(os.getcwd() + "/"+args.tag+"/loss_and_acc.pkl",'wb'))
            

            #pickle.dump(train_history.history,open(os.getcwd() + "/"+args.tag+"/loss_and_acc.pkl",'wb'))
            drawTrainingCurve(os.getcwd() + "/"+args.tag+"/loss_and_acc.pkl",os.getcwd() + "/"+args.tag+"/training_curve.pdf")
    
    else:
        model = load_model(args.TrainingFile)
        print model.summary()
        
        # if args.nepoch>0:
#             batch_size = 128
#             if not os.path.isdir(os.getcwd() + "/"+args.tag): os.mkdir(os.getcwd() + "/"+args.tag)
#             train_history_contd2 = model.fit(X_train, Y_train, batch_size=batch_size, nb_epoch=args.nepoch, validation_data=(X_test, Y_test), callbacks = [ModelCheckpoint(os.getcwd() + "/"+args.tag+"/model_checkpoint_save.hdf5")], shuffle=True,verbose=args.verbose, sample_weight = w_train)
# 
#             pickle.dump(train_history_contd2.history,open(os.getcwd() + "/"+args.tag+"/loss_and_acc_contd2.pkl",'wb'))
#             drawTrainingCurve(os.getcwd() + "/"+args.tag+"/loss_and_acc_contd2.pkl",os.getcwd() + "/"+args.tag+"/training_curve_contd2.pdf")
#     
    
    
    # print X_test[0], X_test[0].shape, type(X_test[0])
#     print X_test, X_test.shape, type(X_test)
#     sys.exit(1)
    
    # Validation
    discr_buffer = model.predict(X_test)
    discr_ttbb = discr_buffer[:,2]
    discr_ttbL = discr_buffer[:,3]
    discr_ttcc = discr_buffer[:,0]
    discr_ttcL = discr_buffer[:,1]
    discr_ttLL = discr_buffer[:,4]
    
    discr = [(i)/(i+k) for i,j,k,l,m in zip(discr_ttcc,discr_ttcL,discr_ttLL,discr_ttbb,discr_ttbL)]
    ttbb_discr = [i for idx,i in enumerate(discr) if y_test[idx]==2]
    ttbL_discr = [i for idx,i in enumerate(discr) if y_test[idx]==3]
    ttcc_discr = [i for idx,i in enumerate(discr) if y_test[idx]==0]
    ttcL_discr = [i for idx,i in enumerate(discr) if y_test[idx]==1]
    ttLL_discr = [i for idx,i in enumerate(discr) if y_test[idx]==4]

    discr_buffer_train = model.predict(X_train)
    discr_train_ttbb = discr_buffer_train[:,2]
    discr_train_ttbL = discr_buffer_train[:,3]
    discr_train_ttcc = discr_buffer_train[:,0]
    discr_train_ttcL = discr_buffer_train[:,1]
    discr_train_ttLL = discr_buffer_train[:,4]
    discr_train = [(i)/(i+k) for i,j,k,l,m in zip(discr_train_ttcc,discr_train_ttcL,discr_train_ttLL,discr_train_ttbb,discr_train_ttbL)]
    ttbb_discr_train = [i for idx,i in enumerate(discr_train) if y_train[idx]==2]
    ttbL_discr_train = [i for idx,i in enumerate(discr_train) if y_train[idx]==3]
    ttcc_discr_train = [i for idx,i in enumerate(discr_train) if y_train[idx]==0]
    ttcL_discr_train = [i for idx,i in enumerate(discr_train) if y_train[idx]==1]
    ttLL_discr_train = [i for idx,i in enumerate(discr_train) if y_train[idx]==4]
    fpr, tpr, thres = roc_curve( np.concatenate(( np.ones(len(ttcc_discr)),np.zeros(len(ttLL_discr)) )),np.concatenate((ttcc_discr,ttLL_discr)) )
    AUC = 1-roc_auc_score( np.concatenate(( np.ones(len(ttcc_discr)),np.zeros(len(ttLL_discr)) )),np.concatenate((ttcc_discr,ttLL_discr))  )
    makeROC(fpr, tpr, thres,AUC,os.getcwd() + "/"+args.tag+"/ROC_curve_CvsL.pdf","ttcc","ttLF")
    makeDiscr([("ttbb_train",ttbb_discr_train),("ttbL_train",ttbL_discr_train),("ttcc_train",ttcc_discr_train),("ttcL_train",ttcL_discr_train),("ttLL_train",ttLL_discr_train)],[("ttbb test",ttbb_discr),("ttbL test",ttbL_discr),("ttcc test",ttcc_discr),("ttcL test",ttcL_discr),("ttLL test",ttLL_discr)],os.getcwd() + "/"+args.tag+"/Discriminator_CvsL.pdf","NN output")
    
    
    
    discr = [(i)/(i+l) for i,j,k,l,m in zip(discr_ttcc,discr_ttcL,discr_ttLL,discr_ttbb,discr_ttbL)]
    ttbb_discr = [i for idx,i in enumerate(discr) if y_test[idx]==2]
    ttbL_discr = [i for idx,i in enumerate(discr) if y_test[idx]==3]
    ttcc_discr = [i for idx,i in enumerate(discr) if y_test[idx]==0]
    ttcL_discr = [i for idx,i in enumerate(discr) if y_test[idx]==1]
    ttLL_discr = [i for idx,i in enumerate(discr) if y_test[idx]==4]

    discr_train = [(i)/(i+l) for i,j,k,l,m in zip(discr_train_ttcc,discr_train_ttcL,discr_train_ttLL,discr_train_ttbb,discr_train_ttbL)]
    ttbb_discr_train = [i for idx,i in enumerate(discr_train) if y_train[idx]==2]
    ttbL_discr_train = [i for idx,i in enumerate(discr_train) if y_train[idx]==3]
    ttcc_discr_train = [i for idx,i in enumerate(discr_train) if y_train[idx]==0]
    ttcL_discr_train = [i for idx,i in enumerate(discr_train) if y_train[idx]==1]
    ttLL_discr_train = [i for idx,i in enumerate(discr_train) if y_train[idx]==4]
    fpr, tpr, thres = roc_curve( np.concatenate(( np.ones(len(ttcc_discr)),np.zeros(len(ttbb_discr)) )),np.concatenate((ttcc_discr,ttbb_discr)) )
    AUC = 1-roc_auc_score( np.concatenate(( np.ones(len(ttcc_discr)),np.zeros(len(ttbb_discr)) )),np.concatenate((ttcc_discr,ttbb_discr))  )
    makeROC(fpr, tpr, thres,AUC,os.getcwd() + "/"+args.tag+"/ROC_curve_CvsB.pdf","ttcc","ttbb")
    makeDiscr([("ttbb_train",ttbb_discr_train),("ttbL_train",ttbL_discr_train),("ttcc_train",ttcc_discr_train),("ttcL_train",ttcL_discr_train),("ttLL_train",ttLL_discr_train)],[("ttbb test",ttbb_discr),("ttbL test",ttbL_discr),("ttcc test",ttcc_discr),("ttcL test",ttcL_discr),("ttLL test",ttLL_discr)],os.getcwd() + "/"+args.tag+"/Discriminator_CvsB.pdf","NN output")
    
    
    
if __name__ == "__main__":
    main()
