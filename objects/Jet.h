#ifndef JET_H
#define JET_H

#include "TObject.h"
#include "TLorentzVector.h"
#include <iostream>

#define VDEF -666

class Jet : public TObject
{
 public:
   Jet();
            
   virtual ~Jet();

   // static bool sortPtPredicate(Jet lhs, Jet rhs)
//      {return (lhs.pt() > rhs.pt());};
   
   //int ID()    {return _ID;};
   
   //void sel();
   
   //bool _isdata;
   
   // Getters
   float E()         {return _E;};
   float Pt()        {return _pt;};
   float Eta()       {return _eta;};
   float Phi()       {return _phi;};
   float M()         {return _m;};
   float Charge()    {return _charge;};
   float ChargeVec()    {return _chargeVec;};
   
   bool IsLooseJetID()  {return _isLooseJetID;};
   bool IsTightJetID()  {return _isTightJetID;};
   
   int PartonFlavour()  {return _partonFlavour;};
   int HadronFlavour()  {return _hadronFlavour;};
   
   float CSVv2()                    {return _CSVv2;};
   float CMVAv2()                   {return _cMVAv2;};
   float CTagCvsL()                 {return _CTagCvsL;};
   float CTagCvsB()                 {return _CTagCvsB;};
   float DeepCSVBDiscr()            {return _DeepCSVBDiscr;};
   float DeepCSVCvsL()              {return _DeepCSVCvsL;};
   float DeepCSVCvsB()              {return _DeepCSVCvsB;};
   float DeepFlavourBDiscr()        {return _DeepFlavourBDiscr;};
   float DeepFlavourCvsL()          {return _DeepFlavourCvsL;};
   float DeepFlavourCvsB()          {return _DeepFlavourCvsB;};
   
   bool HasGenJet()                 {return _hasGenJet;};
   float GenJetPt()                 {return _genJetPt;};
   float GenJetEta()                 {return _genJetEta;};
   float GenJetPhi()                 {return _genJetPhi;};
   float GenJetM()                 {return _genJetM;};
   float GenJetE()                 {return _genJetE;};
   float GenJetStatus()                 {return _genJetStatus;};
   float GenJetID()                 {return _genJetID;};
   
   bool HasGenParton()                 {return _hasGenParton;};
   float GenPartonPt()                 {return _genPartonPt;};
   float GenPartonEta()                 {return _genPartonEta;};
   float GenPartonPhi()                 {return _genPartonPhi;};
   float GenPartonM()                 {return _genPartonM;};
   float GenPartonE()                 {return _genPartonE;};
   float GenPartonStatus()                 {return _genPartonStatus;};
   float GenPartonID()                 {return _genPartonID;};
   

   TLorentzVector p4()  {return _p4;};
   
   
   // Setters
   void setE(float E)         {_E = E;};
   void setPt(float pt)        {_pt = pt;};
   void setEta(float eta)       {_eta = eta;};
   void setPhi(float phi)       {_phi = phi;};
   void setM(float m)         {_m = m;};
   void setCharge(float charge)    {_charge = charge;};
   void setChargeVec(float chargevec)    {_chargeVec = chargevec;};
   
   void setIsLooseJetID(bool isloosejetid)  { _isLooseJetID = isloosejetid;};
   void setIsTightJetID(bool istightjetid)  { _isTightJetID = istightjetid;};
   
   void setPartonFlavour(int partonflavour) { _partonFlavour = partonflavour;};
   void setHadronFlavour(int hadronflavour) { _hadronFlavour = hadronflavour;};
   
