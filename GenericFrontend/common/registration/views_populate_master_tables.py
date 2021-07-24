""" This module is used to populate all the master tables that belong to this app"""

from common.utilities.populate_all_master_tables.populate_master_tables_lib import populate_master_data
from common.registration.models import Sources, SourceStatus, EmailVerificationStatus, MobileVerificationStatus,\
    UserProfileStatus, UserProfileCompletionStatus, DpFlag, UuidToProfileIdMapStatus, CaptchaStatus, WdSocialLoginSecretKeyStatus
from common.registration.serializers import SourceStatusSerializer, EmailVerificationStatusSerializer, SourcesSerializer, \
    MobileVerificationStatusSerializer, UserProfileStatusSerializer, UserProfileCompletionStatusSerializer, DpFlagSerializer, UuidToProfileIdMapStatusSerializer, CaptchaStatusSerializer, WdSocialLoginSecretKeyStatusSerializer


def populate_registration_master_tables(table_population_output_list):
    """
    This function populates all the master table data of the app named registration
    This function will insert additional records. In case you want to update then it will update them as well
    :return:
    """
    try:
        # copy paste the below line for every master model that you want to populate for this app
        # Note the naming convention of the function below.
        # There has to be separate functions for each model, all written one below the other in this file.
        table_population_output_list = populate_source_status(table_population_output_list)
        table_population_output_list = populate_Sources(table_population_output_list)
        table_population_output_list = populate_mobile_verification_status(table_population_output_list)
        table_population_output_list = populate_user_profile_status(table_population_output_list)
        table_population_output_list = populate_user_profile_completion_status(table_population_output_list)
        table_population_output_list = populate_dp_flag(table_population_output_list)
        table_population_output_list = populate_uuid_to_profile_id_map_status(table_population_output_list)
        table_population_output_list = populate_captcha_status(table_population_output_list)
        table_population_output_list = populate_wd_social_login_secret_key_status(table_population_output_list)

        return table_population_output_list

    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ["Failure", f"One or more master tables of registration app could not be populated."
                                           f"Exception encountered: {ex}", table_population_output_list]))
        return output_json


def populate_source_status(table_population_output_list):
    """
    This function populates the master table named SourceStatus in the app named registration
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
            {'status_id': 1, 'status_name': "Active", 'added_by': "genericfrontend", 'last_modified_by': "genericfrontend", 'history': "source Active"},
            {'status_id': 2, 'status_name': "Inactive", 'added_by': "genericfrontend", 'last_modified_by': "genericfrontend", 'history': "source Inactive"},
        ]

        # define the below mentioned parameters for this model
        primary_key_var = "status_id"
        model_name = "SourceStatus"
        model_instance = SourceStatus
        model_serializer_instance = SourceStatusSerializer

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


def populate_Sources(table_population_output_list):
    """
    This function populates the master table named Sources in the app named registration
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
            {'source_id': 1, 'source_name': "Native Email", 'added_by': "genericfrontend", 'last_modified_by': "genericfrontend",
             'history': "email updated", 'source_keys': "esdfghytgfvcxdzfsgtrfc", 'source_status': 1},

            {'source_id': 2, 'source_name': "Native Mobile", 'added_by': "genericfrontend", 'last_modified_by': "genericfrontend",
             'history': "mobile updated", 'source_keys': "drgtyrtgfdghyjuio7iuygf", 'source_status': 1},

            {'source_id': 3, 'source_name': "facebook", 'added_by': "genericfrontend", 'last_modified_by': "genericfrontend",
             'history': "facebook updated", 'source_keys': "drgthgfdsfrtyjytr", 'source_status': 1},

            {'source_id': 4, 'source_name': "Google", 'added_by': "genericfrontend", 'last_modified_by': "genericfrontend",
             'history': "google updated", 'source_keys': "qwertyuhgfgfrthryjt", 'source_status': 1},

            {'source_id': 5, 'source_name': "Twitter", 'added_by': "genericfrontend", 'last_modified_by': "genericfrontend",
             'history': "twitter updated", 'source_keys': "wertyghfhytui8uyhgfds", 'source_status': 1},

            {'source_id': 6, 'source_name': "Linkedin", 'added_by': "genericfrontend", 'last_modified_by': "genericfrontend",
             'history': "linkedin updated", 'source_keys': "dwergfddghyjuuytress", 'source_status': 1},
        ]

        # define the below mentioned parameters for this model
        primary_key_var = "source_id"
        model_name = "Sources"
        model_instance = Sources
        model_serializer_instance = SourcesSerializer

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


