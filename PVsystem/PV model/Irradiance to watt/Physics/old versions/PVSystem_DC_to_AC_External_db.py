######### Import the particular module of the pvlib library#######
import csv
from http import HTTPStatus
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
PvDataImport=2   # Add PV module data by column number 1, by name 2, and manualy 3
InverterDataImport=3   # Add Inverter data by column number 1, by name 2, and randomly 3
##################################################################
irrad = 1000  #e.g. 1000   
temp_cell =55 #e.g. 0040 
##################################################################
PvModuleName='Canadian Solar CS5P-220M'
pv_number=0                                             # You can choose a PV system from the dartabase and  related number of each row
InverterName='SunPower: SPR-E20-327-D-AC [208V]'

inverter_number=423
#############################Main PV##############################
module_data = cec_mod_db.iloc[:,0]
print(module_data)
PvModuleName=PvModuleName.replace(".", "_")
PvModuleName=PvModuleName.replace(" ", "_")
PvModuleName=PvModuleName.replace("]", "_")
PvModuleName=PvModuleName.replace("[", "_")
PvModuleName=PvModuleName.replace(":", "_")
PvModuleName=PvModuleName.replace("-", "_")
PvModuleName=PvModuleName.replace("/", "_")
PvModuleName=PvModuleName.replace("+", "_")
if (PvDataImport==2):
    pv_number=(cec_mod_db.columns.get_loc(PvModuleName))
    print(pv_number)
if  ((PvDataImport==2) or (PvDataImport==1)):
        #print(pv_name)
        # Size of the database
        #print(cec_mod_db.shape)
        #print(cec_mod_db.iloc[:, pv_name])
        # PV module data from a typical datasheet (e.g. Kyocera Solar KD225GX LPB)
        TypeCellFind=cec_mod_db.iloc[0, pv_number]
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

        module_data = {'Name':list(cec_mod_db.keys())[pv_number],
               'celltype': (Typecell), # technology  s.replace('ab', ''
               'Bifacial': (cec_mod_db.iloc[1, pv_number]),  #Bifacial                   
               'STC': (cec_mod_db.iloc[2, pv_number]), # STC power
               'PTC': (cec_mod_db.iloc[3, pv_number]), # PTC power
               'A_c': (cec_mod_db.iloc[4, pv_number]),  #A_c
               'N_s': (cec_mod_db.iloc[7, pv_number]),  #N_s
               'v_mp': (cec_mod_db.iloc[11, pv_number]), # Maximum power voltage
               'i_mp': (cec_mod_db.iloc[10, pv_number]), # Maximum power current
               'v_oc': (cec_mod_db.iloc[9, pv_number]), # Open-circuit voltage
               'i_sc': (cec_mod_db.iloc[8, pv_number]), # Short-circuit current
               'alpha_sc': (cec_mod_db.iloc[12, pv_number]), # Temperature Coeff. Short Circuit Current [A/C]
               'beta_voc': (cec_mod_db.iloc[13, pv_number]), # Temperature Coeff. Open Circuit Voltage [V/C]
               'gamma_pmp': (cec_mod_db.iloc[21, pv_number]), # Temperature coefficient of power at maximum point [%/C]
               'cells_in_series': (cec_mod_db.iloc[7, pv_number]), # Number of cells in series
               'temp_ref': (cec_mod_db.iloc[14, pv_number]),  # Reference temperature conditions
                'I_sc_ref': (cec_mod_db.iloc[8, pv_number]),  # Reference
                'V_oc_ref': (cec_mod_db.iloc[9, pv_number]),  # Reference
                'I_mp_ref': (cec_mod_db.iloc[10, pv_number]),  # Reference
                'V_mp_ref': (cec_mod_db.iloc[11, pv_number]),  # Reference
                'alpha_sc': (cec_mod_db.iloc[12, pv_number]),  # Reference
                'beta_oc': (cec_mod_db.iloc[13, pv_number]),  # Reference
                'a_ref': (cec_mod_db.iloc[15, pv_number]),  # Reference
                'I_L_ref': (cec_mod_db.iloc[16, pv_number]),  # Reference
                'I_o_ref': (cec_mod_db.iloc[17, pv_number]) , # Reference
                'R_s': (cec_mod_db.iloc[18, pv_number]),  # Reference
                'R_sh_ref': (cec_mod_db.iloc[19, pv_number]),  # Reference
                'Adjust': (cec_mod_db.iloc[20, pv_number]),  # Reference
                'gamma_r': (cec_mod_db.iloc[21, pv_number]),  # Reference
                'Version': (cec_mod_db.iloc[23, pv_number])}  # Reference
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
                'temp_ref': 25,  # Reference temperature conditions
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
                                }

print(module_data)
########################################Inverter#########################################
# Accessing the characteristics of one of the modules randomly
#InverterName='Solarmax SEAP60-255'
#inverter_number=10
InverterName=InverterName.replace(".", "_")
InverterName=InverterName.replace("[", "_")
InverterName=InverterName.replace("]", "_")
InverterName=InverterName.replace(":", "_")
InverterName=InverterName.replace("-", "_")
InverterName=InverterName.replace(" ", "_")
InverterName=InverterName.replace("/", "_")
InverterName=InverterName.replace("+", "_")
if (InverterDataImport==2):
    inverter_number=(invdb.columns.get_loc(InverterName))
    print(inverter_number)
if  ((InverterDataImport==2) or (InverterDataImport==1)):
    inverter_data = invdb.iloc[:, inverter_number]
if (InverterDataImport==3):
    #inverter_data = invdb.iloc[:, np.random.randint(0, high=len(invdb))]
    inverter_data={
    'Name':'SunPower__SPR_E20_327_D_AC__208V_',
    'Vac':208,
    'Pso': 2.862352,
    'Paco': 320.0,
    'Pdco':333.699951,
    'Vdco': 60.0,
    'C0': -0.000066,
    'C1': -0.000009,
    'C2':  0.021225,
    'C3':  0.018693,
    'Pnt':  0.018693,
    'Vdcmax':  64.0,
    'Idcmax':  5.561666,
    'Mppt_low':  53.0,
    'Mppt_high': 64.0,
    'CEC_Date':  '2/15/2019',
    'CEC_Type':  'Utility Interactive'
    }
print(inverter_data)
print(list(invdb.keys())[inverter_number])
#########################################################################################
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
gamma_pdc = module_data['gamma_pmp']/100 #-0.0045 # The temperature coefficient in units of 1/C

# Estimate DC power with PVWatts model
dc_power = pvlib.pvsystem.pvwatts_dc(g_poa_effective, temp_cell, pdc0, gamma_pdc, temp_ref=module_data['temp_ref'])
print("dc_power:",iv_values1['p_mp'])

ac_power = pvlib.inverter.sandia(iv_values1['v_mp'], # DC voltage input to the inverter
                                 iv_values1['p_mp'], # DC power input to the inverter
                                 inverter_data) # Parameters for the inverter 
# Estimated Power Output
print("ac_power:",ac_power)