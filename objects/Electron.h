#ifndef ELECTRON_H
#define ELECTRON_H

#include "TObject.h"
#include "TLorentzVector.h"
#include <iostream>

#define VDEF -666

class Electron : public TObject
{
 public:
   Electron();
            
   virtual ~Electron();

   // static bool sortPtPredicate(Electron lhs, Electron rhs)
//      {return (lhs.pt() > rhs.pt());};
   
   //int ID()    {return _ID;};
   
   //void sel();
   
   //bool _isdata;
   
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
   bool isTight()         {return _isTight;};
   
   int Charge()         {return _charge;};
   int Id()         {return _id;};
   
   bool isLooseCBId()     {return _isLooseCBId;};
   bool isMediumCBId()     {return _isMediumCBId;};
   bool isTightCBId()     {return _isTightCBId;};
   
   float relIso()     {return _relIso;};
   
   float wid()     {return _wid;};
   float widUp()     {return _widUp;};
   float widDown()     {return _widDown;};
   
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
        std::cout << "Did you perhaps forget to initialize pt, eta, phi and E?" << std::endl;
    }
   };
   
   void setDxy(float dxy)         {_dxy = dxy;};
   void setDz(float dz)         {_dz = dz;};
   
   void setCharge(int ch)         {_charge = ch;};
   void setId(int id)         {_id = id;};
   
   void setIsLooseCBId(bool isLCBId)     {_isLooseCBId = isLCBId;};
   void setIsMediumCBId(bool isMCBId)     {_isMediumCBId = isMCBId;};
   void setIsTightCBId(bool isTCBId)     {_isTightCBId = isTCBId;};

   void setRelIso(float chargedIso, float neutralIso, float photonIso, float eA=0, float evt_rho=0)
   {
     if (_pt>0){ 
        _relIso = (chargedIso+std::max(neutralIso+photonIso-(eA*evt_rho),0.0f))/_pt;
     }
     else {
        std::cout << "WARNING: pT < 0 (" << _pt << "), relIso not filled!!!" << std::endl;
        std::cout << "Did you perhaps forget to initialize pt?" << std::endl;
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
   
   void setIsTight(){
    _isTight = (
	       _isLoose &&
	       (_pt > 35.) &&
	       (fabs(_eta) < 2.1) &&
	       _isMediumCBId
//	       passRelIsoTight
	      );
   };
   
   //void read();
   void init();
	
 protected:

   //std::pair<float,float> getSF(float eta,float pt);
   
   int _ID;
   
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
   bool _isTight;
   
   int _charge;
   int _id;
   
   bool _isLooseCBId;
   bool _isMediumCBId;
   bool _isTightCBId;
   
   float _relIso;
   
   float _wid;
   float _widUp;
   float _widDown;
   
   ClassDef(Electron,1)
};

#endif
