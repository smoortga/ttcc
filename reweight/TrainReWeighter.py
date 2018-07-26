from ROOT import TFile, TTree, TChain, TCanvas, TH1D, TLegend, gROOT, gStyle, TPad, gPad, TGraph, TMultiGraph, TLatex
import sys
import ROOT
import os
import time
from argparse import ArgumentParser
from array import array
from math import *
import numpy as np
from xsec import xsec_table
from collections import Counter
import root_numpy as rootnp
import matplotlib.pyplot as plt
from keras.objectives import mean_squared_error
from keras.models import Sequential, Model
from keras.layers import Input, Dense, Activation, Dropout
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

lam = 5

def plot_losses(i, losses):
    ax1 = plt.subplot(311)   
    values = np.array(losses["L_f"])
    values_train = np.array(losses["L_f train"])
    plt.plot(range(len(values)), values, label=r"$L_{reco}$ test", color="blue")
    plt.plot(range(len(values_train)), values_train, label=r"$L_{reco}$ train", color="blue", linestyle="dashed")
    plt.legend(loc="lower right")
    
    ax2 = plt.subplot(312, sharex=ax1) 
    values = np.array(losses["L_r"]) 
    values_train = np.array(losses["L_r train"])
    plt.plot(range(len(values)), values, label=r"$L_{disc}$ test", color="green")
    plt.plot(range(len(values_train)), values_train, label=r"$L_{disc}$ train", color="green", linestyle="dashed")
    plt.legend(loc="lower right")
    
    ax3 = plt.subplot(313, sharex=ax1)
    values = np.array(losses["L_f - L_r"])
    values_train = np.array(losses["L_f - L_r train"])
    plt.plot(range(len(values)), values, label=r"$L_{reco} - \lambda L_{disc}$ test", color="red")  
    plt.plot(range(len(values_train)), values_train, label=r"$L_{reco} - \lambda L_{disc}$ train", color="red", linestyle="dashed")  
    plt.legend(loc="upper right")
    
    plt.savefig("./Losses.pdf")
    plt.clf()

def makeROC(fpr, tpr, thresholds,AUC,outfile,signal_label, background_label):
	
    c = TCanvas("c","c",700,600)
    gPad.SetMargin(0.15,0.07,0.15,0.05)
    gPad.SetLogy(0)
    gPad.SetGrid(1,1)
    gStyle.SetGridColor(15)
    
    mg = TMultiGraph()
    
    roc = TGraph(len(fpr),tpr,fpr)

    roc.SetLineColor(2)
    roc.SetLineWidth(3)
    roc.SetTitle(";Signal efficiency (%s); Background efficiency (%s)"%(signal_label, background_label))
    roc.GetXaxis().SetTitleOffset(1.4)
    roc.GetXaxis().SetTitleSize(0.045)
    roc.GetYaxis().SetTitleOffset(1.4)
    roc.GetYaxis().SetTitleSize(0.045)
    roc.GetXaxis().SetRangeUser(0,1)
    roc.GetYaxis().SetRangeUser(0.000,1)
    mg.Add(roc)
    #roc.Draw("AL")
    
    tpr_diag = np.arange(0,1.09,0.1)
    fpr_diag = np.arange(0,1.09,0.1)
    roc_diag = TGraph(len(fpr_diag),tpr_diag,fpr_diag)
    roc_diag.SetLineStyle(2)
    roc_diag.SetLineWidth(3)
    roc_diag.SetLineColor(13)
    mg.Add(roc_diag)
    #roc_diag.Draw("AL same")
    
    mg.Draw("AL")
    mg.SetTitle(";Signal efficiency (%s); Background efficiency (%s)"%(signal_label, background_label))

    latex = TLatex()
    latex.SetTextFont(42)
    latex.SetTextSize(0.05)
    latex.DrawLatexNDC(0.2,0.88,'AUC = %.3f'%AUC)
	
    c.SaveAs(outfile)


    
