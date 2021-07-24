""""This api add country in  database"""
from rest_framework.response import Response
from rest_framework.views import APIView
from common.apiauthentication.api.authenticateapi.views_authenticateapi import api_authenticate
from common.location.api.addcountry.validations_addcountry import validation_addcountry
from common.location.serializers import CountriesSerializer
from common.utilities.lib import serializer_save


class AddCountryAPI(APIView):
    """This class covers the api for add country into database."""
    @api_authenticate
    @validation_addcountry
    def post(self, request):
        """This function covers the API for add country into database"""
        input_json, output_json = request.data["APIParams"], {}
        output_json['AuthenticationDetails'] = request.data['AuthenticationDetails']
        add_country = self.insert_data_into_table(input_json)
        if add_country.data['Status'] == "Success":
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], [
                'Success', 'Country added Successfully.',  add_country.data]))
        return Response(output_json)

    def insert_data_into_table(self, request):
        """Function to add country into database."""
        input_json, output_json = request, {}
        try:
            serialized_var = serializer_save(CountriesSerializer, input_json)
            if serialized_var is not None:
                output_json = dict(
                    zip(['Status', 'Message'], ["Success", "Country successfully added to Database."]))
                return Response(output_json)
        except Exception as ex:
            output_json = dict(
                zip(['Status', 'Message'], ["Failure", f"Internal Database Error, operation failed: {ex}"]))
            return Response(output_json)
        return
