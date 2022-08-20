import numpy as np
import matplotlib.pyplot as plt
### QUESTION 1 ###

#Loading the file with datatype int, as that is what is in the .csv file
pulses = np.loadtxt("pulses.csv", dtype=int, delimiter=",")
print(pulses)

### QUESTION 2 ###

#Using the conversion formula given in the assignment to get the values in V
pulses_volts = pulses/((2**10 - 1) * 0.6)
print(pulses_volts)

###QUESTION 3####

#I use np.linspace along with number of elements and time between measurements to create a time span for plot
time_span = np.linspace(0,56*1e-9,56)
plot1 = plt.figure(1)
plt.plot(time_span, pulses_volts[0,1:],) #We don't want to plot the first value of each row since it isnt the same as the other measurements
plt.ylabel("Volts")
plt.xlabel("time")
plt.title("Pulse without noise correction")
plt.savefig("pulses_picture.jpg")
#plt.show()

###QUESTION 4,5,6###
elements_in_mean = int(input("Please enter the nr. of elements for calculating the noise: ")) #Using input command it is intuitive what this variable represent
cum_min = np.zeros(1000) #More efficient operations by creating an empty np matrix of set dimensions than altering it for each append
cum_max = np.zeros(1000)
cum_sum = np.zeros(1000)

pulses_volts.astype('float64') #We need to convert to float otherwise we get conflicting data types with the "noise" variable
i = 0 #By using an indexing variable we can easily reach our min, max and sum matrixes
for row in pulses_volts:
    noise = sum(row[1:elements_in_mean - 1])/elements_in_mean
    row[1:] -= noise 
    cum_min[i] = np.min(row[1:])
    cum_sum[i] = sum(row[1:])
    cum_max[i] = np.max(row[1:])
    i += 1

plot2 = plt.figure(2)
plt.plot(time_span, pulses_volts[0,1:]) #By using the 0th row we plot the noise-corrected pulse of our first figure
plt.ylabel("Volts")
plt.xlabel("time")
plt.title("Pulse with noise correction")
plt.savefig("pulses_picture_2.jpg")
#plt.show()

plot3 = plt.figure(3)
plt.hist(cum_min,range = (-5.5,1.5)) #These ranges were observed manually using a debugger to make the hists looks nicer
plt.title("Minimum value histogram")
plt.savefig("cum_min.jpg")
plot4 = plt.figure(4)
plt.hist(cum_sum,range = (-151,85))
plt.title("Cumulative value histogram")
plt.savefig("cum_sum.jpg")
plot5 = plt.figure(5)
plt.hist(cum_max,range = (0.5,2))
plt.title("Maximum value histogram")
plt.savefig("cum_max.jpg")
plt.show()