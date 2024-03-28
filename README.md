# **Introduction**
Each year, more than 400,000 service members make a permanent change of station (PCS), causing them to pick up their place of residence and move across the state, country, or world to begin their next job. The COVID-19 pandemic has affected the real estate market in many ways, but significantly it caused a surge in housing prices across the United States. Now more than ever, soldiers need data analysis to improve their decision making to buy, rent, or live on post. 

# **Research Question**
During a PCS, is buying a home a better investment than other means (living on post, renting off-post)? 

# **Objectives**
## 1. Home Values Analysis: 
### a. How do Home Values trend from 2000 – 2024? 
### b. Do Home Values fluctuate with the Calendar season? 

## 2. Return on Investment (ROI) Analysis: 
### a. Does location of Military post in the nation affect ROI? 
### b. How did COVID-19 affect ROI?

## 3. Provide practical estimates for ROI at Fort Stewart, GA using historical data

# About the Dataset
This dataset was pulled off of Zillow. Many people have likely encountered Zillow at some point, either actively looking for a home to buy/rent, or just dreaming for that future house they would like to live in one day.

On its database, Zillow currently possesses 135 million properties and 48.11% of real estate website traffic is through Zillow. This is substantial considering how many different real estate websites exist. 

One of the things Zillow does really well and is known for is its data collection. They have several datasets available to the public, to include Home Values Forecasts for the next month, quarter-ahead, and year-ahead, Rental housing stock information, aggregated for sale listings, breakdown of Information By Home Type and several more. 

The dataset I chose to analyze for this project was the Zillow Home Value Index (ZHVI). This is a measure of the typical home value and market changes across a given region and housing type and housing type. It reflects the typical value for homes in the 35th to 65th percentile Range. While they offer data at different levels even all the way down to summarized by neighborhood, I chose to analyze by Zip code for the scope of this project. 

Lastly, just a note of the Zestimate, this is something internal that Zillow produces based on an algorithm that analyzes several factors, to include data from public property records, tax reords, recent home sales, and user-submitted information. 

# Initial Data Analysis
First, I read in my data: 
Past_df = pd.read_csv('Data/Housing_Zillow_Past.csv')

Then, I conducted some initial analysis of this data: 

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

# Initial Cleaning 
Then I started cleaning the data. I did not want 'RegionID' because I thought I would mix this up with 'RegionName', which is the actual Zip Code. 

del Past_df['RegionID']

I then had to melt the data to allow it to become more useable. 

def melt_data(df):
    melted = pd.melt(df, id_vars=['SizeRank', 'RegionName', 'RegionType', 'StateName', 'State', 'City', 'Metro', 'CountyName'], var_name='Date', value_name='MeanValue')
    melted['Date'] = pd.to_datetime(melted['Date'], format='%Y-%m-%d')
    melted = melted.dropna(subset=['MeanValue'])
    return melted

dfm = melt_data(Past_df)

# Exploratory Data Analysis
Moving into the exploratory data analysis, I wanted to look at how the home values were trending by state across time. To do this, I had to delete the columns I didn't want for this dataframe and then group by state. 

New_Past_df = dfm.copy()
del New_Past_df['SizeRank']
del New_Past_df['RegionName']
del New_Past_df['RegionType']
del New_Past_df['StateName']
del New_Past_df['City']
del New_Past_df['Metro']
del New_Past_df['CountyName']
State_Group_df = New_Past_df.groupby(['State', 'Date']).mean()

# Home Values By State From 2000 - 2024

*HOME VALUES BY STATE FROM 2000 - 2024*

