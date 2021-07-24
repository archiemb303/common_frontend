"""This Module for add city into database"""
from rest_framework.response import Response
from rest_framework.views import APIView
from common.apiauthentication.api.authenticateapi.views_authenticateapi import api_authenticate
from common.location.api.addcity.validations_addcity import validation_addcity
from common.location.serializers import CitiesSerializer
from common.utilities.lib import serializer_save


class AddCityAPI(APIView):
    """This covers the API for add city into database"""
    @api_authenticate
    @validation_addcity
    def post(self, request):
        """This covers the API for add city into database"""
        input_json, output_json = request.data["APIParams"], {}
        output_json['AuthenticationDetails'] = request.data['AuthenticationDetails']
        add_city = self.insert_data_into_table(input_json)
        if add_city.data['Status'] == "Success":
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], [
                'Success', 'City successfully added.',  add_city.data]))
        return Response(output_json)

    def insert_data_into_table(self, request):
        """Function to add city into database."""
        input_json, output_json = request, {}
        try:
            serialized_city_model_var = serializer_save(
                CitiesSerializer, input_json)
            if serialized_city_model_var is not None:
                output_json = dict(zip(['Status', 'Message'],
                                       ["Success", "City successfully added to Database."]))
                return Response(output_json)
        except Exception as ex:
            output_json = dict(
                zip(['Status', 'Message'], ["Failure",
                                            f"Internal Database Error, operation failed: {ex}"]))
            return Response(output_json)
        return
