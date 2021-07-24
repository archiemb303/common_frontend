import re
from datetime import datetime
from common.utilities.lib import sql_fetch_cursor, serializer_save, update_record
from common.supportcentre.models import PostLoginTickets
from common.supportcentre.serializers import PostLoginTicketsSerializer, PostLoginTicketsRepliesSerializer
from django.db.models import F


def fetch_all_ticket_type_and_questions_sql(request):
    """
    This function returns all ticket types and their respective questions
    :param request: none
    :return:
    """

    output_json = {}
    try:
        sql = sql_fetch_cursor("sp_fetch_all_ticket_types_and_questions", 'profile_ref',
                               ['profile_ref'])
        return sql
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ['Failure',
                                f"Unable to fetch ticket types and respective questions. Exception encountered: {ex}",
                                None]))
        return output_json


def fetch_all_ticket_type_and_questions_format(request):
    """ This function formats the output of the sql function named fetch_all_ticket_type_and_questions_sql"""
    input_json = request
    try:
        if input_json:
            distinct_query_type_ids = list(set([x['type_id'] for x in input_json]))
            formatted_output = []
            for item in distinct_query_type_ids:
                # initializing for each ticket_type
                type_details = dict(zip(['query_type_id'], [item]))
                type_details['query_type_name'] = [x['type_name'] for x in input_json if x['type_id'] == item][0]
                type_details['common_questions'] = []
                # initializing for each question respective to ticket_type
                common_questions_var = [[x['common_question_id'], x['common_question_text']] for x in input_json if
                                        x['type_id'] == item]
                for jitem in common_questions_var:
                    question_details = dict(zip(['question_id', 'question_text'], [jitem[0], jitem[1]]))
                    type_details['common_questions'].append(question_details)
                formatted_output.append(type_details)

            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ['Success', 'query types and respective questions fetched successfully',
                                    formatted_output]))
            return output_json
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ['Failure', "No ticket type has been defined in the db yet", 0]))
        return output_json
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ['Failure',
                                f"Unable to format sql output to required json.Exception encountered: {ex}",
                                None]))
        return output_json


def fetch_questions_by_ticket_type_sql(request):
    """
    this function returns all common questiosn that are specific to provided ticket type
    :param request: {'ticket_type':1}
    :return:
    """
    input_json = request
    output_json = {}
    try:
        sql = sql_fetch_cursor("sp_fetch_questions_by_ticket_type", 'profile_ref',
                               ['profile_ref', input_json['ticket_type_id']])
        return sql
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ['Failure',
                                f"Unable to fetch ticket types and respective questions. Exception encountered: {ex}",
                                None]))
        return output_json


def raise_ticket_for_logged_in_user(request):
    """
    This function does the support centre ticket insertion db operation
    :param request:{
                            'profile_id': 1,
                            'raised_by':1,
                            'ticket_details':{
                                        "ticket_type_id": 1,
                                        "ticket_question_id": 2,
                                        "subject": "I want to check this out",
                                        "query": "Wow, you guys are so awesome"
                                }
                        }
    :return:
    """
    input_json = request
    try:
        ticekt_details_var = input_json['ticket_details']
        insert_api_params_var = dict(zip(['ticket_type', 'ticket_question',
                                          'ticket_subject', 'ticket_query',
                                          'ticket_owner', 'ticket_status',
                                          'added_by', 'last_modified_by'],
                                         [
                                             ticekt_details_var['ticket_type_id'],
                                             ticekt_details_var['ticket_question_id'],
                                             ticekt_details_var['subject'], ticekt_details_var['query'],
                                             input_json['profile_id'], 1,
                                             input_json['raised_by'], input_json['raised_by']
                                         ]))

        if input_json['ticket_details']['ticket_question_id'] == 0:
            insert_api_params_var['ticket_question'] = None

        # saving the data from front end form into the database
        serializer_var = serializer_save(
            PostLoginTicketsSerializer, insert_api_params_var)
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ['Success', 'Ticket successfully raised', serializer_var.data]))
        return output_json

    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ["Success", f"Ticket could not be raised. Exception encountered: {ex}", None]))
        return output_json


def fetch_all_tickets_sql(request):
    """
    this function fetches all tickets generated in the system
    :param request: {'profile_id':1}
    :return:
    """
    output_json = dict()
    try:
        sql = sql_fetch_cursor("sp_fetch_all_tickets", 'ticket_ref',
                               ['ticket_ref'])
        return sql
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ["Failure", f"Unable to fetch all tickets. Exception encountered: {ex}",
                                None]))

        return output_json


