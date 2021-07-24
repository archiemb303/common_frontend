"""Module to validate session details for verified users."""
import logging
from functools import wraps
from rest_framework.views import Response
from django.utils.crypto import get_random_string
from common.utilities.lib import sql_exec
from common.sessionmanagement.api.sessioncontrol.validations_sessioncontrol import ValidationsSessionCheckJson
# Get an instance of a logger
logger = logging.getLogger("genericfrontend_1.0")


def session_control(func):
    """Closure Function to validate session details for verified users."""
    @wraps(func)
    def session_control_json(self, request):
        """Function to validate session details for verified users."""
        input_json, output_json, vendor_id = request.data['SessionDetails'], {}, \
            request.data['APIDetails']['token_vendor_id']
        input_json['vendor_id'], output_json['AvailabilityDetails'], output_json['AuthenticationDetails'] = \
            vendor_id, request.data['AvailabilityDetails'], request.data['AuthenticationDetails']
        # Validate session management input json APIParams.
        validation_check_var = ValidationsSessionCheckJson.validations_session_check_json_function(
            self, input_json)
        if validation_check_var['Status'] == "Failure":
            output_json = validation_check_var
            return Response(output_json)
        try:
            # Fetch session details for a given session id from UserSessions table.
            sql = sql_exec("fetch_session_row", [input_json['session_id']])[0]
            status_id = sql['status_id_id']
            if status_id == 2:
                output_json['SessionDetails'] = dict(zip(['Status', 'Message'],
                                                         ['Failure', "given session is already logged out."]))
                return Response(output_json)
            profile_id, session_key, status_id, session_id = input_json['profile_id'], input_json['session_key'], \
                sql['status_id_id'], sql['session_id']
            if sql['profile_id'] == profile_id and sql['session_key'] == session_key and sql['status_id_id'] == 1:
                session_var = dict(zip(['status_id', 'session_key', 'profile_id'],
                                       [1, get_random_string(length=32), input_json["profile_id"]]))

                profile_id, session_key, status_id, session_id, vendor_id = \
                    session_var['profile_id'], session_var['session_key'], session_var['status_id'], \
                    sql['session_id'], input_json['vendor_id']
                # update session details record in UserSessions table.
                sql_update = sql_exec("update_session", [
                                      session_id, profile_id, status_id, vendor_id, session_key])[0]
                logger.info(
                    f"Updating session details for session management table: {sql_update} ")
                new_session = dict(zip(["profile_id", "session_id", "session_key"],
                                       [session_var["profile_id"], sql["session_id"], session_var["session_key"]]))
                if status_id == 1:
                    output_json = dict(zip(['Status', 'Message', 'Payload'],
                                           ['Success', "session is active. session details updated", new_session
                                            ]))
                    request.data['SessionDetails'] = output_json
                    return func(self, request)
                output_json['SessionDetails'] = dict(zip(['Status', 'Message', 'Payload'],
                                                         ['Failure', "Error encountered while updating session details",
                                                          None]))
                return Response(output_json)

            # logging out the existing session since the keys did not match
            session_var = dict(zip(['status_id', 'session_key', 'profile_id'],
                                   [2, input_json['session_key'], input_json["profile_id"]]))
            profile_id, session_key, status_id, session_id, vendor_id = \
                session_var['profile_id'], session_var['session_key'], session_var['status_id'], \
                sql['session_id'], input_json['vendor_id']
            # update session details record in UserSessions table.
            sql_update = sql_exec("update_session", [
                session_id, profile_id, status_id, vendor_id, session_key])[0]
            logger.info(
                f"Updating session details for session management table: {sql_update} ")
            updated_session = dict(zip(["profile_id", "session_id", "session_key"],
                                   [session_var["profile_id"], sql["session_id"], session_var["session_key"]]))
            output_json['SessionDetails'] = dict(zip(['Status', 'Message', 'Payload'],
                                                     ['Failure', "Invalid session details, "
                                                                 "hence user has been logged out ", updated_session]))
            return Response(output_json)
        except Exception as ex:
            output_json['SessionDetails'] = dict(zip(['Status', 'Message', 'Payload'],
                                                     ['Failure', "Invalid Entry for session details " + str(ex), None]))
            return Response(output_json)
    return session_control_json


