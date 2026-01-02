import numpy as np
import pandas as pd
from scipy.stats import t



def deming_regression(x, y, lambda_ratio=1):
    x_mean = np.mean(x)
    y_mean = np.mean(y)
    Sxx = np.mean((x - x_mean)**2)
    Syy = np.mean((y - y_mean)**2)
    Sxy = np.mean((x - x_mean)*(y - y_mean))
    # b0:截距 b1:斜率
    b1 = (Syy - lambda_ratio*Sxx + 
        np.sqrt((Syy - lambda_ratio*Sxx)**2 + 4*lambda_ratio*Sxy**2)
        ) / (2*Sxy)

    b0 = y_mean - b1 * x_mean
    return b0.round(4), b1.round(4)

# df = pd.read_excel("sum_data.xlsx")
df = pd.read_excel("update_data.xlsx", sheet_name=0)
df['編號'] = df['編號'].astype('str')
df['顆數'] = df['顆數'].astype('int')

drugs = df['編號'].unique()
parameters = []
for i in drugs:
    sample = df.query('編號 == @i')
    # 經典 Deming：lambda=1
    b0_dem_1, b1_dem_1 = deming_regression(sample['顆數'], sample['秤重'], lambda_ratio=1.0)
    parameters.append([i, float(b0_dem_1), float(b1_dem_1)])

deming = pd.DataFrame(parameters, columns=['編號', 'b0', 'b1'])
deming.to_excel("deming.xlsx", index=0)
print("== finished ==")