from math import sqrt, pow

def DileptonIvariantMass(lepton_1, lepton_2):
    total_p4 = lepton_1.p4() + lepton_2.p4()
    return total_p4.M()

def DileptonDeltaR(lepton1, lepton2):
    return sqrt(pow(lepton1.Phi()-lepton2.Phi(),2) + pow(lepton1.Eta()-lepton2.Eta(),2))