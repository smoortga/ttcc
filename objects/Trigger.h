#ifndef TRIGGER_H
#define TRIGGER_H

#include "TObject.h"
#include "TString.h"
#include <iostream>

#define VDEF -666

class Trigger : public TObject
{
 public:
   Trigger();
            
   virtual ~Trigger();

   // static bool sortPtPredicate(Muon lhs, Muon rhs)
//      {return (lhs.pt() > rhs.pt());};
   
   //int ID()    {return _ID;};
   
   //void sel();
   
   //bool _isdata;
   
   // Getters
   // kinematics
   int Idx()         {return _idx;};
   TString Name()        {return _name;};
   bool Pass()        {return _pass;};
   float Prescale()        {return _prescale;};
   float HLTprescale()       {return _HLTprescale;};
   float L1prescale()         {return _L1prescale;};

   
   // Setters
   void setIdx(int idx)         {_idx = idx;};
   void setName(TString name)        {_name = name;};
   void setPass(bool pass)       {_pass = pass;};
   void setPrescale(float prescale)       {_prescale = prescale;};
   void setHLTprescale(float hltprescale)       {_HLTprescale = hltprescale;};
   void setL1prescale(float l1prescale)       {_L1prescale = l1prescale;};

   
   //void read();
   void init();
	
 protected:

   //std::pair<float,float> getSF(float eta,float pt);
   
   int _idx;
   TString _name;
   bool _pass;
   float _prescale;
   float _HLTprescale;
   float _L1prescale;
   
   
   ClassDef(Trigger,1)
};

#endif
