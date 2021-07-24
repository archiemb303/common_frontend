"""This  API  cover for fetch state"""
from rest_framework.response import Response
from rest_framework.views import APIView
from apiauthentication.api.authenticateapi.views_authenticateapi import api_authenticate
from common.location.api.getstate.validations_getstate import validation_getstate
from common.location.models import States
from common.location.serializers import StatesAndCountriesSerializer


class GetStateAPI(APIView):
    """This  API  cover for fetch state."""
    @api_authenticate
    @validation_getstate
    def post(self, request):
        """This  API  cover for fetch state."""
        input_json, output_json = request.data["APIParams"], {}
        output_json['AuthenticationDetails'] = request.data['AuthenticationDetails']
        fetch_all_state = self.fetch_states(input_json)
        if fetch_all_state.data['Status'] == "Success":
            payload_details = {
                'state_details': fetch_all_state.data['States']}
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], [
                'Success', 'Successfully retrieved state.', payload_details]))
        return Response(output_json)

    def fetch_states(self, request):
        """Function to fetch states into database."""
        input_json, output_json = request, {}
        try:
            state_model_var = States.objects.select_related(
                'country_id').get(pk=input_json['state_id'])
            serialized_var = StatesAndCountriesSerializer(state_model_var)
            output_json = dict(
                zip(['Status', 'Message', 'States'],
                    ["Success", "Successfully retrieved State.", serialized_var.data]))
            return Response(output_json)
        except Exception as ex:
            output_json = dict(
                zip(['Status', 'Message'], ["Failure", f"Internal Database Error, operation failed: {ex}"]))
            return Response(output_json)
        return
