"""This API returns all the values that should be bound to the raise support center ticket form"""
import logging
import re
import requests
from rest_framework.views import APIView, Response
from common.commondecorators.preloginauthentications import common_pre_login_authentications
from common.registration.specificlib.userprofile_lib import fetch_profile_from_emailotp
from common.supportcentre.api.post_login_raise_ticket.views_post_login_raise_ticket import PostLoginRaiseTicketAPI
from common.supportcentre.api.pre_login_raise_ticket.validations_pre_login_raise_ticket import \
    validation_pre_login_raise_ticket

# Get an instance of a logger

logger = logging.getLogger("genericfrontend_1.0")


class PreLoginRaiseTicketAPI(APIView):
    """This covers the API for get all ticket types."""
    @common_pre_login_authentications
    @validation_pre_login_raise_ticket
    def post(self, request):
        """Post Function for getting ticket types."""
        output_json = dict(zip(['AvailabilityDetails', 'AuthenticationDetails', 'Payload'],
                               [request.data['AvailabilityDetails'], request.data['AuthenticationDetails'], None]))
        json_params = request.data['APIParams']
        output_json['Payload'] = self.pre_login_raise_ticket_json(json_params)
        return Response(output_json)

    def pre_login_raise_ticket_json(self, request):
        """
        This function checks if the email address already has an account with us.
        If yes then it raises a post login ticket else raises a pre-login ticket.
        Pre-login tickets will be submitted with HubSpot
        :param request: {'first_name': 'sdaf', 'last_name': 'sdfg', 'email': 'sdf@sdfg.com',
                            'code': '', 'mobile': '9999999999', 'query': 'dsgrfsdfg'}
        :return:
        """
        try:
            input_json = request
            input_json['email_id'] = input_json['email']

            # checking if the provided email_id has an associated profile
            existing_user_check_var = fetch_profile_from_emailotp(input_json)
            match = re.findall(r"'Status': 'Failure'", str(existing_user_check_var))
            if match:
                # user does not exist in out database. Raise a ticket with HubSpot
                output_json = raise_hubspot_ticket(input_json)
                return output_json

            # raising a post login ticket for the user
            post_login_ticket_params = dict(zip(['profile_id', 'raised_by', 'ticket_details'],
                                                [existing_user_check_var['profile_id'], existing_user_check_var['profile_id'],
                                                 dict(zip(['ticket_type_id', 'ticket_question_id', 'subject', 'query'],
                                                          [1, 1, "Ticket raised without login in", input_json['query']]))]))
            post_login_ticket_details = PostLoginRaiseTicketAPI.post_post_login_raise_ticket_json(request, post_login_ticket_params)
            match = re.findall(r"'Status': 'Failure'", str(post_login_ticket_details))
            if match:
                output_json = post_login_ticket_details
                return output_json
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ["Success", "Ticket raised successfully. Since you already have an account with us, "
                                               "you can login to your account and visit our support center to track "
                                               "your ticket status", post_login_ticket_details['Payload']]))
            return output_json
        except Exception as ex:
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ["Failure", f"Exception encountered while raising ticket: {ex}", None]))
            return output_json


def raise_hubspot_ticket(request):
    """
    This function makes an api call to HubSpot to raise a pre-login/contact-us ticket
    :param request: {'first_name': 'sdaf', 'last_name': 'sdfg', 'email': 'sdf@sdfg.com', 'code': '', 'mobile': '9999999999', 'query': 'dsgrfsdfg'}
    :return:
    """
    try:
        input_json = request
        hs_api_params = dict(zip(['fields', 'context'],
                                 [[], dict(zip(['pageUri', 'pageName'], ["www.genericfrontend.com/contactUs", "ContactUs page"]))]))
        hs_api_params['fields'].append(dict(zip(['name', 'value'], ["firstname", input_json['first_name']])))
        hs_api_params['fields'].append(dict(zip(['name', 'value'], ["lastname", input_json['last_name']])))
        hs_api_params['fields'].append(dict(zip(['name', 'value'], ["email", input_json['email']])))
        hs_api_params['fields'].append(dict(zip(['name', 'value'], ["message", input_json['query']])))
        hs_api_params['fields'].append(dict(zip(['name', 'value'],
                                                ["phone", f"{input_json['code']}{input_json['mobile']}"])))

        url = f"https://api.hsforms.com/submissions/v3/integration/submit/8401274/8eb8ad4c-54de-45d4-927b-f51a125b9364"
        api_request_output = requests.post(url, json=hs_api_params)
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ['Success', 'Ticket raised succefully. Please check your inbox for update', api_request_output.json()]))
        return output_json
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ['Failure', f"API could not be called Successfully. Exception encountered: {ex}", None]))
        return output_json
