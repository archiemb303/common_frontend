""" This API will get appropriate parameters respective to each payment gateway that the gateway would need to process a payment"""
import re
from common.paymentgateways.api.pg_navigators.paytm.get_pg_navigators_paytm.views_get_pg_navigators_paytm \
    import get_pg_navigators_paytm


def get_pg_navigators(request):
    """
    This function checks the payment gateway id and returns the respective navigators by calling
    respective get_navigators functions
    :param request: see apidocumentation_get_pg_navigators.py
    :return:
    """
    try:
        input_json = request
        # checking if pg provider is PayTM
        if input_json['gateway_details']['pg_provider_id'] == 4:
            pg_navigator_vars = get_pg_navigators_paytm(input_json)
            match = re.findall(r"'Status': 'Failure'", str(pg_navigator_vars))
            if match:
                output_json = pg_navigator_vars
                return output_json
            output_json = dict(zip(['Status', 'Message', 'Payload'],
                                   ['Success', 'Navigation vars collected successfully. Navigate to collect payment',
                                    pg_navigator_vars['Payload']]))
            return output_json
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ["Failure", f"Sorry, we do not use the chosen payment gateway anymore",
                                None]))
        return output_json

    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ["Failure", f"Unable to fetch pg navigation variables. Exception encountered: {ex}", None]))
        return output_json
