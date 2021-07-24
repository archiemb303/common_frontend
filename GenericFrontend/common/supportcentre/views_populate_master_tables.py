""" This module is used to populate all the master tables that belong to this app"""

from common.utilities.populate_all_master_tables.populate_master_tables_lib import populate_master_data
from common.supportcentre.models import PostLoginTicketStatus, PostLoginTicketTypes, \
    PostLoginCommonQuestionsByTicketTypes
from common.supportcentre.serializers import PostLoginTicketStatusSerializer, PostLoginTicketTypesSerializer, \
    PostLoginCommonQuestionsByTicketTypesSerializer


def populate_support_centre_master_tables(table_population_output_list):
    """
    This function populates all the master table data of the app named supportcentre
    This function will insert additional records. In case you want to update then it will update them as well
    :return:
    """
    try:
        # copy paste the below line for every master model that you want to populate for this app
        # Note the naming convention of the function below.
        # There has to be separate functions for each model, all written one below the other in this file.
        table_population_output_list = populate_post_login_ticket_status(table_population_output_list)
        table_population_output_list = populate_post_login_ticket_types(table_population_output_list)
        table_population_output_list = populate_post_login_common_questions_by_ticket_types(table_population_output_list)

        return table_population_output_list

    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ["Failure", f"One or more master tables of timeline app could not be populated."
                                           f"Exception encountered: {ex}", table_population_output_list]))
        return output_json


def populate_post_login_ticket_status(table_population_output_list):
    """
    This function populates the master table named UserPortraitStatus in the app named supportcentre
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
            {'status_id': 1, 'status_name': 'Fresh'},
            {'status_id': 2, 'status_name': 'Deprecated'},
            {'status_id': 3, 'status_name': 'Open-Answered'},
            {'status_id': 4, 'status_name': 'Open-Unanswered'},
            {'status_id': 5, 'status_name': 'Closed by owner'},
            {'status_id': 6, 'status_name': 'Closed by staff'}
        ]

        # define the below mentioned parameters for this model
        primary_key_var = "status_id"
        model_name = "PostLoginTicketStatus"
        model_instance = PostLoginTicketStatus
        model_serializer_instance = PostLoginTicketStatusSerializer

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


def populate_post_login_ticket_types(table_population_output_list):
    """
    This function populates the master table named UserPortraitMediaStatus in the app named supportcentre
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
            {'type_id': 1, 'type_name': 'How to use', 'added_by': 'management', 'last_modified_by': 'management'},
            {'type_id': 2, 'type_name': 'Profile related', 'added_by': 'management',
             'last_modified_by': 'management'},
            {'type_id': 3, 'type_name': 'Media related', 'added_by': 'management', 'last_modified_by': 'management'},
            {'type_id': 4, 'type_name': 'Timeline related', 'added_by': 'management',
             'last_modified_by': 'management'},
            {'type_id': 5, 'type_name': 'DP related', 'added_by': 'management', 'last_modified_by': 'management'},
            {'type_id': 6, 'type_name': 'Vitals related', 'added_by': 'management', 'last_modified_by': 'management'},
            {'type_id': 7, 'type_name': 'Skills related', 'added_by': 'management', 'last_modified_by': 'management'},
            {'type_id': 8, 'type_name': 'Wallet related', 'added_by': 'management', 'last_modified_by': 'management'},
            {'type_id': 9, 'type_name': 'I want to suggest improvements', 'added_by': 'management',
             'last_modified_by': 'management'},
            {'type_id': 10, 'type_name': 'Others', 'added_by': 'management', 'last_modified_by': 'management'}
        ]
        primary_key_var = "type_id"
        model_name = "PostLoginTicketTypes"
        model_instance = PostLoginTicketTypes
        model_serializer_instance = PostLoginTicketTypesSerializer
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


