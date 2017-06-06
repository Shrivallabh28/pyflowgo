import math
import json
import pyflowgo.flowgo_logger

import pyflowgo.base.flowgo_base_yield_strength_model

class FlowGoYieldStrengthModelDragoni(pyflowgo.base.flowgo_base_yield_strength_model.FlowGoBaseYieldStrengthModel):
        # using T liquidus instead of T erupt as given in HArris and Rowland 2015
        # TODO: here I add the log
    def __init__(self):
        self.logger = pyflowgo.flowgo_logger.FlowGoLogger()

    def read_initial_condition_from_json_file(self, filename):
            # read json parameters file
        with open(filename) as data_file:
            data = json.load(data_file)
            self._liquidus_temperature = float(data['lava_state']['liquidus_temperature'])

    def compute_yield_strength(self, state, eruption_temperature):
        # yield_strength is tho_0
        b = 0.01  # Constant B given by Dragoni, 1989[Pa]
        c = 0.08  # Constant C given by Dragoni, 1989[K-1]
        #liquidus_temperature = 1393.15
        core_temperature = state.get_core_temperature()
        crystal_fraction = state.get_crystal_fraction()

        # the new yield strength is calculated using this new T and the corresponding slope:
        tho_0 = b * (math.exp(c * (self._liquidus_temperature - core_temperature) - 1.)) + (6500. * (crystal_fraction ** 2.85))
       # print(tho_0)
        # TODO: here I add the log
        self.logger.add_variable("tho_0", state.get_current_position(),tho_0)

        return tho_0

    def compute_basal_shear_stress(self, state, terrain_condition, material_lava):
        #basal_shear_stress is tho_b

        g = terrain_condition.get_gravity(state.get_current_position)
        #print('g =', str(g))
        bulk_density = material_lava.get_bulk_density(state)
        #print('bulk_density =', str(bulk_density))
        channel_depth = terrain_condition.get_channel_depth(state.get_current_position())
        channel_slope = terrain_condition.get_channel_slope(state.get_current_position())

        tho_b = channel_depth * bulk_density * g * math.sin(channel_slope)
        # TODO: here I add the log
        self.logger.add_variable("tho_b", state.get_current_position(),tho_b)

        return tho_b