# Python function to calculate aerodynamic performance for BWB


def OptimizeBWB(filename):
    import subprocess
    import numpy as np
    import xml.etree.ElementTree as ET
    import matplotlib.pyplot as plt






#_____________________________________________________________________________________________________________________
    # Creating paths for objects we want to use such as .vsp3 files and VSPaero program
    # These needs to be specified for the computer working with the script
    path_org = r"C:\Users\abbes\PycharmProjects\KandidatProjekt\Bachelor-MMSX20"
    path_vspaero = r"C:\Users\abbes\PycharmProjects\KandidatProjekt\OpenVSP-3.26.1-win64"
    path_output = "C:/Users/abbes/PycharmProjects/KandidatProjekt/Bachelor-MMSX20"
    path_degengeom = r"C:\Users\abbes\PycharmProjects\KandidatProjekt\OpenVSP-3.26.1-win64\scripts"

    # Choose geometry to run simulation for
    ORIGINAL_GEOMETRY_NAME = "{}".format(filename)

    filename_org = r"{}\{}.vsp3".format(path_org, ORIGINAL_GEOMETRY_NAME)
#______________________________________________________________________________________________________________________







#______________________________CHANGING GEOMETRY______________________________________________________________________
    # TWIST VALUES
    ThetaValues = ["0", "0"]
    # Coded for total amount of sections in model, double check this

    # SWEEP VALUES
    SWEEPValues = "5"

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
        k += 1

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

    # Writes to a new .vsp3 file that can be analyzed in OpenVSP
    Newfile = "output"
    tree.write('{}.vsp3'.format(Newfile))
#______________________________________________________________________________________________________________________







# __________________________________OPENVSP___________________________________________________________________________

    # Create new degenerate geometry for updated file
    subprocess.run(
        r"{}\vspscript.exe {}\{}.vsp3 -script {}\DegenGeom.vspscript".format(path_vspaero, path_output, Newfile,
                                                                             path_degengeom))
    # Running VSPaero simulation for new file with changed values
    subprocess.run(r"{}\vspaero.exe -omp 4 {}/{}_DegenGeom".format(path_vspaero, path_output, Newfile), shell=True)

    # Collect results from simulation
    input_data = r"{}\{}_DegenGeom.polar".format(path_output, Newfile)

#______________________________________________________________________________________________________________________






#_____________Reads the result from the VSPaero simulation and saves results into code_______________________________

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

#______________________________________________________________________________________________________________________




#________________________________________________REQUIREMENTS________________________________________________________
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
#_____________________________________________________________________________________________________________________




#__________________________________INITIAL CALCULATIONS________________________________________________________________

    W = 3 * 9.82
    rho_to = 1.2255
    rho_sp = 1.1677

    DynamicP_to = 0.5 * rho_to * V_to ** 2
    DynamicP_spr = 0.5 * rho_sp * V_sp ** 2

    Cl_max = 0.632  # FOR NOW, change when we have real value
    Cl_to = 0.8 * Cl_max

    W_over_S = Cl_to * DynamicP_to
    Wing_loading = W_over_S / 9.82

    Cl_sp = W_over_S / DynamicP_spr
    # _____________________________________________________________________________________________________________________






    # _________________________________________________TRIMMING CONDITIONS_________________________________________________

    # Find optimal AoA
    AoA_sp = np.interp(Cl_sp, values[:, 4], values[:, 2])

    # Get pithing moment around centre of gravity for sprint condition
    MyCG_sp = np.interp(AoA_sp, values[:, 2], values[:, 15])

    if MyCG_sp != 0:
        return

    # CHECK PITCHING MOMENT VS AoA SLOPE
    coef = np.corrcoef(values[:, 15], values[:, 2])
    coeff = coef[0, 1]
    if coeff >= 0:  # Might want to include specific interval here
        return

    L_D_sp = np.interp(AoA_sp, values[:, 2], values[:, 9])


    # __________________________________________________________________________________________________________________







    # ___________________MAXIMIZING L/D AND MINIMIZING ENERGY CONSUMPTION_______________________________________________
    maxLD = np.max(values[:, 9])

    Cl_loi = np.interp(maxLD, values[:, 9], values[:, 4])  # Max_L/D
    Cd_loi = np.interp(maxLD, values[:, 9], values[:, 7])

    optimal_V_loi = np.sqrt(W_over_S / (0.5 * rho_sp * Cl_loi))

    optimal_V_loiP = 0.75 * optimal_V_loi



    vloi = np.sqrt(W_over_S / (0.5 * rho_sp * values[:, 4]))
    allpower = W * values[:, 7] * (np.sqrt(W_over_S / (0.5 * rho_sp * values[:, 4]))) / values[:, 4]

    Cd_spr = np.interp(Cl_sp, values[:, 4], values[:, 7])
    Power_spr = W * Cd_spr * V_sp / Cl_sp

    Power_loi = W * Cd_loi * optimal_V_loiP / Cl_loi
    print("Power consumption for optimal velocity in loiter: " + str(Power_loi) + " W ")

    Total_power = Power_spr + Power_loi
    #___________________________________________________________________________________________________________________




# "uav_it5_thicknessTE_0dot01_twist6-0_wingsplus30mm"
r = OptimizeBWB("output")
