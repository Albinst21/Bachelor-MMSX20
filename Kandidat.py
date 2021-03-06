# Python function to calculate aerodynamic performance for BWB
import math
import subprocess
from scipy.stats import linregress
import numpy as np
import xml.etree.ElementTree as ET
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt


def OptimizeBWB(sweep,twist1,twist2,twist3,twist4):
    # __________________________________________________________________________________________________________________
    # Creating paths for objects we want to use such as .vsp3 files and VSPaero program
    # These needs to be specified for the computer working with the script
    path_org = r"C:\Users\abbes\PycharmProjects\KandidatProjekt\Bachelor-MMSX20"
    path_vspaero = r"C:\Users\abbes\PycharmProjects\KandidatProjekt\OpenVSP-3.26.1-win64"
    path_output = "C:/Users/abbes/PycharmProjects/KandidatProjekt/Bachelor-MMSX20"
    path_degengeom = r"C:\Users\abbes\PycharmProjects\KandidatProjekt\OpenVSP-3.26.1-win64\scripts"

    # Choose geometry to run simulation for
    ORIGINAL_GEOMETRY_NAME = "easterGrid4sections"

    filename_org = r"{}\{}.vsp3".format(path_org, ORIGINAL_GEOMETRY_NAME)
    # ___________________________________________________________________________________________________________________

    # ______________________________CHANGING GEOMETRY___________________________________________________________________
    # TWIST VALUES
    ThetaValues = [f"{twist1}",f"{twist2}",f"{twist3}",f"{twist4}"]
    # Coded for total amount of sections in model, double check this

    # SWEEP VALUES
    SWEEPValues = f"{sweep}"

    # Do either twist or sweep first and then find the stabilizing values for the next parameter after
    # Part of script that can change twist in wing sections by changing value of Theta
    tree = ET.parse(filename_org)
    root = tree.getroot()

    k = 0  # Counter for the different sections
    for twist in root.iter('Theta'):

        if k == 4:
            value = list(dict.items(twist.attrib))
            value[0] = ('Value', '{}'.format(ThetaValues[0]))
            new_att = dict(value)
            twist.attrib = new_att
        elif k == 5:
            value = list(dict.items(twist.attrib))
            value[0] = ('Value', '{}'.format(ThetaValues[1]))
            new_att = dict(value)
            twist.attrib = new_att
        elif k == 6:
            value = list(dict.items(twist.attrib))
            value[0] = ('Value', '{}'.format(ThetaValues[2]))
            new_att = dict(value)
            twist.attrib = new_att
        elif k == 7:
            value = list(dict.items(twist.attrib))
            value[0] = ('Value', '{}'.format(ThetaValues[3]))
            new_att = dict(value)
            twist.attrib = new_att

        k += 1

    k = 0  # Counter for the different sections
    for sweep in root.iter('Sweep'):

        if k == 4:
            value = list(dict.items(sweep.attrib))
            value[0] = ('Value', '{}'.format(SWEEPValues))
            new_att = dict(value)
            sweep.attrib = new_att
        elif k == 5:
            value = list(dict.items(sweep.attrib))
            value[0] = ('Value', '{}'.format(SWEEPValues))
            new_att = dict(value)
            sweep.attrib = new_att
        elif k == 6:
            value = list(dict.items(sweep.attrib))
            value[0] = ('Value', '{}'.format(SWEEPValues))
            new_att = dict(value)
            sweep.attrib = new_att
        elif k == 7:
            value = list(dict.items(sweep.attrib))
            value[0] = ('Value', '{}'.format(SWEEPValues))
            new_att = dict(value)
            sweep.attrib = new_att
        k += 1

    # Writes to a new .vsp3 file that can be analyzed in OpenVSP
    Newfile = "output"
    tree.write('{}.vsp3'.format(Newfile))
    # ______________________________________________________________________________________________________________________

    # __________________________________OPENVSP___________________________________________________________________________

    # Create new degenerate geometry for updated file
    subprocess.run(r"{}\vspscript.exe {}\{}.vsp3 -script {}\DegenGeom.vspscript".format(path_vspaero, path_output,
                                                                                        Newfile, path_degengeom),
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Running VSPaero simulation for new file with changed values
    subprocess.run(r"{}\vspaero.exe -omp 4 {}/{}_DegenGeom".format(path_vspaero, path_output, Newfile), shell=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

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
    Cd_spr = np.interp(Cl_sp, values[:, 4], values[:, 7])
    # _____________________________________________________________________________________________________________________

    # _________________________________________________TRIMMING CONDITIONS_________________________________________________

    # Find optimal AoA
    AoA_sp = np.interp(Cl_sp, values[:, 4], values[:, 2])

    # Get pithing moment around centre of gravity for sprint condition
    MyCG_sp = np.interp(AoA_sp, values[:, 2], values[:, 15])

    # CHECK PITCHING MOMENT VS AoA SLOPE
    coeff = math.atan(linregress(values[:, 2], values[:, 15])[0])

    L_D_sp = np.interp(AoA_sp, values[:, 2], values[:, 9])

    # __________________________________________________________________________________________________________________

    # ___________________MAXIMIZING L/D AND MINIMIZING ENERGY CONSUMPTION_______________________________________________
    maxLD = np.max(values[:, 9])  # GETTING MAX L/D

    return maxLD, MyCG_sp, coeff

# _______________________________________________________________________________________________________________________


# "uav_it5_thicknessTE_0dot01_twist6-0_wingsplus30mm"
# print(OptimizeBWB(0,0,0,0,6))
