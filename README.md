Introduction 
The Military's population is around _____ with _____ Soldier's PCS'ing every year. The pandemic affected the real estate market in many ways, but one of the most significant impacts it created as the surge in housing prices across the United States. 

Target Audience 
Soldiers PCS'ing in the United States. 

Data Collection and Preprocessing 

What is the Shape of your dataset? 

26353 rows x 299 columns 

Describe the Available Fields 

Categorical = 8 Columns (Region ID, Region Name, Region Type, StateName, State, City, Metro, CountyName)

Quantitative = 290 Columns (Size Rank, 289 Columns of by month average home value form JAN 2000 for that zip code)

Missing Data: There are some missing data per column, specifically in gathering the home values across certain months. The max amount of null values was the first column in January of 2000, with 13,458 values out of 26,353 possible values missing. That's missing just over half of the dataset. However, on average, 6,520 values were missing per zip code for the data set.  That's about 25% of nation that we do not have data for, but I do not see this as a current issue, as analysis can still be completed as most of the values that were missing, were missing across all dates for that specific zip code. 

Summarized? No analysis has been conducted on the home values for all of the zip codes as there are close to 300 months since JAN 2000 that have home values. However, the home values are already an average of that specific zip code, with my current assumption being Zillow created that number from within their system. 

Potential Avenues of Inquiry 

The main question I would want to analyze right now is: "Is buying a home during a PCS a good investment vs. living on post?" 

Coming off of this question, there's several avenues that can be explored. Here are a few of those questions: 

1. Is there a difference between historical ROI around an Army Installation vs. around non-military installations? 

2. Is there a difference between the historical ROI on different home value groups ($100,000 vs. $300,000 home for example)? 
      -This could provide some meaningful data into different pay/BAH rates and how ROI might change per Soldier Rank

3. Any seasonal differences in buying/selling (Winter/Spring/Summer/Fall)?

4. Comparison of interest rates over time 

5. Ending with Zillow Home Values Forecast Data (ZHVF). Explaining would like to do a Time Series, but can use their data set currently for predictions. 

Look at Markdown Cheatsheet 






