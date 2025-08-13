
# Business Data Analysis - Key Insights Jupyter Notebook

This notebook provides a detailed analysis of the ad campaign data, focusing on 10 key insights supported by visualizations.

## Setup and Data Loading

First, let's import the necessary libraries and set up the plotting style.

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3 # Using sqlite3 for demonstration, replace with your DB connector
from io import StringIO

# Set plotting style
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (10, 6) # Default figure size
```

### Database Connection (Placeholder)

In a real scenario, you would connect to your database here. For this notebook, we'll simulate fetching data from CSVs as if they were database tables.

```python
# --- Placeholder for actual database connection ---
# Example for PostgreSQL:
# import psycopg2
# conn = psycopg2.connect(dbname="your_db", user="your_user", password="your_password", host="your_host")

# For demonstration, we'll load from CSVs directly as if they were fetched from DB
# In a real scenario, you would execute SQL queries against 'conn' and read into pandas
ad_events_df = pd.read_csv("ad_events.csv")
ads_df = pd.read_csv("ads.csv")
campaigns_df = pd.read_csv("campaigns.csv")
users_df = pd.read_csv("users.csv")

# Data Cleaning (as performed in analyzer.py)
ad_events_df["timestamp"] = pd.to_datetime(ad_events_df["timestamp"])
campaigns_df["start_date"] = pd.to_datetime(campaigns_df["start_date"])
campaigns_df["end_date"] = pd.to_datetime(campaigns_df["end_date"])

# Merge for insights that require it
merged_df = pd.merge(ad_events_df, ads_df, on="ad_id", how="inner")
merged_df = pd.merge(merged_df, campaigns_df, on="campaign_id", how="inner")
merged_df = pd.merge(merged_df, users_df, on="user_id", how="inner")

merged_df["timestamp"] = pd.to_datetime(merged_df["timestamp"])
merged_df["start_date"] = pd.to_datetime(merged_df["start_date"])
merged_df["end_date"] = pd.to_datetime(merged_df["end_date"])

# Function to simulate SQL query execution (for this notebook)
def execute_sql_query_simulated(query_name):
    if query_name == "ad_platform_distribution":
        return ads_df["ad_platform"].value_counts().reset_index(name="ad_count").rename(columns={"index": "ad_platform"})
    elif query_name == "ad_type_distribution":
        return ads_df["ad_type"].value_counts().reset_index(name="ad_count").rename(columns={"index": "ad_type"})
    elif query_name == "user_gender_distribution":
        return users_df["user_gender"].value_counts().reset_index(name="user_count").rename(columns={"index": "user_gender"})
    elif query_name == "age_group_distribution":
        return users_df["age_group"].value_counts().reset_index(name="user_count").rename(columns={"index": "age_group"})
    elif query_name == "top_5_countries":
        return users_df["country"].value_counts().head(5).reset_index(name="user_count").rename(columns={"index": "country"})
    elif query_name == "impressions_by_platform":
        return merged_df[merged_df["event_type"] == "Impression"]["ad_platform"].value_counts().reset_index(name="impressions_count").rename(columns={"index": "ad_platform"})
    elif query_name == "clicks_by_type":
        return merged_df[merged_df["event_type"] == "Click"]["ad_type"].value_counts().reset_index(name="clicks_count").rename(columns={"index": "ad_type"})
    elif query_name == "ctr_by_platform":
        platform_impressions = merged_df[merged_df["event_type"] == "Impression"].groupby("ad_platform").size().rename("impressions_count")
        platform_clicks = merged_df[merged_df["event_type"] == "Click"].groupby("ad_platform").size().rename("clicks_count")
        ctr_data = pd.concat([platform_impressions, platform_clicks], axis=1).fillna(0)
        ctr_data["ctr"] = (ctr_data["clicks_count"] / ctr_data["impressions_count"]).fillna(0)
        return ctr_data.reset_index()
    elif query_name == "conversion_rate_by_type":
        type_clicks = merged_df[merged_df["event_type"] == "Click"].groupby("ad_type").size().rename("clicks_count")
        type_purchases = merged_df[merged_df["event_type"] == "Purchase"].groupby("ad_type").size().rename("purchases_count")
        conversion_data = pd.concat([type_clicks, type_purchases], axis=1).fillna(0)
        conversion_data["conversion_rate"] = (conversion_data["purchases_count"] / conversion_data["clicks_count"]).fillna(0)
        return conversion_data.reset_index()
    elif query_name == "campaign_performance":
        campaign_clicks = merged_df[merged_df["event_type"] == "Click"].groupby("campaign_id").size().rename("total_clicks")
        return pd.merge(campaigns_df, campaign_clicks, on="campaign_id", how="left").fillna(0)
    else:
        raise ValueError("Unknown query name")