After plotting, the key takeaway was the all home values increased across states during this time period. Some key notes is that there is a steep increase in 2021, directly tied in around the time of COVID-19. Lastly of note, the two highest were Hawaii and California around $875,000 and and the lowest was West Virginia around $141,000 (Someone PCS'ing from California to West Virginia could probably afford a really nice home if they timed it correctly). 

# Home Values By State from 2018 - 2024 

*HOME VALUES BY STATE FROM 2018 - 2024* 

Here I analyzed the home values from 2018 - 2024 because I wanted to take a closer look at the impact of COVID -19. 

This better displays that the prices began to increase in 2021 and kind of peaked around Mid-2022. After this, there appears to be an initial dip but values have been steady since then. 

This is slightly concerning for prediction and will likely create a broad range of expected values using this historical data. I did not do a time series analysis for this project, but if I did, I would want to look at the seasonal decomposition, stationary analysis and choosing the best time series model for that if it passes the other metrics. 

*HOME VALUES BY STATE ANIMATED* 

Here we have an animated heatmap that displays how home values have increased over time by state. As you can see, the mean values on the right go up over time, and different states actually take on different home values in comparison to other states over time. The darker the state, the higher the mean is for that state. 

# Home Values According to the Time of Year 
*SEASONAL FLUCTUATIONS IN HOME VALUES BAR CHART AND LINE CHART* 

Here I analyzed the fluctuations in home values according to the time of year. I was curious if the month or weather played any factors on the home values. If you look at the bar graph on the left, that shows they are all about the same across the board. However, the line graph to the right of that is a data pull of 3 years, specifically 2015 - 2018, looking at Raleigh, NC. The data appears to be mostly linear, but we do see tiny fluctuations around the same time of year and see on average the the fall months appear to have a slightly sharper increase. 

While further research on other cities is needed to come to a deterministic solution, this initial conclusion that season doesn't play a huge factor is actually helpful to the Military, specifically since soldiers don't have a ton of autonomy to choose when they buy/sell to their PCS orders largely being dictated by higher headquarters. 

# ROI Formuala for this Project 
*ROI CALCULATION BASIC* 

So now moving into Return On Investment or ROI. 

For the sake of this model, I provided a very basic calculation for ROI. I just said it was the percent growth of the selling price vs. the cost to buy the house. 

## Assumptions
There are a few important assumptions I made here. 

1. First, that there is no BAH (Basic Housing Allowance) profit/loss.

This goes for those buying a home and for those renting a home. My assumption was that their mortgage and utilities, or rent and utilities absolutely maxed out their BAH for that month.The reason this is important is that it doesn't allow for one to calculate the extra income lost or gained with BAH. It also allows an accurate comparison to those living on post, who we assume a 0% ROI automatically because although their housing is paid for, they do not gain anything when moving. 

2. The housing was based on a fixed-rate mortgage

This was important for the practical application at the end of this presentation

3. That soldiers sold their house after 3-years because this was the average time a soldier spends on station. This allowed me to focus in on 3-year time periods for the analysis. 

# ROI 2021 - 2024 

*ROI 2021 - 2024 (Average Soldier PCS) BAR CHART* 

This is a graph showing the ROI by state from 2021 - 2024. On the y-axis you see the Growth % or ROI and on hte x-axis the bars are the states. The key take away from the cart is that the state a military base is located in does appear to play a factor in ROI. 

Of note, In all states but one (Louisiana) during this time period, there was a positive ROI. 
A key note for this graph is that it is from JAN ‘21 – JAN ’24 Data, which Doesn’t allow for seasonal adjustments, but it does Encapsulate the bulk of COVID-19 spike. 

The highest growth was Florida at 47.09%, so if you are stationed at Eglin Air Force base during this time you are probably doing really well when you sell your house. However, the highest value growth was Hawaii at $193,000. The reason there is a difference between the ROI and the Value growth has to do with teh mean values of homes in both areas, with Hawaii being significatnly higher as discussed earlier. 

# ROI July 2022 - Present 

*ROI: July 2022 - Present (COVID -19) BAR CHART* 

This is a similar chart to the previous one, lookng at ROI over time, but this time only from July of 2022 (that peak of the COVID-19 housing spike) to the prsent. 

The key takeaway from this especially in comparison to the previous graph is that although there is still a little over a year of data to collect to accurately compare to the 3 year timeframe discussed in the last slide, we can reasonably assume that home value growth is trending slower after the COVID-19 housing spike in July and in times decreasing. 

Some key differences are that there are 18 States in the negative now versus one and the highest ROI rather than being near 50% is now actually only 10.7% with conneticut. The lowest growth hear was Mississippi with a -6.5% ROI and the lowest value growth on average being Nevada at -$27,000. 

# PCS Quick Reference Map Chart 

*PCS Quick Reference Map chart* 

This is a heatmap that illustrates the bars in the last slide. This could be a key tool for soliders to use as a quick reference to see if the state they are PCS'ing to has a high or low ROI. 

Once again, the darker colors represnt higher ROI (We said Conneticut was the highest and yellow and lighter colors represent lower ROI (We said Louisiana and Nevada being the lowest value growth and ROI). 

# Practical Application to Fort Stewart Soldiers 

## Distribution of Property Values 

*Distribution of Property Values in GA Chart* 

Now we are starting to get into the practical analysis for soldiers by rank. Specifically, here I focused my search anad analysi for soldiers at Fort Stewart but the same can be assumed for Soldiers at Fort Eisenhower as they are also in Georgia. 

This model displays the value distribution of properties in Georgia. As a reimder, this is the mean of each Zipcode and not individual properties. There were some property zip codes extremely high to the right, but for the sake of the histogram I cut out any outliers with counts of 1. 

The key take away from this model is that it appears to be fairly normal (slight skey to eh right) and all the homes of soliders at Fort Stewart (that they can afford with BAH) fall within one standard distribution of hte mean, so we can reasonably extrapolate this data to provide some meaningful conclsuiosn to soldiers at Fort Stewart. 

## BAH 

*BAH Chart* 

Here is the BAH chart for Fort Stewart by rank. 

For my analysis, I will be determining what rank of soldiers can afford different values of homes and primarily used this as my means for conducting that analysis. 

## FSGA July 2022 - Present ROI 

*FSGA JULY 2022 - Present ROI CHART* 

So, extrapolating the GA average of 3.84% of ROI from July 2022 that peak of COVID, and the present, here are the values that each rank could have gained if they bought a home during this time period. 

Key things to note was the average mortgage for that home value bin was calculated with the current interest rate being around 6.2% and I averaged utilities for $500 a month across the board. 

Here the min being $960 for a $25,000 home and the max around $14,400 for a $375,000 home. 

*FSGA JAN 2021 - PRESENT ROI CHART* 

However, we can see here the results are much different had a soldier bought a home in January of 2021 and held onto it. Now, the value gained ranges from $7,610 to $114,150 depending on the cost of the home. 

*Fort Stewart, GA ROI Estimate* 

Using the data from this analysis, I created a range of values a soldier could reasonably assume their future ROI would be between in GA. 

You'll notice in places that there is a fairly wide gap in the range, specifically as the home values get higher, but the key takeaway for a soldier should be in both cases it is positive and they can reasonably expect that future ROI will fall in that range.

RECOMMENDATIONS AND CONCLUSIONS 
So, is buying a home a better investment than living on post or renting off-post....
The answer is Probably, but it depends!

We established that on average there is a positive ROI across the nation, but just as with any investment, there is always a possibility of going in the negative. 

From our analysis, some factors to consider as you mvoe next are: 

- Post Location = Specifially use the heat map and bar chart to determine if you're post is located in a state with historically high or low ROI 

- Another one is that we can't typically predict Major World Events = We looked at increase due to Covid, but an example of house prices moving in the opposite direction would be the subprime mortgage crisis from 2007 – 2008. 

-Actual time before selling the house= You also want to consider if you do plan to sell your house after 3 years or if you're holding onto it to rent out and sell down the road. 

-Cost of maintenance = A lot of homes require unforseen maintenance. Hopefully you have good insurance for anything major that may happen, but since the ROI calculation did not account for a "Risk Factor" soldiers should consider if the estimated ROI is greater than their expected cost of maintenance. This may also include any improvements they want to add to the property. 

-Also want to consider other hidden costs. If you live off post, do you have to pay extra for gas due to your further drive, do you have an expensive HOA etc. 

-Lastly just happiness factors = My wife always says we are building a home and not a house. At the end of the day, you have to do what is right for your self and your family. If that means you are willing to lose some money for the sake of your sanity and well-being, I think that's the best investment you can make. 

Future Study and Application 
Some things I did not go into with my analysis is if there was a difference in ROI around a military installation vs the rest of the nation, if there was a difference in percent growth/ROI with different home values and maybe the difference between ROI on home stypes. 

In future study and more accurate prediction, time series analysis would prove to be more useful than extrapolating the historical data as I did in this study. 


