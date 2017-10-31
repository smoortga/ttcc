#include "Muon.h"  

Muon::Muon()
{
    init();
}


Muon::~Muon()
{
}


void Muon::init()
{
   _E        = VDEF;
   _pt       = VDEF;
   _eta      = VDEF;
   _phi      = VDEF;
   _m        = VDEF;
   _dxy        = VDEF;
   _dz        = VDEF;
   
   _isLoose   = 0;
   _isTight   = 0;
   _isLooseID   = 0;
   _isTightID   = 0;
      
   _charge   = 0;
   _id   = 0;
   
   _relIso = 0;

}


