"""This  API  cover for fetch  country."""
from rest_framework.views import APIView
from rest_framework.response import Response
from apiauthentication.api.authenticateapi.views_authenticateapi import api_authenticate
from common.location.models import Countries
from common.location.serializers import CountriesSerializer
from common.location.api.getcountry.validations_getcountry import validation_getcountry


class GetCountryAPI(APIView):
    """This  API  cover for fetch  country"""
    @api_authenticate
    @validation_getcountry
    def post(self, request):
        """This  API  cover for fetch  country."""
        input_json, output_json = request.data["APIParams"], {}
        output_json['AuthenticationDetails'] = request.data['AuthenticationDetails']
        fetch_all_state = self.fetch_states(input_json)
        if fetch_all_state.data['Status'] == "Success":
            payload_details = {
                'country_details': fetch_all_state.data['country']}
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], [
                'Success', 'Successfully retrieved country.', payload_details]))
        return Response(output_json)

    def fetch_states(self, request):
        """Function to fetch states into database."""
        input_json, output_json = request, {}
        try:
            country_model_var = Countries.objects.get(
                pk=input_json['country_id'])
            serialized_var = CountriesSerializer(country_model_var)
            output_json = dict(
                zip(['Status', 'Message', 'country'],
                    ["Success", "Successfully retrieved Country.", serialized_var.data]))
            return Response(output_json)
        except Exception as ex:
            output_json = dict(
                zip(['Status', 'Message'], ["Failure", f"Internal Database Error, operation failed: {ex}"]))
            return Response(output_json)
        return
