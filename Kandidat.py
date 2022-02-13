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
    ThetaValues = ["25", "10", "10", "10", "10", "10", "10", "10"] #Coded for total amount of sections in model, double check this

    # SWEEP VALUES
    SWEEPValues = ["45", "45", "10", "10", "10", "10", "10", "10"]

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


    #_______________________________________________________________________________________________________________



    # Reads the result from the VSPaero simulation and saves chosen results

    dummy = []
    with open(input_data, mode='r') as file:
        line = file.readline()
        line = line.strip()
        line = ' '.join(line.split()).split(' ')

        aoa_index = line.index('AoA')
        cl_index = line.index('CL')
        cd_index = line.index('CDtot')
        ld_index = line.index('L/D')
        cmy_index = line.index('CMy')

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





    # CHECK PITCHING MOMENT VS AoA SLOPE

    AOA = values[:, 2]
    My = values[:, 15]

    coef = np.corrcoef(My, AOA)
    coeff = coef[0, 1]
    if coeff >= 0: # Might want to include specific interval here
        return

    #CHECK ZERO PITCHING MOMENT FOR AOA = 0 (IS THIS WHAT WE SHOULD CHECK?)
    # if My[0] != 0:          # Assuming AoA will be zero at the first position, we can choose this ourselves in vspaero-file either way
       #  return

    theta = np.polyfit(AOA,My,1)

    y_line = theta[1]+theta[0]*AOA

    plt.scatter(AOA,My)
    plt.plot(AOA,y_line,'r')
    plt.title('Pitching moment vs AoA')
    plt.ylabel('CMy')
    plt.xlabel('AoA')
    plt.legend(["Slope coefficient: {}".format(coeff)])

    plt.show()






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
    W = 2 * 9.82
    rho = 5
    DynamicP_to = 0.5 * rho * V_to ** 2
    DynamicP_spr = 0.5 * rho * V_sp ** 2

    Cl_max = 2 # Find maximum lift for model airfoil LA2573A (maybe found reference for this) and put in 2D-stall model
    # in vspaero the get Cl-max for model (probably will work)
    Cl_to = 0.8 * Cl_max

    # Wing_loading = W/Surface_area

    Wing_loading = Cl_to * DynamicP_to


    Cl_sp = Wing_loading/DynamicP_spr
    Cd = 2 # Get from VSPaero?
    LvD_sp = Cl_sp/Cd  # Lift drag ratio for sprint



# "uav_it5_thicknessTE_0dot01_twist6-0_wingsplus30mm"
r = OptimizeBWB("output")