def main():
    
    gROOT.SetBatch(1)

    parser = ArgumentParser()
    parser.add_argument('--indirMC', default = os.getcwd()+"/MC_samples_ZControlRegion", help='path to MC files')
    parser.add_argument('--indirData', default = os.getcwd()+"/data_samples_ZControlRegion", help='path to data files')
    parser.add_argument('--skipEvery', type=int, default=1,help='ignore one entry every')
    parser.add_argument('--verbose', type=int, default=1,help='verbosity of training')
    args = parser.parse_args()
    
    
    from keras import backend as K
    #K.set_session(K.tf.Session(config=K.tf.ConfigProto(intra_op_parallelism_threads = 4, inter_op_parallelism_threads = 4)))
    
    
    
    
    print "******** READING MC INPUT FILES ************"
    
    
    input_variables = [
    "DeepCSVcTagCvsL_addJet1",
    "DeepCSVcTagCvsB_addJet1",
    #"hadronFlavour_addJet1",
    #"Eta_addJet1",
    #"Pt_addJet1",
    #"hadronFlavour_addJet1",
    #"DeepCSVcTagCvsL_addJet2",
    #"DeepCSVcTagCvsB_addJet2",
    ]
    
    spectator_variables = [
    "Pt_addJet1",
    "hadronFlavour_addJet1",
    "Eta_addJet1",
    ]
    
    weight_variables = [
        "weight_btag_iterativefit",
        "weight_electron_id",
        "weight_electron_reco",
        "weight_muon_id",
        "weight_muon_iso",
        "mc_weight"
    ]
    
    for idx,filepath in enumerate([(args.indirMC + "/" + i) for i in os.listdir(args.indirMC) if ".root" in i and not "TTTo2" in i]):
        print filepath
        
        fname = filepath.split("/")[-1].split(".root")[0]
        
        # check if tree is empty
        f_ = TFile(filepath)
        t_ = f_.Get("tree")
        if t_.GetEntries()==0: 
            print "WARNING: Found empty tree (%s), skipping..."%filepath
            continue
        
        n_original_h = f_.Get("hweight")
        n_original = n_original_h.GetBinContent(1)
        
        if idx == 0: 
            #X_MC = rootnp.root2array(filepath,"tree",variables)
            #X_MC = rootnp.rec2array(X_MC)
            Xi_MC = rootnp.root2array(filepath,"tree",input_variables)
            Xi_MC = rootnp.rec2array(Xi_MC)
            Xspec_MC = rootnp.root2array(filepath,"tree",spectator_variables)
            Xspec_MC = rootnp.rec2array(Xspec_MC)
            Xspec_MC[:,0] = Xspec_MC[:,0]/1000.
            #Xpt_MC /= max(Xpt_MC)
            #Xpt_MC = rootnp.rec2array(Xpt_MC)
            Xi_MC = np.c_[Xi_MC,Xspec_MC]
            w_MC = rootnp.root2array(filepath,"tree",weight_variables)
            w_MC = rootnp.rec2array(w_MC)
            w_MC = np.prod(w_MC, axis=1)
            xsec = xsec_table[fname]*1000 #[fb]
            int_lumi=41.527 #[fb^-1	]
            sample_weight = float(xsec*int_lumi)/float(n_original)
            w_MC = w_MC*sample_weight
            
        else:
            #X_tmp = rootnp.root2array(filepath,"tree",variables)
            #X_tmp = rootnp.rec2array(X_tmp)
            Xi_tmp = rootnp.root2array(filepath,"tree",input_variables)
            Xi_tmp = rootnp.rec2array(Xi_tmp)
            Xspec_tmp = rootnp.root2array(filepath,"tree",spectator_variables)
            Xspec_tmp = rootnp.rec2array(Xspec_tmp)
            Xspec_tmp[:,0] = Xspec_tmp[:,0]/1000.
            #Xpt_tmp /= max(Xpt_tmp)
            #Xpt_tmp = rootnp.rec2array(Xpt_tmp)
            Xi_tmp = np.c_[Xi_tmp,Xspec_tmp]
            #X_MC = np.concatenate((X_MC,X_tmp))
            Xi_MC = np.concatenate((Xi_MC,Xi_tmp))
            Xspec_MC = np.concatenate((Xspec_MC,Xspec_tmp))
            w_MC_tmp = rootnp.root2array(filepath,"tree",weight_variables)
            w_MC_tmp = rootnp.rec2array(w_MC_tmp)
            w_MC_tmp = np.prod(w_MC_tmp, axis=1)
            xsec = xsec_table[fname]*1000 #[fb]
            int_lumi=41.527 #[fb^-1	]
            sample_weight = float(xsec*int_lumi)/float(n_original)
            w_MC_tmp = w_MC_tmp*sample_weight
            w_MC = np.concatenate((w_MC,w_MC_tmp))
    
    y_MC = np.ones(len(Xi_MC))
    Y_MC = np_utils.to_categorical(y_MC.astype(int), 2)
    
    #print Xi_MC
    
    # scaler_inputs = StandardScaler()
#     scaler.fit(Xi_MC)
#     print "storing scaler output in %s"%(os.getcwd())
#     pickle.dump(scaler,open(os.getcwd()+"/scaler.pkl",'wb'))
#     Xi_MC = scaler.transform(Xi_MC)
#     
#     # shuffle MC
#     def unison_shuffled_copies(a, b):
#         assert len(a) == len(b)
#         p = np.random.permutation(len(a))
#         return a[p], b[p]
    
    
    #w_MC_save = w_MC
