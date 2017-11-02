#include <vector>
#include "../objects/Electron.h"
#include "../objects/Muon.h"
#include "../objects/Jet.h"
#include "../objects/MissingEnergy.h"
#include "../objects/Trigger.h"
#ifdef __MAKECINT__
#pragma link C++ class vector<Electron*>+;
#pragma link C++ class vector<Muon*>+;
#pragma link C++ class vector<Jet*>+;
#pragma link C++ class vector<MET*>+;
#pragma link C++ class vector<Trigger*>+;
#endif