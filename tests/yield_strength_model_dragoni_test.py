import unittest
import pyflowgo.flowgo_yield_strength_model_dragoni
import pyflowgo.flowgo_state
import pyflowgo.flowgo_terrain_condition
import pyflowgo.flowgo_material_lava
import pyflowgo.flowgo_vesicle_fraction_model_constant

class MyTestCase(unittest.TestCase):
    def test_read_initial_condition_from_json_file(self):
        filename = './resources/input_parameters_yield_strength_model.json'

        yield_strength_model_dragoni = pyflowgo.flowgo_yield_strength_model_dragoni.FlowGoYieldStrengthModelDragoni()
        yield_strength_model_dragoni.read_initial_condition_from_json_file(filename)

        self.assertEqual(yield_strength_model_dragoni._liquidus_temperature, 1400)

    def test_compute_yield_strength(self):
        filename = './resources/input_parameters_yield_strength_model.json'
        yield_strength_model_dragoni = pyflowgo.flowgo_yield_strength_model_dragoni.FlowGoYieldStrengthModelDragoni()
        yield_strength_model_dragoni.read_initial_condition_from_json_file(filename)

        state = pyflowgo.flowgo_state.FlowGoState()
        state.set_core_temperature(1273.15)
        state.set_crystal_fraction(0.15)
        yield_strength = yield_strength_model_dragoni.compute_yield_strength(state,eruption_temperature=1400)

        self.assertAlmostEqual(yield_strength, 123.1153581361,10)

    def test_compute_basal_shear_stress(self):

        yield_strength_model_dragoni = pyflowgo.flowgo_yield_strength_model_dragoni.FlowGoYieldStrengthModelDragoni()

        filename_1 = './resources/input_parameters_yield_strength_model.json'
        vesicle_fraction_model_constant = pyflowgo.flowgo_vesicle_fraction_model_constant.FlowGoVesicleFractionModelConstant()
        vesicle_fraction_model_constant.read_initial_condition_from_json_file(filename_1)
        filename = './resources/input_parameters_yield_strength_model.json'
        material_lava = pyflowgo.flowgo_material_lava.FlowGoMaterialLava(vesicle_fraction_model=vesicle_fraction_model_constant)
        material_lava.read_initial_condition_from_json_file(filename)

        filename = './resources/input_parameters_yield_strength_model.json'
        terrain_condition = pyflowgo.flowgo_terrain_condition.FlowGoTerrainCondition()
        terrain_condition.read_initial_condition_from_json_file(filename)
        filename_dem = './resources/DEM_pdf2010_lidar.txt'
        terrain_condition.read_slope_from_file(filename_dem)

        state = pyflowgo.flowgo_state.FlowGoState()
        state.set_current_position(100)

        basal_shear_stress = yield_strength_model_dragoni.compute_basal_shear_stress(state, terrain_condition,
                                                                                   material_lava)

        self.assertAlmostEqual(basal_shear_stress, 3582.02380873042,10)

if __name__ == '__main__':
    unittest.main()
