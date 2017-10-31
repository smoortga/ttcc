{
    gROOT->ProcessLine(".L ../objects/Electron.C+");
    gROOT->ProcessLine(".L ../objects/Muon.C+");
    gROOT->ProcessLine(".L ../selection/LoadVectorDict.C+");
	gSystem->Exit(0);
}
