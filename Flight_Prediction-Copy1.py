#!/usr/bin/env python
# coding: utf-8

# # Design and implement a data science solution to predict the prices of airline flights accurately. The goal is to create a model that can analyze historical flight data and various relevant features to forecast future flight prices with a high degree of precision. The solution should be able to handle diverse datasets containing information such as departure and arrival locations, dates, times, airline carriers, class types, and other pertinent factors influencing flight prices.

# # Design and implement a data science solution to predict and enhance passenger satisfaction scores based on features such as the date of the journey, source, destination, route, duration, total stops, and additional information. The goal is to develop a regression model that accurately forecasts passenger satisfaction scores, providing airlines with insights into the factors influencing passenger experience and enabling targeted improvements.

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


flight_data = pd.read_excel(r"D:\Data for Data science\Data_Train.xlsx")


# In[3]:


flight_data


# In[4]:


flight_data.head()


# In[5]:


flight_data.info()


# In[6]:


flight_data.isnull().sum()


# In[7]:


flight_data["Route"].isnull()


# In[8]:


flight_data[flight_data["Route"].isnull()]


# In[9]:


flight_data.dropna(inplace=True)


# In[10]:


flight_data.isnull().sum()


# In[11]:


flight_data.info(memory_usage="deep")


# In[12]:


flight_data


# In[13]:


def change_into_datetime(col):
    flight_data[col] = pd.to_datetime(flight_data[col], errors = 'coerce')


# In[14]:


import warnings
from warnings import filterwarnings
filterwarnings("ignore")


# In[15]:


flight_data.columns


# In[16]:


for col in ['Date_of_Journey', 'Arrival_Time', 'Dep_Time']:
    change_into_datetime(col)


# In[17]:


flight_data["Duration"] = flight_data["Duration"].astype(str)


# In[18]:


flight_data.dtypes


# In[19]:


flight_data["Journey_Day"] = flight_data["Date_of_Journey"].dt.day
flight_data["Journey_Month"] = flight_data["Date_of_Journey"].dt.month
flight_data["Journey_Year"] = flight_data["Date_of_Journey"].dt.year


# In[20]:


flight_data


# In[21]:


def change_into_time(data, col):
    data[col+"_hour"] = data[col].dt.hour
    data[col+"_minutes"] = data[col].dt.minute


# In[22]:


change_into_time(flight_data, "Arrival_Time")


# In[23]:


change_into_time(flight_data, "Dep_Time")


# In[24]:


flight_data


# In[25]:


cols_toDrop = ["Dep_Time", "Arrival_Time"]
flight_data.drop(cols_toDrop, axis=1, inplace=True)


# In[26]:


flight_data.head()


# In[27]:


flight_data.dtypes


# In[28]:


flight_data["Total_Stops"].unique()
    


# In[29]:


def convertTotal_Stops(data, col):
    for i in range(len(data[col])):
        if data[col].iloc[i] == "non-stop":
            data[col].iloc[i] = 0
        else:
            stops = ''.join(filter(str.isdigit, data[col].iloc[i]))
            # Using ''.join and filter to extract digits from the string
            data[col].iloc[i] = int(stops) if stops else None


# In[30]:


convertTotal_Stops(flight_data, "Total_Stops")


# In[31]:


flight_data.head()


# In[32]:


flight_data.isnull().sum()


# In[33]:


flight_data.dtypes


# In[34]:


flight_data["Additional_Info"].unique()


# In[35]:


flight_data.drop("Date_of_Journey", axis = 1, inplace=True)


# In[36]:


flight_data.head()


# In[37]:


def convert_duration_to_minutes(duration_str):
    # Split the string based on 'h' and 'm' to extract hours and minutes
    duration_parts = duration_str.split(' ')
    
    total_minutes = 0
    
    for part in duration_parts:
        if 'h' in part:
            total_minutes += int(part.replace('h', '')) * 60
        elif 'm' in part:
            total_minutes += int(part.replace('m', ''))
    
    return total_minutes

# Apply the conversion function to the 'Duration' column
flight_data['Duration_in_minutes'] = flight_data['Duration'].apply(convert_duration_to_minutes, inp)


# In[38]:


flight_data.head()


# In[39]:


flight_data.drop("Duration", axis = 1, inplace = True)


# In[41]:


flight_data.head()


# In[42]:


flight_data.columns


# In[50]:


import matplotlib.pyplot as plt
import seaborn as sns

# Assuming 'flight_data' is your DataFrame

# Visualization 1: Distribution of Flight Prices
fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(16, 8))
ax[0, 0].hist(flight_data["Price"], bins=30, color='skyblue', edgecolor='black')
ax[0, 0].set_title('Distribution of Flight Prices')
ax[0, 0].set_xlabel('Price')
ax[0, 0].set_ylabel('Frequency')

# Visualization 2: Airline vs. Average Prices
average_prices_by_airline = flight_data.groupby('Airline')['Price'].mean().sort_values()
ax[0, 1].bar(average_prices_by_airline.index, average_prices_by_airline, color='skyblue')
ax[0, 1].set_title('Average Prices by Airline')
ax[0, 1].set_xlabel('Airline')
ax[0, 1].set_ylabel('Average Price')

# Visualization 3: Scatter Plot for Duration vs. Price
ax[1, 0].scatter(flight_data['Duration_in_minutes'], flight_data['Price'], color='skyblue', edgecolors='black')
ax[1, 0].set_title('Duration vs. Price')
ax[1, 0].set_xlabel('Duration (minutes)')
ax[1, 0].set_ylabel('Price')

# Visualization 4: Box Plot for Total Stops
sns.boxplot(x='Total_Stops', y='Price', data=flight_data, ax=ax[1, 1])
ax[1, 1].set_title('Flight Prices Based on Total Stops')
ax[1, 1].set_xlabel('Total Stops')
ax[1, 1].set_ylabel('Price')

plt.tight_layout()
plt.show()



# In[ ]:




