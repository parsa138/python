######### Import the particular module of the pvlib library#######
import csv
from http import HTTPStatus
from datetime import datetime, timezone
import pytz
from pvlib import pvsystem
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pvlib
import psycopg2
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
        #connection.close()
        #print("PostgreSQL connection is closed")
################################# Variables######################
PvDataImport=2   # Add PV module data by column number 1, by name 2, and manualy 3
InverterDataImport=3   # Add Inverter data by column number 1, by name 2, and randomly 3
##################################################################
irrad = 1000  #e.g. 1000   
temp_cell =40 #e.g. 0040 
##################################################################
PvModuleName='United Renewable Energy Co. Ltd. FBK540M8G'                                            # You can choose a PV system from the dartabase and  related number of each row
InverterName='ABB: PVI-3.0-OUTD-S-US-A [240V]'
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
# 1st step: Estimating the parameters for the CEC single diode model
""" WARNING - This function relies on NREL's SAM tool. So PySAM, its Python API, needs to be installed 
in the same computer. Otherwise, you can expect the following error: 'ImportError if NREL-PySAM is not installed.'
"""
cec_fit_params = pvlib.ivtools.sdm.fit_cec_sam(module_data['Technology'], module_data['V_mp_ref'], module_data['I_mp_ref'],
                                  module_data['V_oc_ref'], module_data['I_sc_ref'], module_data['alpha_sc'],
                                  module_data['beta_oc'], module_data['gamma_r'], 
                                  module_data['N_s'], module_data['T_NOCT'])

# Let's have a look to the output
#print("i_l_ref,            i_o_ref,               r_s,                  r_sh_ref,              a_ref,               adjust")
#print(cec_fit_params)


# 2nd step: Apply model to estimate the 5 parameters of the single diode equation using the CEC model
diode_params = pvlib.pvsystem.calcparams_cec(irrad, temp_cell, module_data['alpha_sc'], cec_fit_params[4], 
                                            cec_fit_params[0], cec_fit_params[1], cec_fit_params[3], 
                                            cec_fit_params[2], cec_fit_params[5])

# The result of the function returns a Tuple of 5 parameters to be used in the single diode equation
#print('Number of elements returned: ', len(diode_params))
# Diod parameters:
#print(diode_params)
iv_values1 = pvlib.pvsystem.singlediode(diode_params[0], 
                                        diode_params[1], 
                                        diode_params[2], 
                                        diode_params[3], 
                                        diode_params[4], 
                                        ivcurve_pnts=25,   # Number of points of the I-V curve (equally distributed)
                                        method='lambertw') # I-V using the Lambert W. function

print(
    'i_sc:', iv_values1['i_sc'],
    'v_oc:', iv_values1['v_oc'],
    'i_mp:', iv_values1['i_mp'],
    'v_mp:', iv_values1['v_mp'],
    'p_mp:', iv_values1['p_mp']
    )
i_sc=float(iv_values1['i_sc'])
v_oc=float(iv_values1['v_oc'])
i_mp=float(iv_values1['i_mp'])
v_mp=float(iv_values1['v_mp'])
p_mp=float(iv_values1['p_mp'])
mpp_values1 = pvlib.pvsystem.max_power_point(diode_params[0], 
                                        diode_params[1], 
                                        diode_params[2], 
                                        diode_params[3], 
                                        diode_params[4], 
                                        d2mutau=0, NsVbi=np.Inf,
                                        method='brentq')
#print('mpp:', mpp_values1)

# Global plane-of-array effective irradiance between 200 and 1000 W/m2
g_poa_effective = irrad #np.random.uniform(low=200, high=1000, size=(80,))
# Mean cell temperature values between 10 and 50 degrees Celsius
#temp_cell = 60 #np.random.uniform(low=10, high=50, size=(80,)) 

# Definition of PV module characteristics:
pdc0 =module_data['STC'] #250 # STC power
gamma_pdc = module_data['gamma_r']/100 #-0.0045 # The temperature coefficient in units of 1/C

# Estimate DC power with PVWatts model
dc_power = pvlib.pvsystem.pvwatts_dc(g_poa_effective, temp_cell, pdc0, gamma_pdc, temp_ref=module_data['T_NOCT'])
print("dc_power:",iv_values1['p_mp'])

ac_power = pvlib.inverter.sandia(iv_values1['v_mp'], # DC voltage input to the inverter
                                 iv_values1['p_mp'], # DC power input to the inverter
                                 inverter_data) # Parameters for the inverter 
# Estimated Power Output
print("ac_power:",ac_power)
dt = datetime.now(pytz.timezone('Australia/Melbourne'))
#print(timezone.utc)

#tzinfo =pytz.timezone('Europe/Berlin')
#print(tzinfo)
date = dt.strftime("%m/%d/%Y")
time = dt.strftime("%H:%M:%S")
print(date)
print(time)
cursor = connection.cursor()
postgres_insert_query ="""INSERT INTO pvsys_ph (i_sc, v_oc, i_mp, v_mp, p_mp,ac_power,dc_power,date,time) VALUES(%s, %s, %s, %s, %s, %s, %s,%s,%s)"""
record_to_insert = (i_sc,v_oc,i_mp,v_mp,p_mp,float(ac_power),float(dc_power),date,time)
cursor.execute(postgres_insert_query,record_to_insert )
connection.commit() # <- We MUST commit to reflect the inserted data
count = cursor.rowcount
print(count, "Record inserted successfully into mobile table")
cursor.close()
connection.close()
print("PostgreSQL connection is closed")