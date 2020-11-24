import pandas as pd
from scipy.stats import pearsonr

from local_utilities import REGIONS
from Fcmeans_regression_local import REGRESSION 

################

train = pd.read_excel('walkertrain.xlsx')
test = pd.read_excel('walkertest.xlsx')

data_train = train[['x','y','v']]
data_test = test[['x','y','v']]

X_train = data_train[['x','y']].values
y_train = data_train['v'].values
X_test = data_test[['x','y']].values

################

def FIT(data_train,data_test,X_train,y_train,X_test,
        num_regions,sigma,n_clusters=4, max_iter=150, fuzzines=2, error=1e-5, 
        random_state=42, dist="euclidean", method="Cmeans",outputCov=True):
    correlations = []
    num_regions = num_regions
    sigma = sigma
    F_regression = REGRESSION(sigma,n_clusters,max_iter,fuzzines,error,random_state, dist, method,outputCov)
    Fextras = REGIONS()
    for i in range(num_regions):
        regionNumber = i
        x_tr,y_tr,x_te,y_te,x_tr_ind = Fextras.getRegion(data_train,data_test,num_regions,regionNumber)
        finalPred = F_regression.fit_regression(X_train,y_train,X_test,Local=True,
        regionTrain=x_tr,regionTrainOut=y_tr,regionTest=x_te,regionTrainIndex=x_tr_ind)
        correlations.append(pearsonr(finalPred,y_te)[0])
    return correlations

correlations = FIT(data_train,data_test,X_train,y_train,X_test,
        25,5,n_clusters=4, max_iter=150, fuzzines=2, error=1e-5, 
        random_state=42, dist="euclidean", method="Cmeans",outputCov=True)

