{
    gROOT->ProcessLine(".L ../objects/Electron.C+");
    gROOT->ProcessLine(".L ../objects/Muon.C+");
    gROOT->ProcessLine(".L ../objects/Jet.C+");
    gROOT->ProcessLine(".L ../objects/MissingEnergy.C+");
    gROOT->ProcessLine(".L ../objects/Trigger.C+");
    gROOT->ProcessLine(".L ../selection/LoadVectorDict.C+");
    gROOT->ProcessLine(".L ../selection/Converter.C+");
	gSystem->Exit(0);
}
