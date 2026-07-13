import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# --- Load Dataset ---
df = pd.read_csv('marketing_campaign.csv', sep=';')
# Display the first few rows of the dataset
print(df.head())
#display missing values in the dataset
print(df.isnull().sum())
# --- Data Cleaning ---
# Fill missing values in 'Income' with the median income
df['Income'] = df['Income'].fillna(df['Income'].median())
#see missing values after filling
print(df.isnull().sum())
#fix weird marital status values
df['Marital_Status'] = df['Marital_Status'].replace(['Alone', 'Absurd', 'YOLO'], 'Single')
#show marital status value counts after fixing
print(df['Marital_Status'].value_counts())
#check for duplicates
print(df.duplicated().sum())
#create age column from year of birth
df['Age'] = 2025 - df['Year_Birth']
#remove unrealistic ages(outliers)
df = df[df['Age'] < 90]
#create total spend column
df['Total_Spend'] = df['MntWines'] + df['MntFruits'] + df['MntMeatProducts'] + df['MntFishProducts'] + df['MntSweetProducts'] + df['MntGoldProds']
#create total purchases column
df['Total_Purchases'] = df['NumWebPurchases'] + df['NumCatalogPurchases'] + df['NumStorePurchases'] + df['NumWebVisitsMonth'] + df['NumDealsPurchases']
# create total campaigns accepted column
df['Total_Campaigns_Accepted'] = df['AcceptedCmp1'] + df['AcceptedCmp2'] + df['AcceptedCmp3'] + df['AcceptedCmp4'] + df['AcceptedCmp5'] + df['Response']
#create customer tenure(day since joining)
df['Tenure'] = (pd.to_datetime('today') - pd.to_datetime(df['Dt_Customer'])).dt.days
#create age groups
bins = [0, 30, 45, 60, 90]
labels = ['<30', '30-45', '45-60', '60+']
df['Age_Group'] = pd.cut(df['Age'], bins=bins, labels=labels)
#create income segments
income_bins = [0, 40000, 70000, 100000, np.inf]
income_labels = ['Low', 'Medium', 'High', 'Very High']
#create customer value segments
df['Customer_Value'] = pd.cut(df['Total_Spend'], bins=income_bins, labels=income_labels)
#create recency segments
recency_bins = [0, 30, 60, 90, np.inf]
recency_labels = ['Recent', 'Active', 'Inactive', 'Very Inactive']
df['Recency_Segment'] = pd.cut(df['Tenure'], bins=recency_bins, labels=recency_labels)
print("Cleaning Done! New Shape:", df.shape)
print("\nNew Columns Added:", ['Age', 'Total_Spend', 'Total_Purchases', 
                               'Total_Campaigns_Accepted', 'Customer_Tenure_Days',
                               'Age_Group', 'Income_Segment', 'Customer_Segment',
                               'Recency_Segment'])

#show dataset after feature engineering
print(df.head())
#exploratory data analysis
# set style
plt.style.use('ggplot')
# spending distribution
plt.figure(figsize=(10, 6))
plt.hist(df['Total_Spend'], bins=30, color='skyblue', edgecolor='black')
plt.xlabel('Total Spend')
plt.ylabel('Frequency')
plt.title('Distribution of Total Spend')
plt.show()
# campaign acceptance rates
campaign_cols = ['AcceptedCmp1', 'AcceptedCmp2', 'AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5', 'Response']
campaign_acceptance = df[campaign_cols].mean() * 100
import seaborn as sns
# spending by education level and customize the plot with blue color and gridlines 
plt.figure(figsize=(10, 6))
sns.boxplot(x='Education', y='Total_Spend', data=df, palette='Blues')
plt.xlabel('Education Level')
plt.ylabel('Total Spend')
plt.title('Spending by Education Level')
plt.grid(True)
plt.show()
#Change Graduation to Graduate
df['Education'] = df['Education'].replace('Graduation', 'Graduate')
#show spending by education level after fixing graduation to graduate
plt.figure(figsize=(10, 6))
sns.boxplot(x='Education', y='Total_Spend', data=df, palette='Blues')
plt.xlabel('Education Level')
plt.ylabel('Total Spend')
plt.title('Spending by Education Level')
plt.grid(True)
plt.show()
#income vs Total Spend
plt.figure(figsize=(10, 6))
plt.scatter(df['Income'], df['Total_Spend'], alpha=0.5)
plt.xlabel('Income')
plt.ylabel('Total Spend')
plt.title('Income vs Total Spend')
plt.show()
#purchase channels comparison
channels = ['NumWebPurchases', 'NumCatalogPurchases', 
            'NumStorePurchases', 'NumDealsPurchases']
channel_avg = df[channels].mean()
plt.figure()
channel_avg.plot(kind='bar', color=['#2196F3','#FF9800','#4CAF50','#E91E63'])
plt.title('Average Purchases by Channel')
plt.xticks(rotation=30)
plt.savefig('purchase_channels.png', bbox_inches='tight')
plt.show()

# key summary statistics
print("Key Summary Statistics:")
print(df.describe())
#export cleaned dataset as CSV
df.to_csv('cleaned_marketing_campaign.csv', index=False)