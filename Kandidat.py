# Python function to calculate aerodynamic performance for BWB


def OptimizeBWB(filename):
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
    ThetaValues = ["0", "0", "0", "0", "0", "0", "0", "0"]
    # Coded for total amount of sections in model, double check this

    # SWEEP VALUES
    SWEEPValues = ["0", "0", "0", "0", "0", "0", "0", "0"]

    # Choose geometry to run simulation for
    ORIGINAL_GEOMETRY_NAME = "{}".format(filename)

    filename_org = r"{}\{}.vsp3".format(path_org, ORIGINAL_GEOMETRY_NAME)

    # Part of script that can change twist in wing sections by changing value of Theta
    tree = ET.parse(filename_org)
    root = tree.getroot()

    k = 0  # Counter for the different sections
    for twist in root.iter('Theta'):

        if k == 0:  # This changes twist for section 1 for example
            value = list(dict.items(twist.attrib))
            value[0] = ('Value', '{}'.format(ThetaValues[k]))
            new_att = dict(value)
            twist.attrib = new_att
        elif k == 1:  # This for section 2
            value = list(dict.items(twist.attrib))
            value[0] = ('Value', '{}'.format(ThetaValues[k]))
            new_att = dict(value)
            twist.attrib = new_att
        elif k == 2:
            value = list(dict.items(twist.attrib))
            value[0] = ('Value', '{}'.format(ThetaValues[k]))
            new_att = dict(value)
            twist.attrib = new_att
        elif k == 3:
            value = list(dict.items(twist.attrib))
            value[0] = ('Value', '{}'.format(ThetaValues[k]))
            new_att = dict(value)
            twist.attrib = new_att
        elif k == 4:
            value = list(dict.items(twist.attrib))
            value[0] = ('Value', '{}'.format(ThetaValues[k]))
            new_att = dict(value)
            twist.attrib = new_att
        elif k == 5:
            value = list(dict.items(twist.attrib))
            value[0] = ('Value', '{}'.format(ThetaValues[k]))
            new_att = dict(value)
            twist.attrib = new_att
        elif k == 6:
            value = list(dict.items(twist.attrib))
            value[0] = ('Value', '{}'.format(ThetaValues[k]))
            new_att = dict(value)
            twist.attrib = new_att
        elif k == 7:
            value = list(dict.items(twist.attrib))
            value[0] = ('Value', '{}'.format(ThetaValues[k]))
            new_att = dict(value)
            twist.attrib = new_att
        k += 1

    k = 0  # Counter for the different sections
    for sweep in root.iter('Sweep'):

        if k == 0:  # This changes twist for section 1 for example
            value = list(dict.items(sweep.attrib))
            value[0] = ('Value', '{}'.format(SWEEPValues[k]))
            new_att = dict(value)
            sweep.attrib = new_att
        elif k == 1:  # This for section 2
            value = list(dict.items(sweep.attrib))
            value[0] = ('Value', '{}'.format(SWEEPValues[k]))
            new_att = dict(value)
            sweep.attrib = new_att
        elif k == 2:
            value = list(dict.items(sweep.attrib))
            value[0] = ('Value', '{}'.format(SWEEPValues[k]))
            new_att = dict(value)
            sweep.attrib = new_att
        elif k == 3:
            value = list(dict.items(sweep.attrib))
            value[0] = ('Value', '{}'.format(SWEEPValues[k]))
            new_att = dict(value)
            sweep.attrib = new_att
        elif k == 4:
            value = list(dict.items(sweep.attrib))
            value[0] = ('Value', '{}'.format(SWEEPValues[k]))
            new_att = dict(value)
            sweep.attrib = new_att
        elif k == 5:
            value = list(dict.items(sweep.attrib))
            value[0] = ('Value', '{}'.format(SWEEPValues[k]))
            new_att = dict(value)
            sweep.attrib = new_att
        elif k == 6:
            value = list(dict.items(sweep.attrib))
            value[0] = ('Value', '{}'.format(SWEEPValues[k]))
            new_att = dict(value)
            sweep.attrib = new_att
        elif k == 7:
            value = list(dict.items(sweep.attrib))
            value[0] = ('Value', '{}'.format(SWEEPValues[k]))
            new_att = dict(value)
            sweep.attrib = new_att
        k += 1

    # Writes to a new .vsp3 file that can be analyzed in OpenVSP
    Newfile = "output"
    tree.write('{}.vsp3'.format(Newfile))

    # __________________________________OPENVSP____________________________________________________________________

    # Create new degenerate geometry for updated file
    subprocess.run(
        r"{}\vspscript.exe {}\{}.vsp3 -script {}\DegenGeom.vspscript".format(path_vspaero, path_output, Newfile,
                                                                             path_degengeom))
    # Running VSPaero simulation for new file with changed values
    subprocess.run(r"{}\vspaero.exe -omp 4 {}/{}_DegenGeom".format(path_vspaero, path_output, Newfile), shell=True)

    # Collect results from simulation
    input_data = r"{}\{}_DegenGeom.polar".format(path_output, Newfile)

    # _______________________________________________________________________________________________________________

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




    # REQUIREMENTS
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
    W = 2 * 9.82
    rho_to = 1.2255
    rho_sp = 1.1677

    DynamicP_to = 0.5 * rho_to * V_to ** 2
    DynamicP_spr = 0.5 * rho_sp * V_sp ** 2

    Cl_max = 1.5  # FOR NOW, change when we have real value
    Cl_to = 0.8 * Cl_max

    Wing_loading = Cl_to * DynamicP_to
    S = W/Wing_loading

    Cl_sp = Wing_loading / DynamicP_spr



    # Find optimal AoA
    def GetAoA(optimalCl, AoA_values, Cl_values):

        AoA_opt = np.interp(optimalCl, Cl_values, AoA_values)
        return AoA_opt

    AoA_sp = GetAoA(Cl_sp, values[:, 2], values[:, 4])

    # Get pithing moment around centre of gravity for sprint condition
    def GetMyCG(AoA, My_values, AoA_values):

        My_CG = np.interp(AoA, AoA_values, My_values, )
        return My_CG

    MyCG_sp = GetMyCG(AoA_sp, values[:, 15], values[:, 2])
    if MyCG_sp != 0:
        return

    # CHECK PITCHING MOMENT VS AoA SLOPE
    coef = np.corrcoef(values[:, 15], values[:, 2])
    coeff = coef[0, 1]
    if coeff >= 0:  # Might want to include specific interval here
        return

    # GET L/D for optimal angle of attack, namely L/D for sprint!
    def LiftOverDrag(AoA,LD_values,AoA_values):

        L_D = np.interp(AoA, AoA_values, LD_values)
        return L_D

    L_D_sp = LiftOverDrag(AoA_sp,values[:,9],values[:,2])
    print(L_D_sp)




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


    maxLD = np.max(values[:,9])

    Cl_loi = np.interp(maxLD, values[:,9], values[:,4])# Max_L/D

    optimal_V_loi = np.sqrt(W/(Cl_loi*0.5 * rho_sp*S))
    print(optimal_V_loi)

    K = 1.2
    Cdnoll = np.interp(0, values[:,4], values[:,7])# where CL = 0
    optimal_V_loiP = (K/(3*Cdnoll))**(1/4)
    print(optimal_V_loiP)

    # Power = A*optimal_V_loiP**3 + B/optimal_V_loiP




# "uav_it5_thicknessTE_0dot01_twist6-0_wingsplus30mm"
r = OptimizeBWB("output")
