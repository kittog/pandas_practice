import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import codecademylib3_seaborn
import glob

#create DF w all files
state_files = glob.glob("states*.csv")
df_list = []

for filename in state_files:
  data = pd.read_csv(filename)
  df_list.append(data)

us_census = pd.concat(df_list)
us_census.reset_index(inplace=True, drop=True)
us_census = us_census[['State', 'TotalPop', 'Hispanic', 'White', 'Black', 'Native', 'Asian', 'Pacific', 'Income', 'GenderPop']]
print(us_census.head())
print(us_census.columns)
print(us_census.dtypes)

us_census.Income = us_census['Income'].replace(['\$'], '', regex=True)
us_census.Income = pd.to_numeric(us_census.Income) #convert to floats

gender_split = us_census.GenderPop.str.split('_', expand=True)
us_census['Women'] = pd.to_numeric(gender_split[1].replace(['F'], '', regex=True))
us_census['Men'] = pd.to_numeric(gender_split[0].replace(['M'], '', regex=True))
print(us_census.head())

plt.scatter(us_census['Women'], us_census['Income'])
plt.show()

us_census['Women'] = us_census.Women.fillna(us_census.TotalPop - us_census.Men)
print(us_census)

#dropping duplicates
print(us_census.duplicated())
census = us_census.drop_duplicates()

#final plot
plt.scatter(census['Women'], census['Income'])
plt.show()

#columns + conv to floats, getting rid of '%'
print(census.columns)
col = ['Hispanic', 'White', 'Black', 'Native', 'Asian', 'Pacific']
for pop in col:
  census[pop] = pd.to_numeric(census[pop].replace(['\%'], '', regex=True)).div(100).round(3)
print(census.head())

#rearrange DF columns
census = census[['State', 'Hispanic', 'White', 'Black', 'Native', 'Asian', 'Pacific', 'Men', 'Women', 'TotalPop', 'Income']]
print(census.head())
