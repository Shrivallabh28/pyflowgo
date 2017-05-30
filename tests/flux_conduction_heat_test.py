import unittest
import pyflowgo.flowgo_material_lava
import pyflowgo.flowgo_vesicle_fraction_model_constant
import pyflowgo.flowgo_state
import pyflowgo.flowgo_terrain_condition
import pyflowgo.flowgo_flux_conduction_heat


class MyTestCase(unittest.TestCase):

    def test_read_initial_condition_from_json_file(self):
        filename = './resources/input_parameters_conduction_heat_flux.json'
        material_lava = pyflowgo.flowgo_material_lava.FlowGoMaterialLava()

        flowgo_flux_conduction_heat = pyflowgo.flowgo_flux_conduction_heat.FlowGoFluxConductionHeat(material_lava)
        flowgo_flux_conduction_heat.read_initial_condition_from_json_file(filename)

        self.assertEqual(flowgo_flux_conduction_heat._base_temperature, 773.15)
        self.assertEqual(flowgo_flux_conduction_heat._core_base_distance, 19)

    def test_compute_flux(self):
        filename = './resources/input_parameters_radiation_flux.json'

        state = pyflowgo.flowgo_state.FlowGoState()
        state.set_core_temperature(1387.13335767292)
        state.set_current_position(10)

        terrain_condition = pyflowgo.flowgo_terrain_condition.FlowGoTerrainCondition()
        terrain_condition.read_initial_condition_from_json_file(filename)
        filename_dem = './resources/DEM_pdf2010_lidar.txt'
        terrain_condition.read_slope_from_file(filename_dem)

        vesicle_fraction_model_constant = pyflowgo.flowgo_vesicle_fraction_model_constant.FlowGoVesicleFractionModelConstant()
        vesicle_fraction_model_constant.read_initial_condition_from_json_file(filename)

        material_lava = pyflowgo.flowgo_material_lava.FlowGoMaterialLava(vesicle_fraction_model=vesicle_fraction_model_constant)
        material_lava.read_initial_condition_from_json_file(filename)

        flowgo_flux_conduction_heat = pyflowgo.flowgo_flux_conduction_heat.FlowGoFluxConductionHeat(material_lava)
        flowgo_flux_conduction_heat.read_initial_condition_from_json_file(filename)

        qcond = flowgo_flux_conduction_heat.compute_flux(state,
                                                         channel_width=6.20861841803369,
                                                         channel_depth=terrain_condition.get_channel_depth(10))

        self.assertAlmostEqual(qcond, 12513.32641041680, 10)

if __name__ == '__main__':
    unittest.main()