def fetch_all_ticket_for_user_sql(request):
    """
    this function returns all common questiosn that are specific to provided ticket type
    :param request: {'profile_id':1}
    :return:
    """
    input_json, output_json = request, dict()
    try:
        sql = sql_fetch_cursor("fetch_all_ticket_for_user", 'profile_ref',
                               ['profile_ref', input_json['profile_id']])
        return sql
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ["Failure", f"Unable to fetch tickets raised by user. Exception encountered: {ex}",
                                None]))

        return output_json


def format_all_ticket_for_user(request):
    """
    This function formats the sql output of fetch_all_ticket_for_user_sql and returns the first three replies
    :param request:
    [
                {
                    "ticket_id": 2,
                    "ticket_subject": "Token of appreciation",
                    "ticket_query": "You are awesome",
                    "ticket_status_id": 1,
                    "ticket_type_id": 1,
                    "ticket_question_id": 2,
                    "added_date": "2020-08-14T15:35:19.330201Z",
                    "last_modified_date": "2020-08-14T15:35:19.330201Z",
                    "status_name": "Fresh",
                    "type_name": "How to use",
                    "common_question_text": "question text is12",
                    "reply_id": 3,
                    "ticket_reply": "ghjgfhjdgfh",
                    "reply_date":"2020-09-01T21:32:32.32323232Z"
                },
                {
                    "ticket_id": 2,
                    "ticket_subject": "Token of appreciation",
                    "ticket_query": "You are awesome",
                    "ticket_status_id": 1,
                    "ticket_type_id": 1,
                    "ticket_question_id": 2,
                    "added_date": "2020-08-14T15:35:19.330201Z",
                    "last_modified_date": "2020-08-14T15:35:19.330201Z",
                    "status_name": "Fresh",
                    "type_name": "How to use",
                    "common_question_text": "question text is12",
                    "reply_id": 2,
                    "ticket_reply": "sadfgasdfasdf",
                    "reply_date":"2020-09-01T21:32:32.32323232Z"
                },
                {
                    "ticket_id": 1,
                    "ticket_subject": "Test Subject",
                    "ticket_query": "Just testing the waters",
                    "ticket_status_id": 1,
                    "ticket_type_id": 1,
                    "ticket_question_id": 2,
                    "added_date": "2020-08-14T15:30:17.826072Z",
                    "last_modified_date": "2020-08-14T15:30:17.826072Z",
                    "status_name": "Fresh",
                    "type_name": "How to use",
                    "common_question_text": "question text is12",
                    "reply_id": 1,
                    "ticket_reply": "sadfgasdfasdf",
                    "reply_date":"2020-09-01T21:32:32.32323232Z"
                }
            ]
    :return:
        [
                {
                    "ticket_id": 2,
                    "ticket_subject": "Token of appreciation",
                    "ticket_query": "You are awesome",
                    "ticket_status_id": 1,
                    "ticket_type_id": 1,
                    "ticket_question_id": 2,
                    "added_date": "2020-08-14T15:35:19.330201Z",
                    "last_modified_date": "2020-08-14T15:35:19.330201Z",
                    "status_name": "Fresh",
                    "type_name": "How to use",
                    "common_question_text": "question text is12",
                    "ticket_replies":[
                        {
                            "reply_id": 3,
                            "ticket_reply": "ghjgfhjdgfh",
                            "reply_date":"2020-09-01T21:32:32.32323232Z"
                        },
                        {
                            "reply_id": 2,
                            "ticket_reply": "sadfgasdfasdf",
                            "reply_date":"2020-09-01T21:32:32.32323232Z"
                        }
                    ]
                },

                {
                    "ticket_id": 1,
                    "ticket_subject": "Test Subject",
                    "ticket_query": "Just testing the waters",
                    "ticket_status_id": 1,
                    "ticket_type_id": 1,
                    "ticket_question_id": 2,
                    "added_date": "2020-08-14T15:30:17.826072Z",
                    "last_modified_date": "2020-08-14T15:30:17.826072Z",
                    "status_name": "Fresh",
                    "type_name": "How to use",
                    "common_question_text": "question text is12",
                    "ticket_replies":[
                        {
                            "reply_id": 1,
                            "ticket_reply": "sadfgasdfasdf",
                            "reply_date":"2020-09-01T21:32:32.32323232Z"
                        }
                    ]
                }
            ]

    """
    input_json, formatted_output, ticket_id_formatted = request, [], []
    ticket_id_list = list(set([int(x['ticket_id']) for x in input_json]))
    try:
        for item in ticket_id_list:
            if item in ticket_id_formatted:
                continue
            item_details = [x for x in input_json if x['ticket_id'] == item][0]
            ticket_details = dict(
                zip(['ticket_id', 'ticket_subject', 'ticket_query', 'ticket_status_id', 'ticket_type_id',
                     'ticket_question_id', 'ticket_owner_name', 'added_date', 'last_modified_date', 'status_name',
                     'type_name', 'common_question_text', 'last_action_date', 'ticket_replies'],
                    [item_details['ticket_id'], item_details['ticket_subject'], item_details['ticket_query'],
                     item_details['ticket_status_id'], item_details['ticket_type_id'],
                     item_details['ticket_question_id'],item_details['ticket_owner_name'],
                     item_details['added_date'], item_details['last_modified_date'], item_details['status_name'],
                     item_details['type_name'], item_details['common_question_text'], item_details['reply_date'], []]))
            ticket_details_list = [[x['reply_id'], x['ticket_reply'], x['reply_date'], x['replied_by']]
                                   for x in input_json if x['ticket_id'] == item]
            if ticket_details_list[0][0] is not None and ticket_details_list[0][1] is not None:
                sorted_ticket_details_list = sorted(ticket_details_list, key=lambda i: i[2])
                for jitem in sorted_ticket_details_list:
                    reply_details = dict(zip(['reply_id', 'ticket_reply', 'reply_date', 'replied_by'],
                                             [jitem[0], jitem[1], jitem[2], 'Staff']))
                    if int(item_details['ticket_owner_id']) == jitem[3]:
                        reply_details['replied_by'] = "User"
                    ticket_details['ticket_replies'].append(reply_details)
            formatted_output.append(ticket_details)
        sorted_formatted_output = sorted(formatted_output, key=lambda i: i['last_action_date'])
        output_json = dict(zip(['Status', 'Message', 'Payload'], ['Success', 'Ticket list formatted successfully',
                                                                  sorted_formatted_output]))
        return output_json
    except Exception as ex:
        output_json = dict(
            zip(['Status', 'Message', 'Payload'], ['Failure', 'Ticket list could not be formatted', ex]))
        return output_json


