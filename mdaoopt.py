# Setup for MDAO calculations

import openmdao.api as om
from Kandidat import OptimizeBWB


class BWBOptimizer(om.ExplicitComponent):  # CORRECT INHERITANCE?

    def setup(self):
        self.add_input('sweep', val=0.0)
        self.add_input('twist_one', val=0.0)
        self.add_input('twist_two', val=0.0)

        self.add_output('maxL/D', val=0.0)
        self.add_output('pitching_moment_c', val=0.0)
        self.add_output('pitching_moment_slope', val=0.0)

    def setup_partials(self):  # Very unclear how to handle this part, its vital to the process so seems like we need it
        self.declare_partials(of='*', wrt='*', method='fd')

    def compute(self, inputs, outputs):
        sweep = inputs['sweep']
        twist_one = inputs['twist_one']
        twist_two = inputs['twist_two']

        outputs['maxL/D'], outputs['pitching_moment_c'], outputs['pitching_moment_slope'] = OptimizeBWB(sweep,twist_one
                                                                                                        ,twist_two)


# ________OPTIMIZATION___________________________________________________

prob = om.Problem()
model = prob.model

model.add_subsystem('p', BWBOptimizer())

prob.driver = om.ScipyOptimizeDriver()
prob.driver.options['optimizer'] = 'SLSQP'  # NOT SURE WHAT SPECIFIC OPTIMIZER IS NEEDED HERE

prob.driver.options['debug_print'] = ['desvars','objs']


prob.model.add_design_var('p.sweep', lower=-20, upper=20, ref=0.0001)
prob.model.add_design_var('p.twist_one', lower=0, upper=15, ref=0.0001)
prob.model.add_design_var('p.twist_two', lower=0, upper=15, ref=0.0001)
prob.model.add_constraint('p.pitching_moment_c', lower=-0.1, upper=0.1)
prob.model.add_constraint('p.pitching_moment_slope', lower=-0.00005, upper=-4.5)

prob.model.add_objective('p.maxL/D')

prob.driver.options['tol'] = 1e-9
prob.driver.options['disp'] = True
recorder = om.SqliteRecorder('cases.sql')
prob.driver.add_recorder(recorder)
prob.driver.recording_options['includes'] = ['*']
prob.driver.recording_options['record_derivatives'] = True

prob.setup()

# Set input values
prob.set_val('p.sweep', 18)
prob.set_val('p.twist_one', 14)
prob.set_val('p.twist_two', 14)

prob.run_driver()

prob.cleanup()
cr = om.CaseReader("cases.sql")
driver_cases = cr.list_cases('driver')