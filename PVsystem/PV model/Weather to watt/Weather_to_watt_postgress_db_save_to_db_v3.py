######### Import the particular module of the pvlib library#######
from pickletools import float8
import string
from unicodedata import numeric
from pvlib import pvsystem
import numpy as np
from datetime import datetime, timezone
import pytz
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import pandas as pd
import pvlib
#import xlsxwriter
from pathlib import Path
import numpy as np
import psycopg2
################################# Variables######################
PvDataImport=2   # Add PV module data by column number 1, by name 2, and manualy 3
InverterDataImport=3   # Add Inverter data by column number 1, by name 2, and randomly 3
StartDate='20221001'  # Start date YYYYMMDD
EndDate='20221102'      #  End  date YYYYMMDD
# Coordinates of the weather station
latitude = -37.8576425
longitude = 145.1830722
altitude = 114
tilt=20
azimuth=140
##################################################################
irrad = 1000  #e.g. 1000   
temp_cell =40 #e.g. 0040 
##################################################################
##################################################################
dt = datetime.now(pytz.timezone('Australia/Melbourne'))
date = dt.strftime("%m/%d/%Y")
time = dt.strftime("%H:%M:%S")
print(date)
print(time)
#############################################################
#######################Databases###################################
try:
    connection = psycopg2.connect(user="postgresuser",
                                  password="postgresadmin741",
                                  host="192.168.0.17",
                                  port="5432",
                                  database="EDW-Database")
    cursor = connection.cursor()
    postgreSQL_select_Query = "select * from inverter"
    cursor.execute(postgreSQL_select_Query)
    print("Selecting rows from invdb table using cursor.fetchall")
    invdb = pd.DataFrame(cursor.fetchall())
    invdb.columns = ['Name','Vac','Pso','Paco','Pdco','Vdco','C0','C1','C2','C3','Pnt','Vdcmax','Idcmax','Mppt_low','Mppt_high','CEC_Date','CEC_hybrid']
    invdb=pd.DataFrame(invdb).T
#####################################################################
    cursor1 = connection.cursor()
    postgreSQL_select_Query1 = "select * from pvsystem"
    cursor.execute(postgreSQL_select_Query1)
    print("Selecting rows from invdb table using cursor.fetchall")
    cec_mod_db = pd.DataFrame(cursor.fetchall())
    cec_mod_db.columns = ['Number','Name','Manufacturer','Technology','Bifacial','STC','PTC','A_c','Length','Width','N_s','I_sc_ref','V_oc_ref','I_mp_ref','V_mp_ref','alpha_sc','beta_oc','T_NOCT','a_ref','I_L_ref','I_o_ref','R_s','R_sh_ref','Adjust','gamma_r','BIPV','Version','Date']
    cec_mod_db=pd.DataFrame(cec_mod_db).T
    #print("Postgress",invdb)
finally:
    # closing database connection.
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

#######################Databases###################################
# CEC Inverter Database
#invdb = pd.read_excel('C:\SolarPanelsData\Inverters_database.xlsx').T
# CEC PV Module Database
#cec_mod_db = pd.read_excel('C:\SolarPanelsData\PV_database.xlsx').T
##################################################################
PvModuleName='Centrosolar America DM72 295'                                         # You can choose a PV system from the dartabase and  related number of each row
InverterName='ABB: PVI-6000-OUTD-US-Z-M-A [277V]                                                                                       '
#######################Path#######################################
AC_Power = Path('C:\WeatherToPower\AC power.csv')  
AC_Power.parent.mkdir(parents=True, exist_ok=True) 
DC_Power = Path('C:\WeatherToPower\DC power.csv')  
DC_Power.parent.mkdir(parents=True, exist_ok=True) 
Weather = Path('C:\WeatherToPower\Weather.csv')  
Weather.parent.mkdir(parents=True, exist_ok=True)
Solar_Position = Path('C:\WeatherToPower\Solar Position.csv')  
Solar_Position.parent.mkdir(parents=True, exist_ok=True)
Irradiance = Path('C:\WeatherToPower\Irradiance.csv')  
Irradiance.parent.mkdir(parents=True, exist_ok=True)
#############################Main PV##############################
pv_number=3
inv_number=3
# print (cec_mod_db.loc['Name']==PvModuleName)
# print (len(cec_mod_db.T))
for index in range(len(cec_mod_db.T)): 
                if cec_mod_db.iloc[1,index]==PvModuleName:
                    pv_number=index
