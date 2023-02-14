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
WS=50.1   #WS is the Volume of water saved (usage) 
r=0.05 #r is the Discount rate
I=0.042 #r is the Inflation rate
PBP=20 #Payback period
WP=0.9 #WP is the  Current Water Price ($/kL)
NPVcost=1500 #Total water tank cost ($)
TC=0  #Tank cost
AC=0  #Accessories cost
OMC=0     #Operation and Maintenance cost
##################################################################
CER=0 #The cost-effectiveness ratio
pvc=0 #Present value of cost
FVwp=0 #The Future Value of water per kL after n years ($/kL)
FVeffect=0 #FVeffect is the Future Value of total water saved after n years ($)
NPVeffect=0  #NPVeffect is the Net present value of effectiveness (cost of total water saved after n years) ($)
FVwp=0 #FVwp is the Future Value of water per kL after n years ($/kL)
PP=0 #Payback period
LC=0 #levelized cost
########(#############Total Production####################################
FVwp=(WP)*(1+r)**n
FVeffect=FVwp*WS
mylst=[]
for i in range(1,n+1):
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
LC=(NPVcost)/ (WS*PBP)
print("Levelized cost of water tank:",LC,"$/kL")