# -*- coding: utf-8 -*-
"""VaccineProject.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13SZgIlqrh6_lMxZtPqhzrOybOO_LuTlr

# **🧬 COVID-19 VACCINATION PROGRESS AND RISING CASES ANALYSIS OF INDIA AND AROUND THE GLOBE 💉**

##Importing libraries
"""

import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
from plotly import subplots
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import metrics
from scipy import stats
from copy import deepcopy
import numpy as np
import pandas as pd



"""##**World vaccination progress**

###Loading Data Set
"""

from google.colab import drive
drive.mount('/content/drive')

df = pd.read_csv("/content/drive/MyDrive/country_vaccinations(original).csv")

"""### `**Data Cleaning**"""

df.info()

df['iso_code'] = df['iso_code'].fillna('GBR')

"""####Colums to drop"""

df = df.drop('daily_vaccinations_raw', axis=1)

"""####Transformation of Data"""

df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date', ascending=True)

df['date'] = df['date'].dt.strftime('%d-%m-%Y')

unique_dates = df['date'].unique()

original_df = df.copy()

for iso_code in df['iso_code'].unique():
    for inc_date in unique_dates:
        if df.loc[df['iso_code'] == iso_code, 'date'].str.contains(inc_date).any():
            continue
        else:
            df.loc[len(df)] = [None, iso_code, inc_date] + 11 * [None]

df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date', ascending=True)

df['date'] = df['date'].dt.strftime('%m-%d-%Y')

df.head()

tdf = df.copy()


for iso_code in tdf['iso_code'].unique():
    tdf.loc[tdf['iso_code'] == iso_code, :] = tdf.loc[tdf['iso_code'] == iso_code, :].fillna(method='ffill').fillna(0)

"""###****Visualisation of data****"""

#@title World vaccination progress

fig = px.choropleth(
    tdf,                            # Input Dataframe
    locations="iso_code",           # identify country code column
    color="total_vaccinations",                     # identify representing column
    hover_name="country",              # identify hover name
    animation_frame="date",
    #category_orders={"frame": list(sorted(tdf['date'].unique()))},            # identify date column
    color_continuous_scale= 'viridis',
    projection="natural earth",        # select projection
    range_color=[0,5000000],
    title='<span style="font-size:36px; font-family:Times New Roman">Number of vaccinations per country</span>',
)             # select range of dataset     
fig.show()

"""**Insight**

Since the World Health Organization (WHO) declared the COVID-19 outbreak a pandemic back in March 2020, the virus has claimed more than 2.5 million lives globally with upwards of 113 million cases being confirmed by laboratory tests (March 2021).

The pandemic has impacted almost every corner of life, causing global economies to stall, changing the way we work and interact with our loved ones, and stretching healthcare systems to the limit. Governments around the world have been forced to implement harsh restrictions on human activity to curb the spread of the virus.
COVID-19 vaccination is now offering a way to transition out of this phase of the pandemic. Without them, many scientists believe that natural herd immunity would not have been sufficient to restore society to its normal status quo and that it would have resulted in extreme fatality. This is something that has been echoed by many health organizations including the WHO. In a scenario without access to vaccines, strict behavioral measures may have had to remain for the foreseeable future.

Fortunately, the beginning of 2021 saw numerous vaccines given emergency approval and begin their roll out in countries across the world. As of March 2021, just shy of 300 million vaccine doses had been administered worldwide. The figures give hope of a return to ‘normal’.
"""

#@title Data Cleaning
df1 = df.drop(['iso_code', 'people_fully_vaccinated', 'total_vaccinations_per_hundred','people_vaccinated_per_hundred','people_fully_vaccinated_per_hundred', 'daily_vaccinations_per_million', 'vaccines','source_name', 'source_website' ], axis=1)

"""###**Data Manipulation**"""

tdf = df.copy()
tdf = tdf.dropna(subset=['vaccines'])

vac_df = tdf.groupby(['iso_code','vaccines']).max().reset_index()
vac_df['vaccines_split'] = vac_df['vaccines'].apply(lambda x: [w.strip() for w in x.split(',')])

def format_number(number):
    return ("{:,}".format(number))

from plotnine import options as op
from plotnine import ggplot, aes, geom_col, coord_flip, scale_fill_manual, labs, theme, element_rect, element_blank, element_text, element_line