def populate_email_verification_Status(table_population_output_list):
    """
    This function populates the master table named EmailVerificationStatus in the app named registration
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
            {'status_id': 1, 'status_name': "Pending", 'added_by': "genericfrontend", 'last_modified_by': "genericfrontend",
             'history': "added by admin: genericfrontend"},

            {'status_id': 2, 'status_name': "Active", 'added_by': "genericfrontend", 'last_modified_by': "genericfrontend",
             'history': "added by admin: genericfrontend"},

            {'status_id': 3, 'status_name': "Inactive", 'added_by': "genericfrontend", 'last_modified_by': "genericfrontend",
             'history': "added by admin: genericfrontend"},

            {'status_id': 4, 'status_name': "Blocked", 'added_by': "genericfrontend", 'last_modified_by': "genericfrontend",
             'history': "added by admin: genericfrontend"},

            {'status_id': 5, 'status_name': "Work In Progress", 'added_by': "genericfrontend", 'last_modified_by': "genericfrontend",
             'history': "added by admin: genericfrontend"},

            {'status_id': 6, 'status_name': "Deactivated", 'added_by': "genericfrontend", 'last_modified_by': "genericfrontend",
             'history': "added by admin: genericfrontend"},

            {'status_id': 7, 'status_name': "Not All Parameter Passed", 'added_by': "genericfrontend", 'last_modified_by': "genericfrontend",
             'history': "added by admin: genericfrontend"},
        ]

        # define the below mentioned parameters for this model
        primary_key_var = "status_id"
        model_name = "EmailVerificationStatus"
        model_instance = EmailVerificationStatus
        model_serializer_instance = EmailVerificationStatusSerializer

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


def populate_mobile_verification_status(table_population_output_list):
    """
    This function populates the master table named MobileVerificationStatus in the app named registration
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
            {'status_id': 1, 'status_name': "Active", 'added_by': "genericfrontend", 'last_modified_by': "genericfrontend",},
            {'status_id': 2, 'status_name': "Inactive", 'added_by': "genericfrontend", 'last_modified_by': "genericfrontend"},
        ]

        # define the below mentioned parameters for this model
        primary_key_var = "status_id"
        model_name = "MobileVerificationStatus"
        model_instance = MobileVerificationStatus
        model_serializer_instance = MobileVerificationStatusSerializer

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


def populate_user_profile_status(table_population_output_list):
    """
    This function populates the master table named UserProfileStatus in the app named registration
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
            {'status_id': 1, 'status_name': "Active", 'added_by': "genericfrontend", 'last_modified_by': "genericfrontend",},
            {'status_id': 2, 'status_name': "Inactive", 'added_by': "genericfrontend", 'last_modified_by': "genericfrontend"},
        ]

        # define the below mentioned parameters for this model
        primary_key_var = "status_id"
        model_name = "UserProfileStatus"
        model_instance = UserProfileStatus
        model_serializer_instance = UserProfileStatusSerializer

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


def populate_user_profile_completion_status(table_population_output_list):
    """
    This function populates the master table named UserProfileCompletionStatus in the app named registration
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
            {'status_id': 1, 'status_name': "Completed", 'added_by': "genericfrontend", 'last_modified_by': "genericfrontend",},
            {'status_id': 2, 'status_name': "Incompleted", 'added_by': "genericfrontend", 'last_modified_by': "genericfrontend"},
        ]

        # define the below mentioned parameters for this model
        primary_key_var = "status_id"
        model_name = "UserProfileCompletionStatus"
        model_instance = UserProfileCompletionStatus
        model_serializer_instance = UserProfileCompletionStatusSerializer

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


def populate_dp_flag(table_population_output_list):
    """
    This function populates the master table named DpFlag in the app named registration
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
            {'flag_id': 1, 'flag_name': "Systemdefined", 'added_by': "genericfrontend", 'last_modified_by': "genericfrontend",},
            {'flag_id': 2, 'flag_name': "Userdefined", 'added_by': "genericfrontend", 'last_modified_by': "genericfrontend"},
        ]

        # define the below mentioned parameters for this model
        primary_key_var = "flag_id"
        model_name = "DpFlag"
        model_instance = DpFlag
        model_serializer_instance = DpFlagSerializer

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


def populate_uuid_to_profile_id_map_status(table_population_output_list):
    """
    This function populates the master table named UuidToProfileIdMapStatus in the app named registration
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
            {'status_id': 1, 'status_name': "Active", 'added_by': "genericfrontend", 'last_modified_by': "genericfrontend",},
            {'status_id': 2, 'status_name': "Inactive", 'added_by': "genericfrontend", 'last_modified_by': "genericfrontend"},
        ]

        # define the below mentioned parameters for this model
        primary_key_var = "status_id"
        model_name = "UuidToProfileIdMapStatus"
        model_instance = UuidToProfileIdMapStatus
        model_serializer_instance = UuidToProfileIdMapStatusSerializer

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


def populate_captcha_status(table_population_output_list):
    """
    This function populates the master table named CaptchaStatus in the app named registration
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
            {'status_id': 1, 'status_name': "Active", 'added_by': "genericfrontend", 'last_modified_by': "genericfrontend",},
            {'status_id': 2, 'status_name': "Inactive", 'added_by': "genericfrontend", 'last_modified_by': "genericfrontend"},
        ]

        # define the below mentioned parameters for this model
        primary_key_var = "status_id"
        model_name = "CaptchaStatus"
        model_instance = CaptchaStatus
        model_serializer_instance = CaptchaStatusSerializer

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


def populate_wd_social_login_secret_key_status(table_population_output_list):
    """
    This function populates the master table named WdSocialLoginSecretKeyStatus in the app named registration
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
            {'status_id': 1, 'status_name': "Active", 'added_by': "genericfrontend", 'last_modified_by': "genericfrontend",},
            {'status_id': 2, 'status_name': "Inactive", 'added_by': "genericfrontend", 'last_modified_by': "genericfrontend"},
        ]

        # define the below mentioned parameters for this model
        primary_key_var = "status_id"
        model_name = "WdSocialLoginSecretKeyStatus"
        model_instance = WdSocialLoginSecretKeyStatus
        model_serializer_instance = WdSocialLoginSecretKeyStatusSerializer

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

