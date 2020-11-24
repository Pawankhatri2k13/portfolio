# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 11:54:50 2019

@author: Hp Pc
"""

import numpy as np
from math import ceil
import copy

class InvertConeInitSchedule(object):
    
    def __init__(self,sellingPrice=6000,discountRate=0.15,cutoff=0.208,recovery=0.90,miningCost=2,
                 processingCost=9,refiningCost=1200):
        
        object.__init__(self)
        
        self.price = sellingPrice #selling price of valueable mineral
        self.dis_rate = discountRate #discount rate
        self.cutoff = cutoff #cutoff grade
        self.rec = recovery #recovery of processing plant
        self.m_cost = miningCost #mining cost
        self.p_cost = processingCost #processing cost
        self.ref_cost = refiningCost #refining cost
    
    @staticmethod
    def _precedence(Data):
        
        coordinates = Data.iloc[:,[0,1,2]].values
        xmin = coordinates[:,0].min()
        xmax = coordinates[:,0].max()
        ymin = coordinates[:,1].min()
        ymax = coordinates[:,1].max()
        zmax = coordinates[:,2].max()
        pre_list = []
        for elem in coordinates:
            lst = []
            lst.append((elem[0],elem[1],elem[2]))
            if elem[2]+1<=zmax: 
                lst.append((elem[0],elem[1],elem[2]+1))
                if (elem[0]-1>=xmin):
                    lst.append((elem[0]-1,elem[1],elem[2]+1))
                if (elem[0]+1<=xmax):
                    lst.append((elem[0]+1,elem[1],elem[2]+1))
                if (elem[1]-1>=ymin):
                    lst.append((elem[0],elem[1]-1,elem[2]+1))
                if (elem[1]+1<=ymax):
                    lst.append((elem[0],elem[1]+1,elem[2]+1))
            arr = np.array(lst)
            for i in range(1,len(lst)):
                if not (np.any(np.equal(arr[i],coordinates).all(axis=1))):
                    lst.remove((arr[i,0],arr[i,1],arr[i,2]))
            pre_list.append(lst)
        return pre_list

    def _value(self, Data):
        cutoff = self.cutoff
        rec = self.rec
        ref_cost = self.ref_cost
        price = self.price
        m_cost = self.m_cost
        p_cost = self.p_cost

        grade = Data.iloc[:,3].values
        tonnage = Data.iloc[:,4].values
        
        B_value = []                
        for i in range(len(grade)):
            if grade[i] >= cutoff:
                B_value.append((((price-ref_cost)*rec*(grade[i]/100))*tonnage[i]) - ((m_cost+p_cost)*tonnage[i]))
            elif grade[i] < cutoff:
                B_value.append(-(m_cost*tonnage[i]))      
        Data['Block Value'] = B_value
        return Data
    
    @staticmethod
    def _switchDict(level):
        lst = [i for i in range(level)]    
        case = dict(zip(tuple(lst),tuple(lst)))
        return case
    
    @staticmethod
    def _func(level,x,y,z,Data):
        Bl = []
        x_ax=x
        y_ax=y
        z_ax=z-level
        bol = (Data[['X','Y','Z']]==[x_ax,y_ax,z_ax]).all(1).any()
        if bol == True:
            vall = np.prod(Data[['X','Y','Z']]==[x_ax,y_ax,z_ax],axis=1)
            valuee = Data[vall==1]["Block Value"].values[0]
        else:
            valuee = 0
        Bl.append(valuee)
        
        x_ax=x-level
        y_ax=y
        z_ax=z-level
        bol = (Data[['X','Y','Z']]==[x_ax,y_ax,z_ax]).all(1).any()
        if bol == True:
            vall = np.prod(Data[['X','Y','Z']]==[x_ax,y_ax,z_ax],axis=1)
            valuee = Data[vall==1]["Block Value"].values[0]
        else:
            valuee = 0
        Bl.append(valuee)
        x_ax=x+level
        y_ax=y
        z_ax=z-level
        bol = (Data[['X','Y','Z']]==[x_ax,y_ax,z_ax]).all(1).any()
        if bol == True:
            vall = np.prod(Data[['X','Y','Z']]==[x_ax,y_ax,z_ax],axis=1)
            valuee = Data[vall==1]["Block Value"].values[0]
        else:
            valuee = 0
        Bl.append(valuee)
        x_ax=x
        y_ax=y-level
        z_ax=z-level
        bol = (Data[['X','Y','Z']]==[x_ax,y_ax,z_ax]).all(1).any()
        if bol == True:
            vall = np.prod(Data[['X','Y','Z']]==[x_ax,y_ax,z_ax],axis=1)
            valuee = Data[vall==1]["Block Value"].values[0]
        else:
            valuee = 0
        Bl.append(valuee)
        x_ax=x
        y_ax=y+level
        z_ax=z-level
        bol = (Data[['X','Y','Z']]==[x_ax,y_ax,z_ax]).all(1).any()
        if bol == True:
            vall = np.prod(Data[['X','Y','Z']]==[x_ax,y_ax,z_ax],axis=1)
            valuee = Data[vall==1]["Block Value"].values[0]
        else:
            valuee = 0
        Bl.append(valuee)
        return Bl

    def _coneVal(self,Data,level):
        coordinates = Data.iloc[:,[0,1,2]].values
        cone_val = []
        for i in range (len(coordinates)):
            blockss=[]
            x = coordinates[i,0]
            y = coordinates[i,1]
            z = coordinates[i,2]
            vall = np.prod(Data[['X','Y','Z']]==[x,y,z],axis=1)
            valuee = Data[vall==1]["Block Value"].values[0]
            blockss.append(valuee)
            case = self._switchDict(level)
            for j in range(level):   
                elem = case.get(j,"Invalid level")
                for element in range(elem,0,-1):
                        blockss.append(self._func(element,x,y,z,Data))            
            cone_val.append(blockss)
        return cone_val
    
    @staticmethod
    def _TopValue(pre_list,DataIndex1):    
        lst = [pre_list[i][0] if len(pre_list[i])==1 else (-1,-1,-1) for i in range(len(pre_list))]
        arr = np.array(lst)
        vall = np.prod(DataIndex1[['X','Y','Z']].values==arr,axis=1)
        top = DataIndex1[vall==1]["coneValues"].argmax()
        return top

    @staticmethod
    def _successorCoord(coordinates,elem):
        lst = [(elem[0],elem[1],elem[2]),(elem[0],elem[1],elem[2]-1),(elem[0]-1,elem[1],elem[2]-1), (elem[0]+1,elem[1],elem[2]-1),(elem[0],elem[1]-1,elem[2]-1),(elem[0],elem[1]+1,elem[2]-1)] 
        arr = np.array(lst)
        for i in range(len(lst)):
            if not (np.any(np.equal(arr[i],coordinates).all(axis=1))):
                lst.remove((arr[i,0],arr[i,1],arr[i,2]))        
        return lst
    
    def _initSchedule(self,Data,cutoff,pre_list,coordinates,prodCapacity):
        Data1 = copy.deepcopy(Data)
        DataIndex1 = Data1.reset_index(level=0)
        for iteration in range((ceil(Data[(Data["Grade"]>=cutoff)]["Tonnage"].sum()/prodCapacity))):
            production = 0
            while(production <= prodCapacity):
                top = self._TopValue(pre_list,DataIndex1) 
                val = np.prod(Data[['X','Y','Z']] == DataIndex1.iloc[top][['X','Y','Z']],axis=1)
                Data["schedule"].iloc[(Data[val==1]).index] = iteration
                
                if float(Data["Grade"].iloc[(Data[val==1]).index]) >= cutoff:
                   production += DataIndex1["Tonnage"].iloc[top]
                (x,y,z) = DataIndex1.iloc[top][["X","Y","Z"]]
                coor = (x,y,z)                        
                success = self._successorCoord(coordinates,coor)
                for ix in range(1,len(success)):
                    if len(success)==1:
                        continue
                    else:    
                        for i in range(len(pre_list)):                
                            if (pre_list[i][0]==success[ix]):
                                for ii in range(len(pre_list[i])):
                                    if pre_list[i][ii]==coor:
                                        pre_list[i].pop(ii)                        
                                        break
                                break
                                        
                pre_list.pop(top)    
                DataIndex1.drop(index=top,inplace=True)
                DataIndex1.reset_index(drop=True, inplace=True)
                coordinates = DataIndex1.iloc[:,[1,2,3]].values 
                if pre_list==[]:
                    return Data
    
    #important
    def initialSchedule(self, Data,level,prodCapacity):
        
        print ("Process started! Have patience. It may take longer depending upon number of levels it has to search...")
        cutoff = self.cutoff
        dis_rate = self.dis_rate
        coordinates = Data.iloc[:,[0,1,2]].values
        Data = self._value(Data)
        pre_list = self._precedence(Data)
        coneValues = []   
        cone_val = self._coneVal(Data,level)   
        for i in range(len(cone_val)):
            coneValues.append(np.sum(np.sum(cone_val[i])))
        
        Data["coneValues"] = coneValues
        Data['schedule'] = -1
         
        newData = self._initSchedule(Data,cutoff,pre_list,coordinates,prodCapacity)
        
        newData = newData[['X','Y','Z','Grade','Tonnage','Block Value','schedule']]
        newData["discounted value"] = newData['Block Value']/(1+dis_rate)**newData["schedule"]
        return newData
    