# print (pv_number)
module_data = cec_mod_db.iloc[:,pv_number]
print (module_data)
#inverter_number=(invdb.columns.get_loc(InverterName))
#inverter_data = invdb.iloc[:, inverter_number]
for index in range(len(invdb.T)): 
                if invdb.iloc[0,index]==InverterName:
                    inv_number=index
print (inv_number)
inverter_data = invdb.iloc[:,inv_number]
print (inverter_data)
print (cec_mod_db.iloc[3, pv_number])
TypeCellFind=cec_mod_db.iloc[3, pv_number]
if TypeCellFind.find("mono"):
             Typecell="mono"
elif TypeCellFind.find("multi"):
             Typecell="multi"
elif TypeCellFind.find("poly"):
             Typecell="poly"
elif TypeCellFind.find("cis"):
             Typecell="cis"
elif TypeCellFind.find("cigs"):
             Typecell="cigs"
elif TypeCellFind.find("cdte"):
             Typecell="cdte"
elif TypeCellFind.find("amorphous"):
             Typecell="amorphous"
module_data['Technology']=(Typecell)

#########################################################################################
# # Read the weather data from the MIDC station using the I/O tools available within pvlib
df_weather = pvlib.iotools.read_midc_raw_data_from_nrel('UOSMRL',               # Station id
                                                     pd.Timestamp(StartDate),   # Start date YYYYMMDD
                                                     pd.Timestamp(EndDate))   # End date  YYYYMMDD
# # Head, shape and columns of the data
# print(df_weather.head(3))
# print(df_weather.shape)
# Subset variables needed
df_weather = df_weather[['Global CMP22 [W/m^2]', 'Diffuse Schenk [W/m^2]', 
                         'Direct CHP1 [W/m^2]','Air Temperature [deg C]', 'Avg Wind Speed @ 10m [m/s]']]
# Rename the columns
df_weather.columns = ['ghi', 'dhi', 'dni', 'temp_air', 'wind_speed']

# See the first columns of our weather dataset
print(df_weather.head(3))

# Define the location object
location = pvlib.location.Location(latitude, longitude, altitude=altitude)

# Define Temperature Paremeters 
temperature_model_parameters = pvlib.temperature.TEMPERATURE_MODEL_PARAMETERS['sapm']['open_rack_glass_glass']

# # Define the PV Module and the Inverter from the CEC databases (For example, the first entry of the databases)
# module_data = cec_mod_db.iloc[:,0]

# Define the basics of the class PVSystem
system = pvlib.pvsystem.PVSystem(surface_tilt=tilt, surface_azimuth=azimuth,
                                 module_parameters=module_data,
                                 inverter_parameters=inverter_data,
                                 temperature_model_parameters=temperature_model_parameters)

# Creation of the ModelChain object
""" The example does not consider AOI losses nor irradiance spectral losses"""
mc = pvlib.modelchain.ModelChain(system, location, 
                                 aoi_model='no_loss', 
                                 spectral_model='no_loss',
                                 name='AssessingSolar_PV')

# Have a look to the ModelChain
print('Results')
print(mc.results)
mc.run_model(df_weather) 
wth=pd.DataFrame(mc.results.weather)
sp=pd.DataFrame(mc.results.solar_position)
irr=pd.DataFrame(mc.results.total_irrad)
dcp=pd.DataFrame(mc.results.dc)
acp=pd.DataFrame(mc.results.ac)
tp=pd.DataFrame(mc.results.times)

