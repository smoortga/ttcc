#ifndef MUON_H
#define MUON_H

#include "TObject.h"
#include "TLorentzVector.h"
#include "TH2F.h"
#include <iostream>

#define VDEF -666

class Muon : public TObject
{
 public:
   Muon();
            
   virtual ~Muon();

   std::pair<float,float> GetSF_pteta(TH2* h);
   std::pair<float,float> GetSF_etapt(TH2* h);
   
   // Getters
   // kinematics
   float E()         {return _E;};
   float Pt()        {return _pt;};
   float Eta()       {return _eta;};
   float Phi()       {return _phi;};
   float M()         {return _m;};

   TLorentzVector p4()  {return _p4;};
   
   float Dxy()         {return _dxy;};
   float Dz()         {return _dz;};
   bool isLoose()         {return _isLoose;};
   bool isTight()         {return _isTight;};
   
   bool isLooseID()         {return _isLooseID;};
   bool isTightID()         {return _isTightID;};
   
   float w_Id()     {return _w_Id;};
   float w_IdUp()     {return _w_IdUp;};
   float w_IdDown()     {return _w_IdDown;};
   
   float w_Iso()     {return _w_Iso;};
   float w_IsoUp()     {return _w_IsoUp;};
   float w_IsoDown()     {return _w_IsoDown;};
   
   float w_Trig()     {return _w_Trig;};
   float w_TrigUp()     {return _w_TrigUp;};
   float w_TrigDown()     {return _w_TrigDown;};
   
   int Charge()         {return _charge;};
   int Id()         {return _id;};
   

   float relIso()     {return _relIso;};
 
   
   // Setters
   void setE(float E)         {_E = E;};
   void setPt(float pt)        {_pt = pt;};
   void setEta(float eta)       {_eta = eta;};
   void setPhi(float phi)       {_phi = phi;};
   void setM(float m)         {_m = m;};

   void setp4()  
   {
    if(_pt > 0.) _p4.SetPtEtaPhiE(_pt,_eta,_phi,_E);
    else{
        std::cout << "WARNING: pT < 0 (" << _pt << "), p4 not filled!!!" << std::endl;
        std::cout << "Did you perhaps forget to initialize pt, eta, phi and E?" << std::endl;
    }
   };
   
   void setDxy(float dxy)         {_dxy = dxy;};
   void setDz(float dz)         {_dz = dz;};
   
   void setCharge(int ch)         {_charge = ch;};
   void setId(int id)         {_id = id;};
   
   void setIsLooseID(bool isLooseID){_isLooseID = isLooseID;} // This is based on the information that is already in MINIAOD (mu_isLooseMuon)
   void setIsTightID(bool isTightID){_isTightID = isTightID;}
   
   void setWeightId(float w_Id)         {_w_Id = w_Id;};
   void setWeightIdUp(float w_IdUp)         {_w_IdUp = w_IdUp;};
   void setWeightIdDown(float w_IdDown)         {_w_IdDown = w_IdDown;};
   
   void setWeightIso(float w_Iso)         {_w_Iso = w_Iso;};
   void setWeightIsoUp(float w_IsoUp)         {_w_IsoUp = w_IsoUp;};
   void setWeightIsoDown(float w_IsoDown)         {_w_IsoDown = w_IsoDown;};
   
   void setWeightTrig(float w_Trig)         {_w_Trig = w_Trig;};
   void setWeightTrigUp(float w_TrigUp)         {_w_TrigUp = w_TrigUp;};
   void setWeightTrigDown(float w_TrigDown)         {_w_TrigDown = w_TrigDown;};
   

   void setRelIso(float chargedIso, float neutralIso, float photonIso, float PUIso, float eA=0, float evt_rho=0)
   {
     if (_pt>0){ 
        _relIso = (chargedIso+std::max((float)(neutralIso+photonIso-0.5*PUIso),0.0f))/_pt;
     }
     else {
        std::cout << "WARNING: pT < 0 (" << _pt << "), relIso not filled!!!" << std::endl;
        std::cout << "Did you perhaps forget to initialize pt?" << std::endl;
     }
   };
   
   void setIsLoose(){ // These definitions are user-defined, i.e. not yet pre-defined in miniAOD
    _isLoose = (
	       (_pt > 10.) &&
	       (fabs(_eta) < 2.5) &&
//	       passDxy &&
//	       passDz &&
	       _isLooseID &&
	       _relIso < 0.25
	      );
	};
   
   void setIsTight(){
    _isTight = (
	       _isLoose &&
	       (_pt > 25.) &&
	       (fabs(_eta) < 2.4) &&
	       _isTightID &&
	       _relIso < 0.15
	      );
   };
   
   
   //void read();
   void init();
	
 protected:

   //std::pair<float,float> getSF(float eta,float pt);
   
   float _E;
   float _pt;
   float _eta;
   float _phi;
   float _m;

   TLorentzVector _p4;
   
   float _dxy;
   float _dz;
   bool _isLoose;
   bool _isTight;
   bool _isLooseID;
   bool _isTightID;
   
   float _w_Id;
   float _w_IdUp;
   float _w_IdDown;
   
   float _w_Iso;
   float _w_IsoUp;
   float _w_IsoDown;
   
   float _w_Trig;
   float _w_TrigUp;
   float _w_TrigDown;
   
   
   int _charge;
   int _id;

   float _relIso;
   
   
   ClassDef(Muon,1)
};

#endif
