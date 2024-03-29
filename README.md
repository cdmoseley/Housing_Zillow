# **Introduction**
Every year, over 400,000 service members undergo a permanent change of station (PCS), necessitating a relocation of their residence across states, countries, or even continents for their next assignment. The dynamic landscape of the real estate market, compounded by the unprecedented impact of the COVID-19 pandemic, has led to a notable surge in housing prices nationwide. In this context, there exists an urgent need for data analysis to empower soldiers in making informed decisions regarding property investment, rental choices, or opting for on-post housing accommodations.

# **Research Question**
During a PCS, is buying a home a better investment than other means (living on post, renting off-post)? 

# About the Dataset
<img width="500" alt="Screenshot 2024-03-28 at 2 06 38 PM" src="https://github.com/cdmoseley/Housing_Zillow/assets/161170070/26632301-4631-4be7-b91e-e92cf405781c">

This dataset comes straight from Zillow, a site many of us have probably browsed while searching for our next home or just daydreaming about what our dream home might look like. Zillow's got a massive database—135 million properties, to be exact—and it's a big player in the real estate scene, pulling in nearly half of all real estate website traffic.

What sets Zillow apart is its knack for gathering data. They have all sorts of datasets up for grabs, from forecasts on home values for the next month, quarter, or year, to info on rental housing stock and aggregated listings for sale. For this project, I honed in on the Zillow Home Value Index (ZHVI), which gives us a pulse on typical home values and market shifts across different regions and housing types. 

Now, while Zillow provides data down neighborhood level, I kept things broader, focusing on zip codes for my analysis.

Lastly, just to note the Zestimate, this is something internal that Zillow produces based on an algorithm that analyzes several factors. These include data from public property records, tax reords, recent home sales, and user-submitted information. 

# Initial Data Analysis
First, I read in my data: 
`Past_df = pd.read_csv('Data/Housing_Zillow_Past.csv')`

Then, I conducted some initial analysis of this data: 
```
Past_df.shape
Past_df.head()
Past_df.columns
Past_df.info()
null_counts = Past_df.isnull().sum()
max_null_column = null_counts.idxmax()
max_null_count = null_counts[max_null_column]
print(max_null_count)
print(max_null_column)
average_null_counts = null_counts.mean()
print(average_null_counts)
```

# Initial Cleaning 
Then I started cleaning the data. I did not want 'RegionID' because I thought I would mix this up with 'RegionName', which is the actual Zip Code. 

`del Past_df['RegionID']`

I then had to melt the data to allow it to become more useable. 

```
def melt_data(df):
    melted = pd.melt(df, id_vars=['SizeRank', 'RegionName', 'RegionType', 'StateName', 'State', 'City', 'Metro', 'CountyName'], var_name='Date', value_name='MeanValue')
    melted['Date'] = pd.to_datetime(melted['Date'], format='%Y-%m-%d')
    melted = melted.dropna(subset=['MeanValue'])
    return melted

dfm = melt_data(Past_df)
```

# Exploratory Data Analysis
Moving into the exploratory data analysis, I wanted to look at how the home values were trending by state across time. To do this, I had to delete the columns I didn't want for this dataframe and then group by state. 

```
New_Past_df = dfm.copy()
del New_Past_df['SizeRank']
del New_Past_df['RegionName']
del New_Past_df['RegionType']
del New_Past_df['StateName']
del New_Past_df['City']
del New_Past_df['Metro']
del New_Past_df['CountyName']
State_Group_df = New_Past_df.groupby(['State', 'Date']).mean()
```

# Home Values By State From 2000 - 2024
<img width="700" alt="Screenshot 2024-03-28 at 5 50 52 PM" src="https://github.com/cdmoseley/Housing_Zillow/assets/161170070/1efdd568-e50b-4e92-b309-414fc2e0c612">

Upon examining the plotted data, a notable trend emerges: all home values experienced a significant uptick across states within the specified timeframe. A particularly striking surge occurred in 2021, coinciding directly with the onset of the COVID-19 pandemic. Noteworthy observations include the substantial rise in home values during this period.

