#include "Trigger.h"  

Trigger::Trigger()
{
    init();
}


Trigger::~Trigger()
{
}


void Trigger::init()
{
    _idx = 0;
    _name = "";
    _pass = 0;
    _prescale = VDEF;
    _HLTprescale = VDEF;
    _L1prescale = VDEF;

}


