# Setup for MDAO calculations

import openmdao.api as om
from Kandidat import OptimizeBWB


class BWBOptimizer(om.ExplicitComponent):  # CORRECT INHERITANCE?

    def setup(self):
        self.add_input('sweep', val=0.0)
        self.add_input('twist_one', val=0.0)
        self.add_input('twist_two', val=0.0)

        self.add_output('power', val=0.0)
        self.add_output('pitching_moment_c', val=0.0)
        self.add_output('pitching_moment_slope', val=0.0)

    def setup_partials(self):  # Very unclear how to handle this part, its vital to the process so seems like we need it
        self.declare_partials(of='*', wrt='*', method='fd')

    def compute(self, inputs, outputs):
        sweep = inputs['sweep']
        twist_one = inputs['twist_one']
        twist_two = inputs['twist_two']

        outputs['power'], outputs['pitching_moment_c'], outputs['pitching_moment_slope'] = OptimizeBWB(sweep, twist_one, twist_two)


# ________OPTIMIZATION___________________________________________________

prob = om.Problem()
model = prob.model

model.add_subsystem('p', BWBOptimizer())

prob.driver = om.ScipyOptimizeDriver()
prob.driver.options['optimizer'] = 'SLSQP'  # NOT SURE WHAT SPECIFIC OPTIMIZER IS NEEDED HERE

prob.model.add_design_var('p.sweep', lower=0, upper=30)
prob.model.add_design_var('p.twist_one', lower=0, upper=10)
prob.model.add_design_var('p.twist_two', lower=0, upper=10)
prob.model.add_constraint('p.pitching_moment_c', lower=-0.01, upper=0.01)
prob.model.add_constraint('p.pitching_moment_slope', lower=-0.01, upper=-50)

prob.model.add_objective('p.power')

prob.driver.options['tol'] = 1e-9
prob.driver.options['disp'] = True

prob.setup()

# Set input values
prob.set_val('p.sweep', 10)
prob.set_val('p.twist_one', 5)
prob.set_val('p.twist_two', 7)

prob.run_driver()
