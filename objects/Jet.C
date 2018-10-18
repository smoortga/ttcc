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

    _hadronFlavour = VDEF;
    _partonFlavour = VDEF;

    _CSVv2 = VDEF;
    _cMVAv2 = VDEF;
    _CTagCvsL = VDEF;
    _CTagCvsB = VDEF;
    _DeepCSVProbudsg = VDEF;
    _DeepCSVProbb = VDEF;
    _DeepCSVProbbb = VDEF;
    _DeepCSVProbc = VDEF;
    _DeepCSVProbcc = VDEF;
    _DeepCSVBDiscr = VDEF;
    _DeepCSVCvsL = VDEF;
    _DeepCSVCvsB = VDEF;
    _DeepFlavourBDiscr = VDEF;
    _DeepFlavourCvsL = VDEF;
    _DeepFlavourCvsB = VDEF;
    _DeepFlavourProbuds = VDEF;
    _DeepFlavourProbg = VDEF;
    _DeepFlavourProbb = VDEF;
    _DeepFlavourProbbb = VDEF;
    _DeepFlavourProblepb = VDEF;
    _DeepFlavourProbc = VDEF;
    
    _hasGenJet = 0;
    _genJetPt = VDEF;
    _genJetEta = VDEF;
    _genJetPhi = VDEF;
    _genJetE = VDEF;
    _genJetM = VDEF;
    _genJetStatus = VDEF;
    _genJetID = VDEF;
    
    _hasGenParton = 0;
    _genPartonPt = VDEF;
    _genPartonEta = VDEF;
    _genPartonPhi = VDEF;
    _genPartonE = VDEF;
    _genPartonM = VDEF;
    _genPartonStatus = VDEF;
    _genPartonID = VDEF;
    
    _SfIterativeFitCentral = 1.;
    _SfIterativeFitJesUp = 1.;
    _SfIterativeFitJesDown = 1.;
    _SfIterativeFitLfUp = 1.;
    _SfIterativeFitLfDown = 1.;
    _SfIterativeFitHfUp = 1.;
    _SfIterativeFitHfDown = 1.;
    _SfIterativeFitHfstats1Up = 1.;
    _SfIterativeFitHfstats1Down = 1.;
    _SfIterativeFitHfstats2Up = 1.;
    _SfIterativeFitHfstats2Down = 1.;
    _SfIterativeFitCferr1Up = 1.;
    _SfIterativeFitCferr1Down = 1.;
    _SfIterativeFitCferr2Up = 1.;
    _SfIterativeFitCferr2Down = 1.;
    _SfIterativeFitLfstats1Up = 1.;
    _SfIterativeFitLfstats1Down = 1.;
    _SfIterativeFitLfstats2Up = 1.;
    _SfIterativeFitLfstats2Down = 1.;
    
    _SfDeepCSVTCentral = 1.;
    _SfDeepCSVTUp = 1.;
    _SfDeepCSVTDown = 1.;
    _SfDeepCSVMCentral = 1.;
    _SfDeepCSVMUp = 1.;
    _SfDeepCSVMDown = 1.;
    _SfDeepCSVLCentral = 1.;
    _SfDeepCSVLUp = 1.;
    _SfDeepCSVLDown = 1.;

}


