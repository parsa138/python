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
system_size=100 #System Size (kW-DC) 
first_year_production=145000      #1st-Year Production (kWh)
annual_degradation=0.5  #Annual Degradation in (%)
system_cost= 3.5 # SystemCost ($/W)  System_Cost ($/W) = (Total-system-cost/Total-system-size-in-watts)
initial_rebate=35000 #Initial Rebate/Incentive
om_cost=15   #O&M Cost ($/kW) O&M Cost ($/kW) = (1st-year-O&M-Cost/Total-system-size-in-kW)
lifetime=25  # 20 or 25 years of lifetime of the PV system
##################################################################
om_cost_yearly=[0]*26 #O&M Cost ($) yearly
om_escalator=3 #(%) #O&M Escalator (%)
total_om_cost=0 #total O&M over a lifetime
production=[0]*26   #Production (kWh)
total_production_inlifetime=0 #total production over lifetime
direct_cost=0  #Direct Purchase Cost ($)
total_cost=0
LCOE=0 #LCOE
#####################Total Production####################################
production[0]=0
production[1]=first_year_production
total_production_inlifetime=first_year_production
for i in range(2, lifetime+1):
    production[i]=production[i-1]*(1-(annual_degradation/100))
    total_production_inlifetime=(total_production_inlifetime+production[i])
    #print(production[i])
total_production_inlifetime=round(total_production_inlifetime)
#print(total_production_inlifetime)
#########################Yearly Maintanance fee#####################################
#direct_cost=system_cost*system_size
om_cost_yearly[0]=0
om_cost_yearly[1]=om_cost*system_size
total_om_cost=om_cost*system_size
for i in range(2, lifetime+1):
    om_cost_yearly[i]=om_cost_yearly[i-1]*(1+(om_escalator)/100)
    total_om_cost=(total_om_cost+om_cost_yearly[i])
    #print(om_cost_yearly[i])
total_om_cost=round(total_om_cost)
#print(total_om_cost)
############################System cost##############################################
direct_cost=(system_cost*system_size*1000)-initial_rebate
total_cost=direct_cost+total_om_cost
################################LCOE#################################################
LCOE=round(total_cost/total_production_inlifetime,5)
print('LCOE is:',LCOE)