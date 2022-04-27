import math
import openmdao.api as om
import subprocess
from scipy.stats import linregress
import numpy as np
import xml.etree.ElementTree as ET

path_org = r"C:\Users\abbes\PycharmProjects\KandidatProjekt\Bachelor-MMSX20"
path_vspaero = r"C:\Users\abbes\PycharmProjects\KandidatProjekt\OpenVSP-3.26.1-win64"
path_output = "C:/Users/abbes/PycharmProjects/KandidatProjekt/Bachelor-MMSX20"
path_degengeom = r"C:\Users\abbes\PycharmProjects\KandidatProjekt\OpenVSP-3.26.1-win64\scripts"
ORIGINAL_GEOMETRY_NAME = "6degTwistGridTesting2"
filename_org = r"{}\{}.vsp3".format(path_org, ORIGINAL_GEOMETRY_NAME)


def CreateGeom(sweepval, twistval):
    tree = ET.parse(filename_org)
    root = tree.getroot()

    k = 0  # Counter for the different sections
    for twist in root.iter('Theta'):

        if k == 4:
            value = list(dict.items(twist.attrib))
            value[0] = ('Value', '{}'.format(twistval[0]))
            new_att = dict(value)
            twist.attrib = new_att
        elif k == 5:
            value = list(dict.items(twist.attrib))
            value[0] = ('Value', '{}'.format(twistval[1]))
            new_att = dict(value)
            twist.attrib = new_att
        k += 1

    k = 0  # Counter for the different sections
    for sweep in root.iter('Sweep'):

        if k == 4:
            value = list(dict.items(sweep.attrib))
            value[0] = ('Value', '{}'.format(sweepval))
            new_att = dict(value)
            sweep.attrib = new_att
        elif k == 5:
            value = list(dict.items(sweep.attrib))
            value[0] = ('Value', '{}'.format(sweepval))
            new_att = dict(value)
            sweep.attrib = new_att
        k += 1

    # Writes to a new .vsp3 file that can be analyzed in OpenVSP
    Newfile = "output"
    tree.write('{}.vsp3'.format(Newfile))


def VSPaeroSim(newfile: str):
    subprocess.run(
        r"{}\vspscript.exe {}\{}.vsp3 -script {}\DegenGeom.vspscript".format(path_vspaero, path_output, newfile,
                                                                             path_degengeom))
    # Running VSPaero simulation for new file with changed values
    subprocess.run(r"{}\vspaero.exe -omp 4 {}/{}_DegenGeom".format(path_vspaero, path_output, newfile), shell=True)

    # Collect results from simulation
    input_data = r"{}\{}_DegenGeom.polar".format(path_output, newfile)

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

    return np.array(dummy)


class BWBOptimizer(om.ExplicitComponent):  # CORRECT INHERITANCE?

    def setup(self):
        self.add_input('sweep', 10)
        self.add_input('twist_one', 10)
        self.add_input('twist_two', 10)

        self.add_output('maxL/D', 0.0)
        self.add_output('pitching_moment_c', 0.0)
        self.add_output('pitching_moment_slope', 0.0)

        self.declare_partials(of='*', wrt='*', method='cs')

    def compute(self, inputs, outputs):
        sweep = inputs['sweep']
        twist_one = inputs['twist_one']
        twist_two = inputs['twist_two']
        print(sweep.real, type(sweep.real))
        CreateGeom(float(sweep.real), [float(twist_one.real), float(twist_two.real)])

        values = VSPaeroSim("output")

        outputs['maxL/D'] = np.max(values[:,9])

        outputs['pitching_moment_c'] = np.interp(np.interp(0.0974620473178567, values[:, 4], values[:, 2]),
                                                 values[:, 2], values[:, 15])

        outputs['pitching_moment_slope'] = math.atan(linregress(values[:, 2], values[:, 15])[0])


# ________OPTIMIZATION___________________________________________________

prob = om.Problem()

prob.model.add_subsystem('BWBopt', BWBOptimizer(), promotes_inputs=['sweep', 'twist_one', 'twist_two'])

prob.driver = om.ScipyOptimizeDriver()
prob.driver.options['optimizer'] = 'SLSQP'  # NOT SURE WHAT SPECIFIC OPTIMIZER IS NEEDED HERE

# prob.driver.options['debug_print'] = ['desvars','objs']


prob.model.add_design_var('sweep', lower=-20, upper=20)
prob.model.add_design_var('twist_one', lower=0, upper=15)
prob.model.add_design_var('twist_two', lower=0, upper=15)
prob.model.add_constraint('BWBopt.pitching_moment_c', lower=-0.2, upper=0.2)
prob.model.add_constraint('BWBopt.pitching_moment_slope', lower=-0.000005, upper=-4.5)

prob.model.add_objective('BWBopt.maxL/D', scaler=-1)

# prob.driver.options['tol'] = 1e-9
#prob.driver.options['disp'] = True
#recorder = om.SqliteRecorder('cases.sql')
#prob.driver.add_recorder(recorder)
#prob.driver.recording_options['includes'] = ['*']
#prob.driver.recording_options['record_derivatives'] = True

prob.setup()

# Set input values
prob.set_val('sweep', 10)
prob.set_val('twist_one', 10)
prob.set_val('twist_two', 10)

prob.run_driver()

#prob.cleanup()
#cr = om.CaseReader("cases.sql")
#driver_cases = cr.list_cases('driver')