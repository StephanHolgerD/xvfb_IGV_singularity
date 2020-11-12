import pandas as pd
from igvXfvb import  PlotVarSingularity,PlotVarIGVlocal

df=pd.read_csv('vars.tsv',sep='\t')

for id,chr,pos,mapping,key in zip(df['id'],df['chr'],df['pos'],df['mapping'],df['key']):
    PlotVarSingularity(id,str(chr),pos,pos,mapping,key)#call can be changed to PlotVarIGVlocal to use local igv installation
