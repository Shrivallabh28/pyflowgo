import math
import json

import pyflowgo.base.flowgo_base_melt_viscosity_model


class FlowGoMeltViscosityModelVFT(pyflowgo.base.flowgo_base_melt_viscosity_model.FlowGoBaseMeltViscosityModel):
    """ This function calculates the viscosity of the melt according to Giordano et al. 2008:

    log viscosity(Pa.s) = A + B / (T(K) - C),

    where A, B and C are adjustable parameters depending of the melt chemical composition<
    here the reads the A, B, C from the json file

    Input data
    -----------
    json file containing the A, B, C parameters (a_vft, b_vft, c_vft) in melt_viscosity_parameters

    variables
    -----------
    temperature of the lava interior : core_temperature

    Returns
    ------------
    the viscosity of the pure melt in Pa.s

    Reference
    ---------
    Giordano, D., Russell, J. K., & Dingwell, D. B. (2008). Viscosity of magmatic liquids: a model.
    Earth and Planetary Science Letters, 271(1), 123-134.

    """
    _a = -4.7
    _b = 5429.7
    _c = 595.5

    # faire le test de bien lire ces valeurs
    def read_initial_condition_from_json_file(self, filename):
        # read json parameters file
        with open(filename) as data_file:
            data = json.load(data_file)
            self._a = float(data['melt_viscosity_parameters']['a_vft'])
            self._b = float(data['melt_viscosity_parameters']['b_vft'])
            self._c = float(data['melt_viscosity_parameters']['c_vft'])

    def compute_melt_viscosity(self, state):

        core_temperature = state.get_core_temperature()

        melt_viscosity = 10 ** (self._a + self._b / (core_temperature - self._c))

        return melt_viscosity
