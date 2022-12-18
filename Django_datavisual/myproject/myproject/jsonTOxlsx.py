import json 
import pandas as pd
import os


files = os.listdir()
files.sort()


for file in files:
    if 'json' not in file:
        continue
    print('converting' + file)
    with open(file) as f:
        data = json.load(f)

    df = pd.DataFrame(data)
    df = pd.DataFrame(df.values.T,index=df.columns , columns=df.index)
    df.to_excel(file.replace('.josn' , '') + 'xlsx')