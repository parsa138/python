from turtle import shapesize
from pvlib import pvsystem
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pvlib
#######################Databases###################################
# CEC Inverter Database
invdb = pd.read_excel('C:\SolarPanelsData\Inverters_database.xlsx').T
# CEC PV Module Database
cec_mod_db = pd.read_excel('C:\SolarPanelsData\PV_database.xlsx').T
##################################################################
irrad = 1000 #e.g. 1000   
temp_cell =40 #e.g. 0040 

##################################################################
PvModuleName='United Renewable Energy Co. Ltd. FBK540M8G'                                            # You can choose a PV system from the dartabase by name
InverterName='ABB: PVI-3.0-OUTD-S-US-A [240V]' 
#################Import data from database#########################
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
#print(cec_mod_db.keys())
# Example module parameters for the Canadian Solar CS5P-220M:
parameters = {
    'Name': 'Canadian Solar CS5P-220M',
    'BIPV': 'N',
    'Date': '10/5/2009',
    'T_NOCT': 42.4,
    'A_c': 1.7,
    'N_s': 100,
    'I_sc_ref': 20.1,
    'V_oc_ref': 80.4,
    'I_mp_ref': 18.69,
    'V_mp_ref': 100.9,
    'alpha_sc': 0.004539,
    'beta_oc': -0.22216,
    'a_ref': 2.6373,
    'I_L_ref': 20.114,
    'I_o_ref': 20.196e-10,
    'R_s': 1.065,
    'R_sh_ref': 381.68,
    'Adjust': 8.7,
    'gamma_r': -0.476,
    'Version': 'MM106',
    'PTC': 200.1,
    'Technology': 'Mono-c-Si',
}

cases = [
    (1000, 55), 
    
   
]

conditions = pd.DataFrame(cases, columns=['Geff', 'Tcell'])
conditions['Geff']=irrad
conditions['Tcell']=temp_cell
# adjust the reference parameters according to the operating
# conditions using the De Soto model:
IL, I0, Rs, Rsh, nNsVth = pvsystem.calcparams_desoto(
    conditions['Geff'],
    conditions['Tcell'],
    alpha_sc=module_data['alpha_sc'],
    a_ref=module_data['a_ref'],
    I_L_ref=module_data['I_L_ref'],
    I_o_ref=module_data['I_o_ref'],
    R_sh_ref=module_data['R_sh_ref'],
    R_s=module_data['R_s'],
    EgRef=1.121,
    dEgdT=-0.0002677
)

# plug the parameters into the SDE and solve for IV curves:
curve_info = pvsystem.singlediode(
    photocurrent=IL,
    saturation_current=I0,
    resistance_series=Rs,
    resistance_shunt=Rsh,
    nNsVth=nNsVth,
    ivcurve_pnts=100,
    method='lambertw'
)


print(pd.DataFrame({
    'i_sc': curve_info['i_sc'],
    'v_oc': curve_info['v_oc'],
    'i_mp': curve_info['i_mp'],
    'v_mp': curve_info['v_mp'],
    'p_mp': curve_info['p_mp'],
}))

# Global plane-of-array effective irradiance between 200 and 1000 W/m2
g_poa_effective = irrad #np.random.uniform(low=200, high=1000, size=(80,))
# Mean cell temperature values between 10 and 50 degrees Celsius
#temp_cell = 60 #np.random.uniform(low=10, high=50, size=(80,)) 

# Definition of PV module characteristics:
pdc0 =module_data['STC'] #250 # STC power
gamma_pdc = module_data['gamma_r']/100 #-0.0045 # The temperature coefficient in units of 1/C

# Estimate DC power with PVWatts model
dc_power = pvsystem.pvwatts_dc(g_poa_effective, temp_cell, pdc0, gamma_pdc, temp_ref=module_data['T_NOCT'])
print("dc_power:",curve_info['p_mp'])
ac_power = pvlib.inverter.sandia(curve_info['v_mp'], # DC voltage input to the inverter
                                 curve_info['p_mp'], # DC power input to the inverter
                                 inverter_data) # Parameters for the inverter 
# Estimated Power Output
print("ac_power:",ac_power)