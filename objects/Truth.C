#include "Truth.h"  

// Label convention
// t(1) >  B(10) W(11) > [l(110) nu(111)] [q(112) q(113)]
// tbar(2) >  B(20) W(21) > [l(210) nu(211)] [q(212) q(213)]
// Additional jets not yet included (they might not be generated but rather come from parton showering)

// label_name convention
// t(top) >  B(top_b) W(top_W) > [l(top_lep) nu(top_nu)] [q(top_had1) q(top_had2)]
// tbar(antitop) >  B(antitop_b) W(antitop_W) > [l(antitop_lep) nu(antitop_nu)] [q(antitop_had1) q(antitop_had2)]


Truth::Truth()
{
    init();
}


Truth::~Truth()
{
}


void Truth::init()
{
   _E        = VDEF;
   _pt       = VDEF;
   _eta      = VDEF;
   _phi      = VDEF;
   _m        = VDEF;
   _charge   = VDEF;
   _id        = VDEF;
   _label        = VDEF;
   _label_name        = "UNDEFINED";
   


}






