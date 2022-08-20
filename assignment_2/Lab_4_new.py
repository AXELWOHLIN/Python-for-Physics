# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 19:48:50 2022

Solving differential equations using scipy.integrate.solve_ivp

@author: matthias
"""

import numpy as np
import math
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import scipy.constants as const


# Get the times and initial values
times = (0, 10)                                 # Time range
ttt = np.linspace(0, 10, 100)                   # Time evaluation points
XV = np.array([0.0, 0.0, 0.0, 0.5, 0.0 ,20.])   # Initial values of X and V
drag = -0.02                                    # make up a drag coefficient



def f_ballistic(t, y):
    """
    Function for use in the ODE solver
    Input: Time span; Initial state
    t: Interval of the integration
    y: x, y, z, v_x, v_y, v_z
    Output: Derivatives of the input: velocites and accelerations
            dy/dt, i.e. v_x, v_y, v_z, a_x, a_y, a_z
    This is for an object moving in a gravity field
    """
    z = np.zeros(6)           # Initialise the vector to return
    z[:3] = y[3:]             # dr/dt = velocity vector
    z[5] = -const.g           # Apply gravity downwards in z
    return z 
    


def f_ballistic_drag_1(t, y):
    """
    Function for use in the ODE solver
    Input and output as above
    This is for an object moving in a gravity field with drag
    Drag proportional to the velocity
    """
    z = np.zeros(6)           # Initialise the vector to return
    z[:3] = y[3:]             # dr/dt = velocity vector
    z[3:] = y[3:]*drag        # Apply drag component-wise on velocity
    z[5] = z[5]-const.g       # Apply gravity down  
    return z 



def f_ballistic_drag_1_v2(t, y):
    """
    Function for use in the ODE solver
    The same as f_ballistic_drag_1, but introducing speed
    """
    z = np.zeros(6)                 # Initialise the vector to return
    s = np.linalg.norm(y[3:])       # Particle speed
    ds = s * drag                   # Drag proportional to speed
    z[:3] = y[3:]                   # dr/dt = velocity vector
    z[3:] = y[3:]/s * ds            # Apply drag on velocity
                                    # Velocity unit vector times acceleration
    z[5] = z[5]-const.g             # Apply gravity down  
    return z 


def f_ballistic_drag_2(t, y):
    """
    Function for use in the ODE solver
    This is for an object moving in a gravity field with drag 
    Drag proportional to the speed squared
    """
    z = np.zeros(6)                 # Initialise the vector to return
    s = np.linalg.norm(y[3:])       # Particle speed
    ds = s*s * drag                 # Drag proportional to speed squared
    z[:3] = y[3:]                   # dr/dt = velocity vector
    z[3:] = y[3:]/s * ds            # Apply drag on velocity
    z[5] = z[5]-const.g             # Apply gravity down  
    return z 

# Prepare the figure, two subplots (one row, two columns)
fig = plt.plot()
(ax1, ax2) = plt.subplots(1, 2, figsize=(12,5))
fig.suptitle('Trajectories of objects with 1 g downwards, with and without drag, drag coefficient = '+str(drag))

# %%
# No drag
# The t_eval is needed to get a decent resolution.
# The t_eval linspace must be within the time range!
# rtol and atol for higher precision are not required here, the default values are good enough
no_drag = solve_ivp(f_ballistic, times, XV, t_eval=ttt, rtol=1e-10, atol=1e-10)
# Plot height against x-position
ax1.plot(no_drag.y[0], no_drag.y[2], label = 'no drag')
# Plot the z-velocity against time
ax2.plot(no_drag.t, no_drag.y[5], label = 'no drag')

# With linear drag, first function
with_drag_1 = solve_ivp(f_ballistic_drag_1, times, XV, t_eval=ttt)
ax1.plot(with_drag_1.y[0], with_drag_1.y[2], label = 'with linear drag, v1')
ax2.plot(with_drag_1.t, with_drag_1.y[5], label = 'with linear drag, v1')

# %%

# Alternatively, the second function
# The plot will be exactly the same as the one from the first function.
# Dashed-dotted lines make both versions visible.
with_drag_1_v2 = solve_ivp(f_ballistic_drag_1_v2, times, XV, t_eval=ttt)
ax1.plot(with_drag_1_v2.y[0], with_drag_1_v2.y[2], '-.', label = 'with linear drag, v2')
ax2.plot(with_drag_1_v2.t, with_drag_1_v2.y[5], '-.', label = 'with linear drag, v2')


# With quadratic drag
with_drag_2 = solve_ivp(f_ballistic_drag_2, times, XV, t_eval=ttt)
ax1.plot(with_drag_2.y[0], with_drag_2.y[2], label = 'with quadratic drag')
ax2.plot(with_drag_2.t, with_drag_2.y[5], label = 'with quadratic drag')


# Finalize the plotting
ax1.set_xlabel('x (m)')
ax1.set_ylabel('z (m)')
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Velocity in z-direction (m/s)')
ax1.legend()
ax2.legend()

fig.show()
