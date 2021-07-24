""" This module is used to populate all the master tables that belong to this app"""

from common.utilities.populate_all_master_tables.populate_master_tables_lib import populate_master_data
from common.apiauthentication.models import VendorStatus, TokenStatus, TokenType, Vendor, ApiTokens
from common.apiauthentication.serializers import VendorStatusSerializer, TokenTypeSerializer, TokenStatusSerializer,\
    VendorSerializer, ApiTokensSerializer


def populate_apiauthentication_master_tables(table_population_output_list):
    """
    This function populates all the master table data of the app named apiauthentication
    This function will insert additional records. In case you want to update then it will update them as well
    :return:
    """
    try:
        # copy paste the below line for every master model that you want to populate for this app
        # Note the naming convention of the function below.
        # There has to be separate functions for each model, all written one below the other in this file.
        table_population_output_list = populate_vendor_status(table_population_output_list)
        table_population_output_list = populate_token_status(table_population_output_list)
        table_population_output_list = populate_token_type(table_population_output_list)
        table_population_output_list = populate_vendor(table_population_output_list)
        table_population_output_list = populate_api_tokens(table_population_output_list)

        return table_population_output_list

    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ["Failure", f"One or more master tables of timeline app could not be populated."
                                           f"Exception encountered: {ex}", table_population_output_list]))
        return output_json


def populate_vendor_status(table_population_output_list):
    """
    This function populates the master table named VendorStatus in the app named apiauthentication
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
            {'status_id': 3, 'status_name': "PendingActivation"},
            {'status_id': 4, 'status_name': "Suspended"},
        ]

        # define the below mentioned parameters for this model
        primary_key_var = "status_id"
        model_name = "VendorStatus"
        model_instance = VendorStatus
        model_serializer_instance = VendorStatusSerializer

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


def populate_token_status(table_population_output_list):
    """
    This function populates the master table named TokenStatus in the app named apiauthentication
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
            {'status_id': 3, 'status_name': "PendingActivation"},
            {'status_id': 4, 'status_name': "Suspended"},
        ]
        primary_key_var = "status_id"
        model_name = "TokenStatus"
        model_instance = TokenStatus
        model_serializer_instance = TokenStatusSerializer  # Serializer is not there
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


def populate_token_type(table_population_output_list):
    """
    This function populates the master table named TokenType in the app named apiauthentication
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
            {'type_id': 1, 'type_name': "Webapp"},
            {'type_id': 2, 'type_name': "MobileApp"},
            {'type_id': 3, 'type_name': "RestAPIClient"},
        ]
        primary_key_var = "type_id"
        model_name = "TokenType"
        model_instance = TokenType
        model_serializer_instance = TokenTypeSerializer  # Serializer is not there
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


def populate_vendor(table_population_output_list):
    """
    This function populates the master table named Vendor in the app named apiauthentication
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
            {'vendor_id': 1, 'vendor_name': "genericfrontend", 'vendor_status': 1},
        ]

        # define the below mentioned parameters for this model
        primary_key_var = "vendor_id"
        model_name = "Vendor"
        model_instance = Vendor
        model_serializer_instance = VendorSerializer

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


def populate_api_tokens(table_population_output_list):
    """
    This function populates the master table named ApiTokens in the app named apiauthentication
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
            {'token_id': 1, 'token_string': "sdxfcgvbhjnmklasdfghjk", 'token_type': 1, 'token_vendor_id': 1,
             'token_status_id': 1},
        ]

        # define the below mentioned parameters for this model
        primary_key_var = "token_id"
        model_name = "ApiTokens"
        model_instance = ApiTokens
        model_serializer_instance = ApiTokensSerializer

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