   void setCSVv2(float csvv2)                           {_CSVv2 = csvv2;};
   void setCMVAv2(float cmvav2)                         {_cMVAv2 = cmvav2;};
   void setCTagCvsL(float ctagcvsl)                     {_CTagCvsL = ctagcvsl;};
   void setCTagCvsB(float ctagcvsb)                     {_CTagCvsB = ctagcvsb;};
   void setDeepCSVBDiscr(float deepcsvbdiscr)           {_DeepCSVBDiscr = deepcsvbdiscr;};
   void setDeepCSVCvsL(float deepcsvcvsl)               {_DeepCSVCvsL = deepcsvcvsl;};
   void setDeepCSVCvsB(float deepcsvcvsb)               {_DeepCSVCvsB = deepcsvcvsb;};
   void setDeepFlavourBDiscr(float deepflavourbdiscr)   {_DeepFlavourBDiscr = deepflavourbdiscr;};
   void setDeepFlavourCvsL(float deepflavourcvsl)       {_DeepFlavourCvsL = deepflavourcvsl;};
   void setDeepFlavourCvsB(float deepflavourcvsb)       {_DeepFlavourCvsB = deepflavourcvsb;};
   
   void setHasGenJet(bool hasgenjet)                    {_hasGenJet = hasgenjet;};
   void setGenJetPt(float genjetpt)                     {_genJetPt = genjetpt;};
   void setGenJetEta(float genjeteta)                   {_genJetEta = genjeteta;};
   void setGenJetPhi(float genjetphi)                   {_genJetPhi = genjetphi;};
   void setGenJetM(float genjetm)                       {_genJetM = genjetm;};
   void setGenJetE(float genjete)                       {_genJetE = genjete;};
   void setGenJetStatus(int genjetstatus)               {_genJetStatus = genjetstatus;};
   void setGenJetID(int genjetid)                       {_genJetID = genjetid;};
   
   void setHasGenParton(bool hasgenparton)              {_hasGenParton = hasgenparton;};
   void setGenPartonPt(float genpartonpt)               {_genPartonPt = genpartonpt;};
   void setGenPartonEta(float genpartoneta)             {_genPartonEta = genpartoneta;};
   void setGenPartonPhi(float genpartonphi)             {_genPartonPhi = genpartonphi;};
   void setGenPartonM(float genpartonm)                 {_genPartonM = genpartonm;};
   void setGenPartonE(float genpartone)                 {_genPartonE = genpartone;};
   void setGenPartonStatus(int genpartonstatus)         {_genPartonStatus = genpartonstatus;};
   void setGenPartonID(int genpartonid)                 {_genPartonID = genpartonid;};

   void setp4()  
   {
    if(_pt > 0.) _p4.SetPtEtaPhiE(_pt,_eta,_phi,_E);
    else{
        std::cout << "WARNING: pT < 0 (" << _pt << "), p4 not filled!!!" << std::endl;
        std::cout << "Did you perhaps forget to initialize pt, eta, phi and E?" << std::endl;
    }
   };
   
   //void read();
   void init();
	
 protected:

   //std::pair<float,float> getSF(float eta,float pt);
   
   float _E;
   float _pt;
   float _eta;
   float _phi;
   float _m;
   float _charge;
   float _chargeVec;
   
   bool _isLooseJetID;
   bool _isTightJetID;
   
   int _partonFlavour;
   int _hadronFlavour;
   
   float _CSVv2;
   float _cMVAv2;
   float _CTagCvsL;
   float _CTagCvsB;
   float _DeepCSVBDiscr;
   float _DeepCSVCvsL;
   float _DeepCSVCvsB;
   float _DeepFlavourBDiscr;
   float _DeepFlavourCvsL;
   float _DeepFlavourCvsB;
   
   bool _hasGenJet;
   float _genJetPt;
   float _genJetEta;
   float _genJetPhi;
   float _genJetE;
   float _genJetM;
   int _genJetStatus;
   int _genJetID;
   
   bool _hasGenParton;
   float _genPartonPt;
   float _genPartonEta;
   float _genPartonPhi;
   float _genPartonE;
   float _genPartonM;
   int _genPartonStatus;
   int _genPartonID;
   

   TLorentzVector _p4;
   
  
   ClassDef(Jet,1)
};

#endif
