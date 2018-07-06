#include "Electron.h"
#include "Muon.h"
#include "Jet.h"
#include "GenJet.h"
#include "Trigger.h"
#include "MissingEnergy.h"
#include "Truth.h"

#ifdef __CINT__

#pragma link off all global;
#pragma link off all class;
#pragma link off all function;

#pragma link C++ nestedclasses;
#pragma link C++ nestedtypedef;

//#pragma link C++ class std::pair<TString,double>+;
//#pragma link C++ class std::pair<unsigned int,double>+;
#pragma link C++ class Electron+;
#pragma link C++ class std::vector<Electron*>+;
#pragma link C++ class Muon+;
#pragma link C++ class std::vector<Muon*>+;
#pragma link C++ class Trigger+;
#pragma link C++ class std::vector<Trigger*>+;
#pragma link C++ class MissingEnergy+;
#pragma link C++ class std::vector<MissingEnergy*>+;
#pragma link C++ class Jet+;
#pragma link C++ class std::vector<Jet*>+;
#pragma link C++ class GenJet+;
#pragma link C++ class std::vector<GenJet*>+;
#pragma link C++ class Truth+;
#pragma link C++ class std::vector<Truth*>+;

#endif
