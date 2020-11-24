from math import ceil,sqrt
import pandas as pd
import numpy as np

class REGIONS:
    
    def __init__(self):
        pass

    def dataSplit(self,data_train,data_test,num_regions):
        x_end = data_test['x'].max()
        y_end = data_test['y'].max()
        x_interval = ceil(x_end/sqrt(num_regions))
        y_interval = ceil(y_end/sqrt(num_regions))
        regions= int(sqrt(num_regions))
        x = np.linspace(0,x_end, regions, endpoint=False)
        y = np.linspace(0, y_end, regions,endpoint=False)
        
        dataSplitLst = []
        for i in range(2):
            if i==0:
                data = data_train
            else:
                data = data_test
            lst = []
            for yval in y:
                for xval in x:
                    xval = ceil(xval)
                    yval = ceil(yval)
                    arr = data.where(data['x'].between(xval+1, (xval+x_interval),inclusive=True) & 
                                    (data['y'].between(yval+1,(yval+y_interval),inclusive=True)),axis=1)
                    arr.dropna(inplace=True)
                    df = pd.DataFrame(arr)
                    lst.append(df)  
            for i in range(len(lst)):
                lst[i].insert(3,'region',i)
            df = pd.concat(lst)
            split_data = df.sort_index(axis = 0)
            dataSplitLst.append(split_data)
        split_data_train = dataSplitLst[0]
        split_data_test = dataSplitLst[1]
        return split_data_train, split_data_test
    
    def regions_Data(self,data_train,data_test,num_regions):
        split_dataTrain, split_dataTest = self.dataSplit(data_train,data_test,num_regions)
        split_dataTrain['index'] = split_dataTrain.index
        regionsData = []
        for regionNumber in range(num_regions):
            regionTrain = split_dataTrain[split_dataTrain['region']==regionNumber][['x','y']].values
            regionTrainOut = split_dataTrain[split_dataTrain['region']==regionNumber]['v'].values
            regionTest = split_dataTest[split_dataTest['region']==regionNumber][['x','y']].values
            regionTestOut = split_dataTest[split_dataTest['region']==regionNumber]['v'].values
            regionTrainIndex = split_dataTrain[split_dataTrain['region']==regionNumber]['index'].values
            regionsData.append((regionTrain,regionTrainOut,regionTest,regionTestOut,regionTrainIndex))
        return regionsData

    def getRegion(self,data_train,data_test,num_regions,regionNumber):
        regionsData = self.regions_Data(data_train,data_test,num_regions)
        regionTrain = regionsData[regionNumber][0]
        regionTrainOut = regionsData[regionNumber][1]
        regionTest = regionsData[regionNumber][2]
        regionTestOut = regionsData[regionNumber][3]
        regionTrainIndex = regionsData[regionNumber][4]
        return regionTrain,regionTrainOut,regionTest,regionTestOut,regionTrainIndex
    
    
    
    