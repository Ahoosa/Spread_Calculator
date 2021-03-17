import pandas as pd
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

 

def get_data():
    # formatting the input data and separating corporate and government data
    df = pd.read_csv('sample_input.csv', index_col='bond')
    df['term'] = df['term'].str.replace(r'years', '').astype(float)
    df['yield'] = df['yield'].str.replace(r'%', '').astype(float)
    CorpData = df[df['type'] == 'corporate']
    GovData = df[df['type'] == 'government'] 
    return CorpData,GovData


# Part 1:


def get_minPairs(CorpData,GovData):
    IndxPairs = []
    # finding the closest benchmarks to the corporate bonds and keeping the resulting indices 
    for i in range (0,len(CorpData['term'])-1):
        minDiff = sys.maxsize
        for j in range (0,len(GovData['term'])-1):
            diff=abs(CorpData['term'][i]-GovData['term'][j])
            if(diff<minDiff):
                minDiff = diff
                minCorp = i
                minGov = j
        IndxPairs.append((minCorp,minGov))

    return IndxPairs


def yield_spread(CorpData,GovData):
    IndxPairs=get_minPairs(CorpData,GovData)
    # renaming index columns to use the values
    CorpData['bond1'] = CorpData.index 
    GovData['bond2'] = GovData.index
    dataFrame = pd.DataFrame (columns = ['bond','benchmark','spread_to_benchmark'])
    # calculating yield spread while adding the calculate data to a new dataframe 
    for indx in IndxPairs:
        yieldSpread="%.2f" % round(CorpData['yield'][indx[0]]-GovData['yield'][indx[1]],2)
        data = {'bond': CorpData['bond1'][indx[0]], 'benchmark': GovData['bond2'][indx[1]], "spread_to_benchmark": yieldSpread+'%'}
        dataFrame=dataFrame.append(data,ignore_index=True)
    return dataFrame
    

# Part 2:


def spread_to_curve_calc(CorpData,GovData): 
    CorpData['bond1'] = CorpData.index
    corpy=CorpData['yield'].tolist()
    corpx=CorpData['term'].tolist()
    y=GovData['yield'].tolist()
    x=GovData['term'].tolist()
    # using linear interpolation to calculate spread_to_curve 
    f = interp1d(x, y,fill_value='extrapolate')
    xnew = np.linspace(min(x), max(x),30) 
    spread_to_curve=corpy-f(corpx) 
    # Adding results to a new dataframe
    dataFrame=add_to_table2(CorpData,spread_to_curve)
    return dataFrame


def add_to_table2(CorpData,spread_to_curve):
    df = pd.DataFrame (columns = ['bond','spread_to_curve'])
    for indx in range(0,len(CorpData)-1):
        data = {'bond':CorpData['bond1'][indx],'spread_to_curve': "%.2f" % spread_to_curve[indx]+'%'}
        df=df.append(data,ignore_index=True)
    return df






