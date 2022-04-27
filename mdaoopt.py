# Setup for MDAO calculations
import openmdao.api as om
from Kandidat import OptimizeBWB


class BWBOptimizer(om.ExplicitComponent):

    def setup(self):
        self.add_input('sweep', 0.0)
        self.add_input('twist_one', 0.0)
        self.add_input('twist_two', 0.0)
        self.add_input('twist_three', 0.0)
        self.add_input('twist_four', 0.0)

        self.add_output('maxL/D', 0.0)
        self.add_output('pitching_moment_c', 0.0)
        self.add_output('pitching_moment_slope', 0.0)

    def setup_partials(self):
        self.declare_partials(of='*', wrt='*', method='fd')

    def compute(self, inputs, outputs):
        sweep = inputs['sweep']
        twist_one = inputs['twist_one']
        twist_two = inputs['twist_two']
        twist_three = inputs['twist_three']
        twist_four = inputs['twist_four']

        print("INPUT: ", sweep,twist_one, twist_two, twist_three ,twist_four)

        outputs['maxL/D'], outputs['pitching_moment_c'], outputs['pitching_moment_slope'] = OptimizeBWB(float(sweep),float(twist_one),float(twist_two),float(twist_three), float(twist_four))
        print("OUTPUT: ", outputs['maxL/D'],outputs['pitching_moment_c'],outputs['pitching_moment_slope'])

# ________OPTIMIZATION___________________________________________________

prob = om.Problem()
model = prob.model

model.add_subsystem('p', BWBOptimizer())

prob.driver = om.DifferentialEvolutionDriver()
prob.driver.options['max_gen'] = 50
prob.driver.options['pop_size'] = 80


prob.model.add_design_var('p.sweep', lower=-3, upper=2)
prob.model.add_design_var('p.twist_one', lower=-5, upper=5)
prob.model.add_design_var('p.twist_two', lower=-5, upper=5)
prob.model.add_design_var('p.twist_three', lower=-5, upper=5)
prob.model.add_design_var('p.twist_four', lower=-5, upper=5)

prob.model.add_constraint('p.pitching_moment_c', lower=-0.00902, upper=0.00902, ref=1e-3)
prob.model.add_constraint('p.pitching_moment_slope', upper=-0.002987, ref=1e-3)

prob.model.add_objective('p.maxL/D', scaler=-1)

prob.setup()

prob.run_driver()
print(prob.get_val('p.sweep'),prob.get_val('p.twist_one'),prob.get_val('p.twist_two'), prob.get_val('p.twist_two'),prob.get_val('p.twist_four'))
