import subprocess
import numpy as np

file = "aidsvinge"
path1 = r"C:\Users\abbes\PycharmProjects\KandidatProjekt\OpenVSP-3.26.1-win64"
path2 = r"C:/Users/abbes/PycharmProjects/KandidatProjekt/OpenVSP-3.26.1-win64"

subprocess.run(r"{}\vspaero.exe -omp 4 {}/{}_DegenGeom".format(path1, path2, file), shell=True)
# subprocess.run("vspaero.exe -omp 4, uav_it5_thicknessTE_0dot01_twist6-0_wingsplus30mm.vsp3")


input_data = r"{}\{}_DegenGeom.polar".format(path1, file)
print(input_data, type(input_data))


def read_file(filename):
    dummy = []
    with open(filename, mode='r') as file:
        line = file.readline()
        line = line.strip()
        line = ' '.join(line.split()).split(' ')
        print(line)
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

                dummy.append([line[aoa_index], line[cl_index], line[cd_index], line[ld_index], line[cmy_index]])

            counter += 1
            line = file.readline()
    values = np.array(dummy)
    return values


Values = read_file(input_data)
print(Values)
