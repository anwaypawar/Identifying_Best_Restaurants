#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# # Name - Anway Pawar
# # Capstone Project - 01
# # Identifying and Recommending Best Restaurants

# In[1]:


import pandas as pd
import numpy as np
print('libraries imported')


# In[2]:


import matplotlib.pyplot as plt
import seaborn as sns


# In[7]:


data = pd.read_excel('data.xlsx')


# In[8]:


# now performing preliminary data analysis


# In[9]:


data.info()


# In[10]:


data.columns = data.columns.str.replace(' ','_')


# In[11]:


(data == 0).sum()


# In[13]:


missing_city = data[(data.Longitude ==0)|(data.Latitude == 0)].City.unique()


# In[14]:


len(missing_city)


# In[15]:


# now filling the missing values using the city names


# In[18]:


lat_n_long = data.groupby('City').agg('mean')[['Latitude','Longitude']].loc[missing_city]


# In[23]:


missing_city_loc = {x:tuple(lat_n_long.loc[x]) for x in missing_city}
((data.Latitude == 0)| (data.Longitude == 0)).sum()


# In[24]:


len(lat_n_long)


# In[29]:


for i in data.index:
    if (data.loc[i,'Latitude']==0) or (data.loc[i, 'Longitude'] == 0):
        city = data.loc[i, 'City']
        lat, long = missing_city_loc[city]
        data.loc[i,'latitude'] = lat
        data.loc[i,'longitude'] = long
    


# In[30]:


#now duplicated 


# In[31]:


print('Any duplicated Rows ?:', data.duplicated().any())
print('No. of Duplicated Rows:', data.duplicated().sum())


# In[32]:


data.duplicated('Restaurant_ID').any()


# In[35]:


print('No. of unique Restaurant_IDs :', data.Restaurant_ID.nunique())
print('No. of unique Restaurant_Names:', data.Restaurant_Name.nunique())


# In[36]:


# above information tells us that the restaurant ids are unique, however there is an overlap in Restaurant names


# In[37]:


# now for geographical disribution


# In[44]:


country_code = pd.read_excel('Country-Code.xlsx')


# In[45]:


country_code.columns = country_code.columns.str.replace(' ','_')


# In[49]:


data = pd.merge(data,country_code, on = 'Country_Code')


# In[50]:


#now explor the geographical distrbution of the restaurant, finding out the cities with maximum/ minimum number of restaurant


# In[51]:


plt.figure(figsize = (20,5))
vc = pd.DataFrame(data.country.Values_counts()).rename({'Country'})


# In[58]:


plt.figure(figsize = (20,5))
vc = pd.DataFrame(data.Country.value_counts()).rename({'Country':'Freq'}, axis= 1)
vc['Perc'] = (vc.Freq/vc.Freq.sum()*100).round(1)
sns.countplot(x = 'Country', data = data, order = vc.index)
for i in range(len(vc)):
    plt.annotate(str(vc.Perc[i]) +'%', xy = (i -0.2, int(vc.Freq[i]/2)), fontsize = 12)
    plt.xticks(size = 12, rotation = 10)
    plt.xlabel('Country',size = 16)
plt.show()


# In[60]:


vc = pd.Series()
vc['India'] = len(data[data.Country == 'India'])
vc['Others'] = len(data[data.Country != 'India'])
vc.plot.pie(radius = 2,autopct = '%1.1f%%' , textprops = {'size':15 }, explode = [0.1,0.1], shadow = True, cmap ='Set2')
plt.xticks(size = 12, rotation = 10)
plt.ylabel('')
plt.show()


# In[62]:


# infrence - Zomato’s largest market is in India itself, nobody even comes close. * Analysing data from India should give us a pretty accurate representation of the entire data. * One importan  that might vary across different regions is the types of Cusinies. So it should be interesting to see how many cusinies are served throughout the world.


# In[63]:


# explore how ratings are distrubuted over all 


# In[64]:


data['Rating_cat'] = data['Aggregate_rating'].round(0).astype(int)


# In[67]:


plt.figure( figsize = (15, 4))
sns.countplot('Aggregate_rating', data = data[data.Aggregate_rating !=0],palette = 'magma')
plt.tick_params('x', rotation = 70)
plt.title('Y')
plt.show()