#     X_MC,w_MC = unison_shuffled_copies(X_MC,w_MC)
    
    
    
    print ""
    print "******** READING DATA INPUT FILES ************"
    

    
    for idx,filepath in enumerate([(args.indirData + "/" + i) for i in os.listdir(args.indirData) if ".root" in i]):
        print filepath
        
        fname = filepath.split("/")[-1].split(".root")[0]
        
        # check if tree is empty
        f_ = TFile(filepath)
        t_ = f_.Get("tree")
        if t_.GetEntries()==0: 
            print "WARNING: Found empty tree (%s), skipping..."%filepath
            continue
        
        if idx == 0: 
            X_Data = rootnp.root2array(filepath,"tree",input_variables)
            X_Data = rootnp.rec2array(X_Data)
            
            
        else:
            X_tmp = rootnp.root2array(filepath,"tree",input_variables)
            X_tmp = rootnp.rec2array(X_tmp)
            X_Data = np.concatenate((X_Data,X_tmp))
            
    y_Data = np.zeros(len(X_Data))
    Y_Data = np_utils.to_categorical(y_Data.astype(int), 2)
    w_Data = np.ones(len(X_Data))
    
    #X_Data = scaler.transform(X_Data)
    
    print X_Data.shape
    
    # Normalize the MC to the data yield with additional weight
    w_MC_normalize = float(len(X_Data))/float(sum(w_MC))
    print w_MC_normalize
    w_MC = w_MC*w_MC_normalize
    #w_MC_save = w_MC_save*w_MC_normalize
    
    # X_all = np.concatenate((Xi_MC,X_Data))
#     y_all = np.concatenate((np.ones(len(Xi_MC)),np.zeros(len(X_Data))))
#     Y_all = np_utils.to_categorical(y_all.astype(int), 2)
#     w_all = np.concatenate((w_MC_save,np.ones(len(X_Data))))
    
    
    # def unison_shuffled_copies_3(a, b, c):
#         assert len(a) == len(b)
#         assert len(b) == len(c)
#         p = np.random.permutation(len(a))
#         return a[p], b[p], c[p]
#     
    #X_all, y_all, w_all = unison_shuffled_copies_3(X_all, y_all, w_all)
    
    #X_MC_train, X_MC_test, w_MC_train, w_MC_test = train_test_split(X_MC, w_MC, test_size=0.5)
    #X_Data_train, X_Data_test = train_test_split(X_Data, test_size=0.2)
    # X_all_train, X_all_test, y_all_train, y_all_test, Y_all_train, Y_all_test, w_all_train, w_all_test = train_test_split(X_all, y_all, Y_all, w_all, test_size=0.2)
