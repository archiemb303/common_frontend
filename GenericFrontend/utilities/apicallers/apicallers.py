import requests, json
import logging

logger = logging.getLogger("msp")


def makebackendapicall_json(request, backend_call_params):
    """
    request: request object that contains all the session and authentication details
    call_params: dictionary that contains details of the API call
    backend_call_params: {
        api_type: "prelogin/postlogin"
        api_name:
        request_type:
        api_params:{}
    }

    """
    # request_base_url = 'https://abkarobe.com/'
    # request_base_url = 'http://ec2-13-212-56-25.ap-southeast-1.compute.amazonaws.com/'
    request_base_url = 'http://127.0.0.1:8001/'

    try:
        # Preparing API call url
        input_json = backend_call_params
        api_url = request_base_url + input_json['api_name'] + "/"

        # Preparing API call body
        request_body = dict(zip(['APIDetails', 'SessionDetails', 'APIParams'],
                                [dict(), dict(), input_json['api_params']]))
        request_body['APIDetails'] = dict(zip(['token_type', 'token_vendor_id', 'token_string', 'dev_key'],
                                              [1, 1, "NtJbwFUyjqLHxuXOuRDb",
                                               "sjdkljagagerukjdgjncjdsnjkfhkjasdghreuiuie@#$%$dgd#$@d234"]))
        if input_json['api_type'] == "postlogin":
            request_body['SessionDetails'] = dict(zip(['profile_id', 'session_id', 'session_key'],
                                                      [request["profile_id"], request["session_id"],
                                                       request["session_key"]]))

        # Making backend api call
        result = requests.post(api_url, json=request_body)

        # Processing output of the backend API call
        output_json = dict(zip(['Status', 'Message', 'Payload'], ["Success", "Details are fetched", result.json()]))
        return output_json
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ["Failure", f"Exception encountered in frontend while making backend api call. "
                                           f"Exception is: {ex}", None]))
        logger.error(output_json['Message'], exc_info=1)
        return output_json
