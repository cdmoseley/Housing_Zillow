#pip install geopandas
#pip install plotly-express
import pandas as pd
import geopandas as gpd
from folium.plugins import HeatMap
from shapely.geometry import Point
import folium
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.offline as py
import plotly.io as pio
from datetime import datetime, time, timezone,date
import os
os.environ['SHAPE_RESTORE_SHX'] = 'YES'

#Import Data
Past_df = pd.read_csv('Data/Housing_Zillow_Past.csv')

#Initial Analyze Dataset
Past_df.head()
Past_df.shape
Past_df.columns
Past_df.info()
null_counts = Past_df.isnull().sum()
max_null_column = null_counts.idxmax()
max_null_count = null_counts[max_null_column]
print(max_null_count)
print(max_null_column)
average_null_counts = null_counts.mean()
print(average_null_counts)

#Clean Data
del Past_df['RegionID']

#Melt Dataset to Workable Code 
def melt_data(df):
    melted = pd.melt(df, id_vars=['SizeRank', 'RegionName', 'RegionType', 'StateName', 'State', 'City', 'Metro', 'CountyName'], var_name='Date', value_name='MeanValue')
    melted['Date'] = pd.to_datetime(melted['Date'], format='%Y-%m-%d')
    melted = melted.dropna(subset=['MeanValue'])
    return melted

dfm = melt_data(Past_df)

#2015 - 2018 Raleigh Home Values 
raleigh_df = dfm[(dfm['City'] == 'Raleigh') & (dfm['Date'].dt.year.between(2015, 2018))]

#2015 - 2018 Raleigh Plot 
plt.figure(figsize=(10, 6))
plt.plot(raleigh_df_new['Date'], raleigh_df_new['MeanValue'], marker='o', linestyle='-')
plt.title('Home Values in Raleigh (2015 - 2018)')
plt.xlabel('Date')
plt.ylabel('Home Values')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#Group Home Value By State on each of the months 
New_Past_df = dfm.copy()
New_Past_df.head()
del New_Past_df['SizeRank']
del New_Past_df['RegionName']
del New_Past_df['RegionType']
del New_Past_df['StateName']
del New_Past_df['City']
del New_Past_df['Metro']
del New_Past_df['CountyName']
State_Group_df = New_Past_df.groupby(['State', 'Date']).mean()

#Pull the Year out 
State_Group_df['Year'] = pd.to_datetime(State_Group_df.index.get_level_values('Date')).year

#Finding the min value in 2024
year_2024_data = State_Group_df[State_Group_df['Year'] == 2024]
min_mean_value_index = year_2024_data['MeanValue'].idxmin()
min_mean_value = year_2024_data.loc[min_mean_value_index, 'MeanValue']
min_state = min_mean_value_index[0]  # Extract the state from the multi-index

#Line Plot Each State Over Time 
plt.figure(figsize=(10, 6))  # Adjust figure size if needed

for state, group in State_Group_df.groupby(level='State'):
    dates = group.index.get_level_values('Date')  
    mean_values = group['MeanValue']  
    plt.plot(dates, mean_values, label=state)

plt.xlabel('Date')
plt.ylabel('Home Value')
plt.title('Home Values By State From 2000 - 2024')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), ncol=3)

plt.show()

#Line Plot Over Time Since 2018 
filtered_df = State_Group_df[(State_Group_df['Year'] >= 2018) & (State_Group_df['Year'] <= 2024)]

plt.figure(figsize=(10, 6))  # Adjust figure size if needed

for state, group in filtered_df.groupby('State'):
    dates = group['Date']  
    mean_values = group['MeanValue']  
    plt.plot(dates, mean_values, label=state)

plt.xlabel('Date')
plt.ylabel('Home Value')
plt.title('Home Values By State From 2018- 2024')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), ncol=3)

plt.show()

#Seasonal Bar Graph 
State_Group_df['Month'] = State_Group_df['Date'].dt.month

def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Fall'

State_Group_df['Season'] = State_Group_df['Month'].apply(get_season)

seasonal_trend = State_Group_df.groupby('Season')['MeanValue'].mean()

seasonal_trend.plot(kind='bar', color='skyblue')
plt.title('Home Values According to Season')
plt.xlabel('Season')
plt.ylabel('Home Values')
plt.xticks(rotation=0)
plt.show()

    #*2021 - 2024 ROI Calculations*
# Filter data for January 2021 and January 2024
filtered_data = State_Group_df[State_Group_df['Date'].dt.month == 1]
filtered_data = filtered_data[(filtered_data['Date'].dt.year == 2021) | (filtered_data['Date'].dt.year == 2024)]

    # Pivot the data to have January 2021 and January 2024 values side by side
New_SG = filtered_data.pivot(index='State', columns='Year', values='MeanValue')
New_SG.head()

percent_growth = round(100*((New_SG[2024] - New_SG[2021])/New_SG[2021]),2)

    # Add percent growth to dataframe
New_SG["Growth"] = percent_growth
New_SG.head()

Dollar_Growth = (New_SG[2024] - New_SG[2021])

    # Add percent growth to dataframe
New_SG["Value_Growth"] = Dollar_Growth
New_SG.head()

Sorted_SG = New_SG.sort_values(by='Value_Growth', ascending = False)
Sorted_SG

#Plotting ROI By State 2021 - 2024
# Plotting the bar plot
plt.figure(figsize=(10, 6))
plt.bar(New_SG.index, New_SG['Growth'], color='skyblue')

    # Adding labels and title
