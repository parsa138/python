from turtle import shapesize
from pvlib import pvsystem
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pvlib
import math

######################VAriables#################################
irrad = 1000 #e.g. 1000   
temp_cell =40 #e.g. 0040 
#####################Variables to be filled up####################
n=25 #n is the Number of years of analysis
water_saving=50.1   #WS is the Volume of water saved (usage) 
I=0.042 #r is the Inflation rate
water_price=0.9 #WP is the  Current Water Price ($/kL)
Rebate=1000 #rebate amount for tank water
r=0.05 #r is the Discount rate
tank_cost=2000  #Tank cost
tank_size=5 #Tank size(kL)
accessory_cost=500+600+70  #Accessories cost
operation_maintanance=0     #Operation and Maintenance cost
##################################################################
CER=0 #The cost-effectiveness ratio
pvc=0 #Present value of cost
FVwp=0 #The Future Value of water per kL after n years ($/kL)
FVeffect=0 #FVeffect is the Future Value of total water saved after n years ($)
NPVeffect=0  #NPVeffect is the Net present value of effectiveness (cost of total water saved after n years) ($)
FVwp=0 #FVwp is the Future Value of water per kL after n years ($/kL)
PP=0 #Payback period
LC=0 #levelized cost
operation_maintanance= 0.5*5*n #Operation and Maintenance cost OMC=0.5xTank capacity (kL)x Analysis of life time (Year)
Tank_price=tank_cost+accessory_cost+operation_maintanance #Total water tank cost ($)
NPVcost=Tank_price-Rebate #Total water tank cost ($)
########(#############LC measurement####################################
FVwp=(water_price)*(1+r)**n
FVeffect=FVwp*water_saving
mylst=[]
for i in range(0,n+1):
     NPVeffect=((FVeffect)/(1+r)**i)
     mylst.append(NPVeffect)
     b=sum(mylst)
     CER=NPVcost/b
     PP=i
     if CER<=1: break
print(mylst)
print("Payback period is:",PP)
NPVeffect=b
print("NPVeffect:",NPVeffect)
LC=(NPVcost)/ (water_saving*PP)
print("Levelized cost of water tank:",LC,"$/kL")