#     X_Data_train = X_all_train[y_all_train == 0]
#     w_Data_train = np.ones(len(X_Data_train))
#     Xi_MC_train = X_all_train[y_all_train == 1]
#     w_MC_train = w_all_train[y_all_train == 1]
#     X_Data_test = X_all_test[y_all_test == 0]
#     w_Data_test = np.ones(len(X_Data_test))
#     Xi_MC_test = X_all_test[y_all_test == 1]
#     w_MC_test = w_all_test[y_all_test == 1]
    
    Xi_MC_train, Xi_MC_test, Xspec_MC_train, Xspec_MC_test, y_MC_train, y_MC_test, Y_MC_train, Y_MC_test, w_MC_train, w_MC_test = train_test_split(Xi_MC, Xspec_MC, y_MC, Y_MC, w_MC, test_size=0.4)
    X_Data_train, X_Data_test, y_Data_train, y_Data_test, Y_Data_train, Y_Data_test, w_Data_train, w_Data_test = train_test_split(X_Data, y_Data, Y_Data, w_Data, test_size=0.4)


    
    print ""
    print "******** START BUILDING MODEL ************"
    
    #lam = 1
    def make_loss_D(c):
        def loss_D(y_true, y_pred):
            return c * mean_squared_error(y_pred, y_true)
        return loss_D
    
    def make_loss_R(d):
        def loss_R(y_true, y_pred):
            return d * K.binary_crossentropy(y_pred, y_true)
        return loss_R
    
    
    inputs = Input(shape=(Xi_MC.shape[1],))
    Dx = Dense(64, activation="relu")(inputs)
    Dx = Dense(64, activation="relu")(Dx)
    Dx = Dense(64, activation="relu")(Dx)
    Dx = Dense(Xi_MC[:,0:len(input_variables)].shape[1])(Dx)
    D = Model(input=[inputs], output=[Dx], name="Reconstructor")
    init_learning_rate_sgd=0.001
    decay_sgd = 0.0001
    momentum_sgd = 0.8
    opt_D = SGD(lr=0.1, decay=0, momentum=momentum_sgd, nesterov=True)
    D.compile(loss=[make_loss_D(c=1.0)], optimizer=opt_D, metrics=['accuracy'])
    #D = load_model(os.getcwd()+"/ReconstructorOnly_checkpoint_save.hdf5", custom_objects={'loss_D': make_loss_D(c=1.)})
    #D = load_model(os.getcwd()+"/final_reconstructor_save.hdf5", custom_objects={'loss_D': make_loss_D(c=1.)})
    
    
    Rx_in = Input(shape=(len(input_variables),))
    Rx = Dense(32, activation="relu")(Rx_in)
    Rx = Dense(32, activation="relu")(Rx)
    Rx = Dense(32, activation="relu")(Rx)
    Rx = Dense(2, activation="softmax")(Rx)
    R = Model(input=[Rx_in], output=[Rx], name="Discriminator")
    opt_R = SGD(lr=0.01, decay=0, momentum=momentum_sgd, nesterov=True)
    R.compile(loss=[make_loss_R(d=1.0)], optimizer=opt_R)
    #R = load_model(os.getcwd()+"/AdversaryOnly_checkpoint_save.hdf5", custom_objects={'loss_R': make_loss_R(d=1.)})
    #R = load_model(os.getcwd()+"/final_discriminator_save.hdf5", custom_objects={'loss_R': make_loss_R(d=1.)})
    
    
    Adv = Model(input=[inputs], output=[D(inputs), R(D(inputs))])
    opt_Adv = SGD(lr=0.0001, decay=0.00005, momentum=momentum_sgd, nesterov=True)
    Adv.compile(loss=[make_loss_D(c=1.0), make_loss_R(d=-lam)],  optimizer=opt_Adv)

    
    print "Summary of D"
    D.summary()
    print "Summary of R"
    R.summary()
    print "Summary of Adv"
    Adv.summary()
    
    
    print ""
    print "******** START INTITAL TRAINING WITHOUT ADVERSARY ************"
    D.trainable = True
    R.trainable = False
    
    train_history_ReconstructorOnly = D.fit(Xi_MC_train, Xi_MC_train[:,0:2],batch_size=256, nb_epoch=10, validation_data=(Xi_MC_test, Xi_MC_test[:,0:2]), callbacks = [ModelCheckpoint(os.getcwd() + "/ReconstructorOnly_checkpoint_save.hdf5")], shuffle=True)#, sample_weight = w_MC_train)
    
    
    test_pred = D.predict(Xi_MC_test)
    # test_pred = np.c_[test_pred,Xspec_MC_test]