```

## 10 Key Insights and Visualizations

### Insight 1: Distribution of Ad Platforms

```python
# Data for Insight 1
ad_platform_distribution = execute_sql_query_simulated("ad_platform_distribution")

plt.figure(figsize=(8, 6))
sns.barplot(x='ad_platform', y='ad_count', data=ad_platform_distribution)
plt.title('Distribution of Ad Platforms')
plt.xlabel('Ad Platform')
plt.ylabel('Number of Ads')
plt.show()
```
**Commentary:** This chart illustrates the distribution of ad platforms, highlighting the primary channels utilized for advertising campaigns. We can observe the dominance of certain platforms.

### Insight 2: Distribution of Ad Types

```python
# Data for Insight 2
ad_type_distribution = execute_sql_query_simulated("ad_type_distribution")

plt.figure(figsize=(8, 6))
sns.barplot(x='ad_type', y='ad_count', data=ad_type_distribution)
plt.title('Distribution of Ad Types')
plt.xlabel('Ad Type')
plt.ylabel('Number of Ads')
plt.show()
```
**Commentary:** This visual showcases the variety and frequency of different ad types deployed, indicating preferred content formats. Some ad types are clearly more prevalent than others.

### Insight 3: Gender Distribution of Users

```python
# Data for Insight 3
user_gender_distribution = execute_sql_query_simulated("user_gender_distribution")

plt.figure(figsize=(8, 8))
plt.pie(user_gender_distribution['user_count'], labels=user_gender_distribution['user_gender'], autopct='%1.1f%%', startangle=90)
plt.title('User Gender Distribution')
plt.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()
```
**Commentary:** A demographic breakdown of the user base by gender, crucial for understanding audience composition. This helps in tailoring ad content and targeting.

### Insight 4: Age Group Distribution of Users

```python
# Data for Insight 4
age_group_distribution = execute_sql_query_simulated("age_group_distribution")

plt.figure(figsize=(10, 6))
sns.barplot(x='age_group', y='user_count', data=age_group_distribution, order=age_group_distribution['age_group'])
plt.title('User Age Group Distribution')
plt.xlabel('Age Group')
plt.ylabel('Number of Users')
plt.show()
```
**Commentary:** This chart displays the distribution of users across various age groups, informing age-specific targeting strategies. It highlights which age segments are most represented.

### Insight 5: Top 5 Countries by User Count

```python
# Data for Insight 5
top_5_countries = execute_sql_query_simulated("top_5_countries")

plt.figure(figsize=(10, 6))
sns.barplot(x='country', y='user_count', data=top_5_countries)
plt.title('Top 5 Countries by User Count')
plt.xlabel('Country')
plt.ylabel('User Count')
plt.show()
```
**Commentary:** Identifies the top geographical regions with the highest concentration of users, guiding regional marketing efforts and resource allocation.

### Insight 6: Impressions by Ad Platform

```python
# Data for Insight 6
impressions_by_platform = execute_sql_query_simulated("impressions_by_platform")

plt.figure(figsize=(8, 6))
sns.barplot(x='ad_platform', y='impressions_count', data=impressions_by_platform)
plt.title('Total Impressions by Ad Platform')
plt.xlabel('Ad Platform')
plt.ylabel('Total Impressions')
plt.show()
```
**Commentary:** Shows the total ad views generated by each platform, indicating their reach and visibility. This helps in understanding where ads are most frequently seen.

### Insight 7: Clicks by Ad Type

```python
# Data for Insight 7
clicks_by_type = execute_sql_query_simulated("clicks_by_type")

plt.figure(figsize=(10, 6))
sns.barplot(x='ad_type', y='clicks_count', data=clicks_by_type)
plt.title('Total Clicks by Ad Type')
plt.xlabel('Ad Type')
plt.ylabel('Total Clicks')
plt.show()
```
**Commentary:** This visual highlights which ad types are most effective in driving user engagement through clicks. It can inform creative development.

### Insight 8: CTR by Ad Platform

```python
# Data for Insight 8
ctr_by_platform = execute_sql_query_simulated("ctr_by_platform")

plt.figure(figsize=(8, 6))
sns.barplot(x='ad_platform', y='ctr', data=ctr_by_platform)
plt.title('Click-Through Rate (CTR) by Ad Platform')
plt.xlabel('Ad Platform')
plt.ylabel('CTR (%)')
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.2%}'.format(y)))
plt.show()
```
**Commentary:** Compares the efficiency of different ad platforms in converting impressions into clicks, a key performance metric for ad effectiveness.

### Insight 9: Conversion Rate (Purchase) by Ad Type

```python
# Data for Insight 9
conversion_rate_by_type = execute_sql_query_simulated("conversion_rate_by_type")

