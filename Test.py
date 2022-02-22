

import subprocess
import numpy as np
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

# First step is to generate VSP3 file with parameters of choosing, for now we only have code to change the twist

# Creating paths for objects we want to use such as .vsp3 files and VSPaero program
# These needs to be specified for the computer working with the script
path_org = r"C:\Users\abbes\PycharmProjects\KandidatProjekt\Bachelor-MMSX20"
path_vspaero = r"C:\Users\abbes\PycharmProjects\KandidatProjekt\OpenVSP-3.26.1-win64"
path_output = "C:/Users/abbes/PycharmProjects/KandidatProjekt/Bachelor-MMSX20"
path_degengeom = r"C:\Users\abbes\PycharmProjects\KandidatProjekt\OpenVSP-3.26.1-win64\scripts"

# TWIST VALUES
ThetaValues = ["4", "5", "6"]

# Coded for total amount of sections in model, double check this

# SWEEP VALUES
# Create range ( Don't need this now ):
# randomvalues = np.linspace(0,20,100)
# SweepValues = []
# for r in randomvalues:
#   Sweepvalues.append(str(r))

SWEEPValues = "5"

# REQUIREMENTS_________________________________________________________________________________________________________
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

# CALCULATIONS (CODE IN PROGRESS)

# BASIC STUFF
W = 3 * 9.82
rho_to = 1.2255
rho_sp = 1.1677

DynamicP_to = 0.5 * rho_to * V_to ** 2
DynamicP_spr = 0.5 * rho_sp * V_sp ** 2

Cl_max = 1.5  # FOR NOW, change when we have real value
Cl_to = 0.8 * Cl_max

Wing_loading = Cl_to * DynamicP_to

S = W / Wing_loading

Cl_sp = Wing_loading / DynamicP_spr
# __________________________________________________________________________________________________________________

# _____________OPENVSP-FUNCTION_____________________________________________________________________________________
def runVSP(filename):

    # Create new degenerate geometry for updated file
    subprocess.run(
        r"{}\vspscript.exe {}\{}.vsp3 -script {}\DegenGeom.vspscript".format(path_vspaero, path_output, filename,
                                                                             path_degengeom))
    # Running VSPaero simulation for new file with changed values
    subprocess.run(r"{}\vspaero.exe -omp 4 {}/{}_DegenGeom".format(path_vspaero, path_output, filename), shell=True)

    # Collect results from simulation
    input_data = r"{}\{}_DegenGeom.polar".format(path_output, filename)

    # Reads the result from the VSPaero simulation and saves results into code

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

    return values
#______________________________________________________________________________________________________________________

#__________CHECK TRIM FUNCTION_________________________________________________________________________________________
def trimming(values):
    AoA_sp = np.interp(Cl_sp, values[:, 2], values[:, 4])
    MyCG_sp = np.interp(AoA_sp, values[:, 15], values[:, 2])
    coef = np.corrcoef(values[:, 15], values[:, 2])
    coeff = coef[0, 1]
    L_D_sp = np.interp(AoA_sp, values[:, 9], values[:, 2])

    return MyCG_sp, coeff
#______________________________________________________________________________________________________________________



# Choose geometry to run simulation for
ORIGINAL_GEOMETRY_NAME = "{}".format("uav_it5_thicknessTE_0dot01_twist6-0_wingsplus30mm")

filename_org = r"{}\{}.vsp3".format(path_org, ORIGINAL_GEOMETRY_NAME)

# Do either twist or sweep first and then find the stabilizing values for the next parameter after
# Part of script that can change twist in wing sections by changing value of Theta
tree = ET.parse(filename_org)
root = tree.getroot()
Newfile = "output3"

def ChangeSweep(SWEEPValues):
    k = 0  # Counter for the different sections
    for sweep in root.iter('Sweep'):

        if k == 3:
            value = list(dict.items(sweep.attrib))
            value[0] = ('Value', '{}'.format(SWEEPValues))
            new_att = dict(value)
            sweep.attrib = new_att
        elif k == 4:
            value = list(dict.items(sweep.attrib))
            value[0] = ('Value', '{}'.format(SWEEPValues))
            new_att = dict(value)
            sweep.attrib = new_att
        elif k == 5:
            value = list(dict.items(sweep.attrib))
            value[0] = ('Value', '{}'.format(SWEEPValues))
            new_att = dict(value)
            sweep.attrib = new_att
        k += 1

def ChangeTwist(ThetaValues):
    k = 0  # Counter for the different sections
    for twist in root.iter('Theta'):

        if k == 3:
            value = list(dict.items(twist.attrib))
            value[0] = ('Value', '{}'.format(ThetaValues[0]))
            new_att = dict(value)
            twist.attrib = new_att

        elif k == 4:
            value = list(dict.items(twist.attrib))
            value[0] = ('Value', '{}'.format(ThetaValues[1]))
            new_att = dict(value)
            twist.attrib = new_att
        elif k == 5:
            value = list(dict.items(twist.attrib))
            value[0] = ('Value', '{}'.format(ThetaValues[2]))
            new_att = dict(value)
            twist.attrib = new_att
        k += 1



def optimizeBWB(Sweep, Twist):

    ChangeSweep(Sweep)




        tree.write('{}.vsp3'.format(Newfile))

        values = runVSP(Newfile)
        trimcond1, trimcond2 = trimming(values)

        if trimcond1 != 0 or trimcond2 >= 0:
            return







