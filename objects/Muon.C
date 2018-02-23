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
   
   _w_Id = 1.;
   _w_IdUp = 1.;
   _w_IdDown = 1.;
   
   _w_Iso = 1.;
   _w_IsoUp = 1.;
   _w_IsoDown = 1.;
      
   _charge   = 0;
   _id   = 0;
   
   _relIso = 0;

}


std::pair<float,float> Muon::GetSF(TH2F* h)
{
    std::pair<float,float> w;

    float v = 1.;
    float err = 0.;
    
    if (_pt == VDEF || _eta == VDEF)
    {
        std::cout << "WARNING: Muon SF is not properly calculated, you may have forgotton to set the Electron pT and Eta before calling this function!" << std::endl;
        std::cout << "The SF will be set to 1 with 0 error!" << std::endl;
        return std::make_pair(v,err);
    }
    
    if (!h)
    {
        std::cout << "WARNING: Muon SF is not properly calculated, The histogram is not valid!" << std::endl;
        std::cout << "The SF will be set to 1 with 0 error!" << std::endl;
        return std::make_pair(v,err);
    }

    if( fabs(_eta) > 2.4 ) 
    {
        // Don't give a warning, SFs are simply not defined in this regime, and people should not use Electrons here anyway
        return std::make_pair(v,err);
    }
    
    int nbinsX = h->GetXaxis()->GetNbins();
    int nbinsY = h->GetYaxis()->GetNbins();

    int ibinX = h->GetXaxis()->FindBin( fabs(_eta) );

    if( _pt < 120 && _pt >= 0 )
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


