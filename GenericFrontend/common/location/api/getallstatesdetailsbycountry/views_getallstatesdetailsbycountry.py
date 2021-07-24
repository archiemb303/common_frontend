"""This  API  cover for fetch all states."""
from rest_framework.views import APIView
from rest_framework.response import Response
from common.commondecorators.preloginauthentications import common_pre_login_authentications
from common.utilities.lib import sql_exec


class GetAllStatesByCountryAPI(APIView):
    """This  API  cover for fetch all states."""
    @common_pre_login_authentications
    def post(self, request):
        """This  API  cover for fetch all states."""
        input_json = request.data["APIParams"]
        output_json = dict(zip(['AvailabilityDetails', 'AuthenticationDetails', 'Payload'],
                               [request.data['AvailabilityDetails'], request.data['AuthenticationDetails'], None]))
        fetch_all_state = self.fetch_states(input_json)

        payload_details = {
            'states_details': fetch_all_state}
        output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], [
            'Success', 'Successfully retrieved States.', payload_details]))

        return Response(output_json)

    def fetch_states(self, request):
        """Function to fetch states into database."""
        input_json, output_json = request, {}
        try:

            sql = sql_exec("fetch_states_by_countryid", [
                           input_json['country_id']])
            return sql

        except Exception as ex:
            output_json = dict(
                zip(['Status', 'Message'], ["Failure", f"Internal Database Error, operation failed: {ex}"]))
            return Response(output_json)
        return
