######### Import the particular module of the pvlib library#######
from pvlib import pvsystem
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import pandas as pd
import pvlib
#import xlsxwriter
from pathlib import Path
import numpy as np

################################# Variables######################
PvDataImport=2   # Add PV module data by column number 1, by name 2, and manualy 3
InverterDataImport=3   # Add Inverter data by column number 1, by name 2, and randomly 3
StartDate='20221001'  # Start date YYYYMMDD
EndDate='20221017'      #  End  date YYYYMMDD
# Coordinates of the weather station
latitude = -37.8576425
longitude = 145.1830722
altitude = 114
tilt=32
azimuth=140
##################################################################
irrad = 1000  #e.g. 1000   
temp_cell =40 #e.g. 0040 
##################################################################
PvModuleName='Centrosolar America DM72 295'
pv_number=170                                              # You can choose a PV system from the dartabase and  related number of each row
InverterName='SunPower: SPR-E20-327-D-AC [208V]'
inverter_number=423
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
#######################Databases###################################
# CEC Inverter Database
invdb = pvsystem.retrieve_sam('CECInverter')
# CEC PV Module Database
cec_mod_db = pvsystem.retrieve_sam('CECmod')
##################################################################
#############################Main PV##############################
PvModuleName=PvModuleName.replace(".", "_")
PvModuleName=PvModuleName.replace(" ", "_")
PvModuleName=PvModuleName.replace("]", "_")
PvModuleName=PvModuleName.replace("[", "_")
PvModuleName=PvModuleName.replace(":", "_")
PvModuleName=PvModuleName.replace("-", "_")
PvModuleName=PvModuleName.replace("/", "_")
PvModuleName=PvModuleName.replace(",", "_")
PvModuleName=PvModuleName.replace("+", "_")
if (PvDataImport==2):
    pv_name=(cec_mod_db.columns.get_loc(PvModuleName))
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
InverterName=InverterName.replace(",", "_")
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
print(mc)
mc.run_model(df_weather) 
wth=pd.DataFrame(mc.results.weather)
sp=pd.DataFrame(mc.results.solar_position)
irr=pd.DataFrame(mc.results.total_irrad)
dcp=pd.DataFrame(mc.results.dc)
acp=pd.DataFrame(mc.results.ac)

acp.to_csv(AC_Power)
dcp.to_csv(DC_Power)
irr.to_csv(Irradiance)
sp.to_csv(Solar_Position)
wth.to_csv(Weather)



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