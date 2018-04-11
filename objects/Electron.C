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
   
   _w_Reco = 1.;
   _w_RecoUp = 1.;
   _w_RecoDown = 1.;
   
   _w_Trig = 1.;
   _w_TrigUp = 1.;
   _w_TrigDown = 1.;
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
    
    float etalow = h->GetXaxis()->GetXmin();
    float etahigh = h->GetXaxis()->GetXmax();
    float ptlow = h->GetYaxis()->GetXmin();
    float pthigh = h->GetYaxis()->GetXmax();
    
    if( fabs(_eta) < etalow || fabs(_eta) > etahigh ) 
    {
        std::cout << "WARNING: Electron SF is not properly calculated, eta = " << _eta << " is not in the range [" << etalow << "," << etahigh << "] ! Returning SF = 1 with err = 0" << std::endl;
        return std::make_pair(v,err);
    }
    
    int nbinsX = h->GetXaxis()->GetNbins();
    int nbinsY = h->GetYaxis()->GetNbins();

    int ibinX = h->GetXaxis()->FindBin(_eta);

    if( _pt < pthigh && _pt > ptlow )
     {	
        int ibinY = h->GetYaxis()->FindBin(_pt);

        v = h->GetBinContent(ibinX,ibinY);
        err = h->GetBinError(ibinX,ibinY);
     }
     // NOTE: PERHAPS THIS IS NOT WHAT SHOULD BE DONE... ALWAYS CHECK IF SF ARE WELL DEFINED IN THESE RANGES
    else if (_pt <= ptlow)
     {
        //std::cout << "WARNING: Electron SF altered, pt = " << _pt << " is below the lower threshold " << ptlow << "! SF of lowest bin will be chosen" << std::endl;
        v = h->GetBinContent(ibinX,1);
        err = h->GetBinError(ibinX,1);
     }
     else if (_pt >= pthigh)
     {
        //std::cout << "WARNING: Electron SF altered, pt = " << _pt << " is above the upper threshold " << pthigh << "! SF of highest bin will be chosen" << std::endl;
        v = h->GetBinContent(ibinX,nbinsY);
        err = h->GetBinError(ibinX,nbinsY);
     }  

    w = std::make_pair(v,err);

    return w;
}

// Trigger SFs for Electrons are stored slightly differently
std::pair<float,float> Electron::GetSFTrigger(TH2D* h)
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
    
    float ptlow = h->GetXaxis()->GetXmin();
    float pthigh = h->GetXaxis()->GetXmax();
    float etalow = h->GetYaxis()->GetXmin();
    float etahigh = h->GetYaxis()->GetXmax();

    if( fabs(_eta) < etalow || fabs(_eta) > etahigh ) 
    {
        std::cout << "WARNING: Electron Trigger SF is not properly calculated, eta = " << _eta << " is not in the range [" << etalow << "," << etahigh << "] ! Returning SF = 1 with err = 0" << std::endl;
        return std::make_pair(v,err);
    }
    
    int nbinsX = h->GetXaxis()->GetNbins();
    int nbinsY = h->GetYaxis()->GetNbins();

    
    if( _pt < pthigh && _pt > ptlow )
     {	
        int ibinX = h->GetXaxis()->FindBin(_pt);
        int ibinY = h->GetYaxis()->FindBin(_eta);

        v = h->GetBinContent(ibinX,ibinY);
        err = h->GetBinError(ibinX,ibinY);
     }
     // NOTE: PERHAPS THIS IS NOT WHAT SHOULD BE DONE... ALWAYS CHECK IF SF ARE WELL DEFINED IN THESE RANGES
    else if (_pt <= ptlow)
     {
        //std::cout << "WARNING: Electron Trigger SF altered, pt = " << _pt << " is below the lower threshold " << ptlow << "! SF of lowest bin will be chosen" << std::endl;
        int ibinY = h->GetYaxis()->FindBin(_eta);
        v = h->GetBinContent(1,ibinY);
        err = h->GetBinError(1,ibinY);
     }
     else if (_pt >= pthigh)
     {
        //std::cout << "WARNING: Electron Trigger SF altered, pt = " << _pt << " is above the upper threshold " << pthigh << "! SF of highest bin will be chosen" << std::endl;
        int ibinY = h->GetYaxis()->FindBin(_eta);
        v = h->GetBinContent(nbinsX,ibinY);
        err = h->GetBinError(nbinsX,ibinY);
     }  

    w = std::make_pair(v,err);

    return w;
}


