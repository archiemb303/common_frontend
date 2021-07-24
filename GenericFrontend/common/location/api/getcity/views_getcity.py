"""This  API  cover for fetch particular city"""
from rest_framework.views import APIView
from rest_framework.response import Response
from apiauthentication.api.authenticateapi.views_authenticateapi import api_authenticate
from common.location.models import Cities
from common.location.serializers import CitiesAndStatesSerializer
from common.location.api.getcity.validations_getcity import validation_getcity


class GetCityAPI(APIView):
    """This  API  cover for fetch  partcular city."""
    @api_authenticate
    @validation_getcity
    def post(self, request):
        """This  API  cover for fetch  partcular city."""
        input_json, output_json = request.data["APIParams"], {}
        output_json['AuthenticationDetails'] = request.data['AuthenticationDetails']
        fetch_city = self.fetch_city(input_json)
        if fetch_city.data['Status'] == "Success":
            payload_details = {
                'cities_details': fetch_city.data['cities']}
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], [
                'Success', 'Successfully retrieved cities.', payload_details]))
        return Response(output_json)

    def fetch_city(self, request):
        """Function to fetch partcular city into database."""
        output_json, input_json = {}, request
        try:
            wd_city_model_var = Cities.objects.select_related(
                'state_id').get(pk=input_json['city_id'])
            serialized_var = CitiesAndStatesSerializer(wd_city_model_var)
            output_json = dict(
                zip(['Status', 'Message', 'cities'],
                    ["Success", "Successfully retrieved city.", serialized_var.data]))
            return Response(output_json)
        except Exception as ex:
            output_json = dict(
                zip(['Status', 'Message'], ["Failure", f"Internal Database Error, operation failed: {ex}"]))
            return Response(output_json)
        return