plt.figure(figsize=(10, 6))
sns.barplot(x='ad_type', y='conversion_rate', data=conversion_rate_by_type)
plt.title('Purchase Conversion Rate by Ad Type')
plt.xlabel('Ad Type')
plt.ylabel('Conversion Rate (%)')
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.2%}'.format(y)))
plt.show()
```
**Commentary:** Evaluates the effectiveness of various ad types in leading to actual purchases after a click, directly impacting revenue generation.

### Insight 10: Campaign Performance (Total Budget vs. Total Clicks)

```python
# Data for Insight 10
campaign_performance = execute_sql_query_simulated("campaign_performance")

plt.figure(figsize=(10, 8))
sns.scatterplot(x='total_budget', y='total_clicks', data=campaign_performance)
plt.title('Campaign Budget vs. Total Clicks')
plt.xlabel('Total Budget')
plt.ylabel('Total Clicks')
plt.show()
```
**Commentary:** Explores the relationship between campaign budget allocation and the resulting total clicks, identifying potential correlations and outliers in campaign efficiency.

## Time Series Forecasting

This section demonstrates time series forecasting for Impressions, Clicks, and Purchases using a simple Linear Regression model.

```python
from sklearn.linear_model import LinearRegression
import numpy as np

# Re-create trends_df for forecasting
trends_impressions = ad_events_df[ad_events_df["event_type"] == "Impression"].set_index("timestamp").resample("W").size().rename("Impressions")
trends_clicks = ad_events_df[ad_events_df["event_type"] == "Click"].set_index("timestamp").resample("W").size().rename("Clicks")
trends_purchases = ad_events_df[ad_events_df["event_type"] == "Purchase"].set_index("timestamp").resample("W").size().rename("Purchases")

trends_df = pd.concat([trends_impressions, trends_clicks, trends_purchases], axis=1).fillna(0)

trends_df['time_idx'] = np.arange(len(trends_df))

forecast_periods = 12 # Next 3 months (approx 12 weeks)

forecast_results = {}

for col in ["Impressions", "Clicks", "Purchases"]:
    X = trends_df[['time_idx']]
    y = trends_df[col]

    model = LinearRegression()
    model.fit(X, y)

    future_time_idx = np.arange(len(trends_df), len(trends_df) + forecast_periods).reshape(-1, 1)
    forecasted_values = model.predict(future_time_idx)
    forecasted_values[forecasted_values < 0] = 0 # Ensure non-negative forecasts

    forecast_results[col] = forecasted_values

last_date = trends_df.index[-1]
forecast_dates = pd.date_range(start=last_date + pd.Timedelta(weeks=1), periods=forecast_periods, freq='W')

forecast_df = pd.DataFrame({
    'Impressions': forecast_results['Impressions'],
    'Clicks': forecast_results['Clicks'],
    'Purchases': forecast_results['Purchases']
}, index=forecast_dates)

# Plotting Forecasts
for col in ["Impressions", "Clicks", "Purchases"]:
    plt.figure(figsize=(12, 6))
    plt.plot(trends_df.index, trends_df[col], label='Historical', marker='o', markersize=4)
    plt.plot(forecast_df.index, forecast_df[col], label='Forecast', linestyle='--', marker='x', markersize=4)
    plt.title(f'Historical and Forecasted {col} (Weekly)')
    plt.xlabel('Date')
    plt.ylabel(col)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
```

**Forecasting Commentary:**

*   **Impressions Forecast:** The linear regression model forecasts a **decreasing** trend in Impressions over the next 3 months. This suggests a potential decline in ad visibility. Business applications include investigating reasons for the decline (e.g., ad fatigue, budget cuts, platform changes), optimizing ad placements, and exploring new channels to maintain or increase reach.

*   **Clicks Forecast:** The linear regression model forecasts a **decreasing** trend in Clicks over the next 3 months. A decline in clicks indicates reduced user engagement. Business applications involve reviewing ad creatives, targeting strategies, and call-to-actions to improve ad relevance and encourage more clicks.

*   **Purchases Forecast:** The linear regression model forecasts a **decreasing** trend in Purchases over the next 3 months. A decreasing trend in purchases is a critical concern, directly impacting revenue. Business applications include analyzing the entire conversion funnel, optimizing landing pages, improving product offerings, and re-evaluating pricing or promotions to drive sales.