def session_form_control(func):
    """Closure Function to validate session details for verified users."""
    @wraps(func)
    def session_form_control_json(self, request):
        """Function to validate session details for verified users."""
        input_json, output_json = request.data.dict(), {}
        input_json['profile_id'], input_json['session_id'], input_json['vendor_id'] = int(input_json['profile_id']), \
            int(input_json['session_id']),\
            int(input_json['token_vendor_id'])
        # Validate session management input json APIParams.
        validation_check_var = ValidationsSessionCheckJson.validations_session_check_json_function(
            self, input_json)
        if validation_check_var['Status'] == "Failure":
            output_json = validation_check_var
            return Response(output_json)
        try:
            # Fetch session details for a given session id from UserSessions table.
            sql = sql_exec("fetch_session_row", [input_json['session_id']])[0]
            status_id = sql['status_id_id']

            if status_id == 2:
                output_json['SessionDetails'] = dict(zip(['Status', 'Message'],
                                                         ['Failure', "Looks like the user is already logged out."]))
                return Response(output_json)
            profile_id, session_key, status_id, session_id = \
                input_json['profile_id'], input_json['session_key'], sql['status_id_id'], sql['session_id']
            if sql['profile_id'] == profile_id and sql['session_key'] == session_key and sql['status_id_id'] == 1:
                session = dict(zip(['status_id', 'session_key', 'profile_id'],
                                   [1, get_random_string(length=32), input_json["profile_id"]]))

                profile_id, session_key, status_id, session_id, vendor_id = \
                    session['profile_id'], session['session_key'], session['status_id'], sql['session_id'], \
                    input_json['vendor_id']
                # update session details record in UserSessions table.
                sql_update = sql_exec(
                    "update_session", [session_id, profile_id, status_id, vendor_id, session_key])[0]
                logger.info(
                    f"Updating session details for session management table: {sql_update} ")
                new_session = dict(zip(["profile_id", "session_id", "session_key"],
                                       [session["profile_id"], sql["session_id"], session["session_key"]]))
                if status_id == 1:
                    output_json = dict(zip(['Status', 'Message', 'Payload'],
                                           ['Success', "session is active. session details updated", new_session
                                            ]))
                    request.data['SessionDetails'] = output_json
                    return func(self, request)
                output_json = dict(zip(['Status', 'Message', 'Payload'],
                                       ['Failure', "Error encountered while updating session details",
                                        None]))
                return Response(output_json)
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ['Failure', "Issues while updating session details", None]))
            return Response(output_json)
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ['Failure', "Invalid Entry for session details " + str(ex), None]))
            return Response(output_json)
    return session_form_control_json


def session_control_search(func):
    """Closure Function to validate session details for verified users."""
    @wraps(func)
    def session_control_search_json(self, request):
        """Function to validate session details for verified users."""
        input_json, output_json, vendor_id = request.data['SessionDetails'], {}, \
                                             request.data['APIDetails']['token_vendor_id']
        input_json['vendor_id'], output_json['AuthenticationDetails'] = vendor_id, request.data['AuthenticationDetails']
        # Validate session management input json APIParams.
        validation_check_var = ValidationsSessionCheckJson.validations_session_check_json_function(
            self, input_json)
        if validation_check_var['Status'] == "Failure":
            output_json = validation_check_var
            return Response(output_json)
        try:
            # Fetch session details for a given session id from UserSessions table.
            sql = sql_exec("fetch_session_row", [input_json['session_id']])[0]
            status_id = sql['status_id_id']
            if status_id == 2:
                output_json['SessionDetails'] = dict(zip(['Status', 'Message'],
                                                         ['Failure', "Looks like the user is already logged out."]))
                return Response(output_json)
            profile_id, session_key, status_id, session_id = input_json['profile_id'], input_json['session_key'], \
                                                             sql['status_id_id'], sql['session_id']
            if sql['profile_id'] == profile_id and sql['session_key'] == session_key and sql['status_id_id'] == 1:
                session_var = dict(zip(['status_id', 'session_key', 'profile_id'],
                                       [1, session_key, input_json["profile_id"]]))

                profile_id, session_key, status_id, session_id, vendor_id = \
                    session_var['profile_id'], session_var['session_key'], session_var['status_id'], \
                    sql['session_id'], input_json['vendor_id']
                # update session details record in UserSessions table.
                # sql_update = sql_exec("update_session", [
                #     session_id, profile_id, status_id, vendor_id, session_key])[0]
                # logger.info(
                #     f"Updating session details for session management table: {sql_update} ")
                new_session = dict(zip(["profile_id", "session_id", "session_key"],
                                       [session_var["profile_id"], sql["session_id"], session_var["session_key"]]))
                if status_id == 1:
                    output_json = dict(zip(['Status', 'Message', 'Payload'],
                                           ['Success', "session is active. session details updated", new_session
                                            ]))
                    request.data['SessionDetails'] = output_json
                    return func(self, request)
                output_json['SessionDetails'] = dict(zip(['Status', 'Message', 'Payload'],
                                                         ['Failure', "Error encountered while updating session details",
                                                          None]))
                return Response(output_json)
            output_json['SessionDetails'] = dict(zip(['Status', 'Message', 'Payload'],
                                                     ['Failure', "Issues while updating session details", None]))
            return Response(output_json)
        except Exception as ex:
            output_json['SessionDetails'] = dict(zip(['Status', 'Message', 'Payload'],
                                                     ['Failure', "Invalid Entry for session details " + str(ex), None]))
            return Response(output_json)
    return session_control_search_json