"""###**Top countries to vaccinate**"""

top_20_countries_vaccinated = pd.DataFrame(df1.groupby("country")["total_vaccinations"].max().sort_values(ascending = False).head(10))
top_20_countries_vaccinated.reset_index(level=0,inplace=True)
# top_20_countries_vaccinated = convert_df_with_continent(top_20_countries_vaccinated)
top_20_countries_vaccinated['number_labels'] = ['']*top_20_countries_vaccinated.shape[0]

for i in range(top_20_countries_vaccinated.shape[0]):
    top_20_countries_vaccinated['number_labels'].iloc[i] = format_number(top_20_countries_vaccinated['total_vaccinations'].iloc[i])
    
op.figure_size=(8,5)
ax = (ggplot(top_20_countries_vaccinated)         
 + aes(x='country', y='total_vaccinations')    
 + geom_col(size=20)
#  + geom_label(aes(label = 'number_labels'),ha='right',color = "white",label_padding= 0.25)
 + coord_flip()
 + scale_fill_manual(values = ["#B21236","#F03812","#FE8826","#FEB914","#2C9FA2","#002C2B","#F7E1C0"])
 + labs(title = "Top 10 Vaccinated Countries")
 + labs(y = "Number of Vaccinations", x = "Country")
 + theme(
     panel_background = element_rect(),    
    plot_background = element_rect(),
  legend_background = element_rect(),
    legend_key = element_blank(),
   
    panel_grid = element_line(size = 0.3),
    panel_grid_minor_y = element_blank(),
    panel_grid_major_y = element_blank(),
    
    legend_text = element_text(color = "black"),
    axis_text_x = element_text(color = "black", size = 20),
    axis_text_y = element_text(color = "black", size = 13, hjust = 1, margin={'b': 20, 't':10}),
    axis_title = element_text(color = "black", size = 14, hjust = 1),
    plot_title = element_text(color = "black", face = "bold", size = 20, hjust = 4, margin={'b': 20, 't':10}),
    panel_spacing_x = 1
  )
)

fig = ax.draw()

image = plt.imread('https://raw.githubusercontent.com/vineethbabu/coronavaccine_images/main/1_enlargev3.png')

fig.figimage(image, xo=0, yo=0, alpha=0.2, norm=None, cmap=None, vmin=None, vmax=None, origin=None, resize=True)

fig.show()

"""##**India's vaccination progress and cases analysis**

#####Importing Libraries
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly

"""#####Loading Dataset"""

dfCase = pd.read_csv("/content/case_time_series.csv")
dfSw = pd.read_csv("/content/state_wise1.csv")
dfSt = pd.read_csv("/content/states.csv")
dfVac = pd.read_csv("/content/vaccine_doses_statewise.csv")
dfExp = pd.read_csv("/content/India_vac_export.csv")

"""#####Analysing Dataset"""

dfCase

dfCase.info()

dfSw

dfSw.info()

dfSt

dfSt.info()

dfVac

dfVac.info()

dfExp

dfExp.info()

"""#####Cleaning Dataset"""

dfCase = dfCase.drop(['Date'],axis=1)

dfCase

dfSw = dfSw.drop(['Last_Updated_Time','Migrated_Other','Delta_Confirmed','Delta_Recovered','Delta_Deaths','State_Notes'],axis=1)

dfSw

dfSt = dfSt.drop(['Other','Tested'],axis=1)

dfSt

# dfvac and dfExp are unchanged

dfVac

dfExp

"""####**Some plots depicting different situations in India**

#####**India's Total Case Load**
"""

plt.style.use("dark_background")
Date=dfCase['Date_YMD']
Tcases=dfCase['Total Confirmed']
Dcases=dfCase['Daily Confirmed']

fig, (ax1,ax2) = plt.subplots(nrows=2,ncols=1)
fig.patch.set_facecolor('black')
ax1.plot(Date, Dcases, label='Daily Cases')
ax2.plot(Date, Tcases, label='Total Cases')

ax1.legend()
ax1.set_title("India's Daily Covid Case Load")
ax1.set_xlabel('Date')
ax1.set_ylabel('Number Of Cases')
ax1.set_xticklabels([])

