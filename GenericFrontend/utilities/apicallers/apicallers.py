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
    request_base_url = 'https://abkarobe.com/'
    # request_base_url = 'http://ec2-13-212-56-25.ap-southeast-1.compute.amazonaws.com/'
    # request_base_url = 'http://127.0.0.1:8001/'

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
                                                      [request.session["profile_id"], request.session["session_id"],
                                                       request.session["session_key"]]))

        # Making backend api call
        result = requests.post(api_url, json=request_body)
        backend_output = result.json()
        # Processing output of the backend API call
        request.session["token_type"] = 1
        request.session["token_vendor_id"] = 1
        request.session["token_string"] = 'sdxfcgvbhjnmklasdfghjk'
        request.session["dev_key"] = 'sjdkljagagerukjdgjncjdsnjkfhkjasdghreuiuie@#$%$dgd#$@d234'
        if 'SessionDetails' in backend_output:
            request.session["profile_id"] = backend_output['SessionDetails']['Payload']['profile_id']
            request.session["session_id"] = backend_output['SessionDetails']['Payload']['session_id']
            # request.session["session_id"] = "asdfsdfsafdgdf"
            request.session["session_key"] = backend_output['SessionDetails']['Payload']['session_key']
        request.session["verified"] = 'yes'
        output_json = dict(zip(['Status', 'Message', 'Payload'], ["Success", "Details are fetched", backend_output]))
        return output_json
    except Exception as ex:
        request.session['login_flag'] = 2
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ["Failure", f"Exception encountered in frontend while making backend api call. "
                                           f"Exception is: {ex}", None]))
        logger.error(output_json['Message'], exc_info=1)
        # return redirect('/prelogin/')
        return output_json