def get_ticket_replies_sql(request):
    """
    this function returns ticket details along with all its replies for the given ticket_id
    :param request: {'profile_id':1, 'ticket_id' = 1}
    :return:
    """
    input_json, output_json = request, dict()
    try:
        sql = sql_fetch_cursor("fetch_ticket_replies", 'profile_ref',
                               ['profile_ref', input_json['ticket_id']])
        return sql
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ["Failure",
                                f"Unable to fetch ticket details and its replies by user. Exception encountered: {ex}",
                                None]))

        return output_json


def get_ticket_replies_format(request):
    """
    this function takes the output from get_ticket_replies_sql function and then formats it
    :param request:
    :return:
    """
    try:
        input_json, ticket_basic_info, output_json = request, request[0], dict(zip(['Status', 'Message', 'Payload'],
                                                                                   ['Success',
                                                                                    'Ticket details formatted successfully',
                                                                                    dict()]))
        output_json['Payload']['ticket_details'] = dict(zip(['ticket_id', 'ticket_owner_name', 'ticket_subject',
                                                             'ticket_query', 'ticket_status_id', 'ticket_status',
                                                             'ticket_type', 'ticket_sub_type', 'ticket_date'],
                                                            [ticket_basic_info['ticket_id'],
                                                             ticket_basic_info['ticket_owner_name'],
                                                             ticket_basic_info['ticket_subject'],
                                                             ticket_basic_info['ticket_query'],
                                                             ticket_basic_info['ticket_status_id'],
                                                             ticket_basic_info['status_name'],
                                                             ticket_basic_info['type_name'],
                                                             ticket_basic_info['common_question_text'],
                                                             ticket_basic_info['added_date']]))
        output_json['Payload']['ticket_replies'] = []
        ticket_replies_list = [[x['reply_id'], x['ticket_reply'], x['reply_date'], x['replied_by']] for x in input_json]
        ticket_reply_check = ticket_replies_list[0]
        if ticket_reply_check[0] is not None and ticket_reply_check[1] is not None:
            sorted_ticket_details_list = sorted(ticket_replies_list, key=lambda i: i[2])
            for item in sorted_ticket_details_list:
                reply_details = dict(zip(['reply_id', 'ticket_reply', 'reply_date', 'replied_by'],
                                         [item[0], item[1], item[2], 'Staff']))
                if int(ticket_basic_info['ticket_owner_id']) == item[3]:
                    reply_details['replied_by'] = "User"
                output_json['Payload']['ticket_replies'].append(reply_details)
        return output_json
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ["Failure",
                                f"Exception encountered while formatting data from db: {ex}",
                                None]))
        return output_json


