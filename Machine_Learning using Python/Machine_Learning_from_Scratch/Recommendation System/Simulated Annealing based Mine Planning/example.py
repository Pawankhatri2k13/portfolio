 
from InitialSchedule import InvertConeInitSchedule
from LongTermMinePlanning import LTMP
import pandas as pd

Data = pd.read_excel('Newman.xlsx')

initsched = InvertConeInitSchedule()
ltmp = LTMP(generations=10,iterations=5)

Data = initsched.initialSchedule(Data,level=2,prodCapacity=245000)

FinalData = ltmp.fit(Data,initSched=False,level=2,prodCapacity=245000)



from plotly.offline import plot
import plotly.graph_objs as go

'3D Plotting'

space1 = FinalData.loc[:,['X','Y','Z','schedule']]        
newman = go.Scatter3d(
    x=space1['X'],
    y=space1['Y'],
    z=space1['Z'],
    mode='markers',
    marker=dict(
        size=5,
        cmax=4,
        cmin=0,
        color=space1['schedule'], 
        colorbar=dict(title='matter'), 
        colorscale='matter'
    )
)
plotData = [newman]
layout = go.Layout(
    margin=dict(
        l=0,
        r=0,
        b=0,
        t=0
    )
)  
fig = go.Figure(data=plotData, layout=layout)
plot(fig)
