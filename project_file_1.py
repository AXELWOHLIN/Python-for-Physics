#Project file for Axel Wohlin
#Latest edited 03/08-22

import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate


#Below I open the files and extract all the contents, I think there's a better way to open .csv files but I was more familiar with this
filenames = ["U5_U8_nubar.csv","U235_xs_cap.csv","U235_xs_nf.csv","U238_xs_cap.csv","U238_xs_nf.csv"]
filecontents = []
for file in filenames:
    temporary = open(file, "r")
    filecontent=temporary.read()
    temporary.close()
    filecontents.append(filecontent.strip().split())

nubar_U238=list(np.float_(filecontents[0][12::3]))
nubar_U235=list(np.float_(filecontents[0][11::3]))
energy1 = list(np.float_(filecontents[0][10::3]))

energy2 = list(np.float_(filecontents[1][7::2]))
u235_sigma_c = list(np.float_(filecontents[1][8::2]))
energy3 = list(np.float_(filecontents[2][7::2]))
u235_sigma_f = list(np.float_(filecontents[2][8::2]))

energy4 = list(np.float_(filecontents[3][7::2]))
u238_sigma_c = list(np.float_(filecontents[3][8::2]))

energy5 = list(np.float_(filecontents[4][7::2]))
u238_sigma_f = list(np.float_(filecontents[4][8::2]))

#Below I make a loglog plot of the fission cross section for both u235 and u238 to show how they compare for all energy levels
plt.figure()
plt.title('Fission Cross section depending on energy')
plt.xlabel('energy (ev)')
plt.ylabel('Cross section (Barn)')
plt.loglog(energy3,u235_sigma_f)
plt.loglog(energy5,u238_sigma_f)
plt.legend(['u235','u238'])
plt.savefig("sigma_f.jpg")

#Do the same thing for the capture cross section
plt.figure(2)
plt.title('Capture Cross section depending on energy')
plt.xlabel('energy (ev)')
plt.ylabel('Cross section (Barn)')
plt.loglog(energy2,u235_sigma_c)
plt.loglog(energy4,u238_sigma_c)
plt.legend(['u235','u238'])
plt.savefig("sigma_c.jpg")
plt.show()

#Below this point my code gets a bit messy because I was really having trouble with data types and dimensions not working
#so I basically made an interpolated function out of everything to ensure that it always worked and could easily be modified.
#I used scipy's interpolate function because I knew how it worked.
NU_238 = interpolate.interp1d(energy1, nubar_U238)
NU_235 = interpolate.interp1d(energy1, nubar_U235)

f_inter_u235f = interpolate.interp1d(energy2, u235_sigma_f)
f_inter_u238f = interpolate.interp1d(energy5, u238_sigma_f)
f_inter_u235c = interpolate.interp1d(energy2, u235_sigma_c)
f_inter_u238c = interpolate.interp1d(energy5, u238_sigma_c)

plt.figure()
plt.title('Reproduction Factor for enrichment')
plt.xlabel('energy (ev)')
plt.ylabel('Reproduction factor')

enrichment_levels = [0.007,0.01,0.02,0.03,0.05,0.1,0.3,0.5,0.7,1]

for enrichment in enrichment_levels:
    temp = (enrichment*f_inter_u235f(energy4)*NU_235(energy4) + (1 - enrichment)*f_inter_u238f(energy4)*NU_238(energy4))/\
        (enrichment*f_inter_u235c(energy4) + (1 - enrichment)*f_inter_u238c(energy4) + enrichment*f_inter_u235f(energy4) + (1 - enrichment)*f_inter_u238f(energy4))
    plt.loglog(energy4,temp)

plt.legend([andel for andel in enrichment_levels])
plt.savefig("repro_fac.jpg")
plt.show()

#Again I used a loglog plot and just made a new plot in the same figure for each enrichment level