#ifndef MISSINGENERGY_H
#define MISSINGENERGY_H

#include "TObject.h"
#include <iostream>

#define VDEF -666

class MissingEnergy : public TObject
{
 public:
   MissingEnergy();
            
   virtual ~MissingEnergy();

   // static bool sortPtPredicate(Muon lhs, Muon rhs)
//      {return (lhs.pt() > rhs.pt());};
   
   //int ID()    {return _ID;};
   
   //void sel();
   
   //bool _isdata;
   
   // Getters
   // kinematics
   float ET()         {return _ET;};
   float Pt()        {return _pt;};
   float Px()        {return _px;};
   float Py()        {return _py;};
   float Phi()       {return _phi;};
   float Sig()         {return _sig;};

   
   // Setters
   void setET(float ET)         {_ET = ET;};
   void setPt(float pt)        {_pt = pt;};
   void setPx(float px)       {_px = px;};
   void setPy(float py)       {_py = py;};
   void setPhi(float phi)       {_phi = phi;};
   void setSig(float sig)         {_sig = sig;};

   
   //void read();
   void init();
	
 protected:

   //std::pair<float,float> getSF(float eta,float pt);
   
   float _ET;
   float _pt;
   float _px;
   float _py;
   float _phi;
   float _sig;
   
   
   ClassDef(MissingEnergy,1)
};

#endif
