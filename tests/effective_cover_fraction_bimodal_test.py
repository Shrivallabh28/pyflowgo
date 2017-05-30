import unittest
import pyflowgo.flowgo_material_lava
import pyflowgo.flowgo_state
import pyflowgo.flowgo_vesicle_fraction_model_constant
import pyflowgo.flowgo_relative_viscosity_model_er
import pyflowgo.flowgo_melt_viscosity_model_vft
import pyflowgo.flowgo_yield_strength_model_basic
import pyflowgo.flowgo_terrain_condition
import pyflowgo.flowgo_effective_cover_crust_model_bimodal
import json


class MyTestCase(unittest.TestCase):
    def test_read_initial_condition_from_json_file(self):
        filename = './resources/input_parameters_effective_cover_crust_bimodal.json'
        terrain_condition = pyflowgo.flowgo_terrain_condition.FlowGoTerrainCondition()
        material_lava = pyflowgo.flowgo_material_lava.FlowGoMaterialLava()
        effective_cover_crust_model_bimodal = pyflowgo.flowgo_effective_cover_crust_model_bimodal.\
            FlowGoEffectiveCoverCrustModelBimodal(terrain_condition,material_lava)
        effective_cover_crust_model_bimodal.read_initial_condition_from_json_file(filename)

    def test_compute_effective_cover_fraction(self):
        filename = './resources/input_parameters_effective_cover_crust_bimodal.json'
        terrain_condition = pyflowgo.flowgo_terrain_condition.FlowGoTerrainCondition()
        material_lava = pyflowgo.flowgo_material_lava.FlowGoMaterialLava()
        state = pyflowgo.flowgo_state.FlowGoState()

        terrain_condition.read_initial_condition_from_json_file(filename)
        filename_dem = './resources/DEM_pdf2010_lidar.txt'
        terrain_condition.read_slope_from_file(filename_dem)

        state = pyflowgo.flowgo_state.FlowGoState()


        melt_viscosity_model_vft = pyflowgo.flowgo_melt_viscosity_model_vft.FlowGoMeltViscosityModelVFT()
        melt_viscosity_model_vft.read_initial_condition_from_json_file(filename)

        relative_viscosity_model_er = pyflowgo.flowgo_relative_viscosity_model_er.FlowGoRelativeViscosityModelER()
        relative_viscosity_model_er.read_initial_condition_from_json_file(filename)

        vesicle_fraction_model_constant = pyflowgo.flowgo_vesicle_fraction_model_constant.\
            FlowGoVesicleFractionModelConstant()
        vesicle_fraction_model_constant.read_initial_condition_from_json_file(filename)

        yield_strength_model_basic = pyflowgo.flowgo_yield_strength_model_basic.FlowGoYieldStrengthModelBasic()
        yield_strength_model_basic.read_initial_condition_from_json_file(filename)

        material_lava = pyflowgo.flowgo_material_lava.FlowGoMaterialLava(melt_viscosity_model=melt_viscosity_model_vft,
                                                                         relative_viscosity_model=relative_viscosity_model_er,
                                                                         yield_strength_model=yield_strength_model_basic,
                                                                         vesicle_fraction_model=vesicle_fraction_model_constant)
        material_lava.read_initial_condition_from_json_file(filename)
        mean_velocity = material_lava.compute_mean_velocity(state, terrain_condition)
        print(mean_velocity)

        effective_cover_crust_model_bimodal = pyflowgo.flowgo_effective_cover_crust_model_bimodal.\
            FlowGoEffectiveCoverCrustModelBimodal(terrain_condition,material_lava)
        effective_cover_crust_model_bimodal.read_initial_condition_from_json_file(filename)

        state.set_core_temperature(1387.13335767292)
        state.set_crystal_fraction(0.104)
        state.set_current_position(10)
        effective_cover_fraction = effective_cover_crust_model_bimodal.compute_effective_cover_fraction(state)
        self.assertAlmostEqual(effective_cover_fraction, 0.968487820088, 10)

        state.set_core_temperature(1387.07761422317)
        state.set_crystal_fraction(0.104332974207)
        state.set_current_position(30)
        effective_cover_fraction = effective_cover_crust_model_bimodal.compute_effective_cover_fraction(state)
        self.assertAlmostEqual(effective_cover_fraction, 0.809856902811,10)

if __name__ == '__main__':
    unittest.main()