ax2.legend()
ax2.set_title("India's Total Covid Case Load")
ax2.set_xlabel('Date')
ax2.set_ylabel('Number Of Cases')
ax2.set_xticklabels([])

plt.subplots_adjust(right=2, top=3)
# plt.tight_layout()
plt.show()

"""#####**India's Recovery Record**"""

plt.style.use("dark_background")
Date=dfCase['Date_YMD']
Trec=dfCase['Total Recovered']
Drec=dfCase['Daily Recovered']

fig, (ax1,ax2) = plt.subplots(nrows=2,ncols=1)
fig.patch.set_facecolor('black')
ax1.plot(Date, Drec, label='Daily Recovered')
ax2.plot(Date, Trec, label='Total Recovered')

ax1.legend()
ax1.set_title("India's Daily Recovery Record")
ax1.set_xlabel('Date')
ax1.set_ylabel('Number Of People Recovered')
ax1.set_xticklabels([])

ax2.legend()
ax2.set_title("India's Total Recovery Record")
ax2.set_xlabel('Date')
ax2.set_ylabel('Number Of People Recovered')
ax2.set_xticklabels([])

plt.subplots_adjust(right=2, top=3)
# plt.tight_layout()
plt.show()

"""#####**India's Mortality Situation**"""

plt.style.use("dark_background")
Date=dfCase['Date_YMD']
Tdet=dfCase['Total Deceased']
Ddet=dfCase['Daily Deceased']

fig, (ax1,ax2) = plt.subplots(nrows=2,ncols=1)
fig.patch.set_facecolor('black')
ax1.plot(Date, Ddet, label='Daily Deceased')
ax2.plot(Date, Tdet, label='Total Deceased')

ax1.legend()
ax1.set_title("India's Daily Death Toll")
ax1.set_xlabel('Date')
ax1.set_ylabel('Number Of People Deceased')
ax1.set_xticklabels([])

ax2.legend()
ax2.set_title("India's Total Death Toll")
ax2.set_xlabel('Date')
ax2.set_ylabel('Number Of People Deceased')
ax2.set_xticklabels([])

plt.subplots_adjust(right=2, top=3)
# plt.tight_layout()
plt.show()

plt.style.use("dark_background")
plt.figure(figsize= (7, 4), facecolor='white')
plt.xkcd(False)
plt.rcdefaults()
state = []
for i in range(1,21):
  state.append(dfSw['State'][i])

cases = []
for i in range(1,21):
  cases.append(dfSw['Confirmed'][i])

cases.reverse()  
state.reverse() 
plt.barh(state, cases)
plt.title("State Wise Cases")
plt.xlabel("Number Of Covid Cases   (scale = num*10 Lakhs)")
plt.subplots_adjust(right=1.5, top=2)
plt.figure(figsize=(250, 250), dpi=144)
plt.show()

plt.style.use("dark_background")
# plt.xkcd(False)
# plt.rcdefaults()
state = []
for i in range(1,35):
  state.append(dfVac['State'][i])

act_cases = []
for i in range(1,35):
  act_cases.append(dfVac['30-04-2021'][i])

# act_cases.reverse()  
# state.reverse() 
plt.barh(state, act_cases)
plt.title("State Wise Vaccination")
plt.xlabel("Number Of Vaccine Doses Administered   (scale = num*100 lakh)")
plt.subplots_adjust(right=2, top=3)
# plt.figure(figsize=(250, 250), dpi=144)
# plt.tight_layout()
plt.show()

"""#####**India's Vaccine Export Analysis**"""

plt.style.use("dark_background")

con1 = []
for i in range(0,23):
  con1.append(dfExp['Country'][i])

vac1 = []
for i in range(0,23):
  vac1.append(dfExp['Total Vaccines'][i])

con2 = []
for i in range(23,48):
  con2.append(dfExp['Country'][i])

vac2 = []
for i in range(23,48):
  vac2.append(dfExp['Total Vaccines'][i])

con3 = []
for i in range(48,73):
  con3.append(dfExp['Country'][i])

vac3 = []
for i in range(48,73):
  vac3.append(dfExp['Total Vaccines'][i])

con4 = []
for i in range(73,95):
  con4.append(dfExp['Country'][i])

vac4 = []
for i in range(73,95):
  vac4.append(dfExp['Total Vaccines'][i])


