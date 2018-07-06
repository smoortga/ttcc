#ifndef GENJET_H
#define GENJET_H

#include "TObject.h"
#include "TLorentzVector.h"
#include <iostream>

#define VDEF -666

class GenJet : public TObject
{
 public:
   GenJet();
            
   virtual ~GenJet();
   
   // Getters
   float E()         {return _E;};
   float Pt()        {return _pt;};
   float Eta()       {return _eta;};
   float Phi()       {return _phi;};
   float M()         {return _m;};
   int Flavour()  {return _flavour;};
   
   void setE(float E)         {_E = E;};
   void setPt(float pt)        {_pt = pt;};
   void setEta(float eta)       {_eta = eta;};
   void setPhi(float phi)       {_phi = phi;};
   void setM(float m)         {_m = m;};
   void setFlavour(float flavour)    {_flavour = flavour;};
   
   
   
   //void read();
   void init();
	
 protected:

   //std::pair<float,float> getSF(float eta,float pt);
   
   float _E;
   float _pt;
   float _eta;
   float _phi;
   float _m;
   int _flavour;
   
   
   
  
   ClassDef(GenJet,1)
};

#endif
