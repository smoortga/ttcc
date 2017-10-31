#include "Electron.h"  
Electron::Electron()
{
    init();
}


Electron::~Electron()
{
}


void Electron::init()
{
   _E        = VDEF;
   _pt       = VDEF;
   _eta      = VDEF;
   _phi      = VDEF;
   _m        = VDEF;
   _dxy        = VDEF;
   _dz        = VDEF;
   _scleta    = VDEF;
   
   _isLoose   = 0;
   _isTight   = 0;
      
   _charge   = 0;
   _id   = 0;
   
   _isLooseCBId = 0;
   _isMediumCBId = 0;
   _isTightCBId = 0;
   
   _relIso = 0;
   
   _wid = 1.;
   _widUp = 1.;
   _widDown = 1.;
}