fig, [[ax1, ax2],[ax3, ax4]] = plt.subplots(nrows=2,ncols=2)
ax1.barh(con1,vac1, label='Vaccine Doses Exported (in Lakhs)')
ax2.barh(con2,vac2, label='Vaccine Doses Exported (in Lakhs)')
ax3.barh(con3,vac3, label='Vaccine Doses Exported (in Lakhs)')
ax4.barh(con4,vac4, label='Vaccine Doses Exported (in Lakhs)')


ax1.legend()
ax1.set_title("Vaccines Exported By India")
ax1.set_xlabel('No. Of Vaccines Exported')

ax2.legend()
ax2.set_title("Vaccines Exported By India")
ax2.set_xlabel('No. Of Vaccines Exported')

ax3.legend()
ax3.set_title("Vaccines Exported By India")
ax3.set_xlabel('No. Of Vaccines Exported')

ax4.legend()
ax4.set_title("Vaccines Exported By India")
ax4.set_xlabel('No. Of Vaccines Exported')

plt.subplots_adjust(right=4, top=5)
# plt.tight_layout()
plt.show()

"""**Insight**

While India was not a part of the initial research and development efforts, it was a foregone conclusion that it would eventually have a significant role to play in vaccine manufacturing and development. India is known as the “pharmacy of the world,” and manufactures about 60 percent of all the world’s vaccines. India is also home to the Serum Institute of India, which is the world’s largest vaccine manufacturer. The Serum Institute has signed multiple deals with vaccine developers, including with Oxford-AstraZeneca and Novavax.

With the Serum Institute selling doses around the world, the door is wide open for India to play a constructive role in ensuring the world gets vaccinated, especially as higher income countries focus on taking care of their own citizens first. And, with India in competition with China in the immediate neighborhood, India can effectively use vaccines as a mechanism to pushback against Chinese influence.

###**State wise analysis of India**

####**Correaltion of covid-19 cases and vaccination in India**

#####Importing libraries and data cleaning
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import matplotlib.dates as mdates
from matplotlib import cm
from matplotlib.ticker import LinearLocator
from matplotlib.ticker import FormatStrFormatter

# %matplotlib inline

df3 = pd.read_csv("/content/Book2.csv")

df3.head()

df3 = df3.dropna()
x = df3['Date']
y1 = df3['Daily']
y2 = df3['Vaccinated']

"""#####**A plot to show vaccination and cases over the period of time**"""

fig, ax1 = plt.subplots(1,1,figsize=(15,7), dpi= 80)
fig.set_facecolor('white')
fig.patch.set_facecolor('lightgrey')

ax1.plot(x, y1, color='tab:red')

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
ax2.plot(x, y2, color='tab:green')

ax1.set_xlabel('Time', fontsize=20)
ax1.tick_params(axis='x', rotation=45, labelsize=12)
ax1.set_ylabel('Covid cases', color='tab:red', fontsize=25)
ax1.tick_params(axis='y', rotation=0, labelcolor='tab:red', labelsize=15)
ax1.grid(alpha=.4)

ax2.set_ylabel("Vaccinated", color='tab:green', fontsize=25)
ax2.tick_params(axis='y', labelcolor='tab:green', labelsize = 15)
ax2.set_xticks(np.arange(0, len(x), 12))
ax2.set_xticklabels(x[::12], rotation=0, fontdict={'fontsize':10})
ax2.set_title("Covid Cases and vaccination", fontsize=25)
fig.tight_layout()
plt.show()

"""#####**Regressive analysis of vaccination and covid cases**

######Data cleaning
"""

x1 = df3.iloc[:, 1].values
y1 = df3.iloc[:, 2].values

x1 = x1.reshape(-1,1)

from sklearn.model_selection import train_test_split
x1_train, x1_test, y1_train, y1_test = train_test_split(x1, y1, test_size = 0.1, random_state = 0, shuffle = False)

from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
polynom = PolynomialFeatures(degree=4)
x_polynom = polynom.fit_transform(x1_train)
x_polynom_test = polynom.fit_transform(x1_test)

polyReg= LinearRegression()
polyReg.fit(x_polynom, y1_train)

y1_pred = polyReg.predict(x_polynom)

"""#####**Coefficients of polynomial regression of degree 4**


"""

print(polyReg.coef_)