# In[70]:


data["Rating_color"].value_counts()
Color_represents = data.groupby(['Rating_color'],as_index =False)['Aggregate_rating'].mean()


# In[71]:


Color_represents.columns = ['Rating_color','Average_rating']


# In[73]:


Color_represents =Color_represents.sort_values(by='Average_rating',ascending=False)


# In[74]:


Color_represents = Color_represents[0:5]
Color_represents['Ratings'] = ['Excellent','Very Good','Good','Okay','Poor']


# In[75]:


Color_represents


# In[76]:


# Now restaurant franchise is a thiriving venture. So, it becomes very important to explore the franchise with most national presense


# In[79]:


plt.figure(figsize = (15,5))
vc = data.City.value_counts()[:5]
g = sns.barplot(x = vc.index, y = vc.values, palette = 'Set2')
g.set_xticklabels(g.get_xticklabels(),fontsize = 13)
for i in range(5):
    value = vc[i]
    g.text(y = value - 2,x = i +0.125 , s = value, color='black', ha="center",fontsize = 15)
    g.set_ylabel('Count', fontsize = 15)
    g.set_title('Restaurant Presence', fontsize = 30, color = 'darkred')
plt.show()


# In[80]:


# form above we can see that new delhi has most no. of restaurant, gurgoan, nodia, and faridabad are behind it but by very 
# huge margin  and other cities like amhedabad, amrtisar, bhubaneshwar have least no. of restuarant. It is a noticable point that there
# is not even a single city outside india to be in top 10 no. of restaurants


# In[87]:


plt.figure(figsize = (15,10))
vc = data.Restaurant_Name.value_counts()[:10]
g = sns.barplot(y = vc.index, x = vc.values, palette = 'Set2')
g.set_yticklabels(g.get_yticklabels(),fontsize = 13)
for i in range(10):
    value = vc[i]
g.text(x = value - 2,y = i +0.125 , s = value, color='black', ha="center",fontsize = 15)
g.set_xlabel('Count', fontsize = 15)
g.set_title('c', fontsize = 30, color = 'darkred')
plt.show()


# In[ ]:


# What is the ratio between restaurants that allow table booking vs that do not allow table booking?
# What is the percentage of restaurants providing online delivery?


# In[112]:


f,axes = plt.subplots(1,2,figsize = (20,7))
data.Has_Table_booking.value_counts().plot.pie(ax = axes[0],autopct = '%0.1f%%', radius = 1.25, wedgeprops = {'width' : 0.75}, cmap = 'Set2',
textprops = {'size' : 18,} )
#axes[0].set_xticklabels(labels = axes[0].get_xticklabels(),rotation = 0)
axes[0].set_title('Table Booking\n',fontsize = 16)
axes[0].set_ylabel('')
data.Has_Online_delivery.value_counts().plot.pie(ax = axes[1], autopct = '%0.1f%%', radius = 1.25,wedgeprops = {'width' : 0.75}, cmap = 'Set2_r',
textprops = {'size' : 18} )
axes[1].set_title('Online Delivery\n', fontsize = 16)
#axes[1].set_xticklabels(labels = axes[1].get_xticklabels(),rotation = 0)
axes[1].set_ylabel('')
plt.tight_layout(w_pad = 20, h_pad = 10, pad = 4)
plt.show()


# In[113]:


pd.crosstab(data.Has_Online_delivery,data.Has_Table_booking)


# In[117]:


#Is there a difference in no. of votes for the restaurants that deliver and the restaurant that don’t?


# In[118]:


d = data[data.Aggregate_rating != 0]
pd.crosstab(d.Aggregate_rating, d.Has_Online_delivery).plot.bar()


# In[121]:


plt.figure(figsize=(20,6))
sns.countplot(data=data[data.Aggregate_rating !=0],x='Aggregate_rating',hue='Has_Online_delivery',palette='viridis')
plt.show()


# In[122]:


top10 = data.City.value_counts()[:10]
top10[:2]


# In[123]:


# What are the top 10 cuisines served across cities?


# In[ ]:


