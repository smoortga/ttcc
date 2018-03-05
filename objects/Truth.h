#ifndef TRUTH_H
#define TRUTH_H

#include "TObject.h"
#include "TLorentzVector.h"
#include <iostream>

#define VDEF -666

class Truth : public TObject
{
 public:
   Truth();
            
   virtual ~Truth();


   // Getters
   // kinematics
   float E()         {return _E;};
   float Pt()        {return _pt;};
   float Eta()       {return _eta;};
   float Phi()       {return _phi;};
   float M()         {return _m;};
   int Charge()      {return _charge;};
   int Id()          {return _id;};
   int Label()         {return _label;};
   TString LabelName()   {return _label_name;};
   TLorentzVector p4()  {return _p4;};

   // Setters
   void setE(float E)         {_E = E;};
   void setPt(float pt)        {_pt = pt;};
   void setEta(float eta)       {_eta = eta;};
   void setPhi(float phi)       {_phi = phi;};
   void setM(float m)       {_m = m;};
   void setCharge(int ch)   {_charge = ch;};
   void setId (int id)          {_id = id;};
   void setLabel (int label)          {_label = label;};
   void setLabelName (TString label_name)          {_label_name = label_name;};

   void setp4()  
   {
    if(_pt > 0.) _p4.SetPtEtaPhiE(_pt,_eta,_phi,_E);
    else{
        std::cout << "WARNING: pT < 0 (" << _pt << "), p4 not filled!!!" << std::endl;
        std::cout << "Did you perhaps forget to initialize pt, eta, phi and E?" << std::endl;
    }
   };
   
   // initializer
   void init();
	
 protected:

   
   float _E;
   float _pt;
   float _eta;
   float _phi;
   float _m;
   int _id;
   int _charge;
   int _label;
   TString _label_name;

   TLorentzVector _p4;
   
   
   ClassDef(Truth,1)
};

#endif
