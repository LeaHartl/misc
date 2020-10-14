
#! /usr/bin/env python3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
from matplotlib.colors import ListedColormap
from matplotlib.colors import TwoSlopeNorm

## adapted from: https://matplotlib.org/matplotblog/posts/warming-stripes/
## get mass balance data from wgms website and plot as stripes, individual glacier.
## example URL of WGMS .csv file: 'http://wgms.ch/data/min-data-series/FoG_MB_491.csv'

# set ID number for the desired glacier
ID = 491

# get data
data = pd.read_csv('http://wgms.ch/data/min-data-series/FoG_MB_'+str(ID)+'.csv', sep= ';', header=13, encoding = "ISO-8859-1")  
yr= data.REFERENCE_YEAR.values
mb= data.ANNUAL_BALANCE.values
glcName = data.NAME.values[0]
print('collecting data:', data.NAME.values[0])

# get mb range
lim_pos= mb.max()
lim_neg= mb.min()

#set diverging color map and make norm so it is centered at zero.
cmap='RdBu'
divnorm = TwoSlopeNorm(vmin=lim_neg, vcenter=0, vmax=lim_pos)


# make figure
fig, ax = plt.subplots(1, 1, figsize=(10, 4))
ax.set_yticks([])
col = PatchCollection([
    Rectangle((y, 0), 1, 1)
    for y in range(yr[0], yr[-1] + 1)
	])
col.set_array(mb)
col.set_cmap(cmap)
col.set_norm(divnorm)
col.set_clim(lim_neg, lim_pos)
cb = ax.add_collection(col)
ax.set_ylim(0, 1)
ax.set_xlim(yr[0], yr[-1])
ax.set_title(glcName)

cbar = fig.colorbar(cb)
cbar.set_label('Annual mass balance (mm w.e.)', rotation=90)
plt.show()

fig.savefig(glcName+'_stripes.png')