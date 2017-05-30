import unittest
import pyflowgo.flowgo_material_lava
import pyflowgo.flowgo_state
import pyflowgo.flowgo_crystallization_rate_model_bimodal


class MyTestCase(unittest.TestCase):
    def test_read_initial_condition_from_json_file(self):
        filename = './resources/input_parameters_crystallization_rate_bimodal.json'
        crystallization_rate_model_bimodal =pyflowgo.flowgo_crystallization_rate_model_bimodal.FlowGoCrystallizationRateModelBimodal()
        crystallization_rate_model_bimodal.read_initial_condition_from_json_file(filename)

    def test_get_crystal_fraction(self):
        filename = './resources/input_parameters_crystallization_rate_bimodal.json'
        crystallization_rate_model_bimodal =pyflowgo.flowgo_crystallization_rate_model_bimodal.FlowGoCrystallizationRateModelBimodal()
        crystallization_rate_model_bimodal.read_initial_condition_from_json_file(filename)
        state=pyflowgo.flowgo_state.FlowGoState()
        state.set_core_temperature(0)
        crystal_fraction= crystallization_rate_model_bimodal.get_crystal_fraction(state)
        self.assertEqual(crystal_fraction, 0.104)

    def test_get_solid_temperature(self):
        filename = './resources/input_parameters_crystallization_rate_bimodal.json'
        crystallization_rate_model_bimodal =pyflowgo.flowgo_crystallization_rate_model_bimodal.FlowGoCrystallizationRateModelBimodal()
        crystallization_rate_model_bimodal.read_initial_condition_from_json_file(filename)
        self.assertEqual(crystallization_rate_model_bimodal.get_solid_temperature(), 1237.15)

    def test_compute_crystallization_rate(self):
        filename = './resources/input_parameters_crystallization_rate_bimodal.json'
        crystallization_rate_model_bimodal =pyflowgo.flowgo_crystallization_rate_model_bimodal.FlowGoCrystallizationRateModelBimodal()
        crystallization_rate_model_bimodal.read_initial_condition_from_json_file(filename)
        state=pyflowgo.flowgo_state.FlowGoState()
        state.set_current_position(0)
        crystallization_rate=crystallization_rate_model_bimodal.compute_crystallization_rate(state)
        self.assertAlmostEqual(crystallization_rate, 0.00597333333,10)

        state.set_current_position(40)
        crystallization_rate=crystallization_rate_model_bimodal.compute_crystallization_rate(state)
        self.assertAlmostEqual(crystallization_rate, 0.02,10)

if __name__ == '__main__':
    unittest.main()
