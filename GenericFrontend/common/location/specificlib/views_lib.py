from rest_framework.views import APIView
import re
import requests
from common.location.models import Cities
from common.utilities.lib import sql_fetch_cursor


class ValidateCity(APIView):
    def validate_city_function(self, request, format='json'):
        input_json = request
        output_json={}
        try:
            city_check = Cities.objects.filter(city_id = input_json)
            if not len(city_check):
                output_json['Status'] = "Failure"
                output_json['Message'] = "city code is invalid"
                return output_json

            output_json['Status'] = "Success"
            output_json['Message'] = "city code validated"
            return output_json

        except Exception as ex:
            output_json['Status'] = "Failure"
            output_json['Message'] = "city code invalid.Exception encountered: "
            return output_json


def get_user_country_from_ip(request):
    """
    This function makes an API call to the third party service provider and returns the response appropriately
    :param request:{'ip_address': '43.224.158.170'}
    :return:
    """
    try:
        input_json = request
        ipify_api_url = f"https://geo.ipify.org/api/v1?apiKey=at_qsLfESUSFyxiGcwyaxA85tiMnmW4d&ipAddress={input_json['ip_address']}"
        api_request_output = requests.get(ipify_api_url)
        user_country_iso2 = api_request_output.json()['location']['country']
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ['Success', 'Ticket raised successfully. Please check your inbox for update',
                                user_country_iso2]))
        return output_json
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ['Failure', f"API could not be called Successfully. Exception encountered: {ex}", None]))
        return output_json


def get_user_geo_by_name_iso(request):
    """
    this function checks gets user's location details based on the following keys in the same order of priority.
    ISO3, ISO2, country_name
    :param request: {"iso3":"IND", "iso2":"IN", "country_name": "India"}
    :return:
    """
    try:
        input_json, query_params = request, dict(zip(['iso3', 'iso2', 'country_name'], [None, None, None]))
        if 'iso3' in input_json:
            query_params['iso3'] = input_json['iso3']
        if 'iso2' in input_json:
            query_params['iso2'] = input_json['iso2']
        if 'country_name' in input_json:
            query_params['country_name'] = input_json['country_name']
        user_geo_details_var = get_user_geo_from_iso_name_sql(query_params)
        match = re.findall(r"'Status': 'Failure'", str(user_geo_details_var))
        if match:
            return user_geo_details_var
        if len(user_geo_details_var) > 0:
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ["Success", "Users country details fetched successfully from third party api",
                                user_geo_details_var[0]]))
            return output_json
        if len(user_geo_details_var) == 0:
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ['Failure', "No matching country found for the given IP", None]))
            return output_json
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ["Failure", f"Unable to find country for the given IP. Exception Encountered: {ex}",
                                None]))
        return output_json


def get_user_geo_from_profile(request):
    """
    This function takes in the user profile and returns all geo information including currency for the user
    :param request: {"profile_id" : 159}
    :return:
    """
    try:
        input_json = request
        user_geo_details_var = get_user_geo_from_profile_sql(input_json)
        match = re.findall(r"'Status': 'Failure'", str(user_geo_details_var))
        if match:
            return user_geo_details_var
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ["Success", "Users country details fetched successfully from userprofile details",
                                user_geo_details_var[0]]))
        return output_json
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ["Failure", f"Unable to Users country details from userprofile details. "
                                           f"Exception Encountered: {ex}", None]))
        return output_json


def get_user_geo_from_profile_sql(request):
    """
    this function does sql operation to get geo details of given profile_id
    :param request: {'profile_id':1}
    :return:
    """
    input_json, output_json = request, dict()
    try:
        sql = sql_fetch_cursor("fetch_user_location_by_profile_id", 'profile_ref',
                               ['profile_ref', input_json['profile_id']])
        return sql
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ["Failure", f"Unable to fetch geo details by user profile id. "
                                           f"Exception encountered: {ex}", None]))
        return output_json


def get_user_geo_from_iso_name_sql(request):
    """
    this function does sql operation to get geo details of given profile_id
    :param request: {'iso3':"IND", 'iso2':"IN", "country_name": "India"}
    :return:
    """
    input_json, output_json = request, dict()
    try:
        sql = sql_fetch_cursor("fetch_user_location_by_iso_country_name", 'profile_ref',
                               ['profile_ref', input_json['iso3'], input_json['iso2'], input_json['country_name']])
        return sql
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ["Failure", f"Unable to fetch geo details by iso and country name. "
                                           f"Exception encountered: {ex}", None]))
        return output_json


def get_currency_id_from_text_sql(request):
    """
    this function takes currency initials and finds the currency id
    :param request: {"currency_text": INR}
    :return:
    """
    input_json, output_json = request, dict()
    try:
        sql = sql_fetch_cursor("sp_fetch_currency_id_from_text", 'profile_ref',
                               ['profile_ref', input_json['currency_text']])
        return sql
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ["Failure", f"Unable to fetch currency id from currency_text. "
                                           f"Exception encountered: {ex}", None]))
        return output_json


def get_all_currencies_sql():
    """
        this function returns all entries in the currencies table
        :param request:
        :return:
        """
    try:
        sql = sql_fetch_cursor("sp_fetch_all_currencies", 'profile_ref',
                               ['profile_ref'])
        return sql
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ["Failure", f"Unable to fetch all currencies. "
                                           f"Exception encountered: {ex}", None]))
        return output_json
