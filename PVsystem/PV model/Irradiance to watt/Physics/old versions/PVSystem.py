######### Import the particular module of the pvlib library#######
from pvlib import pvsystem
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pvlib
#######################Databases###################################
# CEC Inverter Database
invdb = pvsystem.retrieve_sam('CECInverter')
# CEC PV Module Database
cec_mod_db = pvsystem.retrieve_sam('CECmod')
################################# Variables######################
# Add PV module data by column number 1, by name 2, and manualy 3
PvDataImport=2
irrad = 1000 #np.array([1000])   # Effective irradiance values (W/m2) #E.g. irrad = np.array([200,400,600,800,1000])
temp_cell =40 #np.array([ 40]) # Average cell temperature (degrees Celsius) #E.g. temp_cell = np.array([40, 40, 40, 40, 40])
#############################Main PV##############################
# You can choose a PV system from the dartabase and  related number of each row
pv_name=11411
if (PvDataImport==2):
    pv_name=(cec_mod_db.columns.get_loc('Solartech_Energy_ASC_6P_54_205'))
if  ((PvDataImport==2) or (PvDataImport==1)):
        #print(pv_name)
        # Size of the database
        #print(cec_mod_db.shape)
        #print(cec_mod_db.iloc[:, pv_name])
        # PV module data from a typical datasheet (e.g. Kyocera Solar KD225GX LPB)
        TypeCellFind=cec_mod_db.iloc[0, pv_name]
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
        module_data = {'Name':list(cec_mod_db.keys())[pv_name],
               'celltype': (Typecell), # technology  s.replace('ab', ''
               'STC': (cec_mod_db.iloc[2, pv_name]), # STC power
               'PTC': (cec_mod_db.iloc[3, pv_name]), # PTC power
               'v_mp': (cec_mod_db.iloc[11, pv_name]), # Maximum power voltage
               'i_mp': (cec_mod_db.iloc[10, pv_name]), # Maximum power current
               'v_oc': (cec_mod_db.iloc[9, pv_name]), # Open-circuit voltage
               'i_sc': (cec_mod_db.iloc[8, pv_name]), # Short-circuit current
               'alpha_sc': (cec_mod_db.iloc[12, pv_name]), # Temperature Coeff. Short Circuit Current [A/C]
               'beta_voc': (cec_mod_db.iloc[13, pv_name]), # Temperature Coeff. Open Circuit Voltage [V/C]
               'gamma_pmp': (cec_mod_db.iloc[21, pv_name]), # Temperature coefficient of power at maximum point [%/C]
               'cells_in_series': (cec_mod_db.iloc[7, pv_name]), # Number of cells in series
               'temp_ref': (cec_mod_db.iloc[14, pv_name])}  # Reference temperature conditions
else:
    # PV module data from a typical datasheet (e.g. Kyocera Solar KD225GX LPB)
    module_data = {'celltype': 'multicSi', # technology
               'STC': 270.643, # STC power
               'PTC': 242.1, # PTC power
               'v_mp': 30.72, # Maximum power voltage
               'i_mp': 8.81, # Maximum power current
               'v_oc': 38.63, # Open-circuit voltage
               'i_sc': 9.34, # Short-circuit current
               'alpha_sc': 0.00486614, # Temperature Coeff. Short Circuit Current [A/C]
               'beta_voc': -0.121182, # Temperature Coeff. Open Circuit Voltage [V/C]
               'gamma_pmp': -0.4509, # Temperature coefficient of power at maximum point [%/C]
               'cells_in_series': 60, # Number of cells in series
               'temp_ref': 25}  # Reference temperature conditions

print(module_data)

# 1st step: Estimating the parameters for the CEC single diode model
""" WARNING - This function relies on NREL's SAM tool. So PySAM, its Python API, needs to be installed 
in the same computer. Otherwise, you can expect the following error: 'ImportError if NREL-PySAM is not installed.'
"""
cec_fit_params = pvlib.ivtools.sdm.fit_cec_sam(module_data['celltype'], module_data['v_mp'], module_data['i_mp'],
                                  module_data['v_oc'], module_data['i_sc'], module_data['alpha_sc'],
                                  module_data['beta_voc'], module_data['gamma_pmp'], 
                                  module_data['cells_in_series'], module_data['temp_ref'])

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

# Accessing the characteristics of one of the modules randomly
inverter_data = invdb.iloc[:, np.random.randint(0, high=len(invdb))]
#print(inverter_data)

# Global plane-of-array effective irradiance between 200 and 1000 W/m2
g_poa_effective = 1000 #np.random.uniform(low=200, high=1000, size=(80,))
# Mean cell temperature values between 10 and 50 degrees Celsius
temp_cell = 40 #np.random.uniform(low=10, high=50, size=(80,)) 

# Definition of PV module characteristics:
pdc0 =(cec_mod_db.iloc[2, pv_name]) #250 # STC power
gamma_pdc = (cec_mod_db.iloc[21, pv_name])/100 #-0.0045 # The temperature coefficient in units of 1/C

# Estimate DC power with PVWatts model
dc_power = pvlib.pvsystem.pvwatts_dc(g_poa_effective, temp_cell, pdc0, gamma_pdc, temp_ref=25.0)
print(dc_power)