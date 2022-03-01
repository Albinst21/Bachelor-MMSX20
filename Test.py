import subprocess
import numpy as np
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

Newfile = "uav_it5_thicknessTE_0dot01_twist6-0_wingsplus30mm"

path_org = r"C:\Users\abbes\PycharmProjects\KandidatProjekt\Bachelor-MMSX20"
path_vspaero = r"C:\Users\abbes\PycharmProjects\KandidatProjekt\OpenVSP-3.26.1-win64"
path_output = "C:/Users/abbes/PycharmProjects/KandidatProjekt/Bachelor-MMSX20"
path_degengeom = r"C:\Users\abbes\PycharmProjects\KandidatProjekt\OpenVSP-3.26.1-win64\scripts"


subprocess.run(r"{}\vspaero.exe -omp 4 {}/{}_DegenGeom".format(path_vspaero, path_output, Newfile), shell=True)

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
rho_to = 1.2255
rho_sp = 1.1677

DynamicP_to = 0.5 * rho_to * V_to ** 2
DynamicP_spr = 0.5 * rho_sp * V_sp ** 2

Cl_max = 0.632  # FOR NOW, change when we have real value
Cl_to = 0.8 * Cl_max

W_over_S = Cl_to * DynamicP_to
Wing_loading = W_over_S/9.82
print("Wing loading: " + str(Wing_loading) + " kg/m^2 ")


Cl_sp = W_over_S / DynamicP_spr
print("CL Sprint: ", Cl_sp)
# _____________________________________________________________________________________________________________________


# _________________________________________________TRIMMING CONDITIONS_________________________________________________

# Find optimal AoA
plt.plot(values[:, 2], values[:, 4])
plt.title('CL vs AoA')
plt.ylabel('CL')
plt.xlabel('AoA')
plt.show()

AoA_sp = np.interp(Cl_sp, values[:, 4], values[:,2])
print("Angle of attack in sprint: ", AoA_sp)

# Get pithing moment around centre of gravity for sprint condition
plt.plot(values[:, 2], values[:, 15])
plt.title('Pitching moment vs AoA')
plt.ylabel('CMy')
plt.xlabel('AoA')
plt.show()

MyCG_sp = np.interp(AoA_sp, values[:, 2],values[:, 15])

# if MyCG_sp != 0:
# return
# CHECK PITCHING MOMENT VS AoA SLOPE
coef = np.corrcoef(values[:, 15], values[:, 2])
coeff = coef[0, 1]
# if coeff >= 0:  # Might want to include specific interval here
# return

# GET L/D for optimal angle of attack, namely L/D for sprint!
plt.plot(values[:, 2], values[:, 9])
plt.title('L/D vs AoA')
plt.ylabel('L/D')
plt.xlabel('AoA')
plt.show()

L_D_sp = np.interp(AoA_sp, values[:, 2], values[:,9])
print("Lift over drag in sprint: ", L_D_sp)

# ___________________________________________________________________________________________________________________


# PLOTTING; NO REAL USE JUST FUN
# theta = np.polyfit(AOA, My, 1)

# y_line = theta[1] + theta[0] * AOA

# plt.scatter(AOA, My)
# plt.plot(AOA, y_line, 'r')
# plt.title('Pitching moment vs AoA')
# plt.ylabel('CMy')
# plt.xlabel('AoA')
# plt.legend(["Slope coefficient: {}".format(coeff)])
# plt.show()


# ___________________MAXIMIZING L/D AND MINIMIZING ENERGY CONSUMPTION__________________________________________________
maxLD = np.max(values[:, 9])
print("Maximal lift over drag: ", maxLD)

Cl_loi = np.interp(maxLD, values[:, 9], values[:, 4])  # Max_L/D
Cd_loi = np.interp(maxLD, values[:, 9], values[:, 7])

optimal_V_loi = np.sqrt(W_over_S/(0.5*rho_sp*Cl_loi))


optimal_V_loiP = 0.75 * optimal_V_loi
print("Optimal velocity in loiter for L/D and power consumption: ", optimal_V_loiP)

# K = 1.2 # DOUBLE CHECK THIS
# Cdnoll = np.interp(0, values[:,4], values[:,7])# where CL = 0?

vloi = np.sqrt(W_over_S/(0.5*rho_sp*values[:,4]))
allpower = W*values[:, 7]*(np.sqrt(W_over_S/(0.5*rho_sp*values[:,4])))/values[:,4]

plt.plot(vloi, allpower)
plt.title('Power consumption vs Velocity in loiter')
plt.ylabel('PowerC')
plt.xlabel('V_loi')
plt.show()

Power = W*Cd_loi*optimal_V_loiP/Cl_loi
print("Power consumption for optimal velocity in loiter: " + str(Power) + " W ")