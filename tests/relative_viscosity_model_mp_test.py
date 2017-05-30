import unittest
import pyflowgo.flowgo_relative_viscosity_model_mp
import pyflowgo.flowgo_state

class MyTestCase(unittest.TestCase):

    def test_read_initial_condition_from_json_file(self):
        filename = './resources/input_parameters_relative_viscosity_model.json'

        relative_viscosity_model_mp = pyflowgo.flowgo_relative_viscosity_model_mp.FlowGoRelativeViscosityModelMP()
        relative_viscosity_model_mp.read_initial_condition_from_json_file(filename)

        self.assertEqual(relative_viscosity_model_mp._phimax, 0.641)

    def test_computes_relative_viscosity(self):
        filename = './resources/input_parameters_relative_viscosity_model.json'
        relative_viscosity_model_mp = pyflowgo.flowgo_relative_viscosity_model_mp.FlowGoRelativeViscosityModelMP()
        relative_viscosity_model_mp.read_initial_condition_from_json_file(filename)
        state = pyflowgo.flowgo_state.FlowGoState()
        state.set_crystal_fraction(0.2)
        relative_viscosity = relative_viscosity_model_mp.compute_relative_viscosity(state)
        self.assertAlmostEqual(relative_viscosity, 2.11270509716,10)

if __name__ == '__main__':
    unittest.main()
