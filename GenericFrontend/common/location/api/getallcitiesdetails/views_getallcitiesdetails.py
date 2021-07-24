"""This api cover fetch all cities"""
from rest_framework.response import Response
from rest_framework.views import APIView
from common.apiauthentication.api.authenticateapi.views_authenticateapi import api_authenticate
from common.location.models import Cities
from common.location.serializers import CitiesSerializer


class GetAllCitiesAPI(APIView):
    """This api fetch all cities"""
    @api_authenticate
    def post(self, request):
        """This  API  cover for fetch all cities."""
        input_json, output_json = request.data["APIParams"], {}
        output_json['AuthenticationDetails'] = request.data['AuthenticationDetails']
        fetch_all_city = self.fetch_cities(input_json)
        if fetch_all_city.data['Status'] == "Success":
            payload_details = {
                'cities_details': fetch_all_city.data['cities']}
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], [
                'Success', 'Successfully retrieved cities.', payload_details]))
        return Response(output_json)

    def fetch_cities(self, request):
        """Function to add country into database."""
        output_json = {}
        try:

            serialized_var = CitiesSerializer(Cities.objects.all(), many=True)
            output_json = dict(
                zip(['Status', 'Message', 'cities'], ["Success", "Successfully retrieved Cities.", serialized_var.data]))
            return Response(output_json)
        except Exception as ex:
            output_json = dict(
                zip(['Status', 'Message'], ["Failure", f"Internal Database Error, operation failed: {ex}"]))
            return Response(output_json)
        return
