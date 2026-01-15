import numpy as np
import pandas as pd
from scipy.stats import t


# 剔除偏差值（Outliers，Modified Z-Score
def get_outliers_modified_z(s, threshold=3.5):
    median = s.median()
    mad = (s - median).abs().median()
    mod_z = 0.6745 * (s - median) / mad
    return mod_z.abs()

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

# 剔除偏差值
df['單重'] = df['秤重'] / df['顆數']
df['mod_z'] = get_outliers_modified_z(df['單重'])
# 判別準則：當 \(M_{i}>3.5\) 時，視為偏差值。依NIST (美國國家標準技術研究所) 的規範
df['Note'] = df['mod_z'] <= 4.5 
df_ = df.query('Note == True')

drugs = df_['編號'].unique()
parameters = []
for i in drugs:
    sample = df_.query('編號 == @i')
    # 經典 Deming：lambda=1
    b0_dem_1, b1_dem_1 = deming_regression(sample['顆數'], sample['秤重'], lambda_ratio=1.0)
    parameters.append([i, float(b0_dem_1), float(b1_dem_1)])

deming = pd.DataFrame(parameters, columns=['編號', 'b0', 'b1'])
deming.to_excel("deming.xlsx", index=0)
print("== finished ==")