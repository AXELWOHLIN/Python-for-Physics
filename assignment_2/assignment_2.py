#Axel Wohlin's assignment 2

import numpy as np
import math
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import scipy.constants as const
from mpl_toolkits.mplot3d import Axes3D

#Since the proton has kinetic energy 1MeV we know E = mv^2/2
#So its velocity will be equal to sqrt(2E/m)


times = (0, 1)                                 
time_span = np.linspace(0, 1, 1000000)   
#Setup initial position and velocity vector. We use const.eV to get SI units                
XV = np.array([0.0, 0.0, 0.0, math.sqrt(1e6*const.electron_volt/const.proton_mass), 0.0 ,0.0])  


def PosVel_to_VelAcc(t, y):
    #F = q*V cross B and a = F/m, so we can find the acceleration now.
    z = np.zeros(6)           # Initialise the vector to return
    z[:3] = y[3:]             
    z[3:] = const.elementary_charge*np.cross(z[:3],np.array([0.0,0.0,3.0]))+np.array([0.0,9.81*const.proton_mass,0.0])
    return z 

results_1 = solve_ivp(PosVel_to_VelAcc, times, XV, t_eval=time_span, rtol=1e-10, atol=1e-10)

#I understood question 2 as them having total 1MeV kinetic energy so it's half in x and half in z dir.
XV_2 = np.array([0.0, 0.0, 0.0, 0.5*math.sqrt(1e6*const.electron_volt/const.proton_mass), 0.0 ,0.5*math.sqrt(1e6*const.electron_volt/const.proton_mass)])
results_2 = solve_ivp(PosVel_to_VelAcc, times, XV_2, t_eval=time_span, rtol=1e-10, atol=1e-10)

#Plots and save figures for report.

fig, axs = plt.subplots(1, 3)
axs[0].plot(results_1.t, results_1.y[0])
axs[0].set_title('X-axis 1')
axs[1].plot(results_1.t, results_1.y[1], 'tab:orange')
axs[1].set_title('Y-Axis 1')
axs[2].plot(results_1.t, results_1.y[2], 'tab:green')
axs[2].set_title('Z-Axis 1')
plt.savefig("assignment_2_fig_1.jpg")


fig2, axes = plt.subplots(1,3)
axes[0].plot(results_1.t, results_2.y[0], 'tab:red')
axes[0].set_title('X-Axis 2')
axes[1].plot(results_1.t, results_2.y[1], 'tab:red')
axes[1].set_title('Y-Axis 2')
axes[2].plot(results_1.t, results_2.y[2], 'tab:red')
axes[2].set_title('Z-Axis 2')
plt.savefig("assignment_2_fig_2.jpg")


fig3 = plt.figure(3)
plt.title("Question 3")
ax = fig3.add_subplot(projection='3d')
ax.plot3D(results_2.y[0], results_2.y[1], results_2.y[2], color='C0')
plt.savefig("assignment_2_fig_3.jpg")
plt.xlabel("x")
plt.ylabel("y")
plt.show()