plt.title('ROI: 2021 - 2024')
plt.xlabel('State')
plt.ylabel('Growth (%)')

    # Rotate x-axis labels for better readability (optional)
plt.xticks(rotation=90)

    # Display the plot
plt.grid(True)
plt.tight_layout()  
plt.show()

#2022 - 2024 Data Calculations 
    # Filter data for July 2022 and present
filtered_data = State_Group_df[(State_Group_df['Date'] >= '2022-07-01')]

    # Check for and remove duplicate entries in the index
filtered_data = filtered_data[~filtered_data.index.duplicated(keep='first')]

    # Aggregate duplicate values before pivoting (using mean as an example)
filtered_data = filtered_data.groupby(['State', 'Year']).agg({'MeanValue': np.mean}).reset_index()

    # Pivot the data to have July 2022 and present values side by side
Newest_SG = filtered_data.pivot(index='State', columns='Year', values='MeanValue')
Newest_SG.head()

Sorted_Newest = Newest_SG.sort_values(by='Value_Growth', ascending = False)
Sorted_Newest

#Plotting 2022 - 2024
    # Plotting the bar plot
plt.figure(figsize=(10, 6))
plt.bar(Newest_SG.index, Newest_SG['Growth'], color='skyblue')

    # Adding labels and title
plt.title('ROI: July 2022 - Present')
plt.xlabel('State')
plt.ylabel('Growth (%)')

    # Rotate x-axis labels for better readability (optional)
plt.xticks(rotation=90)

    # Display the plot
plt.grid(True)
plt.tight_layout()  
plt.show()

#Creating Bins By $50,000
    # Filter data for July 2022 and present and only for GA zip codes
filtered_data_ga = dfm[(dfm['Date'] >= '2022-07-01') & (dfm['State'] == 'GA')]

    # Extract year information from the 'Date' column
filtered_data_ga['Year'] = filtered_data_ga['Date'].dt.year

    # Create custom bins for mean values in $50,000 increments
max_mean_value = int(filtered_data_ga['MeanValue'].max())
bins = np.arange(0, max_mean_value + 50000, 50000)

    # Group the data by mean value bins and year
filtered_data_ga['MeanValueBin'] = pd.cut(filtered_data_ga['MeanValue'], bins, labels=[f'${i}-{i+50000}' for i in range(0, max_mean_value, 50000)])
grouped_data_ga = filtered_data_ga.groupby(['MeanValueBin', 'Year']).size().reset_index(name='Counts')

#Creating Georgia Home Values Histogram 
    # Filter the DataFrame to include only mean value brackets with counts for both 2022 and 2024
mean_value_brackets_with_counts = grouped_data_ga.groupby('MeanValueBin')['Year'].apply(lambda x: (2022 in x.values) and (2024 in x.values)).reset_index(name='BothYears')
mean_value_brackets_with_counts = mean_value_brackets_with_counts[mean_value_brackets_with_counts['BothYears']]

    # Filter the original DataFrame based on mean value brackets with counts for both 2022 and 2024
filtered_df = grouped_data_ga[grouped_data_ga['MeanValueBin'].isin(mean_value_brackets_with_counts['MeanValueBin'])]

    # Display the filtered DataFrame
filtered_df.head(50)

    # Filter out bins with low counts 
filtered_data_ga = grouped_data_ga[grouped_data_ga['Counts'] > 10]

    # Plotting the histogram
plt.figure(figsize=(10, 6))
bar_width = 0.8  # Width of the bars
index = np.arange(len(filtered_data_ga))  # Index for the bars

plt.bar(index, filtered_data_ga['Counts'], color='skyblue', width=bar_width)
plt.xlabel('Home Values')
plt.ylabel('Count Zip-Codes')
plt.title('Property Value Distribution in Georgia')
plt.xticks(index, filtered_data_ga['MeanValueBin'], rotation=90)  # Setting the x-axis ticks and labels
plt.tight_layout()
plt.show()

#Making HeatMap of ROI 
df = Newest_SG
import plotly.express as px
fig = px.choropleth(df,
                    locations=df.index, 
                    locationmode="USA-states", 
                    scope="usa",
                    color='Growth',
                    color_continuous_scale="Viridis_r", 
                    
                    )
fig.show()

fig.update_layout(
      title_text = 'ROI By State July 2022 - Present',
      title_font_family="Times New Roman",
      title_font_size = 22,
      title_font_color="black", 
      title_x=0.45, 
         )

#Making Animated Heatmap of HomeValues over Time 
df1 = State_Group_df
fig = px.choropleth(df1,
                    locations='State', 
                    locationmode="USA-states", 
                    color='MeanValue',
                    color_continuous_scale="Viridis_r", 
                    scope="usa",
                    animation_frame='Year') #make sure 'period_begin' is string type and sorted in ascending order

fig.show()
    # Adjust the size of the figure
fig.update_layout(geo=dict(scope='usa', projection=dict(type='albers usa'), 
                           showlakes=True, lakecolor='rgb(255, 255, 255)'),
                  width=800, height=600)

    #Export the plot 
gif_path = 'choropleth_map.gif'
pio.write_html(fig, 'temp_plot.html')
py.init_notebook_mode()
py.plot(fig, filename='temp_plot.html', auto_open=True, include_plotlyjs='cdn', image='svg', image_filename='choropleth_map')
py.offline.iplot(fig)