#     test_pred = scaler.inverse_transform(test_pred)[:,0:2]
    
    #Xi_MC_test_orig = scaler.inverse_transform(Xi_MC_test)[:,0:2]
    
    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2,figsize=(10,10))
    
    test_pred0 = test_pred[:,0]
    ax1.hist(Xi_MC_test[:,0],20,range=(0,1),label="original MC",weights=w_MC_test,normed=0,histtype='step',linestyle='solid',color='red',linewidth=2)
    ax1.hist(test_pred0,20,range=(0,1),label="tranformed MC",weights=w_MC_test,normed=0,histtype='step',linestyle='dashed',color='blue',linewidth=2)
    ax1.hist(X_Data_test[:,0],20,range=(0,1),label="data",normed=0,histtype='stepfilled',linestyle='dotted',color='green',linewidth=2, alpha=0.4)
    ax1.legend(loc='best')
    ax1.set_xlabel(input_variables[0])
    
    test_pred1 = test_pred[:,1]
    ax2.hist(Xi_MC_test[:,1],20,range=(0,1),label="original MC",weights=w_MC_test,normed=0,histtype='step',linestyle='solid',color='red',linewidth=2)
    ax2.hist(test_pred1,20,range=(0,1),label="tranformed MC",weights=w_MC_test,normed=0,histtype='step',linestyle='dashed',color='blue',linewidth=2)
    ax2.hist(X_Data_test[:,1],20,range=(0,1),label="data",normed=0,histtype='stepfilled',linestyle='dotted',color='green',linewidth=2, alpha=0.4)
    ax2.set_xlabel(input_variables[1])
    
    test_pred0 = test_pred[:,0]
    ax3.hist(Xi_MC_test[:,0],50,range=(0,1),label="original MC",weights=w_MC_test,normed=1,histtype='step',linestyle='solid',color='red',linewidth=2,cumulative=-1)
    ax3.hist(test_pred0,50,range=(0,1),label="tranformed MC",weights=w_MC_test,normed=1,histtype='step',linestyle='dashed',color='blue',linewidth=2,cumulative=-1)
    ax3.hist(X_Data_test[:,0],50,range=(0,1),label="data",normed=1,histtype='stepfilled',linestyle='dotted',color='green',linewidth=2, alpha=0.4,cumulative=-1)
    ax3.set_xlabel(input_variables[0])
    ax3.set_ylabel("CDF")
    
    test_pred1 = test_pred[:,1]
    ax4.hist(Xi_MC_test[:,1],50,range=(0,1),label="original MC",weights=w_MC_test,normed=1,histtype='step',linestyle='solid',color='red',linewidth=2,cumulative=-1)
    ax4.hist(test_pred1,50,range=(0,1),label="tranformed MC",weights=w_MC_test,normed=1,histtype='step',linestyle='dashed',color='blue',linewidth=2,cumulative=-1)
    ax4.hist(X_Data_test[:,1],50,range=(0,1),label="data",normed=1,histtype='stepfilled',linestyle='dotted',color='green',linewidth=2, alpha=0.4,cumulative=-1)
    ax4.set_xlabel(input_variables[1])
    #ax4.set_ylabel("CDF")
    
    f.savefig("./inital_comparison.pdf")
    f.clf()
    

    
    
    print ""
    print "******** START PRETRAINING OF ADVERSARY ************"
    D.trainable = False
    R.trainable = True
    Xi_MC_train_R = D.predict(Xi_MC_train)
    #Xi_MC_train_R = np.c_[Xi_MC_train_R,Xspec_MC_train]
    #Xi_MC_train_R = scaler.inverse_transform(Xi_MC_train_R)[:,0:2]
    Xi_R_train = np.concatenate((Xi_MC_train_R,X_Data_train))
    w_R_train = np.concatenate((w_MC_train,w_Data_train))
    y_R_train = np.concatenate((np.ones(len(Xi_MC_train_R)),np.zeros(len(X_Data_train))))
    Y_R_train = np_utils.to_categorical(y_R_train.astype(int), 2)
    
    Xi_MC_test_R = D.predict(Xi_MC_test)
    #Xi_MC_test_R = np.c_[Xi_MC_test_R,Xspec_MC_test]
    #Xi_MC_test_R = scaler.inverse_transform(Xi_MC_test_R)[:,0:2]
    Xi_R_test = np.concatenate((Xi_MC_test_R,X_Data_test))
    w_R_test = np.concatenate((w_MC_test,w_Data_test))
    y_R_test = np.concatenate((np.ones(len(Xi_MC_test_R)),np.zeros(len(X_Data_test))))
    Y_R_test = np_utils.to_categorical(y_R_test.astype(int), 2)
    
    train_history_AdversaryOnly = R.fit(Xi_R_train, Y_R_train,batch_size=512, nb_epoch=30, validation_data=(Xi_R_test, Y_R_test, w_R_test),callbacks = [ModelCheckpoint(os.getcwd() + "/AdversaryOnly_checkpoint_save.hdf5")], shuffle=True, sample_weight =  w_R_train)
    
    #Xi_MC_test_R = D.predict(Xi_MC_test)
    #Xi_R_test = np.concatenate((Xi_MC_test_R,X_Data_test))
    pred_label = R.predict(Xi_R_test)[:,1]
    y_all_test = np.concatenate((y_MC_test,y_Data_test))
    w_all_test = np.concatenate((w_MC_test,w_Data_test))
    fpr, tpr, thres = roc_curve(y_all_test,pred_label,sample_weight=w_all_test)
    AUC = 1-roc_auc_score( y_all_test,pred_label,sample_weight=w_all_test )
    makeROC(fpr, tpr, thres,AUC,os.getcwd() +"/ROC_curve_AdversaryOnly.pdf","data","MC")


    #sys.exit(1)
    
    print ""
    print "******** START Full combined training ************"
    batch_size = 512
    
    

    losses = {"L_f": [], "L_r": [], "L_f - L_r": [],"L_f train": [], "L_r train": [], "L_f - L_r train": []}
    
    for i in range(101):
        print "Starting iteration %i"%i
        #X_MC_test_R = D.predict(X_MC_test)
        l = Adv.evaluate(Xi_MC_test, [Xi_MC_test[:,0:2], np_utils.to_categorical(np.ones(len(Xi_MC_test)).astype(int), 2)], verbose=0, sample_weight = [np.ones(len(Xi_MC_test)),w_MC_test])    
        losses["L_f - L_r"].append(l[0][None][0])
        losses["L_f"].append(l[1][None][0])
        losses["L_r"].append(-l[2][None][0]/lam)
        ltrain = Adv.evaluate(Xi_MC_train, [Xi_MC_train[:,0:2], np_utils.to_categorical(np.ones(len(Xi_MC_train)).astype(int), 2)], verbose=0, sample_weight = [np.ones(len(Xi_MC_train)),w_MC_train])    
        losses["L_f - L_r train"].append(ltrain[0][None][0])
        losses["L_f train"].append(ltrain[1][None][0])
        losses["L_r train"].append(-ltrain[2][None][0]/lam)
        plot_losses(i, losses)
        
        
        Xi_MC_train, Xi_MC_test, Xspec_MC_train, Xspec_MC_test, y_MC_train, y_MC_test, Y_MC_train, Y_MC_test, w_MC_train, w_MC_test = train_test_split(Xi_MC, Xspec_MC, y_MC, Y_MC, w_MC, test_size=0.4)
        X_Data_train, X_Data_test, y_Data_train, y_Data_test, Y_Data_train, Y_Data_test, w_Data_train, w_Data_test = train_test_split(X_Data, y_Data, Y_Data, w_Data, test_size=0.4)

        

        #Fit D for a few batch updates
        D.trainable = True
        R.trainable = False
        indices = np.random.permutation(len(Xi_MC_train))[:batch_size]
        y_R_train = np.ones(batch_size)
        Y_R_train = np_utils.to_categorical(y_R_train.astype(int), 2)
        Xi_MC_train_R = D.predict(Xi_MC_train)
        # Xi_MC_train_R = np.c_[Xi_MC_train_R,Xspec_MC_train]