"""#####**Plot of regression analysis**"""

plt.figure(figsize = (15,8), facecolor='white')
plt.scatter(x1_train, y1_train, color = "red")
plt.plot(x1_train, polyReg.predict(polynom.fit_transform(x1_train)), color = "green")
plt.title("A regressive analysis of vaccination vs cases", fontsize =20)
plt.xlabel("Vaccination", fontsize = 16)
plt.ylabel("Daily cases", fontsize = 16)
plt.show()

"""From this regresion model we can predict that as vaccination is increasing covid cases are decreasing. Covid daily cases achieved a peak in India at a certain point claimed by the experts as a second wave of the virus, but as  our country started vaccinating people from January 2021 and with time it gained pace, initially it was on a slower pace which was not sufficient to control upcoming second wave of corona virus, but with time it increased to manyfolds and as peak passed cases started decreasing and will keep on decreasing with vaccination.

#####Data manipulations
"""

df3.set_index('Date',inplace=True)

df3['Vaccinated_daily']=df3['Vaccinated'].shift(-1) 
df3['Vaccinated_daily']=df3['Vaccinated_daily']-df3['Vaccinated']
df3['moving_vacc']=df3['Vaccinated_daily'].rolling(20).mean()
df3['moving_case']=df3['Daily'].rolling(20).mean()

df3['moving_vac/10']=df3['moving_vacc'].values/10

"""#####**Trying to get an insight from daily covid cases and daily vacciantions**"""

plt.figure(figsize=(17,7))
plt.ylabel('Daily cases and (Daily vaccinations)/10', rotation=90, fontsize=15)
plt.xlabel('Date', fontsize=16)
plt.title("Daily cases and daily people vaccinated", fontsize = 20)
#df.loc['16-01-2021':'27-05-2021','Vaccinated_daily'].plot()
df3.loc['16-01-2021':'27-05-2021','moving_vac/10'].plot()
# df.loc['16-01-2021':'27-05-2021','Daily'].plot()
df3.loc['16-01-2021':'27-05-2021','moving_case'].plot()

"""######**Insight**
Here, blue curve represents daily vaccinations and orange curve represents daily covid cases, we can sort find a correlation here. It is visible that before second wave of corona virus hit india i.e in march 2021 daily vaccination was not up to the mark, here we can see two reasons for that first of all government was not in a hurry to vaccinate everyone it had opened vaccination for 60+ first then 45+ age group. Secondly people were also a bit skeptical about the vaccine and its side effects intially so daily vaccination was not up to the mark. But when second wave hits india cases went on spiking numbers, people become a bit aware about the vaccine and started volunteering for it, so daily vaccination kept on increasing. But it dipped because of opening of vaccination of age group 18-44 from may 2021 which incresed demand of vaccines and supply was not sufficient to meet the demands.

####**Visualisation on map of India**

#####Importing libraries
"""

!pip install geopandas
!pip install geojson
!pip install plotly --upgrade

import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import datetime as dt
import geojson 
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
from plotly import subplots
import plotly.figure_factory as ff
import json
import numpy as np

"""#####Data cleaning"""

df1 = pd.read_csv('/content/state_wise.csv')
df1.head()

india_geojson = json.load(open("/content/states_india.geojson", "r"))

state_id_map={}
for feature in india_geojson['features']:
  feature['id'] = feature['properties']['state_code']
  state_id_map[feature['properties']['st_nm']]= feature['id']

df1['id'] = df1['State'].apply(lambda x: state_id_map[x])

"""#####**Visualiation on map of India**"""

fig = px.choropleth(
    df1,
    locations="id", 
    geojson = india_geojson,         
    color="Confirmed",                  
    hover_name="State",
    hover_data = ['Confirmed'],            
    color_continuous_scale= 'viridis',
    range_color=[0,1100000],
    title='<span style="font-size:36px; font-family:Times New Roman">Covid-19 cases confirmed till 1 June 2021</span>',
) 
fig.update_geos(fitbounds = 'locations', visible= False)                
fig.show()

"""####**Time journey of covid cases in different states in India**

#####Importing libraries
"""

import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
from plotly import subplots
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import metrics
from scipy import stats
from copy import deepcopy
import numpy as np
import pandas as pd

import matplotlib
matplotlib.rcParams['animation.embed_limit'] = 2**128