Of particular interest are the extremes: California, which I made bold in order to better see the fluctuations in the market, boasted the highest average home values, hovering around $875,000, while West Virginia claimed the lowest, averaging around $141,000. This discrepancy suggests that someone undergoing a PCS from California to West Virginia might find themselves in a prime position to secure a considerably upscale residence, given the right timing.

# Home Values By State from 2018 - 2024 

<img width="570" alt="Screenshot 2024-03-28 at 6 06 19 PM" src="https://github.com/cdmoseley/Housing_Zillow/assets/161170070/ecfaba15-684e-4720-839e-095f2eace42d">

In examining home values spanning from 2018 to 2024, I aimed to dissect the nuanced impact of the COVID-19 pandemic. The analysis uncovered a discernible pattern: a steady uptick in prices beginning in 2021, reaching a notable peak around mid-2022. Following this peak, there was a modest decline, followed by a period of relative stability in home values.

This observed trend presents a challenge in terms of predictive modeling, as the fluctuating trajectory complicates the task of forecasting future values with precision. Although a detailed time series analysis was not conducted in this project, the potential avenues for such exploration are intriguing. Were I to delve deeper, I would prioritize methodologies such as seasonal decomposition, assessing stationarity, and selecting the most suitable time series model based on rigorous evaluation metrics.


https://github.com/cdmoseley/Housing_Zillow/assets/161170070/58cad2d3-4e50-45ed-a8fb-2bbbc06450c5

Here we have an animated heatmap that displays how home values have increased over time by state. As you can see, the mean values on the right go up over time, and different states actually take on different home values in comparison to other states over time. The darker the state, the higher the mean is for that state. 

# Home Values According to the Time of Year 
<img width="400" alt="Screenshot 2024-03-28 at 2 11 09 PM" src="https://github.com/cdmoseley/Housing_Zillow/assets/161170070/048988b2-c402-4da1-b70c-a08cf0231d66">

<img width="400" alt="Screenshot 2024-03-28 at 2 11 15 PM" src="https://github.com/cdmoseley/Housing_Zillow/assets/161170070/80de3f46-3b2e-4369-a63c-4a787cd72e80">

In this analysis, I explored fluctuations in home values concerning the time of year, aiming to discern whether factors such as month or weather exerted any notable influence. The bar graph on the left provides a comprehensive overview, indicating relatively consistent values across different time periods.

However, the line graph adjacent to it draws from a three-year dataset spanning from 2015 to 2018 and focuses specifically on Raleigh, NC. Here, we observe a predominantly linear trend, punctuated by minor fluctuations occurring around certain times of the year. Notably, the fall months seem to exhibit a slightly sharper increase on average.

While it's imperative to conduct further research encompassing additional cities to arrive at a conclusive understanding, this initial finding—that seasonal variations may not significantly impact home values—holds practical significance, particularly for military personnel. Given the constrained autonomy soldiers often face in timing their home transactions, dictated largely by PCS orders from higher headquarters, this insight proves invaluable in informing housing decisions amidst shifting seasons.

# ROI Formula for this Project 
<img width="550" alt="Screenshot 2024-03-28 at 2 11 59 PM" src="https://github.com/cdmoseley/Housing_Zillow/assets/161170070/22d05450-fe87-4949-ba67-bbe9a23c2900">

Now, let's talk about Return On Investment (ROI). To keep things simple, I've come up with a basic calculation method for this model. ROI is basically just the percent increase in the selling price compared to what you originally paid for the house. It's a straightforward way to see how your investment is doing.

## Assumptions
There are a few important assumptions I made here. 

1. First, that there is no BAH (Basic Housing Allowance) profit/loss.

This goes for those buying a home and for those renting a home. My assumption was that their mortgage and utilities, or rent and utilities absolutely maxed out their BAH for that month.The reason this is important is that it doesn't allow for one to calculate the extra income lost or gained with BAH. It also allows an accurate comparison to those living on post, who we assume a 0% ROI automatically because although their housing is paid for, they do not gain anything when moving. 

