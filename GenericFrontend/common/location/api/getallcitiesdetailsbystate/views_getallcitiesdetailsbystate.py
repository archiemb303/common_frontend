"""This api cover fetch all cities"""
from rest_framework.response import Response
from rest_framework.views import APIView
from common.commondecorators.preloginauthentications import common_pre_login_authentications
from common.utilities.lib import sql_exec


class GetAllCitiesByStateAPI(APIView):
    """This api fetch all cities"""
    @common_pre_login_authentications
    def post(self, request):
        """This  API  cover for fetch all cities."""
        input_json = request.data["APIParams"]
        output_json = dict(zip(['AvailabilityDetails', 'AuthenticationDetails', 'Payload'],
                               [request.data['AvailabilityDetails'], request.data['AuthenticationDetails'], None]))
        fetch_all_city = self.fetch_cities(input_json)
        payload_details = {
            'cities_details': fetch_all_city}
        output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], [
            'Success', 'Successfully retrieved cities.', payload_details]))
        return Response(output_json)

    def fetch_cities(self, request):
        """Function to add country into database."""
        input_json, output_json = request, {}
        try:
            sql = sql_exec("fetch_cities_by_stateid", [
                           input_json['state_id']])
            return sql
        except Exception as ex:
            output_json = dict(
                zip(['Status', 'Message'], ["Failure", f"Internal Database Error, operation failed: {ex}"]))
            return Response(output_json)
        return
