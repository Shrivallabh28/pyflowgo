import json
import math
import pyflowgo.flowgo_state

import pyflowgo.base.flowgo_base_crust_temperature_model


class FlowGoCrustTemperatureModelHR2001(pyflowgo.base.flowgo_base_crust_temperature_model.
                                     FlowGoBaseCrustTemperatureModel):
    """
    This method  "HR2001" allows the crust temperature to decrease downflow ain the same way as the core temperature is
    decreasing as applied by Harris and Rowland (2001):

    crust_temperature = core_temperature - 712


    Input data
    -----------
    json file containing the crust_temperature

    variables
    -----------

    Returns
    ------------
    crust temperature in K

    References
    ---------


    """

    _crust_temperature = 425 + 273.15

    def read_initial_condition_from_json_file(self, filename):
        # read json parameters file
        with open(filename) as data_file:
            data = json.load(data_file)
            self._crust_temperature = float(data['thermal_parameters']['crust_temperature'])

    def compute_crust_temperature(self, state):

        crust_temperature = 0.

        #if (current_time / 3600 >= 0.00001):

        core_temperature = state.get_core_temperature()
        #for COLD ML84
        self._crust_temperature = core_temperature - 712.0

        # for HOT ML84
        #self._crust_temperature = core_temperature - 468.0

        return self._crust_temperature