l = []
for i in data.Cuisines.str.split(','):
    l.extend(i)
    s = pd.Series([i.strip() for i in l])
from wordcloud import WordCloud, STOPWORDS
stopwords = set(STOPWORDS)
wordcloud = (WordCloud(stopwords=stopwords).generate_from_frequencies(s.value_counts()))
fig = plt.figure(1,figsize=(15, 15))
plt.imshow(wordcloud)
plt.axis('off')
plt.show()


# In[136]:


plt.figure(figsize = (15,5))
sns.barplot(x = s.value_counts()[:10].index, y = s.value_counts()[:10] )
for i in range(10):
    plt.annotate(s.value_counts()[i], xy = (i-0.15,s.value_counts()[i]+50),fontsize = 14)
plt.ylim(0, round(s.value_counts()[0]+300))
plt.show()


# In[145]:


#Q10)


# In[153]:


data.columns


# In[154]:


plt.figure(figsize = (15,5))
sns.distplot(data[data.Average_Cost_for_two != 0].Average_Cost_for_two)
plt.show()


# In[157]:


data['Average_Cost_for_two_cat']= pd.cut(data[data.Average_Cost_for_two != 0].Average_Cost_for_two,
bins = [0, 200, 500, 1000, 3000, 5000,10000, 800000000],
labels = ['<=200', '<=500', '<=1000', '<=3000', '<=5000', '<=10000', 'no,limit'])


# In[159]:


f = plt.figure(figsize = (20,10))
ax = plt.subplot2grid((2,5), (0,0),colspan = 2)
sns.countplot(data['Average_Cost_for_two_cat'], ax = ax, palette = sns.color_palette('magma', 7))
ax.set_title('Average Price')

ax.set_xlabel('')
ax.tick_params('x', rotation = 70)

ax = plt.subplot2grid((2,5), (0,2), colspan = 3)
sns.boxplot(x = 'Average_Cost_for_two_cat', y = 'Aggregate_rating', data =data, ax = ax, palette = sns.color_palette('magma', 7))
count = data['Price_range'].value_counts().reset_index()
count.columns = ['Price_range', 'Count']

ax = plt.subplot2grid((2,5), (1,0),colspan = 2)
sns.barplot(x = 'Price_range', y = 'Count', data = count, ax=ax, palette = sns.color_palette('magma', 5))
ax.set_title('Price Range')
ax.set_xlabel('')

ax = plt.subplot2grid((2,5), (1,2), colspan = 3)
sns.boxplot(x='Price_range', y ='Aggregate_rating', data = data, ax = ax,palette = sns.color_palette('magma', 5))
plt.subplots_adjust(wspace = 0.3, hspace = 0.4,)
plt.suptitle('Price Count & Rating Distribution', size = 30)
plt.show()



# In[164]:


f,ax = plt.subplots(1,2,figsize=(20,6))
sns.scatterplot(data=data,x='Aggregate_rating',y='Votes', ax = ax[0], palette ='Set2')
agg = data.pivot_table(index = 'Rating_cat', values = 'Votes', aggfunc = 'sum').reset_index()
agg['Perc_votes']= (agg.Votes/agg.Votes.sum()*100).round(2)
sns.barplot(x = 'Rating_cat', y = 'Votes', data = agg, ax = ax[1], palette='Set2')
for i in range(len(agg)):
    ax[1].annotate(str(agg.Perc_votes[i])+' %', xy = (i-0.2,int(agg.Votes[i]/2)), fontsize = 14, fontweight = 'medium')
    ax[0].set_ylim(0,1000)
    ax[0].set_xlim(1,5)
    ax[0].set_ylabel('Votes',fontsize = 18 )
    ax[0].set_xlabel('Aggregate Rating',fontsize = 18 )
    ax[0].set_xticklabels(ax[0].get_xticks(),fontsize = 12)
    ax[1].set_ylabel('Total Votes',fontsize = 18 )
    ax[1].set_xlabel('Rating Category',fontsize = 18 )
    ax[1].set_xticklabels(agg.Rating_cat,fontsize = 12)
plt.suptitle('Aggregate Rating Vs Votes', size = 30)
plt.show()


# In[ ]:




