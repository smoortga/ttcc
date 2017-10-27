# ttcc
Analysis framework for ttcc Analysis in CMS


```
git clone https://github.com/smoortga/ttcc.git
cd ttcc/setup
root -l setup.C
cd ..
```

## Workflow
### Step 1: Selection
This framework starts from ntuples produced from MINIAOD using the following code: [```https://github.com/smoortga/FlatTree```](https://github.com/smoortga) (original code taken from Kiril Skovpen: [```https://github.com/kskovpen/FlatTree```](https://github.com/kskovpen/FlatTree)). This produces a flat tree structure that is very quick to process.

Therefore the first selection is made on this flat tree structure using the code in the selection directory. After the full selection has been made, the selected events are stored in Object Oriented structures which are defined in the objects directory. This is achieved by a conversion class called "Converter", converting the flat tree structure in a tree containing physical classes (Electrons, Muons and Jets).