#         Xi_MC_train_R = scaler.inverse_transform(Xi_MC_train_R)[:,0:2]
        for j in range(1):
            #if i < 5: 
            Adv.train_on_batch(Xi_MC_train[indices], [Xi_MC_train[indices,0:2], Y_R_train], sample_weight=[np.ones(batch_size),w_MC_train[indices]])
            #else: Adv.train_on_batch(Xi_MC_train[indices], [Xi_MC_train_R[indices,0:2], Y_R_train], sample_weight=[np.ones(batch_size),w_MC_train[indices]])
            #Adv.train_on_batch(X_MC_train[indices], [X_MC_train[indices], Y_R_train], sample_weight=[w_MC_train[indices],w_MC_train[indices]])
        
        
        # D.trainable = True
#         R.trainable = False
#         y_R_train = np.ones(len(X_MC_train))
#         Y_R_train = np_utils.to_categorical(y_R_train.astype(int), 2)
#         #Adv.fit(X_MC_train, [X_MC_train,Y_R_train], batch_size=512, nb_epoch=1, shuffle=True, verbose=1, sample_weight = [np.ones(len(X_MC_train)),w_MC_train])
#         Adv.fit(X_MC_train, [X_MC_train,Y_R_train], batch_size=512, nb_epoch=1, shuffle=True, verbose=1, sample_weight = [w_MC_train,w_MC_train])
        
        #Fit R
        D.trainable = False
        R.trainable = True
        X_MC_train_R = D.predict(Xi_MC_train)
        # X_MC_train_R = np.c_[X_MC_train_R,Xspec_MC_train]
#         X_MC_train_R = scaler.inverse_transform(X_MC_train_R)[:,0:2]
        X_R_train = np.concatenate((X_MC_train_R,X_Data_train))
        w_R_train = np.concatenate((w_MC_train,w_Data_train))
        y_R_train = np.concatenate((np.ones(len(X_MC_train_R)),np.zeros(len(X_Data_train))))
        Y_R_train = np_utils.to_categorical(y_R_train.astype(int), 2)
        X_MC_test_R = D.predict(Xi_MC_test)
        # X_MC_test_R = np.c_[X_MC_test_R,Xspec_MC_test]
