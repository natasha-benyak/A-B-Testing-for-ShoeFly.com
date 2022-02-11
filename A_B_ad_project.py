import codecademylib3
import pandas as pd

ad_clicks = pd.read_csv('ad_clicks.csv')

# examine first few rows of df
print(ad_clicks.head())

# how many views came from each utm_source
views = ad_clicks.groupby('utm_source').user_id.count().reset_index()

# create a column and set to True if value is not null
ad_clicks['is_click'] = ad_clicks.ad_click_timestamp.isnull()

# find percent of people who clicked on the add from each utm_group
clicks_by_source = ad_clicks.groupby(['utm_source', 'is_click']).user_id.count().reset_index()

# pivot the data 
clicks_pivot = clicks_by_source.pivot(
  columns = 'is_click',
  index = 'utm_source',
  values = 'user_id'
).reset_index()

# create enw column that is equal to percent of users who clicked on the ad from each utm_source
clicks_pivot['percent_clicked'] = clicks_pivot[True] / (clicks_pivot[True] + clicks_pivot[False])

print(clicks_pivot.head())

# how many ads were shown to experimental_group
count_AB = ad_clicks.groupby('experimental_group').user_id.count().reset_index()
print(count_AB)

# using is_click, check if greater percentage clicked ad A or B and pivot
A_or_B = ad_clicks.groupby(['experimental_group', 'is_click']).user_id.count().reset_index().pivot(
  columns = 'is_click',
  index = 'experimental_group',
  values = 'user_id'
).reset_index()
print(A_or_B)

# create separate DF for different ads A and B
a_clicks = ad_clicks[ad_clicks.experimental_group == 'A']
b_clicks = ad_clicks[ad_clicks.experimental_group == 'B']

# for each group (a and b) calculate the percent of users who clicked on the ad by day
a_clicks_pivot = a_clicks.groupby(['is_click', 'day']).user_id.count().reset_index().pivot(
  columns = 'day',
  index = 'is_click',
  values = 'user_id'
).reset_index()

b_clicks_pivot = b_clicks.groupby(['is_click', 'day']).user_id.count().reset_index().pivot(
  columns = 'day',
  index = 'is_click',
  values = 'user_id'
).reset_index()

print(a_clicks_pivot)
print(b_clicks_pivot)

# based on the results - reccomending ad B