#! /bin/env python

'''
Plotting Correlation matrix for variables of specified input samples
'''

import rootpy.io as io
import rootpy
from ROOT import TH1D, TObjString
import numpy as np
np.set_printoptions(precision=5)
import root_numpy as rootnp
from sklearn.externals import joblib
log = rootpy.log["/Correlation_Matrix"]
log.setLevel(rootpy.log.INFO)
from argparse import ArgumentParser
import pandas as pd
import matplotlib.pyplot as plt
import os



parser = ArgumentParser()
parser.add_argument('--infile', default=os.getcwd(), help='Input Training File')
parser.add_argument('--outdir', default=os.getcwd()+'/CorrelationMatrix', help='output directory for correlation matrix')
parser.add_argument('--category', default='correct', help='category to be used for drawing correlation matrix')
parser.add_argument('--pickEvery', type=int, default=1, help='pick one event every to draw the correlation matrix')
#parser.add_argument('--batch', action='store_true', help='batch mode')

args = parser.parse_args()

# args_dict = deepcopy(args.__dict__)
# current_file = os.path.abspath(inspect.getfile(inspect.currentframe()))
# 
# watermark = TObjString(prettyjson.dumps(args_dict))
# codeset = open(current_file).read() #zlib.compress(open(current_file).read()) compressing does not work well with root...
# codemark = TObjString(
#    codeset
# )


variables = [
    # "CSVv2_addlead",
#     "CSVv2_addsublead",
#     "CSVv2_antitopb",
#     "CSVv2_topb",
    "DeepCSVBDiscr_addlead",
    "DeepCSVBDiscr_addsublead",
    "DeepCSVBDiscr_antitopb",
    "DeepCSVBDiscr_topb",
    # "DeepCSVCvsB_addlead",
#     "DeepCSVCvsB_addsublead",
#     "DeepCSVCvsB_antitopb",
#     "DeepCSVCvsB_topb",
#     "DeepCSVCvsL_addlead",
#     "DeepCSVCvsL_addsublead",
#     "DeepCSVCvsL_antitopb",
#     "DeepCSVCvsL_topb",
    "DeltaR_adds",
    "DeltaR_antitopb_lepneg",
    "DeltaR_topb_leppos",
    "Eta_addlead",
    "Eta_addsublead",
    "Eta_antitopb",
    "Eta_topb",
   #  "Phi_addlead",
#     "Phi_addsublead",
#     "Phi_antitopb",
#     "Phi_topb",
    "minv_adds",
    "minv_antitopb_lepneg",
    "minv_topb_leppos",
    "pT_addlead",
    "pT_addsublead",
    "pT_antitopb",
    "pT_topb"
    ]


#
# 	CORRELATION MATRIX
#


tree = rootnp.root2array(args.infile,'tree_'+args.category,variables,step=args.pickEvery)
X = rootnp.rec2array(tree)
y = np.ones(len(X))

print "number of events: " + str(len(X))

log.info('Converting data to pandas DataFrame structure')
# Create a pandas DataFrame for our data
# this provides many convenience functions
# for exploring your dataset
# see http://betatim.github.io/posts/sklearn-for-TMVA-users/ for more info
# need to reshape y so it is a 2D array with one column
df = pd.DataFrame(np.hstack((X, y.reshape(y.shape[0], -1))),columns=variables+['y'])

corrmat = df.drop('y', 1).corr(method='pearson', min_periods=1)

fig, ax1 = plt.subplots(ncols=1, figsize=(12,10))
    
opts = {'cmap': plt.get_cmap("RdBu"),'vmin': -1, 'vmax': +1}
heatmap1 = ax1.pcolor(corrmat, **opts)
plt.colorbar(heatmap1, ax=ax1)


ax1.set_title("Correlation Matrix: " + args.category+ " permutations")

labels = corrmat.columns.values
for ax in (ax1,):
	# shift location of ticks to center of the bins
	ax.set_xticks(np.arange(len(labels))+0.5, minor=False)
	ax.set_yticks(np.arange(len(labels))+0.5, minor=False)
	ax.set_xticklabels(labels, minor=False, ha='right', rotation=70)
	ax.set_yticklabels(labels, minor=False)
        
plt.tight_layout()

if not os.path.isdir(args.outdir): os.mkdir(args.outdir)
#log.info("Dumping output in ./Correlation_Matrix_" + args.flavour + "_Inclusive.png" )
plt.savefig(args.outdir+"/Correlation_Matrix_" + args.category +".pdf")
   	
log.info('done')
