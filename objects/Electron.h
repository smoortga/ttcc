#ifndef ELECTRON_H
#define ELECTRON_H

#include "TObject.h"
#include "TLorentzVector.h"
#include "TH2F.h"
#include "TFile.h"
#include <iostream>

#define VDEF -666

class Electron : public TObject
{
 public:
   Electron();
            
   virtual ~Electron();
    
   // Get SF
   std::pair<float,float> GetSF(TH2F* h);
   std::pair<float,float> GetSFTrigger(TH2D* h);
   
   // Getters
   // kinematics
   float E()         {return _E;};
   float Pt()        {return _pt;};
   float Eta()       {return _eta;};
   float Scleta()       {return _scleta;};
   float Phi()       {return _phi;};
   float M()         {return _m;};

   TLorentzVector p4()  {return _p4;};
   
   float Dxy()         {return _dxy;};
   float Dz()         {return _dz;};
   bool isLoose()         {return _isLoose;};
   bool isMedium()         {return _isMedium;};
   bool isTight()         {return _isTight;};
   
   int Charge()         {return _charge;};
   int Id()         {return _id;};
   
   // https://twiki.cern.ch/twiki/bin/view/CMS/EgammaIDRecipesRun2
   bool isLooseCBId()     {return _isLooseCBId;};
   bool isMediumCBId()     {return _isMediumCBId;};
   bool isTightCBId()     {return _isTightCBId;};
   
   bool isMediumMVAId()     {return _isMediumMVAId;};
   bool isTightMVAId()     {return _isTightMVAId;};
   
   float relIso()     {return _relIso;};
   
   float w_CBid()     {return _w_CBid;};
   float w_CBidUp()     {return _w_CBidUp;};
   float w_CBidDown()     {return _w_CBidDown;};
   
   float w_MVAid()     {return _w_MVAid;};
   float w_MVAidUp()     {return _w_MVAidUp;};
   float w_MVAidDown()     {return _w_MVAidDown;};
   
   float w_Reco()     {return _w_Reco;};
   float w_RecoUp()     {return _w_RecoUp;};
   float w_RecoDown()     {return _w_RecoDown;};
   
   float w_Trig()     {return _w_Trig;};
   float w_TrigUp()     {return _w_TrigUp;};
   float w_TrigDown()     {return _w_TrigDown;};
   
   // Setters
   void setE(float E)         {_E = E;};
   void setPt(float pt)        {_pt = pt;};
   void setEta(float eta)       {_eta = eta;};
   void setScleta(float scleta)       {_scleta = scleta;};
   void setPhi(float phi)       {_phi = phi;};
   void setM(float m)         {_m = m;};

   void setp4()  
   {
    if(_pt > 0.) _p4.SetPtEtaPhiE(_pt,_eta,_phi,_E);
    else{
        std::cout << "WARNING: pT < 0 (" << _pt << "), p4 not filled!!!" << std::endl;
        std::cout << "Please check if pt, eta, phi and E were properly set" << std::endl;
    }
   };
   
   void setDxy(float dxy)         {_dxy = dxy;};
   void setDz(float dz)         {_dz = dz;};
   
   void setCharge(int ch)         {_charge = ch;};
   void setId(int id)         {_id = id;};
   
   void setIsLooseCBId(bool isLCBId)     {_isLooseCBId = isLCBId;};
   void setIsMediumCBId(bool isMCBId)     {_isMediumCBId = isMCBId;};
   void setIsTightCBId(bool isTCBId)     {_isTightCBId = isTCBId;};
   
   void setIsMediumMVAId(bool isMMVAId)     {_isMediumMVAId = isMMVAId;};
   void setIsTightMVAId(bool isTMVAId)     {_isTightMVAId = isTMVAId;};
   
   void setWeightCBId(float w_CBid)         {_w_CBid = w_CBid;};
   void setWeightCBIdUp(float w_CBidUp)         {_w_CBidUp = w_CBidUp;};
   void setWeightCBIdDown(float w_CBidDown)         {_w_CBidDown = w_CBidDown;};
   
   void setWeightMVAId(float w_MVAid)         {_w_MVAid = w_MVAid;};
   void setWeightMVAIdUp(float w_MVAidUp)         {_w_MVAidUp = w_MVAidUp;};
   void setWeightMVAIdDown(float w_MVAidDown)         {_w_MVAidDown = w_MVAidDown;};
   
   void setWeightReco(float w_Reco)         {_w_Reco = w_Reco;};
   void setWeightRecoUp(float w_RecoUp)         {_w_RecoUp = w_RecoUp;};
   void setWeightRecoDown(float w_RecoDown)         {_w_RecoDown = w_RecoDown;};
   
   void setWeightTrig(float w_Trig)         {_w_Trig = w_Trig;};
   void setWeightTrigUp(float w_TrigUp)         {_w_TrigUp = w_TrigUp;};
   void setWeightTrigDown(float w_TrigDown)         {_w_TrigDown = w_TrigDown;};

   void setRelIso(float chargedIso, float neutralIso, float photonIso, float eA=0, float evt_rho=0)
   {
     if (_pt>0){ 
        _relIso = (chargedIso+std::max(neutralIso+photonIso-(eA*evt_rho),0.0f))/_pt;
     }
     else {
        std::cout << "WARNING: pT < 0 (" << _pt << "), relIso not filled!!!" << std::endl;
        std::cout << "Please check if pT was properly set" << std::endl;
     }
   };
   
   void setIsLoose(){
    _isLoose = (
	       (_pt > 10.) &&
	       (fabs(_eta) < 2.5) &&
//	       passDxy &&
//	       passDz &&
//	       passCrack &&
//	       passConversionVeto &&
//	       passRelIsoLoose &&
	       _isLooseCBId
	      );
	};
   
   void setIsMedium(){
    _isMedium = (
	       _isLoose &&
	       (_pt > 20.) &&
	       (fabs(_eta) < 2.4) &&
	       _isMediumCBId
//	       passRelIsoTight
	      );
   };
   
   void setIsTight(){
    _isTight = (
	       _isMedium &&
	       (_pt > 35.) &&
	       (fabs(_eta) < 2.1) &&
	       _isTightCBId
//	       passRelIsoTight
	      );
   };
   
   //void read();
   void init();
	
 protected:

   //std::pair<float,float> getSF(float eta,float pt);
   
   float _E;
   float _pt;
   float _eta;
   float _scleta;
   float _phi;
   float _m;

   TLorentzVector _p4;
   
   float _dxy;
   float _dz;
   bool _isLoose;
   bool _isMedium;
   bool _isTight;
   
   int _charge;
   int _id;
   
   bool _isLooseCBId;
   bool _isMediumCBId;
   bool _isTightCBId;
   
   bool _isMediumMVAId;
   bool _isTightMVAId;
   
   float _relIso;
   
   float _w_CBid;
   float _w_CBidUp;
   float _w_CBidDown;
   
   float _w_MVAid;
   float _w_MVAidUp;
   float _w_MVAidDown;
   
   float _w_Reco;
   float _w_RecoUp;
   float _w_RecoDown;
   
   float _w_Trig;
   float _w_TrigUp;
   float _w_TrigDown;
   
   ClassDef(Electron,1)
};

#endif
