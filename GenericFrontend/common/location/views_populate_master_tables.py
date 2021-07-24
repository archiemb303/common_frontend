""" This module is used to populate all the master tables that belong to this app"""

from common.utilities.populate_all_master_tables.populate_master_tables_lib import populate_master_data
from common.location.models import Currencies, Geos
from common.location.serializers import CurrenciesSerializer, GeosSerializer


def populate_location_master_tables(table_population_output_list):
    """
    This function populates all the master table data of the app named location
    This function will insert additional records. In case you want to update then it will update them as well
    :return:
    """
    try:
        # copy paste the below line for every master model that you want to populate for this app
        # Note the naming convention of the function below.
        # There has to be separate functions for each model, all written one below the other in this file.
        table_population_output_list = populate_currencies(table_population_output_list)
        table_population_output_list = populate_geos(table_population_output_list)

        return table_population_output_list

    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ["Failure", f"One or more master tables of location app could not be populated."
                                           f"Exception encountered: {ex}", table_population_output_list]))
        return output_json


def populate_currencies(table_population_output_list):
    """
    This function populates the master table named Currencies in the app named location
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
            {'currency_id': 1, 'currency_name': "Credit Point", 'value_of_one_credit_point': 1},
            {'currency_id': 2, 'currency_name': "INR", 'value_of_one_credit_point': 0.9999},
            {'currency_id': 3, 'currency_name': "USD", 'value_of_one_credit_point': 0.0149},
            {'currency_id': 4, 'currency_name': "EUR", 'value_of_one_credit_point': 0.0149},
            {'currency_id': 5, 'currency_name': "AED", 'value_of_one_credit_point': 0.0499},
            {'currency_id': 6, 'currency_name': "AUD", 'value_of_one_credit_point': 0.0199},
            {'currency_id': 7, 'currency_name': "SGD", 'value_of_one_credit_point': 0.0199},
            {'currency_id': 8, 'currency_name': "CNY", 'value_of_one_credit_point': 0.0999},
            {'currency_id': 9, 'currency_name': "JPY", 'value_of_one_credit_point': 1.4999},
            {'currency_id': 10, 'currency_name': "GBP", 'value_of_one_credit_point': 0.0149},
        ]

        # define the below mentioned parameters for this model
        primary_key_var = "currency_id"
        model_name = "Currencies"
        model_instance = Currencies
        model_serializer_instance = CurrenciesSerializer

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


def populate_geos(table_population_output_list):
    """
    This function populates the master table named Geos in the app named location
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
            {'geo_id': 1, 'geo_name': "Online", 'geo_currency': "", 'tax_percentage': 0},  # geo_currency is ForeignKey
            {'geo_id': 2, 'geo_name': "Indian Subcontinent", 'geo_currency': "", 'tax_percentage': 18},
            {'geo_id': 3, 'geo_name': "US and Canada", 'geo_currency': "", 'tax_percentage': 0},
            {'geo_id': 4, 'geo_name': "Europe", 'geo_currency': "", 'tax_percentage': 0},
            {'geo_id': 5, 'geo_name': "UK", 'geo_currency': "", 'tax_percentage': 0},
            {'geo_id': 6, 'geo_name': "Middle East", 'geo_currency': "", 'tax_percentage': 5},
            {'geo_id': 7, 'geo_name': "Australia", 'geo_currency': "", 'tax_percentage': 0},
            {'geo_id': 8, 'geo_name': "South East Asia", 'geo_currency': "", 'tax_percentage': 0},
            {'geo_id': 9, 'geo_name': "China", 'geo_currency': "", 'tax_percentage': 0},
            {'geo_id': 10, 'geo_name': "Japan", 'geo_currency': "", 'tax_percentage': 0},
            {'geo_id': 11, 'geo_name': "Credit Point", 'geo_currency': "", 'tax_percentage': 0},
            {'geo_id': 12, 'geo_name': "Credit Point", 'geo_currency': "", 'tax_percentage': 0},
            {'geo_id': 13, 'geo_name': "Credit Point", 'geo_currency': "", 'tax_percentage': 0},




        ]

        # define the below mentioned parameters for this model
        primary_key_var = "geo_id"
        model_name = "Geos"
        model_instance = Geos
        model_serializer_instance = GeosSerializer

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
