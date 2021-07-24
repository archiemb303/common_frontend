"""
This API finds user's geo information by either their ip or by the information provided by user in his profile
"""
import logging
import re
from rest_framework.views import APIView, Response
from common.commondecorators.postloginauthentications import common_post_login_authentications
from common.location.specificlib.views_lib import get_user_country_from_ip, get_user_geo_by_name_iso, \
    get_user_geo_from_profile
# Get an instance of a logger

logger = logging.getLogger("genericfrontend_1.0")


class GetUserGeosAPI(APIView):
    """This covers the API for fetching all support centre tickets raised by the user"""
    @common_post_login_authentications
    def post(self, request):
        """Post Function to fetching common questions based on ticket type."""
        input_json = request.data
        output_json = dict(zip(['AvailabilityDetails', 'AuthenticationDetails', 'Payload'],
                               [request.data['AvailabilityDetails'], request.data['AuthenticationDetails'], None]))
        if 'APIParams' not in input_json or 'user_ip' not in input_json['APIParams']:
            # uncomment this part for local and comment it for staging/production
            user_ip_var = None
            # uncomment this part for local and comment it for staging/production

            # uncomment this part for staging/production and comment it for local
            # x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            # user_ip_var = x_forwarded_for.split(',')[0]
            # uncomment this part for staging/production and comment it for local
        else:
            user_ip_var = input_json['APIParams']['user_ip']
        json_params = dict(zip(['profile_id', 'user_ip'],
                               [input_json['SessionDetails']['Payload']['profile_id'],
                                user_ip_var]))
        output_json['Payload'] = self.get_user_geos_json(json_params)
        return Response(output_json)

    def get_user_geos_json(self, request):
        """
        this function calls third party API to get user's country from ip_address in case user_ip
        is provided in the input. If user_ip is not provided or the third party API returns incorrect or no response,
        then this function finds the user's geo based on the his city id as provided during registration or
        as updated by him in his profile.
        :param request: {"profile_id": "1", "user_ip":"192.168.0.1"}
        :return: {
                    "Status": "Success",
                    "Message": "ticket types and respective questions Fetched successfully",
                    "Payload": {
                        "geo_id": 2,
                        "geo_name": "Indian Subcontinent",
                        "geo_currency": "INR"
                }
        """
        input_json, user_geo_details = request, dict()
        try:
            # if user_ip is provided then it takes it to make third party call, else gets users geo info from profile
            if input_json['user_ip']:
                third_party_params = dict(zip(['ip_address'], [input_json['user_ip']]))
                third_party_response = get_user_country_from_ip(third_party_params)
                match = re.findall(r"'Status': 'Failure'", str(third_party_response))
                if not match:
                    # third party api has returned an iso2 value of user's country
                    iso_vars = {"iso3": "", "iso2": third_party_response['Payload'], "country_name": ""}
                    user_geo_details = get_user_geo_by_name_iso(iso_vars)
                    match = re.findall(r"'Status': 'Failure'", str(user_geo_details))
                    if not match:
                        # iso2 provided by third party matches with a record in our db
                        output_json = user_geo_details
                        return output_json
            # third party api was either not used or it gave an incorrect output that we can do nothing with it.
            # So we falling back on the location as provided by the user in his profile information/
            user_geo_details = get_user_geo_from_profile(input_json)
            match = re.findall(r"'Status': 'Failure'", str(user_geo_details))
            if match:
                output_json = user_geo_details
                return output_json
            output_json = user_geo_details
            return output_json
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ["Failure", f"User geo could not be fetched. Exception encountered: {ex}", None]))
            return output_json
