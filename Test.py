import subprocess
import numpy as np
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

Newfile = "6degTwistGridTesting"

path_org = r"C:\Users\abbes\PycharmProjects\KandidatProjekt\Bachelor-MMSX20"
path_vspaero = r"C:\Users\abbes\PycharmProjects\KandidatProjekt\OpenVSP-3.26.1-win64"
path_output = "C:/Users/abbes/PycharmProjects/KandidatProjekt/Bachelor-MMSX20"
path_degengeom = r"C:\Users\abbes\PycharmProjects\KandidatProjekt\OpenVSP-3.26.1-win64\scripts"


# subprocess.run(r"{}\vspaero.exe -omp 4 {}/{}_DegenGeom".format(path_vspaero, path_output, Newfile), shell=True)

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

W = 2.5 * 9.82
rho_to = 1.2255
rho_sp = 1.1677

DynamicP_to = 0.5 * rho_to * V_to ** 2
DynamicP_spr = 0.5 * rho_sp * V_sp ** 2

## CL-TAKEOFF ##
Cl_max = 0.632  # FOR NOW, change when we have real value
Cl_to = 0.8 * Cl_max
print("CL takeoff: ", Cl_to)


## WING LOADING ##
W_over_S = Cl_to * DynamicP_to
Wing_loading = W_over_S/9.82
S = W/W_over_S
print("Wing loading: " + str(Wing_loading) + " kg/m^2 ")

## LIFT TAKEOFF ##
# Lift_to = Cl_to*S*DynamicP_to
# print("Lift Take off: ", Lift_to, " N ")

## CL SPRINT ##
Cl_sp = W_over_S / DynamicP_spr
print("CL Sprint: ", Cl_sp)

## LIFT SPRINT ##
# Lift_sp = Cl_sp*S*DynamicP_spr
# print("Lift Sprint: ", Lift_sp, " N ")
# _____________________________________________________________________________________________________________________


# _________________________________________________TRIMMING CONDITIONS_________________________________________________


## AOA SPRINT ##
AoA_sp = np.interp(Cl_sp, values[:, 4], values[:,2])
print("Angle of attack in sprint: ", AoA_sp)

## CD AND TRUST SPRINT ##
Cd_sp = np.interp(Cl_sp, values[:,4], values[:,7])
print("CD for sprint: ", Cd_sp)
Drag_sp = Cd_sp*S*DynamicP_spr
print("Drag/Thrust in sprint: ", Drag_sp , " N ")

######
MyCG_sp = np.interp(AoA_sp, values[:, 2],values[:, 15])

# if MyCG_sp != 0:
# return
# CHECK PITCHING MOMENT VS AoA SLOPE
coef = np.corrcoef(values[:, 15], values[:, 2])
coeff = coef[0, 1]
# if coeff >= 0:  # Might want to include specific interval here
# return
#######


## LIFT OVER DRAG SPRINT ##
L_D_sp = np.interp(AoA_sp, values[:, 2], values[:,9])
print("Lift over drag in sprint: ", L_D_sp)

# ___________________________________________________________________________________________________________________




# ___________________MAXIMIZING L/D AND MINIMIZING ENERGY CONSUMPTION__________________________________________________

## MAX LIFT OVER DRAG ##
maxLD = np.max(values[:, 9])
print("Maximal lift over drag: ", maxLD)

# print("Optimal lift over drag for power consumption: ", optimalLD)
f1 = interp1d(values[:,9], values[:,2], kind='cubic')
AoA_loi = f1(maxLD)
print("Angle of Attack for loiter with max L/D: ", AoA_loi)
f2 = interp1d(values[:,9], values[:,4], kind='cubic')
Cl_loi = f2(maxLD)



## CL and CD for max L/D ##
# Cl_loi = np.interp(AoA_loi, values[:, 2], values[:, 4]) # Max_L/D
f3 = interp1d(values[:, 9], values[:, 7])
Cd_loi = f3(maxLD)
print(" CL for max L/D: ", Cl_loi)
# print("CD for loiter with respect to power consumption: ", Cd_loi)




## VELOCITY LOITER ##
optimal_V_loi = np.sqrt(W/(S*0.5*rho_sp*Cl_loi))


print("MAX LOITER VELOCITY: ", optimal_V_loi, " m/s ")
newvel = 0.766*optimal_V_loi
print("NEW velocity at 0.766% of old velocity: ", newvel, " m/s ")



newCl_loi = W/(S*rho_sp*0.5*newvel**2)
print("New CL with 76% velocity: ", newCl_loi)
AoAnew_loi = np.interp(newCl_loi, values[:, 4], values[:,2])

print(AoAnew_loi)

newCd_loi = np.interp(newCl_loi, values[:,4], values[:,7])




## THRUST IN LOITER ##
Drag_loi= newCd_loi*S*0.5*rho_sp*newvel**2
print("Drag/Thrust in loiter: ", Drag_loi, " N ")


aids = 0.866*maxLD

f4 = interp1d(values[:,9], values[:,2], kind='cubic')
AoA_loi1 = f4(10)
print("AOA: ", AoA_loi1)
plt.plot(values[:,2], values[:,9])
plt.show()


## LIFT IN LOITER ##
# Lift_loi = newCl_loi*S*0.5*rho_sp*optimal_V_loiP**2
# print("Lift in loiter: ", Lift_loi, " N ")

## LIFT OVER DRAG IN LOITER WITH BEST POWER CONSUMPTION ##
print("Optimal velocity in loiter for L/D and power consumption: " + str(optimal_V_loi) + " m/s ")
# print("L/D in loiter for optimal loiter velocity: ", optimLD)


Cd_spr = np.interp(Cl_sp, values[:, 4], values[:, 7])

## POWER CALCULATIONS ##
Power_loi = (W * newCd_loi * newvel / newCl_loi)
print("Power consumption for optimal velocity in loiter: " + str(Power_loi) + " W ")


Power_spr = (W * Cd_spr * V_sp / Cl_sp)
print("Power consumption for sprint: " + str(Power_spr) + " W ")