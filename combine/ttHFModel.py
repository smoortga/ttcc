from HiggsAnalysis.CombinedLimit.PhysicsModel import *

class TTHFModelScale(PhysicsModel):
    def setModelBuilder(self, modelBuilder):
        PhysicsModel.setModelBuilder(self, modelBuilder)
        self.modelBuilder.doModelBOnly = False
        
    def getYieldScale(self,bin,process):
        #print process
        #print self.DC.print_structure()
        #print self.DC.exp[bin][process]
        #if not self.DC.isSignal[process]: return 1
        # if process == "ttbb": return "TTBB"
#         if process == "ttbj": return "TTBJ"
#         if process == "ttcc": return "TTCC"
#         if process == "ttcj": return "TTCJ"
#         if process == "ttjj": return "TTJJ"
        if process == "ttbb": return "TTBB"
        if process == "ttbj": return "TTBJ"
        if process == "ttcc": return "TTCC"
        if process == "ttcj": return "TTCJ"
        if process == "ttjj": return "TTJJ"
        if process == "bkg": return "1"
        if process == "ttother": return "TTOTHER"
#         if process == "zjets": return "1"
#         if process == "singletop": return "1"
    
    def doParametersOfInterest(self):
        """ create poi and other parameters, and define the poi set."""
        initFb = 1.
        initFc = 1.
        initFl = 1.
                
        #self.modelBuilder.doVar("k[%f,%f,%f]"%(initK, 0.1, 1))
        self.modelBuilder.doVar("Fb[%f,%f,%f]"%(initFb, 0.1, 3))
        poi = "Fb"
        self.modelBuilder.doVar("Fc[%f,%f,%f]"%(initFc, 0.1, 3))
        poi += ",Fc"
        self.modelBuilder.doVar("Fl[%f,%f,%f]"%(initFl, 0.1, 3))
        poi += ",Fl"
        
        
        # exp_ttbb = str(self.DC.exp["incl"]["ttbb"])
#         exp_ttbj = str(self.DC.exp["incl"]["ttbj"])
#         exp_ttcc = str(self.DC.exp["incl"]["ttcc"])
#         exp_ttcj = str(self.DC.exp["incl"]["ttcj"])
#         exp_ttjj = str(self.DC.exp["incl"]["ttjj"])
        
        self.modelBuilder.factory_("expr::TTBB(\"@0\", Fb)")
        self.modelBuilder.factory_("expr::TTBJ(\"@0\", Fb)")
        self.modelBuilder.factory_("expr::TTCC(\"@0\", Fc)")
        self.modelBuilder.factory_("expr::TTCJ(\"@0\", Fc)")
        self.modelBuilder.factory_("expr::TTJJ(\"@0\", Fl)")
        self.modelBuilder.factory_("expr::TTOTHER(\"@0\", Fl)")
        self.modelBuilder.doSet("POI",poi)



class TTHFModelAbsolute(PhysicsModel):
    def setModelBuilder(self, modelBuilder):
        PhysicsModel.setModelBuilder(self, modelBuilder)
        self.modelBuilder.doModelBOnly = False
        
    def getYieldScale(self,bin,process):
        #print process
        #print self.DC.print_structure()
        #print self.DC.exp[bin][process]
        if not self.DC.isSignal[process]: return 1
        if process == "ttbb": return "TTBB"
        if process == "ttbj": return "TTBJ"
        if process == "ttcc": return "TTCC"
        if process == "ttcj": return "TTCJ"
        if process == "ttjj": return "TTJJ"
        # if process == "rare": return "1"
