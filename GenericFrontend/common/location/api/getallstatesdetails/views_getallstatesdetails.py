"""This  API  cover for fetch all states."""
from rest_framework.views import APIView
from rest_framework.response import Response
from apiauthentication.api.authenticateapi.views_authenticateapi import api_authenticate
from common.location.models import States
from common.location.serializers import StatesSerializer


class GetAllStatesAPI(APIView):
    """This  API  cover for fetch all states."""
    @api_authenticate
    def post(self, request):
        """This  API  cover for fetch all states."""
        input_json, output_json = request.data["APIParams"], {}
        output_json['AuthenticationDetails'] = request.data['AuthenticationDetails']
        fetch_all_state = self.fetch_states(input_json)

        if fetch_all_state.data['Status'] == "Success":
            payload_details = {
                'states_details': fetch_all_state.data['States']}
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], [
                'Success', 'Successfully retrieved States.', payload_details]))
            return Response(output_json)

    def fetch_states(self, request):
        """Function to fetch states into database."""
        output_json = {}
        try:
            serialized_var = StatesSerializer(States.objects.all(), many=True)
            output_json = dict(
                zip(['Status', 'Message', 'States'], ["Success", "Successfully retrieved States.", serialized_var.data]))
            return Response(output_json)
        except Exception as ex:
            output_json = dict(
                zip(['Status', 'Message'], ["Failure", f"Internal Database Error, operation failed: {ex}"]))
            return Response(output_json)
        return
