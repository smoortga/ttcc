source /user/smoortga/sklearn_setenv.sh
cd /user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/matching/
python /user/smoortga/Analysis/2017/ttcc_Analysis/CMSSW_8_0_25/src/ttcc/matching/TrainMatchingNN.py --tag=testWithFlippedDeepLocalGrid --skipEvery=50 --nepoch=20