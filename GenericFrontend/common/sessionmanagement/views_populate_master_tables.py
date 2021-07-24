""" This module is used to populate all the master tables that belong to SessionManagement app"""

from common.utilities.populate_all_master_tables.populate_master_tables_lib import populate_master_data
from common.sessionmanagement.models import UserSessionsStatus
from common.sessionmanagement.serializers import UserSessionsStatusSerializer

def populate_session_management_master_tables(table_population_output_list):
    """
    This function populates all the master table data of the app named sessionmanagement
    This function will insert additional records. In case you want to update then it will update them as well
    :return:
    """
    try:
        # copy paste the below line for every master model that you want to populate for this app
        # Note the naming convention of the function below.
        # There has to be separate functions for each model, all written one below the other in this file.
        table_population_output_list = populate_user_session_status(table_population_output_list)
        return table_population_output_list

    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ["Failure", f"One or more master tables of SessionManagement app could not be populated."
                                           f"Exception encountered: {ex}", table_population_output_list]))
        return output_json


def populate_user_session_status(table_population_output_list):
    """
    This function populates the master table named UserSessionsStatus in the app named sessionmanagement
    :return:
    """
    try:
        # defining all the master table rows. This is the final data that should be there in the master table.
        # Hence write all information that you want to populate including the ones that are existing.
        # Remember to use the exact field names in this definition as it is defined in the respective model definitions.
        # Do not forget to keep the primary keys values in this list of dictionaries.
        # Also keep the same order in you want to populate the tables.
        # You may ignore to add values of fields that are auto populated,
        # or assigned default values in the db definition.
        # Do not define datetime values for such respective keys

        final_model_data = [
            {'status_id': 1, 'status_name': "Active"},
            {'status_id': 2, 'status_name': "Inactive"},
        ]

        # define the below mentioned parameters for this model
        primary_key_var = "status_id"
        model_name = "UserSessionsStatus"
        model_instance = UserSessionsStatus
        model_serializer_instance = UserSessionsStatusSerializer

        # do not change the piece of code below. Keep it as such
        populate_master_data_params = dict(zip(['primary_key_var', 'model_name', 'model_instance',
                                                'model_serializer_instance', 'final_model_data'],
                                               [primary_key_var, model_name, model_instance,
                                                model_serializer_instance, final_model_data]))
        output_json = populate_master_data(populate_master_data_params, table_population_output_list)
        return output_json

    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ["Failure", f"Exception encountered while calling function "
                                           f"to populate master table data: {ex}", None]))
        return output_json