#         X_MC_test_R = scaler.inverse_transform(X_MC_test_R)[:,0:2]
        X_R_test = np.concatenate((X_MC_test_R,X_Data_test))
        w_R_test = np.concatenate((w_MC_test,w_Data_test))
        y_R_test = np.concatenate((np.ones(len(X_MC_test_R)),np.zeros(len(X_Data_test))))
        Y_R_test = np_utils.to_categorical(y_R_test.astype(int), 2)
        R.fit(X_R_train, Y_R_train, batch_size=512, nb_epoch=5, validation_data=(X_R_test, Y_R_test, w_R_test), shuffle=True, verbose=1, sample_weight = w_R_train)
    
        
        
        

        #X_MC_test_R = D.predict(Xi_MC_test)
        #X_R_test = np.concatenate((X_MC_test_R,X_Data_test))
        pred_label = R.predict(X_R_test)[:,1]
        y_all_test = np.concatenate((y_MC_test,y_Data_test))
        w_all_test = np.concatenate((w_MC_test,w_Data_test))
        fpr, tpr, thres = roc_curve(y_all_test,pred_label,sample_weight=w_all_test)
        AUC = 1-roc_auc_score( y_all_test,pred_label,sample_weight=w_all_test )
        
        if abs(AUC-0.5) < 0.001 : break
        
        D.save(os.getcwd() + "/final_reconstructor_save.hdf5")
        R.save(os.getcwd() + "/final_discriminator_save.hdf5")
        Adv.save(os.getcwd() + "/final_adversary_save.hdf5")
        
        makeROC(fpr, tpr, thres,AUC,os.getcwd() +"/ROC_curve_FullCombinedTraining.pdf","data","MC")
        


        test_pred = D.predict(Xi_MC_test)
        f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2,figsize=(10,10))
    
        test_pred0 = test_pred[:,0]
        ax1.hist(Xi_MC_test[:,0],20,range=(0,1),label="original MC",weights=w_MC_test,normed=0,histtype='step',linestyle='solid',color='red',linewidth=2)
        ax1.hist(test_pred0,20,range=(0,1),label="tranformed MC",weights=w_MC_test,normed=0,histtype='step',linestyle='solid',color='blue',linewidth=2)
        ax1.hist(X_Data_test[:,0],20,range=(0,1),label="data",normed=0,histtype='stepfilled',linestyle='dotted',color='green',linewidth=2, alpha=0.4)
        ax1.legend(loc='best')
        ax1.set_xlabel(input_variables[0])
    
        test_pred1 = test_pred[:,1]
        ax2.hist(Xi_MC_test[:,1],20,range=(0,1),label="original MC",weights=w_MC_test,normed=0,histtype='step',linestyle='solid',color='red',linewidth=2)
        ax2.hist(test_pred1,20,range=(0,1),label="tranformed MC",weights=w_MC_test,normed=0,histtype='step',linestyle='solid',color='blue',linewidth=2)
        ax2.hist(X_Data_test[:,1],20,range=(0,1),label="data",normed=0,histtype='stepfilled',linestyle='dotted',color='green',linewidth=2, alpha=0.4)
        ax2.set_xlabel(input_variables[1])
    
        test_pred0 = test_pred[:,0]
        ax3.hist(Xi_MC_test[:,0],50,range=(0,1),label="original MC",weights=w_MC_test,normed=1,histtype='step',linestyle='solid',color='red',linewidth=2,cumulative=-1)
        ax3.hist(test_pred0,50,range=(0,1),label="tranformed MC",weights=w_MC_test,normed=1,histtype='step',linestyle='solid',color='blue',linewidth=2,cumulative=-1)
        ax3.hist(X_Data_test[:,0],50,range=(0,1),label="data",normed=1,histtype='stepfilled',linestyle='dotted',color='green',linewidth=2, alpha=0.4,cumulative=-1)
        ax3.set_xlabel(input_variables[0])
        ax3.set_ylabel("CDF")
    
        test_pred1 = test_pred[:,1]
        ax4.hist(Xi_MC_test[:,1],50,range=(0,1),label="original MC",weights=w_MC_test,normed=1,histtype='step',linestyle='solid',color='red',linewidth=2,cumulative=-1)
        ax4.hist(test_pred1,50,range=(0,1),label="tranformed MC",weights=w_MC_test,normed=1,histtype='step',linestyle='solid',color='blue',linewidth=2,cumulative=-1)
        ax4.hist(X_Data_test[:,1],50,range=(0,1),label="data",normed=1,histtype='stepfilled',linestyle='dotted',color='green',linewidth=2, alpha=0.4,cumulative=-1)
        ax4.set_xlabel(input_variables[1])
        #ax4.set_ylabel("CDF")

        f.savefig("./final_comparison.pdf")
        
        f.clf()
    
            # test_pred2 = test_pred[:,2]
#             test_pred_data2 = test_pred_data[:,2]
#             ax3.hist(X_MC_test[:,2],20,range=(0,1),label="original MC",weights=w_MC_test,normed=0,histtype='step',linestyle='solid',color='red',linewidth=2)
#             ax3.hist(test_pred2,20,range=(0,1),label="tranformed MC",weights=w_MC_test,normed=0,histtype='step',linestyle='dashed',color='blue',linewidth=2)
#             ax3.hist(test_pred_data2,20,range=(0,1),label="data",normed=0,histtype='stepfilled',linestyle='dotted',color='green',linewidth=2, alpha=0.4)
#             ax3.set_xlabel(variables[2])
#     
#             f.savefig("./final_comparison.pdf")
#     
#             test_pred3 = test_pred[:,3]
#             test_pred_data3 = test_pred_data[:,3]
#             ax4.hist(X_MC_test[:,3],20,range=(0,1),label="original MC",weights=w_MC_test,normed=0,histtype='step',linestyle='solid',color='red',linewidth=2)
#             ax4.hist(test_pred3,20,range=(0,1),label="tranformed MC",weights=w_MC_test,normed=0,histtype='step',linestyle='dashed',color='blue',linewidth=2)
#             ax4.hist(test_pred_data3,20,range=(0,1),label="data",normed=0,histtype='stepfilled',linestyle='dotted',color='green',linewidth=2, alpha=0.4)
#             ax4.set_xlabel(variables[3])
#     
#             f.savefig("./final_comparison.pdf")
        
        
        
        
    
    # X_MC_test_R = D.predict(Xi_MC_test)
