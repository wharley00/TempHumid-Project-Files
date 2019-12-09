# python_code.py

## Authors: Students

## Last Revision: 12/4/2019

## This code is used to read data from an arduino Temperature and Humidity sensor, then upload that data to a thingspeal account.
## Then the data is called from that account and plotted.



# Imports
import serial
import time
import numpy as np
import pandas as pd
import requests
import matplotlib.pyplot as plt
%matplotlib inline



# opens the serial connection with arduino
ser = serial.Serial('COM3', 9600)
time.sleep(1)

# create empty lists to append data to
data_hum=[]
data_temp=[]

# ask the user for how many data points they would like
data_str = input('How many data points would you like?: ')
data_int = int(data_str)

# ask the user how long they would like to record data for
time_str = input('How many seconds would you like to collect data for?:')
time_int = int(time_str)

# calculate appropriate interval over the user's desired time based on the number of data points
time_interval = time_int/data_int

# Read data from serial output
for i in range(data_int):
    b = ser.readline()          # read a byte string line from Arduino's serial output
    b_string = b.decode()       # decode byte string into regular Python string
    string = b_string.rstrip()  # strip r/n/
    hum = string[0:5]           # index out humidity data         
    temp = string[6:]           # index out temperature data
    data_hum.append(hum)        # append humidity data to list
    data_temp.append(temp)      # append temperature data to list
    time.sleep(time_interval)   # pause appropriate interval before next loop
    
ser.close()    # close the serial connection with arduino

# print the lists to verify data before upload
print(data_hum)
print(data_temp)




### failsafe if decoding error occurs. Run "ser.close()" then re-run prior cell
ser.close()




# upload temperature data to thingspeak
for i in range(data_int):
    base_url = "https://api.thingspeak.com/update?api_key="
    api_key = "XXXXXXXXXXXXXXXX"
    
    temp_mid_url_2 ='&field1='                                    # temperature field number
    temp_index = data_temp[i]                                     # index out the appropriate data based on iteration of loop
    
    temp_url = base_url + api_key + temp_mid_url_2 + temp_index   # create url with data point

    r_temp  = requests.get(temp_url)                              # upload data point to thingspeak
    
    time.sleep(15)                                                # pause to account for thingspeak upload rate
    
# upload humidity data to thingspeak
for i in range(data_int):
    base_url = "https://api.thingspeak.com/update?api_key="
    api_key = "XXXXXXXXXXXXXXXX"
    
    hum_mid_url_1 ='&field1='                                     # humidity field number
    hum_index = data_hum[i]                                       # index out the appropriate data based on iteration of loop
    
    hum_url = base_url + api_key + hum_mid_url_1 + hum_index      # create url with data point
    
    r_hum = requests.get(hum_url)                                 # upload data point to thingspeak
    
    time.sleep(15)                                                # pause to account for thingspeak upload rate

    
    
    
# ask user many data points they would like
n_str = input('How many data points would you like?: ')

# create URL for Humidity
base_url = 'https://api.thingspeak.com/channels/'

hum_channel_num = '908572'
temp_channel_num = '928892'

mid_url = '/fields/'
end_url = '.csv?results='

hum_field_num = '1'                                                                        # appropriate field number for humidity
temp_field_num = '1'                                                                       # appropriate field number for temp.

results_num = n_str                                                                        # number of datapoints, saved as a string

hum_url = base_url + hum_channel_num + mid_url + hum_field_num + end_url + results_num     # create url for humidity
temp_url = base_url + temp_channel_num + mid_url + temp_field_num + end_url + results_num  # create url for temperature

# print urls
print(f'The Temperature url is {temp_url}')
print(f'The Humidity url is {hum_url}')

# use pandas to read data from thingspeak
r_hum = pd.read_csv(hum_url)
r_temp = pd.read_csv(temp_url)

# clean data and display array
r_hum_array = np.array(r_hum)
r_hum_array_clean = r_hum_array[:,-1:-2:-1]

r_temp_array = np.array(r_temp)
r_temp_array_clean = r_temp_array[:,-1:-2:-1]



# creates a list of x-axis values that represents the time at each point based on user input
x = []
for i in range(0, time_int,time_interval):
    x.append(i)

# plot Humidity with customizations
fig, ax = plt.subplots()

ax.plot(x, r_hum_array_clean,'r',linewidth=1)

ax.set_xlabel('Time (seconds)')

ax.set_ylabel('Humidity(%)')

ax.set_title('Humidity in a Closed System')

plt.show()


# plot Temperature with customizations
fig, ax = plt.subplots()

ax.plot(x,r_temp_array_clean,'r',linewidth=1)

ax.set_xlabel('Time (seconds)')

ax.set_ylabel('Temperature (C)')

ax.set_title('Temperature in a Closed System')

plt.show()
