import subprocess
import numpy as np
import math
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from scipy.stats import linregress
from scipy.interpolate import interp1d

path_org = r"C:\Users\abbes\PycharmProjects\KandidatProjekt\Bachelor-MMSX20"
path_vspaero = r"C:\Users\abbes\PycharmProjects\KandidatProjekt\OpenVSP-3.26.1-win64"
path_output = "C:/Users/abbes/PycharmProjects/KandidatProjekt/Bachelor-MMSX20"
path_degengeom = r"C:\Users\abbes\PycharmProjects\KandidatProjekt\OpenVSP-3.26.1-win64\scripts"

Newfile = "6degTwistGridTesting"
Aidsfile = 'carlos_data'
# ______________________________________________________________________________________________________________________

# __________________________________OPENVSP___________________________________________________________________________

# Collect results from simulation
input_data = r"{}\{}_DegenGeom.polar".format(path_output, Newfile)

# ______________________________________________________________________________________________________________________

# _____________Reads the result from the VSPaero simulation and saves results into code_______________________________

dummy = []
with open(input_data, mode='r') as file:
    line = file.readline()
    line = line.strip()
    line = ' '.join(line.split()).split(' ')

    counter = 0
    while line:
        if counter != 0:
            line = line.strip()
            line = ' '.join(line.split()).split(' ')
            line = list(map(float, line))

            dummy.append(line)

        counter += 1
        line = file.readline()
values = np.array(dummy)

# ______________________________________________________________________________________________________________________

# ________________________________________________REQUIREMENTS________________________________________________________
# Take-off
V_to = 15  # m/s
alt_to = 0
DISA_to = 0  # degree

# Sprint
V_sp = 35
alt_sp = 500
DISA_sp = 0
# Coefficient of moment needs to be 0 at the centre of gravity - pos:[0.215,0,0]

# Loiter
alt_loi = 500
DISA_loi = 0
# We want maximum lift to drag ratio
# _____________________________________________________________________________________________________________________

# __________________________________INITIAL CALCULATIONS________________________________________________________________

W = 3 * 9.82
rho_to = 1.2255  # For take off altitude 0m
rho_sp = 1.1677  # For sprint altitude 500m

DynamicP_to = 0.5 * rho_to * V_to ** 2
DynamicP_spr = 0.5 * rho_sp * V_sp ** 2

Cl_max = 0.632  # FOR NOW, change when we have real value
Cl_to = 0.8 * Cl_max

W_over_S = Cl_to * DynamicP_to
Wing_loading = W_over_S / 9.82
S = W / W_over_S

Cl_sp = W_over_S / DynamicP_spr
print("CL SPRINT: ", Cl_sp)
Cd_spr = np.interp(Cl_sp, values[:, 4], values[:, 7])
print("CD SPRINT: ", Cd_spr)
# _____________________________________________________________________________________________________________________

# _________________________________________________TRIMMING CONDITIONS_________________________________________________

# Find optimal AoA
AoA_sp = np.interp(Cl_sp, values[:, 4], values[:, 2])
print("AoA SPRINT: ", AoA_sp)

# Get pithing moment around centre of gravity for sprint condition
MyCG_sp = np.interp(AoA_sp, values[:, 2], values[:, 15])

L_D_sp = np.interp(AoA_sp, values[:, 2], values[:, 9])
print("L/D SPRINT: ", L_D_sp)

# __________________________________________________________________________________________________________________

# ___________________MAXIMIZING L/D AND MINIMIZING ENERGY CONSUMPTION___________________________________________________
maxLD = np.max(values[:, 9])  # GETTING MAX L/D
print("MAX L/D: ", maxLD)

f2 = interp1d(values[:, 9], values[:, 4], kind='cubic')  # FINDING CL FOR MAX L/D
Cl_loi = f2(maxLD)

print("CL LOITER: ", Cl_loi)
f3 = interp1d(values[:, 9], values[:, 7], kind='cubic')
Cd_loi = f3(maxLD)
print("CD LOITER: ", Cd_loi)

optimal_V_loi = np.sqrt(W / (S*0.5 * rho_sp * Cl_loi))  # FINDING VELOCITY FOR MAX L/D
print("VELOCITY LOITER FOR MAX L/D: ", optimal_V_loi)

optimal_V_loiP = 0.75 * optimal_V_loi  # MULTIPLY WITH 0.75 TO GET VELOCTY FOR POWER CONSUM-
print("VELOCITY LOITER FOR OPTIMAL POWER CONSUMPTION: ", optimal_V_loiP)

newCl_loi = W / (S * rho_sp * 0.5 * optimal_V_loiP ** 2)  # NEW CL FOR THE NEW VELOCITY
print("NEW CL LOITER: ", newCl_loi)
newCd_loi = np.interp(newCl_loi, values[:, 4], values[:, 7])  # GET CD THROUGH THE NEW CL
# plt.plot(values[:, 4], values[:, 7])
print("NEW CD LOITER: ", newCd_loi)

Power_spr = (W * Cd_spr * V_sp / Cl_sp)  # POWER SPRINT
print("POWER CONSUMPTION SPRINT: ", Power_spr, " W ")

Power_loi = (W * newCd_loi * optimal_V_loiP / newCl_loi)  # POWER LOITER
print("POWER CONSUMPTION LOITER: ", Power_loi, " W ")

power_total = Power_loi + Power_spr  # THIS IS OBVIOUSLY WRONG, BUT WE NEED TO RETURN
# SOMETHING?

coeff = math.atan(linregress(values[:, 2],values[:, 15])[0])
plt.plot(values[:,2], values[:,15])
print("COEFFICIENT FOR PITCHING MOMENT SLOPE: ", coeff)

plt.show()