2. The housing was based on a fixed-rate mortgage

This was important for the practical application at the end of this presentation

3. That soldiers sold their house after 3-years because this was the average time a soldier spends on station. This allowed me to focus in on 3-year time periods for the analysis. 

# ROI 2021 - 2024 

<img width="700" alt="Screenshot 2024-03-28 at 2 12 44 PM" src="https://github.com/cdmoseley/Housing_Zillow/assets/161170070/296eac08-f717-4eb0-93c3-15812b218256">

This is a graph showing the ROI by state from 2021 - 2024. On the y-axis you see the Growth % or ROI and on hte x-axis the bars are the states. The key take away from the cart is that the state a military base is located in does appear to play a factor in ROI. 

Of note, In all states but one (Louisiana) during this time period, there was a positive ROI. 
A key note for this graph is that it is from JAN ‘21 – JAN ’24 Data, which Doesn’t allow for seasonal adjustments, but it does Encapsulate the bulk of COVID-19 spike. 

The highest growth was Florida at 47.09%, so if you are stationed at Eglin Air Force base during this time you are probably doing really well when you sell your house. However, the highest value growth was Hawaii at $193,000. The reason there is a difference between the ROI and the Value growth has to do with teh mean values of homes in both areas, with Hawaii being significatnly higher as discussed earlier. 

# ROI July 2022 - Present 

<img width="700" alt="Screenshot 2024-03-28 at 2 13 22 PM" src="https://github.com/cdmoseley/Housing_Zillow/assets/161170070/d74445a1-f2de-4cbb-9c38-4aeb0aaf8482">

This is a similar chart to the previous one, lookng at ROI over time, but this time only from July of 2022 (that peak of the COVID-19 housing spike) to the prsent. 

The key takeaway from this especially in comparison to the previous graph is that although there is still a little over a year of data to collect to accurately compare to the 3 year timeframe discussed in the last slide, we can reasonably assume that home value growth is trending slower after the COVID-19 housing spike in July and in times decreasing. 

Some key differences are that there are 18 States in the negative now versus one and the highest ROI rather than being near 50% is now actually only 10.7% with conneticut. The lowest growth hear was Mississippi with a -6.5% ROI and the lowest value growth on average being Nevada at -$27,000. 

# PCS Quick Reference Map Chart 

<img width="700" alt="Screenshot 2024-03-28 at 2 13 48 PM" src="https://github.com/cdmoseley/Housing_Zillow/assets/161170070/6b106d23-c94b-4e23-8343-ceb06b3a287b">

This is a heatmap that illustrates the bars in the last slide. This could be a key tool for soliders to use as a quick reference to see if the state they are PCS'ing to has a high or low ROI. 