acps=[]
dcps=[]
wths=[]
wths1=[]
wths2=[]
wths3=[]
wths4=[]
wths5=[]
wths6=[]
wths7=[]
sps1=[]
sps2=[]
sps3=[]
sps4=[]
sps5=[]
sps6=[]
irrs=[]
tps=[]
arr=[]
col=[]
# print(arr)
# con = np.concatenate((acp, tp), axis=1)
# con = np.concatenate((con, dcp), axis=1)
# con = np.concatenate((con, wth), axis=1)
# con = np.concatenate((con, irr), axis=1)
# con = np.concatenate((con, sp), axis=1)
# print(con)
#query_ready=pd.DataFrame()
#query_ready.columns =['ac','dc','ir','sp','wth','t']
#for i in range(len(acp)):

# for index in range(6):
#         [col.append(str(acp.iloc[index,0]))]
#         [col.append(str(dcp.iloc[index,0]))]
#for i in range(len(acp)):
for index in range(len(acp)):
   
    acps.append(str(acp.iloc[index,0]))
    tps.append(str(tp.iloc[index,0]))
    dcps.append(str(dcp.iloc[index,0]))
    wths.append(str(wth.iloc[index,0]))
    wths1.append(str(wth.iloc[index,1]))
    wths2.append(str(wth.iloc[index,2]))
    wths3.append(str(wth.iloc[index,3]))
    wths4.append(str(wth.iloc[index,4]))
    wths5.append(str(tp.iloc[index,0]))
    wths6.append(str(date))
    wths7.append(str(time))
    sps1.append(str(sp.iloc[index,1]))
    sps2.append(str(sp.iloc[index,2]))
    sps3.append(str(sp.iloc[index,3]))
    sps4.append(str(sp.iloc[index,4]))
    sps5.append(str(sp.iloc[index,5]))
    sps6.append(str(sp.iloc[index,1]))
    irrs.append(str(irr.iloc[index,0]))
# con = np.concatenate((acps, tps), axis=1)
# con = np.concatenate((con, dcps), axis=1)
# con = np.concatenate((con, wths), axis=1)
# con = np.concatenate((con, wths1), axis=1)
# con = np.concatenate((con, wths2), axis=1)
# con = np.concatenate((con, wths3), axis=1)
# con = np.concatenate((con, wths4), axis=1)
# con = np.concatenate((con, irr), axis=1)
# con = np.concatenate((con, sp), axis=1)
# print(con)

dcps=pd.DataFrame(dcps,dtype=str)
dcps=np.array(dcps,dtype=str)
acps=pd.DataFrame(acps,dtype=str)
acps=np.array(acps,dtype=str)
wths=pd.DataFrame(wths,dtype=str)
wths=np.array(wths,dtype=str)
wths1=pd.DataFrame(wths1,dtype=str)
wths1=np.array(wths1,dtype=str)
wths2=pd.DataFrame(wths2,dtype=str)
wths2=np.array(wths2,dtype=str)
wths3=pd.DataFrame(wths3,dtype=str)
wths3=np.array(wths3,dtype=str)
wths4=pd.DataFrame(wths4,dtype=str)
wths4=np.array(wths4,dtype=str)
wths5=pd.DataFrame(wths5,dtype=str)
wths5=np.array(wths5,dtype=str)
wths6=pd.DataFrame(wths6,dtype=str)
wths6=np.array(wths6,dtype=str)
wths7=pd.DataFrame(wths7,dtype=str)
wths7=np.array(wths7,dtype=str)
sps1=pd.DataFrame(sps1,dtype=str)
sps1=np.array(sps1,dtype=str)
sps2=pd.DataFrame(sps2,dtype=str)
sps2=np.array(sps2,dtype=str)
sps3=pd.DataFrame(sps3,dtype=str)
sps3=np.array(sps3,dtype=str)
sps4=pd.DataFrame(sps4,dtype=str)
sps4=np.array(sps4,dtype=str)
sps5=pd.DataFrame(sps5,dtype=str)
sps5=np.array(sps5,dtype=str)
sps6=pd.DataFrame(sps6,dtype=str)
sps6=np.array(sps6,dtype=str)
irrs=pd.DataFrame(irrs,dtype=str)
irrs=np.array(irrs,dtype=str)
tps=pd.DataFrame(tps,dtype=str)
tps=np.array(tps,dtype=str)
wthf=np.vstack((wths.T, wths1.T))
wthf=np.vstack((wthf, wths2.T))
wthf=np.vstack((wthf, wths3.T))
wthf=np.vstack((wthf, wths4.T))
wthf=np.vstack((wthf, wths5.T))
wthf=np.vstack((wthf, wths6.T))
wthf=np.vstack((wthf, wths7.T))
spsf=np.vstack((sps1.T, sps2.T))
spsf=np.vstack((spsf, sps3.T))
spsf=np.vstack((spsf, sps4.T))
spsf=np.vstack((spsf, sps5.T))
spsf=np.vstack((spsf, sps6.T))
spsf=np.vstack((spsf, tps.T))
spsf=np.vstack((spsf, wths6.T))
spsf=np.vstack((spsf, wths7.T))
print ("weather",wthf.T)
print ("solar position",spsf.T)