#     X_R_test = np.concatenate((X_MC_test_R,X_Data_test))
#     pred_label = R.predict(X_R_test)[:,1]
#     y_all_test = np.concatenate((y_MC_test,y_Data_test))
#     w_all_test = np.concatenate((w_MC_test,w_Data_test))
#     fpr, tpr, thres = roc_curve(y_all_test,pred_label,sample_weight=w_all_test)
#     AUC = 1-roc_auc_score( y_all_test,pred_label,sample_weight=w_all_test )
#     makeROC(fpr, tpr, thres,AUC,os.getcwd() +"/ROC_curve_FullCombinedTraining.pdf","data","MC")
#     
#     
#     test_pred = D.predict(Xi_MC_test)
#     test_pred_data = X_Data_test#D.predict(X_Data)
#     f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2,figsize=(10,10))
#     
#     test_pred0 = test_pred[:,0]
#     test_pred_data0 = test_pred_data[:,0]
#     ax1.hist(Xi_MC_test[:,0],20,range=(0,1),label="original MC",weights=w_MC_test,normed=0,histtype='step',linestyle='solid',color='red',linewidth=2)
#     ax1.hist(test_pred0,20,range=(0,1),label="tranformed MC",weights=w_MC_test,normed=0,histtype='step',linestyle='dashed',color='blue',linewidth=2)
#     ax1.hist(test_pred_data0,20,range=(0,1),label="data",normed=0,histtype='stepfilled',linestyle='dotted',color='green',linewidth=2, alpha=0.4)
#     ax1.legend(loc='best')
#     ax1.set_xlabel(variables[0])
#     
#     f.savefig("./final_comparison.pdf")
#     
#     test_pred1 = test_pred[:,1]
#     test_pred_data1 = test_pred_data[:,1]
#     ax2.hist(Xi_MC_test[:,1],20,range=(0,1),label="original MC",weights=w_MC_test,normed=0,histtype='step',linestyle='solid',color='red',linewidth=2)
#     ax2.hist(test_pred1,20,range=(0,1),label="tranformed MC",weights=w_MC_test,normed=0,histtype='step',linestyle='dashed',color='blue',linewidth=2)
#     ax2.hist(test_pred_data1,20,range=(0,1),label="data",normed=0,histtype='stepfilled',linestyle='dotted',color='green',linewidth=2, alpha=0.4)
#     ax2.set_xlabel(variables[1])
#     
#     f.savefig("./final_comparison.pdf")
    
    # test_pred2 = test_pred[:,2]
#     test_pred_data2 = test_pred_data[:,2]
#     ax3.hist(X_MC_test[:,2],20,range=(0,1),label="original MC",weights=w_MC_test,normed=0,histtype='step',linestyle='solid',color='red',linewidth=2)
#     ax3.hist(test_pred2,20,range=(0,1),label="tranformed MC",weights=w_MC_test,normed=0,histtype='step',linestyle='dashed',color='blue',linewidth=2)
#     ax3.hist(test_pred_data2,20,range=(0,1),label="data",normed=0,histtype='stepfilled',linestyle='dotted',color='green',linewidth=2, alpha=0.4)
#     ax3.set_xlabel(variables[2])
#     
#     f.savefig("./final_comparison.pdf")
#     
#     test_pred3 = test_pred[:,3]
#     test_pred_data3 = test_pred_data[:,3]
#     ax4.hist(X_MC_test[:,3],20,range=(0,1),label="original MC",weights=w_MC_test,normed=0,histtype='step',linestyle='solid',color='red',linewidth=2)
#     ax4.hist(test_pred3,20,range=(0,1),label="tranformed MC",weights=w_MC_test,normed=0,histtype='step',linestyle='dashed',color='blue',linewidth=2)
#     ax4.hist(test_pred_data3,20,range=(0,1),label="data",normed=0,histtype='stepfilled',linestyle='dotted',color='green',linewidth=2, alpha=0.4)
#     ax4.set_xlabel(variables[3])
#     
#     f.savefig("./final_comparison.pdf")
    
    

    
    
    
    
if __name__ == "__main__":
    main()