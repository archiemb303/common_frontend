""" This API is used internally to get the user's ip from request headers"""
from rest_framework.views import APIView, Response
from common.apiauthentication.api.authenticateapi.views_authenticateapi import api_authenticate


class GetUserIPAPI(APIView):
    """This API gets user's ip"""
    @api_authenticate
    def post(self, request):
        """Post function to get user's ip"""
        output_json = dict()
        output_json['AuthenticationDetails'] = request.data['AuthenticationDetails']
        output_json['SessionDetails'] = request.data['SessionDetails']
        output_json['Payload'] = dict(zip(['user_ip'], [None]))
        return Response(output_json)

    def get_user_ip_json(self, request):
        """ json function to get user's ip. This is an unusual json function as it takes request object (request)
        instead of json object (request.data) as input"""
        try:
            input_json = request.data
            # local initialization of user's ip based on if the information is passed in the request body or not
            if 'APIParams' not in input_json or 'user_ip' not in input_json['APIParams']:
                # uncomment this part for local and comment it for staging/production
                # user_ip_var = '5.62.23.25'
                user_ip_var = None
                # uncomment this part for local and comment it for staging/production

                # uncomment this part for staging/production and comment it for local
                # x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                # user_ip_var = x_forwarded_for.split(',')[0]
                # uncomment this part for staging/production and comment it for local
            else:
                user_ip_var = input_json['APIParams']['user_ip']
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ["Success", "User's IP successfully found", user_ip_var]))
            return output_json
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ["Failure", f"Issue while fetching user's ip'. "
                                               f"Exception encountered: {ex}", None]))
            return output_json
