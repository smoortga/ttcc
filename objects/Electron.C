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
   
   _isMediumMVAId = 0;
   _isTightMVAId = 0;
   
   _relIso = 0;
   
   _w_CBid = 1.;
   _w_CBidUp = 1.;
   _w_CBidDown = 1.;
   
   _w_MVAid = 1.;
   _w_MVAidUp = 1.;
   _w_MVAidDown = 1.;
}

std::pair<float,float> Electron::GetSF(TH2F* h)
{
    
    
    std::pair<float,float> w;

    float v = 1.;
    float err = 0.;
    
    if (_pt == VDEF || _eta == VDEF)
    {
        std::cout << "WARNING: Electron SF is not properly calculated, you may have forgotton to set the Electron pT and Eta before calling this function!" << std::endl;
        std::cout << "The SF will be set to 1 with 0 error!" << std::endl;
        return std::make_pair(v,err);
    }
    
    if (!h)
    {
        std::cout << "WARNING: Electron SF is not properly calculated, The histogram is not valid!" << std::endl;
        std::cout << "The SF will be set to 1 with 0 error!" << std::endl;
        return std::make_pair(v,err);
    }

    if( fabs(_eta) > 2.5 ) 
    {
        // Don't give a warning, SFs are simply not defined in this regime, and people should not use Electrons here anyway
        return std::make_pair(v,err);
    }
    
    int nbinsX = h->GetXaxis()->GetNbins();
    int nbinsY = h->GetYaxis()->GetNbins();

    int ibinX = h->GetXaxis()->FindBin(_eta);

    if( _pt < 500 && _pt >= 0 )
     {	
        int ibinY = h->GetYaxis()->FindBin(_pt);

        v = h->GetBinContent(ibinX,ibinY);
        err = h->GetBinError(ibinX,ibinY);
     }
    else
     {
        v = h->GetBinContent(ibinX,nbinsY);
        err = h->GetBinError(ibinX,nbinsY);
     }  

    w = std::make_pair(v,err);

    return w;
}


