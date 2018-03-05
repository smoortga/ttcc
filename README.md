# ttcc
Analysis framework for ttcc Analysis in CMS


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

Or one can use the [batch submission script](https://github.com/smoortga/ttcc/blob/master/selection/submit_batch.py) in the selection directory. In this python file you can define the input and output paths, the number of events and a TAG which defines the output directory
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
