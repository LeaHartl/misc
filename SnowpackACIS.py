#! /usr/bin/env python3

##########
# Leas script to make graph
##########


# load standard modules
import argparse
import json
import urllib
import requests
# import os.path
import numpy as np
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import matplotlib.pyplot as plt


from matplotlib.animation import FuncAnimation
import matplotlib.dates as mdates


def update(frame):
    xdata.append(frame)
    ydata.append(np.sin(frame))
    ln.set_data(xdata, ydata)
    return ln,


# read data from REST endpoint
def read_data( url, params, header="" ):
  resq = requests.get(url, headers=header, params=params)
  # print( resq.url )
  return resq.json()

def assign_wy(row):
	if row.date.month>=7:

		daynum=row.date - pd.to_datetime(str(row.date.year)+'-07-01')
		# print(daynum.days)

		# return(pd.datetime(row.date.year+1,1,1).year)
		return(daynum.days)
	else:
		daynum=row.date - pd.to_datetime(str(row.date.year-1)+'-07-01')
		# return(pd.datetime(row.date.year,1,1).year)
		return(daynum.days)

def assign_yr(row):
	if row.date.month>=7:

		yrnum=str(row.date.year)
		# print(daynum.days)

		# return(pd.datetime(row.date.year+1,1,1).year)
		return(yrnum)
	else:
		yrnum=str(row.date.year-1)
		# return(pd.datetime(row.date.year,1,1).year)
		return(yrnum)


def update_line(num, data, line):
    line.set_data(data[..., :num])
    return line,




stnID = 'USW00026411'
sdate = 'por'
edate = 'por'
# ac_params = {"sid":stnID ,"sdate":sdate,"edate":edate,"elems":[{"name":"snow", "interval":"dly", "duration":"dly"},{"name":"pcpn","interval":"dly","duration":"dly"}]}
ac_params = {"sid":stnID ,"sdate":sdate,"edate":edate,"elems":[{"name":"snwd","interval":"dly","duration":1}]}
# ac_params = {"sid":stnID ,"sdate":sdate,"edate":edate,"elems":[{"name":"snow", "interval":"dly", "duration":"dly"},{"name":"snow","interval":"dly","duration":"dly", "reduce": "mean","normal":"departure", "maxmissing": 3}]}
acis_station_url = "https://data.rcc-acis.org/StnData?"


# setup final dataset dictionary
station_data = {}
col_names = ['date', 'snow']

# # #call acis and parse to df
# request_params = urllib.parse.urlencode({'params': json.dumps(ac_params)})
# acis_station_data = read_data(acis_station_url, params=request_params)
# station_df = pd.DataFrame(acis_station_data['data'], columns=col_names)
# station_df.replace('M', np.nan, inplace = True)
# station_df.replace('T', 0, inplace = True)
# station_df[['snow']] = station_df[['snow']].astype(float)
# station_df['date'] = pd.to_datetime(station_df['date'])
# # station_df['tdepC'] = (station_df['tdep']) * 5 / 9 #convert F to Celsius

# # station_df['doy']=station_df['date'].dt.dayofyear





# station_df['date'] = pd.to_datetime(station_df['date'])
# station_df['WY'] = station_df.apply(lambda x: assign_wy(x), axis=1)
# station_df['yr'] = station_df.apply(lambda x: assign_yr(x), axis=1)


# station_df.to_csv('out.csv', index=False) 

station_df= pd.read_csv('out.csv') 


station_df['date'] = pd.to_datetime(station_df['date'])

station_df.snow = station_df.snow * 2.54


station_clim = station_df.loc[(station_df['yr'] >=1981) & (station_df['yr'] <=2010)]
station_clim.set_index('date', inplace=True)

grpMd= station_clim.groupby([station_clim.index.month, station_clim.index.day]).median()


climMedian=grpMd.set_index('WY')
climMedian.sort_index(ascending=True, inplace=True)

grpMean= station_clim.groupby([station_clim.index.month, station_clim.index.day]).mean()
climMean=grpMean.set_index('WY')
climMean.sort_index(ascending=True, inplace=True)


station = station_df.copy()
station.set_index('date', inplace=True)

grpMax= station.groupby([station.index.month, station.index.day]).max()
SnowMax=grpMax.set_index('WY')
SnowMax.sort_index(ascending=True, inplace=True)

grpMin= station.groupby([station.index.month, station.index.day]).min()
SnowMin=grpMin.set_index('WY')
SnowMin.sort_index(ascending=True, inplace=True)


# station= pd.pivot_table(station_df,index=station_df['WY'],columns=station_df['date'].dt.year)
station= pd.pivot_table(station_df,index=station_df['WY'],columns=station_df.yr)

station.columns = station.columns.get_level_values(1)




# # #### FIGURE #####

# fig, ax = plt.subplots(figsize=(12, 7))
fig= plt.figure(figsize=(8,5))
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
# camera = Camera(fig)

# x = station.index.values
x = pd.date_range('2019-07-01', '2020-06-30', freq = 'D')
Z = station.rolling(31, center=True).mean()

Z1 = station

ax.set_xlim(x[0],x[-1])
ax.set_ylim(0,160)
ax.set_ylabel('Snow depth (cm)')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))


# graph, = plt.plot([], [])
# graph,= plt.plot(x, Z.iloc[:, 1], color='blue', alpha=.3)# Z[1930])
graph,= ax.plot([], [], color='blue', alpha=.3, linewidth=2, label='Snow depth, 31 day running mean')# Z[1930])
graph2,= ax.plot([], [], color='blue', alpha=.3, linewidth=1, label='Snow depth')

# graph5 = ax.plot(x, climMax.snow, color='r', alpha=.3)
# graph3= ax.plot([], [], color='k', alpha=.3)
yearlbl= ax.annotate('', xy=(x[-40], 20), color='k')#, weight='bold')

graph3 = ax.plot(x, climMedian.snow, color='k', alpha=.3, label='1981-2010 Median')
graph4 = ax.plot(x, climMean.snow, color='g', alpha=.3, label='1981-2010 Mean')
graph5 = ax.plot(x, SnowMax.snow, color='r', alpha=.3, label='por Max')
# graph6 = ax.plot(x, SnowMin.snow, color='r', alpha=.3, label='por Min')
ax.legend(loc='upper left')
ax.set_title('FAI daily snow depth, July-June')

ax.annotate('data: ACIS', xy=(x[2], 2), color='k')

def animate(i):
	col=station.columns[i]
	graph.set_data(x, Z.iloc[:, i])
	graph2.set_data(x, Z1.iloc[:, i])

	yearlbl.set_text(col)#, weight='bold')

	return graph, graph2, yearlbl

ani = FuncAnimation(fig, animate, frames=len(station.columns), interval=300, blit=True)
plt.show()
# ani.save('snowFAI.mp4')

# plt.tight_layout()
# plt.show()
# animation.save('celluloid_legends.gif', writer = 'imagemagick')
	# print(col)
# ax.annotate("Alaska Climate Research Center\n Geophysical Institute UAF", xy=(1, 1), xytext=(-5, -380), fontsize=8,
#         xycoords='axes fraction', textcoords='offset points',
#         bbox=dict(facecolor='white', alpha=0.8),
#         horizontalalignment='right', verticalalignment='bottom')
# plt.xlim(1948, 2018)  


