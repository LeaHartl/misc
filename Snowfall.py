#! /usr/bin/env python3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from random import random, randrange
from matplotlib.animation import FuncAnimation




def koch_snowflake(order, scale=10):
    """
    Return two lists x, y of point coordinates of the Koch snowflake.

    Arguments
    ---------
    order : int
        The recursion depth.
    scale : float
        The extent of the snowflake (edge length of the base triangle).
    """
    def _koch_snowflake_complex(order):
        if order == 0:
            # initial triangle
            angles = np.array([0, 120, 240]) + 90
            return scale / np.sqrt(3) * np.exp(np.deg2rad(angles) * 1j)
        else:
            ZR = 0.5 - 0.5j * np.sqrt(3) / 3

            p1 = _koch_snowflake_complex(order - 1)  # start points
            p2 = np.roll(p1, shift=-1)  # end points
            dp = p2 - p1  # connection vectors

            new_points = np.empty(len(p1) * 4, dtype=np.complex128)
            new_points[::4] = p1
            new_points[1::4] = p1 + dp / 3
            new_points[2::4] = p1 + dp * ZR
            new_points[3::4] = p1 + dp / 3 * 2
            return new_points

    points = _koch_snowflake_complex(order)
    x, y = points.real, points.imag
    return x, y



# Create new Figure and an Axes which fills it.
fig = plt.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1], frameon=False)
ax.set_xlim(-15, 15), ax.set_xticks([])
ax.set_ylim(-15, 15), ax.set_yticks([])

x, y = koch_snowflake(order=3)

df = pd.DataFrame(columns=['sizefactor', 'shiftfactor'])
df.sizefactor = np.linspace(0, 1, 50)
df.shiftfactor = np.linspace(-15, 15, 50)


def makeSnowflakes(x,y,df):
	a =df.sizefactor.sample(n=1).values
	# b =df.shiftfactor.sample(n=1).values
	x1 = (x*a)+df.shiftfactor.sample(n=1).values
	y1 = (y*a)+df.shiftfactor.sample(n=1).values
	return(x1, y1)


ax.fill(x, y, color='blue', alpha=.1)




def update(frame_number):

	x1, y1 = makeSnowflakes(x,y,df)
	ax.fill(x1, y1,color='blue', alpha=.1)


# # Construct the animation, using the update function as the animation director.
animation = FuncAnimation(fig, update, interval=100, frames=100)#, repeat=False)
# plt.show()
animation.save('animation.gif', writer='imagemagick', fps=10)
