import pyflowgo.flowgo_terrain_condition
import pyflowgo.flowgo_model_factory
import pyflowgo.flowgo_integrator
import pyflowgo.flowgo_state
import pyflowgo.flowgo_logger

import json
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Gives the configuration file as input.')
    parser.add_argument('configuration_file', metavar='example_input_parameters.json', type=str, nargs=1,
                        help='the configuration file to be used by PyFlowGo')

    args = parser.parse_args()
    configuration_file = args.configuration_file[0]

    # ---------------------------------- LOAD CONFIGURATION FILE AND INPUT PARAMETERS ----------------------------------
    # TODO:choose the configuration file in the edit parameters

    # read json parameters file
    with open(configuration_file) as data_file:
        data = json.load(data_file)
        lava_name = data['lava_name']
        slope_file = data['slope_file']

    # ------------------------------------------------- DEFINE THE STEP ------------------------------------------------
    # TODO:choose your step in meter
    step_size = 10 # in meters

# --------------------------------- READ INITIAL CONFIGURATION FILE AND MODEL FACTORY ----------------------------------

    terrain_condition = pyflowgo.flowgo_terrain_condition.FlowGoTerrainCondition()
    terrain_condition.read_slope_from_file(slope_file)
    terrain_condition.read_initial_condition_from_json_file(configuration_file)

    models_factory = pyflowgo.flowgo_model_factory.FlowgoModelFactory(configuration_file, terrain_condition)

    #vesicle_fraction_model = models_factory.get_vesicle_fraction_model()
    #and why not:
    crust_temperature_model = models_factory.get_crust_temperature_model()

    effective_cover_crust_model = models_factory.get_effective_cover_crust_model()
    crystallization_rate_model = models_factory.get_crystallization_rate_model()
    material_lava = models_factory.get_material_lava()
    material_air = models_factory.get_material_air()
    heat_budget = models_factory.get_heat_budget()

    # ------------------------------------------ GENERATE THE INTEGRATOR -----------------------------------------------

    integrator = pyflowgo.flowgo_integrator.FlowGoIntegrator(step_size, material_lava=material_lava,
                                                             material_air=material_air,
                                                             terrain_condition=terrain_condition,
                                                             heat_budget=heat_budget,
                                                             crystallization_rate_model=crystallization_rate_model)
    integrator.read_initial_condition_from_json_file(configuration_file)

    # ------------------------------------------------- LOG THE DATA --------------------------------------------------

    logger = pyflowgo.flowgo_logger.FlowGoLogger()

    state = pyflowgo.flowgo_state.FlowGoState()
    integrator.initialize_state(state, configuration_file)

    while not integrator.has_finished():
        integrator.single_step(state)

    logger.write_values_to_file("results_"+str(lava_name).replace(" ", "_").lower() + "_"+ str(step_size) +"m.csv")