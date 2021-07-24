""" This module is used to populate all master tables across all apps"""
from rest_framework.response import Response
from rest_framework.views import APIView
# from common.apiauthentication.views_populate_master_tables import populate_apiauthentication_master_tables
from common.registration.views_populate_master_tables import populate_registration_master_tables
from common.apiauthentication.api.authenticateapi.views_authenticateapi import api_authenticate
from common.location.views_populate_master_tables import populate_location_master_tables

from common.notifications_new.views_populate_master_tables import populate_notification_new_master_tables

# from common.staffmanagement.staffregister.views_populate_master_tables import populate_staff_register_master_tables
from common.supportcentre.views_populate_master_tables import populate_support_centre_master_tables

from common.media.views_populate_master_tables import populate_media_master_tables

from common.sessionmanagement.views_populate_master_tables import populate_session_management_master_tables

from common.website_management.views_populate_master_tables import populate_website_management_master_tables


class PopulateAllMasterTablesAPI(APIView):
    """
    API that updates all master tables as defined in their
    respective views_populate_master_tables.py
    """
    @api_authenticate
    def post(self, request):
        """
        Post function of the api call that updates all master tables as defined in their
        respective views_populate_master_tables.py
        :param request: {APIDetails:{}}
        :return:
        """
        output_json = dict()
        output_json['AuthenticationDetails'] = request.data['AuthenticationDetails']
        try:
            output_json['Payload'] = populate_all_master_tables()
            return Response(output_json)
        except Exception as ex:
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'],
                                              ["Failure", f"Master Table population could not be completed "
                                                          f"at post function level. Exception encountered: {ex}",
                                               None]))
            return Response(output_json)


def populate_all_master_tables():
    """
    This function runs population of master tables one by one across all django apps that are registered here
    :return:
    """
    try:
        table_population_output_list = []
        # populating master table for each django app one by one.
        # copy paste the below line for every app
        # note the function name. There has to be function with this naming convention
        # in each app views_populate_master_tables.py file
        # table_population_output_list = populate_website_management_master_tables(table_population_output_list)
        # table_population_output_list = populate_apiauthentication_master_tables(table_population_output_list)
        table_population_output_list = populate_session_management_master_tables(table_population_output_list)
        table_population_output_list = populate_location_master_tables(table_population_output_list)
        table_population_output_list = populate_registration_master_tables(table_population_output_list)
        table_population_output_list = populate_notification_new_master_tables(table_population_output_list)
        # table_population_output_list = populate_staff_register_master_tables(table_population_output_list)
        table_population_output_list = populate_support_centre_master_tables(table_population_output_list)
        # table_population_output_list = populate_apiauthentication_master_tables(table_population_output_list)
        table_population_output_list = populate_registration_master_tables(table_population_output_list)
        table_population_output_list = populate_location_master_tables(table_population_output_list)
        table_population_output_list = populate_media_master_tables(table_population_output_list)

        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ["Success", "Master Table population completed", table_population_output_list]))
        return output_json
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ["Failure", f"Master Table population could not be completed. "
                                           f"Exception encountered: {ex}", None]))
        return output_json
