
#! /usr/bin/env python3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
from matplotlib.colors import ListedColormap
from matplotlib.colors import TwoSlopeNorm

## get mass balance data from wgms website and plot as stripes, reference glaciers.
## example URL of WGMS .csv file: 'http://wgms.ch/data/min-data-series/FoG_MB_491.csv'
## Data at: https://wgms.ch/products_ref_glaciers/
 
# WGMS ID numbers of reference glaciers:
refgl_IDs = [90, 94, 76, 3334, 79, 205, 45, 57, 41, 39, 16, 3690, 0,
292, 291, 317, 298, 299, 300, 290, 2296, 302, 332, 334, 491, 507, 489,
394, 367, 359, 408, 354, 356, 357, 635, 726, 761, 817, 853, 1344]

#Collect data and put into dataframe
MB_df = pd.DataFrame(columns=refgl_IDs, index=range(1915, 2021))
glaciers = []
for wgmsid in refgl_IDs:
	data = pd.read_csv('http://wgms.ch/data/min-data-series/FoG_MB_'+str(wgmsid)+'.csv', sep= ';', header=13, encoding = "ISO-8859-1")  
	yr= data.REFERENCE_YEAR.values
	mb= data.ANNUAL_BALANCE.values

	# this does not work when csv files have missing years.
	# MB_df.loc[yr[0]:yr[-1], wgmsid] = mb

	# need loop because some have missing years.
	for i, yy in enumerate(yr):
		MB_df.loc[yy, wgmsid] = mb[i]

	# get glacier names and add to list
	glaciers.append(data.NAME.values[0])
	print('collected ', data.NAME.values[0])

# get mb range of all ref. glaciers
lim_pos= MB_df.max().max()
lim_neg= MB_df.min().min()

#set diverging color map and make norm so it is centered at zero.
cmap='RdBu'
divnorm = TwoSlopeNorm(vmin=lim_neg, vcenter=0, vmax=lim_pos)

# make figure/ subplots
fig, axs = plt.subplots(len(MB_df.columns), 1, figsize=(10, 10), sharex=True)
ax = axs.flatten()

for i, col in enumerate(MB_df.columns):
	ax[i].set_yticks([])
	dat = pd.to_numeric(MB_df[col].dropna())
	col = PatchCollection([
    	Rectangle((y, 0), 1, 1)
    	for y in range(dat.index.values[0], dat.index.values[-1] + 1)
	])
	col.set_array(dat.values)
	col.set_cmap(cmap)
	col.set_norm(divnorm)
	col.set_clim(lim_neg, lim_pos)
	cb= ax[i].add_collection(col)
	ax[i].set_ylim(0, 1)
	ax[i].set_xlim(1918,  2020)
	ax[i].annotate(glaciers[i],xy=(1920 ,0.2),xycoords='data')
	ax[i].set_facecolor('grey')

ax[-1].set_xlabel('REFERENCE_YEAR')
# add colorbar
fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.15, 0.02, 0.7])
cbar = fig.colorbar(cb, cax=cbar_ax)
# add title
ax[0].set_title('WGMS reference glaciers, annual mass balance (mm w.e.)')

plt.show()
fig.savefig('stripes_refglaciers.png')