def populate_post_login_common_questions_by_ticket_types(table_population_output_list):
    """
    This function populates the master table named UserPortraitMediaStatus in the app named supportcentre
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
            {'common_question_id': 1, 'common_question_text': 'question text is11', 'added_by': 'management',
             'last_modified_by': 'management', 'ticket_type_id': '1'},
            {'common_question_id': 2, 'common_question_text': 'question text is12', 'added_by': 'management',
             'last_modified_by': 'management', 'ticket_type_id': '1'},
            {'common_question_id': 3, 'common_question_text': 'question text is13', 'added_by': 'management',
             'last_modified_by': 'management', 'ticket_type_id': '1'},
            {'common_question_id': 4, 'common_question_text': 'question text is21', 'added_by': 'management',
             'last_modified_by': 'management', 'ticket_type_id': '2'},
            {'common_question_id': 5, 'common_question_text': 'question text is22', 'added_by': 'management',
             'last_modified_by': 'management', 'ticket_type_id': '2'},
            {'common_question_id': 6, 'common_question_text': 'question text is23', 'added_by': 'management',
             'last_modified_by': 'management', 'ticket_type_id': '2'},
            {'common_question_id': 7, 'common_question_text': 'question text is31', 'added_by': 'management',
             'last_modified_by': 'management', 'ticket_type_id': '3'},
            {'common_question_id': 8, 'common_question_text': 'question text is32', 'added_by': 'management',
             'last_modified_by': 'management', 'ticket_type_id': '3'},
            {'common_question_id': 9, 'common_question_text': 'question text is33', 'added_by': 'management',
             'last_modified_by': 'management', 'ticket_type_id': '3'},
            {'common_question_id': 10, 'common_question_text': 'question text is41', 'added_by': 'management',
             'last_modified_by': 'management', 'ticket_type_id': '4'},
            {'common_question_id': 11, 'common_question_text': 'question text is42', 'added_by': 'management',
             'last_modified_by': 'management', 'ticket_type_id': '4'},
            {'common_question_id': 12, 'common_question_text': 'question text is43', 'added_by': 'management',
             'last_modified_by': 'management', 'ticket_type_id': '4'},
            {'common_question_id': 13, 'common_question_text': 'question text is51', 'added_by': 'management',
             'last_modified_by': 'management', 'ticket_type_id': '5'},
            {'common_question_id': 14, 'common_question_text': 'question text is52', 'added_by': 'management',
             'last_modified_by': 'management', 'ticket_type_id': '5'},
            {'common_question_id': 15, 'common_question_text': 'question text is53', 'added_by': 'management',
             'last_modified_by': 'management', 'ticket_type_id': '5'},
            {'common_question_id': 16, 'common_question_text': 'question text is61', 'added_by': 'management',
             'last_modified_by': 'management', 'ticket_type_id': '6'},
            {'common_question_id': 17, 'common_question_text': 'question text is62', 'added_by': 'management',
             'last_modified_by': 'management', 'ticket_type_id': '6'},
            {'common_question_id': 18, 'common_question_text': 'question text is63', 'added_by': 'management',
             'last_modified_by': 'management', 'ticket_type_id': '6'},
            {'common_question_id': 19, 'common_question_text': 'question text is71', 'added_by': 'management',
             'last_modified_by': 'management', 'ticket_type_id': '7'},
            {'common_question_id': 20, 'common_question_text': 'question text is72', 'added_by': 'management',
             'last_modified_by': 'management', 'ticket_type_id': '7'},
            {'common_question_id': 21, 'common_question_text': 'question text is73', 'added_by': 'management',
             'last_modified_by': 'management', 'ticket_type_id': '7'},
            {'common_question_id': 22, 'common_question_text': 'question text is81', 'added_by': 'management',
             'last_modified_by': 'management', 'ticket_type_id': '8'},
            {'common_question_id': 23, 'common_question_text': 'question text is82', 'added_by': 'management',
             'last_modified_by': 'management', 'ticket_type_id': '8'},
            {'common_question_id': 24, 'common_question_text': 'question text is83', 'added_by': 'management',
             'last_modified_by': 'management', 'ticket_type_id': '8'},
            {'common_question_id': 25, 'common_question_text': 'question text is91', 'added_by': 'management',
             'last_modified_by': 'management', 'ticket_type_id': '9'},
            {'common_question_id': 26, 'common_question_text': 'question text is92', 'added_by': 'management',
             'last_modified_by': 'management', 'ticket_type_id': '9'},
            {'common_question_id': 27, 'common_question_text': 'question text is93', 'added_by': 'management',
             'last_modified_by': 'management', 'ticket_type_id': '9'},
            {'common_question_id': 28, 'common_question_text': 'others', 'added_by': 'management',
             'last_modified_by': 'management', 'ticket_type_id': '1'},
            {'common_question_id': 29, 'common_question_text': 'others', 'added_by': 'management',
             'last_modified_by': 'management', 'ticket_type_id': '2'},
            {'common_question_id': 30, 'common_question_text': 'others', 'added_by': 'management',
             'last_modified_by': 'management', 'ticket_type_id': '3'},
            {'common_question_id': 31, 'common_question_text': 'others', 'added_by': 'management',
             'last_modified_by': 'management', 'ticket_type_id': '4'},
            {'common_question_id': 32, 'common_question_text': 'others', 'added_by': 'management',
             'last_modified_by': 'management', 'ticket_type_id': '5'},
            {'common_question_id': 33, 'common_question_text': 'others', 'added_by': 'management',
             'last_modified_by': 'management', 'ticket_type_id': '6'},
            {'common_question_id': 34, 'common_question_text': 'others', 'added_by': 'management',
             'last_modified_by': 'management', 'ticket_type_id': '7'},
            {'common_question_id': 35, 'common_question_text': 'others', 'added_by': 'management',
             'last_modified_by': 'management', 'ticket_type_id': '8'},
            {'common_question_id': 36, 'common_question_text': 'others', 'added_by': 'management',
             'last_modified_by': 'management', 'ticket_type_id': '9'},
            {'common_question_id': 37, 'common_question_text': 'others', 'added_by': 'management',
             'last_modified_by': 'management', 'ticket_type_id': '10'}

        ]
        primary_key_var = "common_question_id"
        model_name = "PostLoginCommonQuestionsByTicketTypes"
        model_instance = PostLoginCommonQuestionsByTicketTypes
        model_serializer_instance = PostLoginCommonQuestionsByTicketTypesSerializer
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
