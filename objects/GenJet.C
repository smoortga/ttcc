#include "GenJet.h"  

GenJet::GenJet()
{
    init();
}


GenJet::~GenJet()
{
}


void GenJet::init()
{
    _E        = VDEF;
    _pt       = VDEF;
    _eta      = VDEF;
    _phi      = VDEF;
    _m        = VDEF;

    _flavour = VDEF;

}


