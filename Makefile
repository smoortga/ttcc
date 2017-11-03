CMSINC      = -I$(CMSSW_BASE)/src

CMSSWINC      = -I/cvmfs/cms.cern.ch/slc6_amd64_gcc530/cms/cmssw/CMSSW_8_0_25/src
JECLIB      = -L/cvmfs/cms.cern.ch/slc6_amd64_gcc530/cms/cmssw/CMSSW_8_0_25/lib/slc6_amd64_gcc530/ -lCondFormatsJetMETObjects -lJetMETCorrectionsModules -lRecoEgammaEgammaTools

ROOTCFLAGS    = $(shell root-config --cflags)
ROOTLIBS      = $(shell root-config --libs)
ROOTGLIBS     = $(shell root-config --glibs)

CXX           = g++ -g -Wno-write-strings -Wno-attributes -fPIC
LD            = g++
LDFLAGS       = -g
SOFLAGS       = -shared

CXXFLAGS       = $(ROOTCFLAGS)
INCLUDE_FLAGS  = $(CMSSWINC)
LDLIBS         = $(ROOTLIBS) $(JECLIB)
GLIBS          = $(ROOTGLIBS)

EXE           = selection/Selection

INC 	      = selection/Selection.h selection/Converter.h \
                objects/Electron.h objects/Muon.h objects/Jet.h \
		        objects/Trigger.h objects/MissingEnergy.h \

SRC	          = selection/Selection.C selection/Converter.C \
                objects/Electron.C objects/Muon.C objects/Jet.C \
		        objects/Trigger.C objects/MissingEnergy.C \

OBJS          = selection/Selection.o selection/Converter.o \
                objects/Electron.o objects/Muon.o objects/Jet.o \
		        objects/Trigger.o objects/MissingEnergy.o 

LIB           = selection/libSelection.so

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
