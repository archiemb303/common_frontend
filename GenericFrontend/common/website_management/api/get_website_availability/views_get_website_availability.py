"""This API will  return our website's live and state flags"""
import logging
from functools import wraps
import re
from rest_framework.views import APIView, Response
from common.apiauthentication.api.authenticateapi.views_authenticateapi import api_authenticate
from common.utilities.lib import sql_fetch_cursor

# Get an instance of a logger
logger = logging.getLogger("genericfrontend_1.0")


class GetWebsiteAvailabilityAPI(APIView):

    """This API will return our website's live and state flags"""
    # @api_authenticate
    def post(self, request):
        """Post function to return our website's live and state flags"""
        try:
            input_json, output_json = request.data, {}
            output_json['AvailabilityDetails'] = get_website_availability_json()
            output_json['AuthenticationDetails'] = dict(zip(['Status', 'Message'],
                                                            ["Success", "ApiDetails fine to process"]))
            return Response(output_json)
        except Exception as ex:
            output_json['AvailabilityDetails'] = dict(zip(["Status", "Message", "Payload"],
                                              ["Failure", f"Website availability could not be fetched. "
                                                          f"Exception encountered: {ex}", None]))
            return Response(output_json)


def get_website_availability_json():
    """
     JSON function to return our website's live and state flags
    :return:
    """
    try:
        # Get website availability status by calling sql proc
        website_availability_var = get_website_availability_sql()
        match = re.findall(r"'Status': 'Failure'", str(website_availability_var))
        if match:
            return website_availability_var
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ["Success", "Website Availability status fetched successfully",
                                dict(zip(['live_flag', 'state_flag'],
                                         [website_availability_var[0]['launch_flag'],
                                          website_availability_var[0]['state_flag']]))]))
        return output_json
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ['Failure', f"Website availability status could not be fetched. "
                                           f"Exception Encountered. {ex}", None]))
        return output_json


def get_website_availability_sql():
    """
    This function executes the sql function to get our website's availability
    :return:
    [{'launch_flag':1, 'state_flag':1}]
    """
    try:
        sql = sql_fetch_cursor("sp_fetch_website_maintenance_flags", 'call_ref',
                               ['call_ref'])
        return sql
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ['Failure', f"Website availability status could not be fetched from sql."
                                           f"Exception encountered: {ex}", None]))
        return output_json


def website_control(func):
    """Closure Function to fetch website availability."""

    @wraps(func)
    def website_control_json(self, request):
        """Function to fetch website availability"""
        try:
            website_status = get_website_availability_json()
            if website_status['Payload']['live_flag'] == 0:
                output_json = dict(zip(['AvailabilityDetails'],
                                       [dict(zip(['Status', 'Message', 'Payload'],
                                                 ['Failure', "We are coming soon. Please try later",
                                                  website_status['Payload']]))]))
                return Response(output_json)
            if website_status['Payload']['state_flag'] == 0:
                output_json = dict(zip(['AvailabilityDetails'],
                                       [dict(zip(['Status', 'Message', 'Payload'],
                                                 ['Failure', "We are undergoing maintenance. Please try later",
                                                  website_status['Payload']]))]))
                return Response(output_json)
            request.data['AvailabilityDetails'] = website_status
            return func(self, request)
        except Exception as ex:
            output_json = dict(zip(['AvailabilityDetails'],
                                   [dict(zip(['Status', 'Message', 'Payload'],
                                             ['Failure',
                                              f"Exception encountered while getting website availability: {ex}",
                                              dict(zip(['live_flag', 'state_flag'], [0, 0]))]))]))
            return Response(output_json)
    return website_control_json