def check_if_ticket_owner_sql(request):
    """
        This function checks if user is the ticket owner
        :param request: {'profile_id': 186,
                         'ticket_id':1}
        """
    input_json, output_json = request, {}
    try:
        sql = sql_fetch_cursor("sp_check_if_ticket_owner", 'ticket_ref',
                               ['ticket_ref', input_json['profile_id'], input_json['ticket_id']])
        return sql
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'], ["Failure",
                                                                  f"Exception Encountered while "
                                                                  f"fetching details: {ex} ", None]))
        return output_json


def reply_to_ticket(request):
    """
    This function adds reply to given ticket.
    :param request:{
                            'profile_id': 1,
                            'ticket_id':1,
                            'reply_body'
                        }
    :return:
    """
    input_json = request
    try:
        insert_api_params_var = dict(zip(['ticket_id', 'ticket_reply',
                                          'added_by', 'last_modified_by'],
                                         [
                                             input_json['ticket_id'], input_json['reply_body'],
                                             input_json['profile_id'], input_json['profile_id']
                                         ]))
        # saving the data from front end into the database
        serializer_var = serializer_save(
            PostLoginTicketsRepliesSerializer, insert_api_params_var)
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ['Success', 'Ticket is successfully replied ', serializer_var.data]))
        return output_json

    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ["Success", f"Ticket could not be replied. Exception encountered: {ex}", None]))
        return output_json


def get_new_ticket_status(request):
    """
    This function decides new ticket status according to current ticket status and user type
    :param request:{
                            'ticket_id':1,
                            'user_type':'staff'/'ticket-owner',
                            'closing_flag':0/1,
                            'current_ticket_status':1
                        }
    :return:
    """
    input_json = request
    try:
        new_ticket_status = input_json['current_ticket_status']
        if input_json['user_type'] == 'ticket-owner':
            if input_json['current_ticket_status'] != 1:
                new_ticket_status = 4
            if input_json["closing_flag"] == 1:
                new_ticket_status = 5
        if input_json['user_type'] == 'staff':
            new_ticket_status = 3
            if input_json["closing_flag"] == 1:
                new_ticket_status = 6
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ['Success', 'New ticket status is created ', new_ticket_status]))
        return output_json

    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ["Success", f"Exception encountered: {ex}", None]))
        return output_json


def update_ticket_status(request):
    """
    This function updates ticket status for the ticket
    :param request: {'profile_id': 186}
    """
    input_json, output_json = request, {}
    try:
        update_record_var = update_record(PostLoginTickets, input_json['ticket_id'],
                                          ticket_status_id=input_json['new_ticket_status'])
        return update_record_var
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                  f"Exception Encountered while "
                                                                  f"fetching details: {ex} ", None]))
        return output_json


def fetch_ticket_details(request):
    """
        This function fetches ticket details for a ticket.
        :param request: {'ticket_id':1}
        """
    input_json, output_json = request, {}
    try:
        sql = sql_fetch_cursor("sp_fetch_ticket_details", 'ticket_ref',
                               ['ticket_ref', input_json['ticket_id']])
        return sql[0]
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'], ["Failure",
                                                                  f"Exception Encountered while "
                                                                  f"fetching details: {ex} ", None]))
        return output_json


def filter_all_tickets_sql(request):
    """
    this function fetches all tickets generated in the system
    :param request: {'search_query':'test ticket'}
    :return:
    """
    input_json, output_json = request, dict()
    try:
        sql = sql_fetch_cursor("sp_filter_all_tickets", 'ticket_ref',
                               ['ticket_ref', f"%{input_json['search_query']}%"])
        return sql
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ["Failure", f"Unable to fetch all tickets. Exception encountered: {ex}",
                                None]))

        return output_json


def filter_all_ticket_for_user_sql(request):
    """
    this function returns all common questiosn that are specific to provided ticket type
    :param request: {'profile_id':1}
    :return:
    """
    input_json, output_json = request, dict()
    try:
        sql = sql_fetch_cursor("filter_all_ticket_for_user", 'profile_ref',
                               ['profile_ref', input_json['profile_id'], f"%{input_json['search_query']}%"])
        return sql
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ["Failure", f"Unable to fetch tickets raised by user. Exception encountered: {ex}",
                                None]))

        return output_json

