"""This function add state to database."""
from rest_framework.views import APIView
from rest_framework.response import Response
from common.apiauthentication.api.authenticateapi.views_authenticateapi import api_authenticate
from common.location.serializers import StatesSerializer
from common.utilities.lib import serializer_save
from common.location.api.addstate.validations_addstate import validation_addstate


class AddStateAPI(APIView):
    """This covers the API for add state."""
    @api_authenticate
    @validation_addstate
    def post(self, request):
        """This covers the API for add state."""
        input_json, output_json = request.data["APIParams"], {}
        output_json['AuthenticationDetails'] = request.data['AuthenticationDetails']
        add_state = self.insert_data_into_table(input_json)
        if add_state.data['Status'] == "Success":
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], [
                'Success', 'Country added Successfully.', add_state.data]))
        return Response(output_json)



    def insert_data_into_table(self, request):
        """Function to add country into database."""
        input_json, output_json = request, {}
        try:
            serialized_var = serializer_save(StatesSerializer, input_json)
            if serialized_var is not None:
                output_json = dict(
                    zip(['Status', 'Message'], ["Success", "State successfully added to Database."]))
                return Response(output_json)
        except Exception as ex:
            output_json = dict(
                zip(['Status', 'Message'], ["Failure", f"Internal Database Error, operation failed: {ex}"]))
            return Response(output_json)
        return

