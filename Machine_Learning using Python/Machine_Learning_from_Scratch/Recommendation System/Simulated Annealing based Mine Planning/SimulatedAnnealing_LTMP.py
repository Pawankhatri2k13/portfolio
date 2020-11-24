import pandas as pd
import numpy as np
import copy
from InitialSchedule import InvertConeInitSchedule

class LTMP(InvertConeInitSchedule):
    
    def __init__(self,initialTemp=10000,generations=500,iterations=500,tempReductionRate=0.90,
                 maxBlockSwap=3,reqMillCapacity=250000,penaltyLowerProd=2,penaltyUpperProd=2,
                 sellingPrice=6000,discountRate=0.15,cutoff=0.208,recovery=0.90,miningCost=2,
                 processingCost=9,refiningCost=1200):    
        
        InvertConeInitSchedule.__init__(self,sellingPrice=6000,discountRate=0.15,
             cutoff=0.208,recovery=0.90,miningCost=2,processingCost=9,refiningCost=1200)
        
        self.T0 = initialTemp
        self.M = generations
        self.N = iterations
        self.alpha = tempReductionRate
        self.maxs_b_swap = maxBlockSwap
        self.reqmil = reqMillCapacity 
        self.costofP1l = penaltyLowerProd 
        self.costofP1 = penaltyUpperProd

    @staticmethod
    def _successor(Data):
        coordinates = Data.iloc[:,[0,1,2]].values
        xmin = coordinates[:,0].min()
        xmax = coordinates[:,0].max()
        ymin = coordinates[:,1].min()
        ymax = coordinates[:,1].max()
        zmin = coordinates[:,2].min()
        
        succ_list = []
        for elem in coordinates:
            lst = []
            lst.append((elem[0],elem[1],elem[2]))
            if elem[2]-1>=zmin: 
                lst.append((elem[0],elem[1],elem[2]-1))
                if (elem[0]-1>=xmin):
                    lst.append((elem[0]-1,elem[1],elem[2]-1))
                if (elem[0]+1<=xmax):
                    lst.append((elem[0]+1,elem[1],elem[2]-1))
                if (elem[1]-1>=ymin):
                    lst.append((elem[0],elem[1]-1,elem[2]-1))
                if (elem[1]+1<=ymax):
                    lst.append((elem[0],elem[1]+1,elem[2]-1))
            arr = np.array(lst)
            for i in range(1,len(lst)):
                if not (np.any(np.equal(arr[i],coordinates).all(axis=1))):
                    lst.remove((arr[i,0],arr[i,1],arr[i,2]))
            succ_list.append(lst)
        return succ_list
    
    @staticmethod
    def _Indexes(Data,pre_list,succ_list):
        coordinates = Data.iloc[:,[0,1,2]].values
        coordinates = pd.DataFrame(coordinates)
        
        indexes = []
        for i in range(len(pre_list)):
            if len(pre_list[i]) == 1:
                lst = -1
            if len(pre_list[i]) > 1:
                lst = []
                for ii in range(1, len(pre_list[i])):     
                    v=np.prod(coordinates==pre_list[i][ii],axis=1)      
                    va = coordinates[v==1].index[0]
                    lst.append(va) 
            indexes.append(lst)
        Data["precedence index"] = indexes
        
        indexes = []
        for i in range(len(succ_list)):
            if len(succ_list[i]) == 1:
                lst = -1          
            else: 
                lst = []
                for ii in range(1, len(succ_list[i])):
                    v=np.prod(coordinates==succ_list[i][ii],axis=1) 
                    va = coordinates[v==1].index[0]
                    lst.append(va)
            indexes.append(lst)
        Data["successor index"] = indexes
        return Data
    
        
    
    @staticmethod
    def _swapprecedence(Data,minimum_period):
        arr = Data[['schedule','precedence index']].values
        arr_sched = Data["schedule"].values
       
        swaparray = []
        for index,value in enumerate(arr):
            sched,prec = value        
            timeperiodB = sched
            if prec == -1 and timeperiodB != minimum_period:
                swaparray.append([index,timeperiodB])
            if prec != -1:
                if timeperiodB>np.max(arr_sched[prec]):
                    swaparray.append([index,timeperiodB])
        swaparray = np.array(swaparray)      
        return swaparray
    
    @staticmethod
    def _swapsuccessor(Data,maximum_period):
        arr = Data[['schedule','successor index']].values
        arr_sched = Data["schedule"].values
        
        swaparray = []
        for index,value in enumerate(arr):
            sched,succ = value        
            timeperiodB = sched
            if succ == -1 and timeperiodB != maximum_period:
                swaparray.append([index,timeperiodB])
            if succ != -1:
                if timeperiodB<np.min(arr_sched[succ]):
                    swaparray.append([index,timeperiodB])
        swaparray = np.array(swaparray)       
        return swaparray 
    
    def _setterFunc(self,Data):
        pre_list = self._precedence(Data)
        succ_list = self._successor(Data)
        return pre_list, succ_list
    
    def _objectiveValue(self,Data):
        cutoff = self.cutoff
        reqmil = self.reqmil
        costofP1 = self.costofP1
        costofP1l = self.costofP1l
        Mine_value = np.sum(Data['discounted value']) #NPV
        processingTonnagePerYear = []
        schedMax = Data["schedule"].max()
        for i in range(schedMax+1):
            processingTonnagePerYear.append(Data[(Data["Grade"]>=cutoff) & (Data["schedule"]==i)]["Tonnage"].sum())     
        ProcessingPenaltyPerYear = []  
        val = processingTonnagePerYear[i] - reqmil 
        if processingTonnagePerYear[i] > reqmil:
            costVal = costofP1 * val
            ProcessingPenaltyPerYear.append(costVal)
        elif processingTonnagePerYear[i] < reqmil:
            costVal = abs(costofP1l * val)
            ProcessingPenaltyPerYear.append(costVal)   
        penaltycost = sum(ProcessingPenaltyPerYear)
        objValue = Mine_value - penaltycost
        return objValue
    
    
    def _mutation(self,Data,swaparray_p,swaparray_s,minimum_period,maximum_period):
        tempData = copy.deepcopy(Data)
        maxs_b_swap = self.maxs_b_swap
        rand_num = np.random.randint(2, size=1)
        sched = Data['schedule'].values
        if rand_num == 0:
            randNblocks = np.random.randint(1,maxs_b_swap)
            blocksIndex = np.random.randint(len(swaparray_p),size=randNblocks)         
            blocks = swaparray_p[blocksIndex][:,0]  
            timeperiod = np.array(sched[blocks])
            timeperiod[timeperiod!=minimum_period] -= 1
            tempData.schedule.iloc[blocks] = timeperiod 
        elif rand_num == 1:
            randNblocks = np.random.randint(1,maxs_b_swap)
            blocksIndex = np.random.randint(len(swaparray_s),size=randNblocks)
            blocks = swaparray_s[blocksIndex][:,0]
            timeperiod = np.array(sched[blocks])
            timeperiod[timeperiod!=maximum_period] += 1
            tempData.schedule.iloc[blocks] = timeperiod
        return tempData
    
    def fit(self,Data,initSched=True,level=2,prodCapacity=245000):
        if initSched:
            Data = self.initialSchedule(Data,level,prodCapacity)
        minimum_period = Data['schedule'].min()
        maximum_period = Data['schedule'].max()
        M = self.M 
        N = self.N
        T0 = self.T0
        alpha = self.alpha
        objValue = self._objectiveValue(Data)
        self.pre_list,self.succ_list = self._setterFunc(Data)
        pre_list = self.pre_list
        succ_list = self.succ_list
        self.Data = self._Indexes(Data,pre_list,succ_list) 
        swaparray_p = self._swapprecedence(Data, minimum_period)
        swaparray_s = self._swapsuccessor(Data, maximum_period)
        for i in range(M):
            acceptanceCount = 0.000001
            rejectionCount = 0.000001
            for j in range(N): 
                mutatedData = self._mutation(Data,swaparray_p,swaparray_s,
                                             minimum_period,maximum_period )   
                objNewValue = self._objectiveValue(mutatedData)
                prob = (np.exp((objNewValue - objValue)/T0))
                random_num = np.random.rand()
                if objNewValue >= objValue:
                    Data = mutatedData
                    objValue = objNewValue
                    swaparray_p = self._swapprecedence(Data, minimum_period)
                    swaparray_s = self._swapsuccessor(Data, maximum_period)
                     
                elif objNewValue < objValue and random_num < prob:
                    Data = mutatedData
                    objValue = objNewValue    
                    swaparray_p = self._swapprecedence(Data, minimum_period)
                    swaparray_s = self._swapsuccessor(Data, maximum_period)
                    acceptanceCount += 1 
                else:
                    rejectionCount += 1           
                #ratio = ((rejectionCount/acceptanceCount)*100)
                print(f'Objective value of current solution: {objValue}')
            T0 = alpha * T0
            
        return Data
            

    
        