#         if process == "zjets": return "1"
#         if process == "singletop": return "1"
    
    def doParametersOfInterest(self):
        """ create poi and other parameters, and define the poi set."""
        init_ttLF = 15
        init_ttbb = 0.2
        init_ttcc = 0.2
                
        #self.modelBuilder.doVar("k[%f,%f,%f]"%(initK, 0.1, 1))
        self.modelBuilder.doVar("xsec_ttLF[%f,%f,%f]"%(init_ttLF, 1, 25))
        poi = "xsec_ttLF"
        self.modelBuilder.doVar("xsec_ttbb[%f,%f,%f]"%(init_ttbb, 0.01, 2))
        poi += ",xsec_ttbb"
        self.modelBuilder.doVar("xsec_ttcc[%f,%f,%f]"%(init_ttcc, 0.01, 2))
        poi += ",xsec_ttcc"
        
        print self.DC.systs
        
        exp_ttbb = str(self.DC.exp["incl"]["ttbb"])
        exp_ttbj = str(self.DC.exp["incl"]["ttbj"])
        exp_ttcc = str(self.DC.exp["incl"]["ttcc"])
        exp_ttcj = str(self.DC.exp["incl"]["ttcj"])
        exp_ttjj = str(self.DC.exp["incl"]["ttjj"])
        exp_ttother = str(self.DC.exp["incl"]["ttother"])
        exp_bkg = str(self.DC.exp["incl"]["bkg"])
        
        eff_vis_ttbb = str(0.1189)
        eff_vis_ttbj = str(0.0704)
        eff_vis_ttcc = str(0.0474)
        eff_vis_ttcj = str(0.0396)
        eff_vis_ttjj = str(0.0268)

        self.modelBuilder.factory_("expr::TTBB(\"41500*%s*@0/%s\", xsec_ttbb)"%(eff_vis_ttbb,exp_ttbb))
        self.modelBuilder.factory_("expr::TTBJ(\"41500*%s*@0/%s\", xsec_ttbb)"%(eff_vis_ttbb,exp_ttbb))
        self.modelBuilder.factory_("expr::TTCC(\"41500*%s*@0/%s\", xsec_ttcc)"%(eff_vis_ttcc,exp_ttcc))
        self.modelBuilder.factory_("expr::TTCJ(\"41500*%s*@0/%s\", xsec_ttcc)"%(eff_vis_ttcc,exp_ttcc))
        self.modelBuilder.factory_("expr::TTJJ(\"41500*%s*@0/%s\", xsec_ttLF)"%(eff_vis_ttjj,exp_ttjj))
        self.modelBuilder.doSet("POI",poi)

class TTHFModelRelative(PhysicsModel):
    def setModelBuilder(self, modelBuilder):
        PhysicsModel.setModelBuilder(self, modelBuilder)
        self.modelBuilder.doModelBOnly = False
        
    def getYieldScale(self,bin,process):
        #print process
        #print self.DC.print_structure()
        #print self.DC.exp[bin][process]
        if not self.DC.isSignal[process]: return 1
        if process == "ttbb": return "TTBB"
        if process == "ttbj": return "TTBJ"
        if process == "ttcc": return "TTCC"
        if process == "ttcj": return "TTCJ"
        if process == "ttjj": return "TTJJ"
        # if process == "rare": return "1"
#         if process == "zjets": return "1"
#         if process == "singletop": return "1"
    
    def doParametersOfInterest(self):
        """ create poi and other parameters, and define the poi set."""
        init_ttincl = 17
        init_rb = 0.01
        init_rc = 0.01
                
        #self.modelBuilder.doVar("k[%f,%f,%f]"%(initK, 0.1, 1))
        self.modelBuilder.doVar("xsec_ttincl[%f,%f,%f]"%(init_ttincl, 1, 25))
        poi = "xsec_ttincl"
        self.modelBuilder.doVar("rb[%f,%f,%f]"%(init_rb, 0.001, 0.2))
        poi += ",rb"
        self.modelBuilder.doVar("rc[%f,%f,%f]"%(init_rc, 0.001, 0.2))
        poi += ",rc"
        
        exp_ttbb = str(self.DC.exp["incl"]["ttbb"])
        exp_ttbj = str(self.DC.exp["incl"]["ttbj"])
        exp_ttcc = str(self.DC.exp["incl"]["ttcc"])
        exp_ttcj = str(self.DC.exp["incl"]["ttcj"])
        exp_ttjj = str(self.DC.exp["incl"]["ttjj"])
        exp_ttother = str(self.DC.exp["incl"]["ttother"])
        exp_bkg = str(self.DC.exp["incl"]["bkg"])
        
        eff_vis_ttbb = str(0.1189)
        eff_vis_ttbj = str(0.0704)
        eff_vis_ttcc = str(0.0474)
        eff_vis_ttcj = str(0.0396)
        eff_vis_ttjj = str(0.0268)

        self.modelBuilder.factory_("expr::TTBB(\"41500*%s*@0*@1/%s\", xsec_ttincl,rb)"%(eff_vis_ttbb,exp_ttbb))
        self.modelBuilder.factory_("expr::TTBJ(\"41500*%s*@0*@1/%s\", xsec_ttincl,rb)"%(eff_vis_ttbb,exp_ttbb))
        self.modelBuilder.factory_("expr::TTCC(\"41500*%s*@0*@1/%s\", xsec_ttincl,rc)"%(eff_vis_ttcc,exp_ttcc))
        self.modelBuilder.factory_("expr::TTCJ(\"41500*%s*@0*@1/%s\", xsec_ttincl,rc)"%(eff_vis_ttcc,exp_ttcc))
        self.modelBuilder.factory_("expr::TTJJ(\"41500*%s*@0*(1-@1-@2)/%s\", xsec_ttincl,rb,rc)"%(eff_vis_ttjj,exp_ttjj))
        self.modelBuilder.doSet("POI",poi)

TTHFModelScale = TTHFModelScale()
TTHFModelAbsolute = TTHFModelAbsolute()
TTHFModelRelative = TTHFModelRelative()