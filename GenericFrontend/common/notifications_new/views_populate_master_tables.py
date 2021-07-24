""" This module is used to populate all the master tables that belong to this app"""

from common.utilities.populate_all_master_tables.populate_master_tables_lib import populate_master_data
from common.notifications_new.models import IndividualNotificationStatus, SuperNotificationStatus, NotificationType, \
    NotificationDistributionType
from common.notifications_new.serializers import IndividualNotificationStatusSerializer, SuperNotificationStatusSerializer,\
    NotificationTypeSerializer, NotificationDistributionTypeSerializer


def populate_notification_new_master_tables(table_population_output_list):
    """
    This function populates all the master table data of the app named notification_new
    This function will insert additional records. In case you want to update then it will update them as well
    :return:
    """
    try:
        # copy paste the below line for every master model that you want to populate for this app
        # Note the naming convention of the function below.
        # There has to be separate functions for each model, all written one below the other in this file.
        table_population_output_list = populate_individual_notification_status(table_population_output_list)
        table_population_output_list = populate_super_notification_status(table_population_output_list)
        table_population_output_list = populate_notification_type(table_population_output_list)
        table_population_output_list = populate_notification_distribution_type(table_population_output_list)

        return table_population_output_list

    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ["Failure", f"One or more master tables of timeline app could not be populated."
                                           f"Exception encountered: {ex}", table_population_output_list]))
        return output_json


def populate_individual_notification_status(table_population_output_list):
    """
    This function populates the master table named UserPortraitStatus in the app named notification_new
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
            {'status_id': 1, 'status_name': "Unseen"},
            {'status_id': 2, 'status_name': "Seen"},
            {'status_id': 3, 'status_name': "Read"}
        ]

        # define the below mentioned parameters for this model
        primary_key_var = "status_id"
        model_name = "IndividualNotificationStatus"
        model_instance = IndividualNotificationStatus
        model_serializer_instance = IndividualNotificationStatusSerializer

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


def populate_super_notification_status(table_population_output_list):
    """
    This function populates the master table named UserPortraitMediaStatus in the app named notification_new
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
            {'status_id': 2, 'status_name': "Inactive"}
        ]
        primary_key_var = "status_id"
        model_name = "SuperNotificationStatus"
        model_instance = SuperNotificationStatus
        model_serializer_instance = SuperNotificationStatusSerializer
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


def populate_notification_type(table_population_output_list):
    """
    This function populates the master table named UserPortraitMediaStatus in the app named notification_new
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
            {'type_id': 1, 'type_name': "Core"},
            {'type_id': 2, 'type_name': "User-Generated"}
        ]
        primary_key_var = "type_id"
        model_name = "NotificationType"
        model_instance = NotificationType
        model_serializer_instance = NotificationTypeSerializer
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


def populate_notification_distribution_type(table_population_output_list):
    """
    This function populates the master table named UserPortraitMediaStatus in the app named notification_new
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
            {'distribution_type_id': 1, 'distribution_type_name': "Individually-targetted"},
            {'distribution_type_id': 2, 'distribution_type_name': "Segment-targetted"},
            {'distribution_type_id': 3, 'distribution_type_name': "Generic"}
        ]
        primary_key_var = "distribution_type_id"
        model_name = "NotificationDistributionType"
        model_instance = NotificationDistributionType
        model_serializer_instance = NotificationDistributionTypeSerializer
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