"""#####Data Cleaning"""

df2 = pd.read_csv("/content/state_wise_daily.csv")

df2 = df2.drop(['Date'], axis=1)

df2 = df2[df2.Status!='Recovered']

df2 = df2[df2.Status!='Deceased']

df2=df2.set_index("Date_YMD")

df2 = df2.drop(['Status'], axis=1)

s=df2.loc['2020-03-15']

import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 5), dpi=144)
colors = plt.cm.Dark2(range(6))
ax.set_facecolor("white")
ax.tick_params(axis='x', colors='black')  
ax.tick_params(axis='y', colors='black')
ax.barh(s.index, s.values, color=colors);

def nice_axes(ax):
    ax.set_facecolor('0.8')
    ax.tick_params(labelsize=8, length=0)
    ax.grid(True, axis='x', color='white')
    ax.set_axisbelow(True)
    [spine.set_visible(False) for spine in ax.spines.values()]
    
nice_axes(ax)
fig

fig, ax_array = plt.subplots(nrows=1, ncols=3, figsize=(15, 2.5), dpi=144, tight_layout=True)
dates = ['2020-03-15', '2020-03-25', '2020-04-14']
for ax, date in zip(ax_array, dates):
    s = df2.loc[date].sort_values()
    ax.barh(s.index, s.values, color=colors)
    ax.set_title(date, fontsize='smaller')
    nice_axes(ax)

df2_expanded = df2['2020-03-14': '2021-05-30']

df_rank_expanded2 = df2_expanded.assign(TT = lambda x: 1, 
          AN = lambda x: 2 ,AP=lambda x: 3, AR=lambda x: 4, AS=lambda x: 5, BR=lambda x: 6, CH=lambda x: 7, CT=lambda x: 8, DN=lambda x:9, DD=lambda x:10, DL=lambda x:11, GA=lambda x:12, GJ=lambda x:13, HR=lambda x:14, HP=lambda x:15, JK=lambda x:16, JH=lambda x:17, KA=lambda x:18,	KL=lambda x:19,	LA=lambda x:20,	LD=lambda x:21,	MP=lambda x:22,	MH=lambda x:23,	MN=lambda x:24,	ML=lambda x:25,	MZ=lambda x:26,	NL=lambda x:27,	OR=lambda x:28,	PY=lambda x:29,	PB=lambda x:30,	RJ=lambda x:31,	SK=lambda x:32,	TN=lambda x:33,	TG=lambda x:34,	TR=lambda x:35,	UP=lambda x:36,	UT=lambda x:37,	WB=lambda x:38,	UN=lambda x:39)

fig, ax_array = plt.subplots(nrows=1, ncols=4, figsize=(15, 2), dpi=144, tight_layout=True)
labels = df2_expanded.columns
for i, ax in enumerate(ax_array.flatten()):
    y = df_rank_expanded2.iloc[i]
    width = df2_expanded.iloc[i]
    ax.barh(y, width, color=colors, tick_label=labels)
    nice_axes(ax)
ax_array[0].set_title('')
ax_array[-1].set_title('');

from matplotlib.animation import FuncAnimation

def init():
    ax.clear()
    nice_axes(ax)
    ax.set_ylim(.2, 6.8)

def update(i):
    for bar in ax.containers:
        bar.remove()
    y = df_rank_expanded2.iloc[i]
    width = df2_expanded.iloc[i]
    ax.barh(y=y, width=width, color=colors, tick_label=labels)
    # dates = dfIndonesia_expanded['date']
    ax.set_title(f'Vaccinations in Asean Countries', fontsize='smaller')
    
fig = plt.Figure(figsize=(15, 7), dpi=144)
ax = fig.add_subplot()
ax.tick_params(axis='x', colors='black')   
ax.tick_params(axis='y', colors='black')
ax.set_facecolor("white")
anim = FuncAnimation(fig=fig, func=update, init_func=init, frames=len(df2_expanded), 
                     interval=100, repeat=False)

from IPython.display import HTML
html = anim.to_html5_video()
HTML(html)

"""#####**Time journey**"""

!pip install bar_chart_race
import bar_chart_race as bcr
bcr.bar_chart_race(df2_expanded, figsize=(6, 5), title='Vaccination in india in different states')

