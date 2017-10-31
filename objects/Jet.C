#include "Jet.h"  

Jet::Jet()
{
    init();
}


Jet::~Jet()
{
}


void Jet::init()
{
    _E        = VDEF;
    _pt       = VDEF;
    _eta      = VDEF;
    _phi      = VDEF;
    _m        = VDEF;

    _charge   = VDEF;
    _chargeVec = VDEF;

    _isLooseJetID = 0;
    _isTightJetID = 0;

    _hadronFlavour = 0;
    _partonFlavour = 0;

    _CSVv2 = VDEF;
    _cMVAv2 = VDEF;
    _CTagCvsL = VDEF;
    _CTagCvsB = VDEF;
    _DeepCSVBDiscr = VDEF;
    _DeepCSVCvsL = VDEF;
    _DeepCSVCvsB = VDEF;
    _DeepFlavourBDiscr = VDEF;
    _DeepFlavourCvsL = VDEF;
    _DeepFlavourCvsB = VDEF;
    
    _hasGenJet = 0;
    _genJetPt = VDEF;
    _genJetEta = VDEF;
    _genJetPhi = VDEF;
    _genJetE = VDEF;
    _genJetM = VDEF;
    _genJetStatus = 0;
    _genJetID = 0;
    
    _hasGenParton = 0;
    _genPartonPt = VDEF;
    _genPartonEta = VDEF;
    _genPartonPhi = VDEF;
    _genPartonE = VDEF;
    _genPartonM = VDEF;
    _genPartonStatus = 0;
    _genPartonID = 0;



}


