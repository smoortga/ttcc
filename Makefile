CMSINC      = -I$(CMSSW_BASE)/src

CMSSWINC      = -I/cvmfs/cms.cern.ch/slc6_amd64_gcc530/cms/cmssw/CMSSW_8_0_25/src
JECLIB      = -L/cvmfs/cms.cern.ch/slc6_amd64_gcc530/cms/cmssw/CMSSW_8_0_25/lib/slc6_amd64_gcc530/ -lCondFormatsJetMETObjects -lJetMETCorrectionsModules -lRecoEgammaEgammaTools

ROOTCFLAGS    = $(shell $(ROOTSYS)/bin/root-config --cflags)
ROOTLIBS      = $(shell $(ROOTSYS)/bin/root-config --libs)
ROOTGLIBS     = $(shell $(ROOTSYS)/bin/root-config --glibs)

CXX           = g++ -g -Wno-write-strings -Wno-attributes -fPIC
LD            = g++
LDFLAGS       = -g
SOFLAGS       = -shared

CXXFLAGS       = $(ROOTCFLAGS)
INCLUDE_FLAGS  = $(CMSSWINC)
LDLIBS         = $(ROOTLIBS) $(JECLIB)
GLIBS          = $(ROOTGLIBS)

EXE           = selection/Selection

INC 	      = selection/Selection.h selection/Converter.h selection/BTagCalibrationStandalone.h \
                objects/Electron.h objects/Muon.h objects/Jet.h objects/GenJet.h \
		        objects/Trigger.h objects/MissingEnergy.h objects/Truth.h \

SRC	          = selection/Selection.C selection/Converter.C  selection/BTagCalibrationStandalone.C\
                objects/Electron.C objects/Muon.C objects/Jet.C objects/GenJet.C \
		        objects/Trigger.C objects/MissingEnergy.C objects/Truth.C \

OBJS          = selection/Selection.o selection/Converter.o selection/BTagCalibrationStandalone.o\
                objects/Electron.o objects/Muon.o objects/Jet.o objects/GenJet.o \
		        objects/Trigger.o objects/MissingEnergy.o objects/Truth.o

LIB           = libSelection.so

all: 	      $(LIB) $(EXE)

$(LIB):	      $(INC) $(SRC)
	      @echo "####### Generating dictionary"
	      @rootcint -f selection/SelectionDict.cxx -c -p $(CXXFLAGS) \
	      $(INCLUDE_FLAGS) -I. $(INC) objects/LinkDef.h

	      @echo "####### Building library $(LIB)"
	      @$(CXX) $(SOFLAGS) $(CXXFLAGS) $(ROOTLIBS) $(INCLUDE_FLAGS) -I. $(SRC) \
	      selection/SelectionDict.cxx -o $(LIB) $(ROOTLIBS)
	      
	      @echo  "####### Removing generated dictionary"
	      @rm -f selection/SelectionDict.cxx selection/SelectionDict.h
	      @rm -f *.o

$(EXE):	      $(LIB) selection/Selection.C
	      @echo "####### Building object file for executable"
	      @$(CXX) -c $(CXXFLAGS) $(INCLUDE_FLAGS) selection/Selection.C -o selection/Selection.o
	      @echo "####### Building executable"
	      @$(CXX) $(CXXFLAGS) selection/Selection.o $(LDLIBS) $(LIB) -o $(EXE)

clean:
	      @rm -f $(OBJS) $(EXE) selection/SelectionDict.cxx selection/SelectionDict.h selection/SelectionDict_rdict.pcm $(LIB)
