# ttcc
Analysis framework for ttcc Analysis in CMS

First time using the repositry:
```
cmsrel CMSSW_8_0_25
cd CMSSW_8_0_25/src
cmsenv
git cms-init
git clone https://github.com/smoortga/ttcc.git
cd ttcc
make
cdir=$(pwd)
export LD_LIBRARY_PATH=${cdir}:${cdir}/selection:$LD_LIBRARY_PATH
```

Next time after each login:
```
cd CMSSW_8_0_25/src
cmsenv
cd ttcc
cdir=$(pwd)
export LD_LIBRARY_PATH=${cdir}:${cdir}/selection:$LD_LIBRARY_PATH
```

## Workflow
### Step 1: Selection
This framework starts from ntuples produced from MINIAOD using the following code: [```https://github.com/smoortga/FlatTree```](https://github.com/smoortga/FlatTree) (original code taken from Kiril Skovpen: [```https://github.com/kskovpen/FlatTree```](https://github.com/kskovpen/FlatTree)). This produces a flat tree structure that is very quick to process.

Therefore the first selection is made on this flat tree structure using the code in the selection directory. After the full selection has been made, the selected events are stored in Object Oriented structures which are defined in the objects directory. This is achieved by a conversion class called "Converter", converting the flat tree structure in a tree containing physical classes (Electrons, Muons and Jets).

The selection requirements are defined in the [selection/config/config.ini](https://github.com/smoortga/ttcc/blob/master/selection/config/config.ini) file and involve number of electrons, muons and jets, their kinematic range and some isolation requirements.

The executable is called Selection (located in the selection directory) and can be called with the arguments

```
./selection/Selection
--infiledirectory <path to directory with FlatTrees>
--outfilepath <path of the output .root file>
--config <path to the the config.ini file located in the selection/config directory>
--nevents <number of events to process or -1 (default) for all events>
```

On the batch systems in Brussels (IIHE) one can use the [batch submission script](https://github.com/smoortga/ttcc/blob/master/selection/submit_batch.py) in the selection directory. In this python file you can define the input and output paths, the number of events and a TAG which defines the output directory. This output directory will contain two sub-directories, one called SelectedSamples, containig the output .root files and another one called localgeid_<TAG>, containing the output logs of the batch jobs:
```
cd selection
python submit_batch.py --nevents=1000 --tag=TEST
```
  
### Intermezzo: Adding a new user-defined Class
The final output of the Converter stores the objects in user-defined classes. The headers and definitions of these classes can be found in the [objects](https://github.com/smoortga/ttcc/blob/master/objects) directory. If one wants to add a new user-defined class, the following steps need to be taken:
#### Step 1: Create .C and .h
Copy the structure of the previously defined classes and fill the member functions and objects of your class according to your preference. Store the .C and .h files in the objects directory
#### Step 2: Create ROOT dictionary
Add the proper dictionary definitions to the [objects/LinkDef.h](https://github.com/smoortga/ttcc/blob/master/objects/LinkDef.h) file
#### Step 3: Add your class to the Makefile
in the [Makefile](https://github.com/smoortga/ttcc/blob/master/Makefile) (located in the home directory), make sure you also add the .C file (under SRC), the .h file (under INC) and define the location of the .o file during complitation (under OBJS). Then re-compile your directory:
```
make clean
make
```
#### Step 4 (Only when using PyROOT): Create python-readable dictionaries for your class 
In order to use your class later on in a PyROOT environment, add your new class to the [setup/setup.C](https://github.com/smoortga/ttcc/blob/master/setup/setup.C) script and run
```
root -l setup.C
```


### Step 2: Analyzing the ntuples
The ntuples defined in step 1 rely only on ROOT and the user-defined classes which can be found in the [objects](https://github.com/smoortga/ttcc/tree/master/objects) directory. For further event selection or other studies, one can in principle choose to use either a C++ based analysis code (using default ROOT) or a python based ([pyROOT](https://root.cern.ch/pyroot)) framework. This repositry contains an example of a pyROOT-based architecture to analyse the ntuples, which can be found in the [analyse](https://github.com/smoortga/ttcc/tree/master/analyse) directory. Below is a description on how to use it:

First one needs to create libraries for the user-defined classes such that they can be imported in the pyROOT framework, which can be done with the [setup/setup.C](https://github.com/smoortga/ttcc/blob/master/setup/setup.C) script:
```
cd setup
root -l setup.C
cd ../analyse
```
This should in principle be done only once (except when some of the user-defined classes were adapted/added/deleted.

Once in the [analyse](https://github.com/smoortga/ttcc/tree/master/analyse) directory, there are two files to take into account:
1. [Helper.py](https://github.com/smoortga/ttcc/blob/master/analyse/Helper.py): This file imports all the user-defined classes and defines some useful functions that can be used later on.
2. [Analyze.py](https://github.com/smoortga/ttcc/blob/master/analyse/Analyze.py): This is the main analyzer that will (in parallel) run any further event selection.

The analyzer will allow you to make further event selection and store the output in a new file. It can be run using:
```
python Analyze.py
--indir=<path to output directory of the Selection step: [../selection/OUTPUT_<TAG>/SelectedSamples/]>
--infiles=<string to specify which files to run over, use * for all (default). example:ST_*>
--tag=<Tag for the output dir, which will be called [SELECTED_<TAG>]>
--nevents=<maximum number of events per sample, use -1 (default) for all events>
--nmaxevtsperjob=<Maximum number of events per parallel job. If more are available, the job will be split>
--ncpu=<number of cpu cores to use (on local machines, this is not ran on batch system!)>
```
This will run the different jobs in parallel on the local cpu cores (not batch!) and create proper output files. Splitted jobs will be automatically merged using 'hadd' in the end.

On top of that the user can define new branches to the output tree which can be important for easy plotting later on. These new branches should be defined by adding them to "dict_variableName_Leaves" and should be filled later on in the code.


### Step 3: Plotting
TBC