Once again, the darker colors represnt higher ROI (We said Conneticut was the highest and yellow and lighter colors represent lower ROI (We said Louisiana and Nevada being the lowest value growth and ROI). 

# Practical Application to Fort Stewart Soldiers 

## Distribution of Property Values 

<img width="700" alt="Screenshot 2024-03-28 at 2 14 22 PM" src="https://github.com/cdmoseley/Housing_Zillow/assets/161170070/2a7ef35b-f9b6-4a94-ba47-77d8ce7c74e4">

Now we are starting to get into the practical analysis for soldiers by rank. Specifically, here I focused my search anad analysi for soldiers at Fort Stewart but the same can be assumed for Soldiers at Fort Eisenhower as they are also in Georgia. 

This model displays the value distribution of properties in Georgia. As a reimder, this is the mean of each Zipcode and not individual properties. There were some property zip codes extremely high to the right, but for the sake of the histogram I cut out any outliers with counts of 1. 

The key take away from this model is that it appears to be fairly normal (slight skey to eh right) and all the homes of soliders at Fort Stewart (that they can afford with BAH) fall within one standard distribution of hte mean, so we can reasonably extrapolate this data to provide some meaningful conclsuiosn to soldiers at Fort Stewart. 

## BAH 

<img width="700" alt="Screenshot 2024-03-28 at 2 14 50 PM" src="https://github.com/cdmoseley/Housing_Zillow/assets/161170070/359be1ad-f875-4eb5-aecb-4556c41d0d7b">

Here is the BAH chart for Fort Stewart by rank. 

For my analysis, I will be determining what rank of soldiers can afford different values of homes and primarily used this as my means for conducting that analysis. 

## FSGA July 2022 - Present ROI 
<img width="700" alt="Screenshot 2024-03-29 at 11 13 45 AM" src="https://github.com/cdmoseley/Housing_Zillow/assets/161170070/e55baeb8-2050-4a50-9ec9-3113f5ff5e71">

So, extrapolating the GA average of 3.84% of ROI from July 2022 that peak of COVID, and the present, here are the values that each rank could have gained if they bought a home during this time period. 

Key things to note was the average mortgage for that home value bin was calculated with the current interest rate being around 6.2% and I averaged utilities for $500 a month across the board. 

Here the min being $960 for a $25,000 home and the max around $14,400 for a $375,000 home. 

## FSGA JAN 2021 - Present ROI 
<img width="694" alt="Screenshot 2024-03-29 at 11 13 52 AM" src="https://github.com/cdmoseley/Housing_Zillow/assets/161170070/0828e031-3899-4134-96c4-423d60fa9422">

However, we can see here the results are much different had a soldier bought a home in January of 2021 and held onto it. Now, the value gained ranges from $7,610 to $114,150 depending on the cost of the home. 

## Combined Charts for Estimate 

<img width="700" alt="Screenshot 2024-03-29 at 11 14 00 AM" src="https://github.com/cdmoseley/Housing_Zillow/assets/161170070/15077302-23a4-46cf-ae18-ec1cd135a28a">

Using the data from this analysis, I created a range of values a soldier could reasonably assume their future ROI would be between in GA. 

You'll notice in places that there is a fairly wide gap in the range, specifically as the home values get higher, but the key takeaway for a soldier should be in both cases it is positive and they can reasonably expect that future ROI will fall in that range.

# Recommendations and Conclusions 
So, is buying a home a better investment than living on post or renting off-post....
**The answer is Probably, but it depends!**

We established that on average there is a positive ROI across the nation, but just as with any investment, there is always a possibility of going in the negative. 

From our analysis, some factors to consider in your next PCS are: 

1. **Post Location**: Specifially use the heat map and bar chart to determine if you're post is located in a state with historically high or low ROI 

2. **Can't Predict Major World Events**: We looked at increase due to Covid, but an example of house prices moving in the opposite direction would be the subprime mortgage crisis from 2007 – 2008. 

3. **Actual timeframe before selling the house**: We assumed 3 years in this model, but you also want to consider if you do plan to sell your house after 3 years or if you're holding onto it to rent out or if you are selling prior to 3 years. 

4. **Cost of maintenance**: Many homes require unforseen maintenance. Hopefully you have good insurance for anything major, but since the basic ROI calculation in this project did not account for a "Risk Factor", soldiers should consider if the estimated ROI is greater than their expected cost of maintenance. This may also include any improvements they want to add to the property. 

5. **Other Hidden Costs**: Some include paying extra for gas due to your further drive, HOA costs., etc. 

6. **Happiness Factors**: My wife always says we are building a home and not a house. At the end of the day, you have to do what is right for yourself and/or your family. If that means you are willing to lose some potential for the sake of your well-being, then I think that's the best investment you can make. 

# Future Study and Application 
Some things I did not go into with my analysis and that other Zillow datasets can certainly explore greater are: 
- Is there a difference in ROI around a military installation vs the rest of the nation?
- Is there a difference in percent growth/ROI with different home values
- Is there a difference between ROI on home types?

Lastly, in future study and more accurate prediction, time series analysis would prove to be most useful tool to more accurately predict future ROI. 