# acp.to_csv(AC_Power)
# dcp.to_csv(DC_Power)
# irr.to_csv(Irradiance)
# sp.to_csv(Solar_Position)
# wth.to_csv(Weather)

con2=np.vstack((dcps.T, acps.T))
con2=np.vstack((con2, irrs.T))
con2=np.vstack((con2, tps.T))
con2=np.vstack((con2, wths6.T))
con2=np.vstack((con2, wths7.T))
print ("concatinate",con2.T)

fig, ax = plt.subplots(figsize=(7, 3))

mc.results.dc['p_mp'].plot(label='DC power')
ax = mc.results.ac.plot(label='AC power')
#ax.xaxis.set_major_formatter(DateFormatter("%H:%M"))
ax.set_ylabel('Power [W]')
ax.set_xlabel('UTC Time [HH:MM]')
ax.set_title('Power Output of PV System')
plt.legend()
plt.tight_layout()
plt.show() 


def bulkInsert(record1,record2,record3):
    try:
        connection = psycopg2.connect(user="postgresuser",
                                      password="postgresadmin741",
                                      host="192.168.0.17",
                                      port="5432",
                                      database="EDW-Database")
        cursor = connection.cursor()
        sql_insert_query1 = """ INSERT INTO ac (ac_power, dc_power, irradiance, time, date, utime) VALUES (%s,%s,%s,%s,%s,%s)"""
       # executemany() to insert multiple rows
        result = cursor.executemany(sql_insert_query1, record1)
        connection.commit()
        print(cursor.rowcount, "data inserted successfully into ac table")
        sql_insert_query2 = """ INSERT INTO weather (ghi, dhi, dni, windspeed, temp, time, date, utime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
        sql_insert_query3 = """ INSERT INTO solar_position (app_zenith, zenith, app_elevation, elevation, azimuth, eq_time, time, date, utime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        # executemany() to insert multiple rows
        result = cursor.executemany(sql_insert_query2, record2)
        connection.commit()
        print(cursor.rowcount, "data inserted successfully into weather table")
        result = cursor.executemany(sql_insert_query3, record3)
        connection.commit()
        print(cursor.rowcount, "data inserted successfully into solar position table")
    except (Exception, psycopg2.Error) as error:
        print("Failed inserting record into all tables {}".format(error))

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

#records_to_insert = [(['1'], ['LG']), (['One Plus 6'], ['950']),(['One Plus 6'], ['950'])]
bulkInsert(con2.T,wthf.T,spsf.T)
#bulkInsert(acps,dcps,wths,sps,irrs,tps)
