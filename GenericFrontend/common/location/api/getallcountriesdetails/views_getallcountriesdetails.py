"""This api fetch all counties"""
from rest_framework.views import APIView
from rest_framework.response import Response
from common.commondecorators.preloginauthentications import common_pre_login_authentications
from common.location.models import Countries
from common.location.serializers import CountriesSerializer


class GetAllCountriesAPI(APIView):
    """This  API  cover for fetch all countries"""
    @common_pre_login_authentications
    def post(self, request):
        """This  API  cover for fetch all countries."""
        input_json = request.data["APIParams"]
        output_json = dict(zip(['AvailabilityDetails', 'AuthenticationDetails', 'Payload'],
                               [request.data['AvailabilityDetails'], request.data['AuthenticationDetails'], None]))

        fetch_all_country = self.fetch_countries(input_json)

        if fetch_all_country.data['Status'] == "Success":
            payload_details = {
                'countries_details': fetch_all_country.data['countries']}
            output_json['Payload'] = dict(zip(['Status', 'Message', 'Payload'], [
                'Success', 'Successfully retrieved countries.', payload_details]))
            return Response(output_json)
        output_json['payload'] = fetch_all_country.data
        return Response(output_json)

    def fetch_countries(self, request):
        """Function to fetch country from database."""
        output_json = {}
        try:
            serialized_var = CountriesSerializer(
                Countries.objects.all(), many=True)
            output_json = dict(
                zip(['Status', 'Message', 'countries'],
                    ["Success", "Successfully retrieved countries.", serialized_var.data]))
            return Response(output_json)
        except Exception as ex:
            output_json = dict(
                zip(['Status', 'Message'], ["Failure", f"Internal Database Error, operation failed: {ex}"]))
            return Response(output_json)
        return
