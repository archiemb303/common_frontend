import boto3
from genericfrontend.dev_settings import AWS_ACCESS_KEY_ID, AWS_REGION, AWS_SECRET_ACCESS_KEY, AWS_ARN
import http.client
import requests

def send_sms_promotional(request):
    """Code to send sms to mobile numbers."""
    client = boto3.client("sns", aws_access_key_id=AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                          region_name=AWS_REGION)
    # client.setSMSAttributes(
    #     {
    #         attributes : {
    #             DefaultSMSType : "Transactional"
    #         }
    #     },
    #     function(error){
    # if(error){
    #     console.log(error);
    # }
    # }
    # );
    # input_jsons = dict(mobile_numbers=[
    #     '+917406135629',
    #     '+919741601203',
    #     '+917795123525',
    #     '+918939099619',
    #     '+919606230339',
    #     '+918909308092',
    #     '+919741292046',
    #     '+919686064664'
    # ], message="Hello folks, welcome to www.genericfrontend.com")
    phone_number = request['phone_number']
    input_json = dict(mobile_numbers=[phone_number], message=f"Hello folks, welcome to www.genericfrontend.com, "
                                                               f"The One Time Password (OTP) for registering to "
                                                               f"genericfrontend.com is {request['text']}")
    some_list_of_contacts = input_json['mobile_numbers']

    # Add SMS Subscribers
    for number in some_list_of_contacts:
        client.subscribe(
            TopicArn=AWS_ARN,
            Protocol='sms',
            Endpoint=number  # <-- number who'll receive an SMS message.
        )
    response = client.publish(
        TopicArn=AWS_ARN,
        Message=input_json["message"],
        MessageAttributes={'string': {'DataType': 'String', 'StringValue': 'String', },
                           'AWS.SNS.SMS.SenderID': {'DataType': 'String', 'StringValue': "abk"}}
    )
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        output_json = {"Status": "Success", "Message": "SMS has been sent"}

    else:
        output_json = {"Status": "Failure", "Message": "Something Went Wrong"}
    return output_json


# declared static data

# input_json = dict(mobile_numbers=[
#     '#+917795123525',
#     '+919606230339',
#     '+12085475909',
#     '+447572120508'
# ], message="Hello folks, how r u")
#
# # calling function
# send_sms(input_json)


def send_sms_transactional(request):
    """
    This function sends SMS through our chosen SMS partner for transactional SMSs
    :param request:
        {
            'text': "asdfasdf",
            'phone_number': "8660970120",
            'country_code": "91"
        }
    :return:
    """
    try:
        input_json = request
        headers_var = {
                'content-type': "application/json",
                'authkey': "334097AuBU02YGOYB5efae2b6P1"
            }
        payload = dict(zip(['sender', 'route', 'country', 'sms'],
                           ["genericfrontend", "4", input_json['country_code'],
                            [dict(zip(["message", "to"], [input_json['text'], [input_json['phone_number']]]))]]))
        result = requests.post("https://api.msg91.com/api/v2/sendsms", headers=headers_var, json=payload)
        # print(result.content)
        output_json = dict(zip(['Status', 'Message', 'Payload'],
                               ["Success", "OTP SMS has been sent to given phone number", result.content]))
        return output_json

    except Exception as ex:
        output_json = dict(zip(["Status", "Message", "Payload"],
                               ["Failure", f"Unable to send SMS via MSG91. Exception encountered: {ex}", None]))
        return output_json


def send_sms(request):
    """
    This function calls respective function to send promotional or transactional sms
    :param request:
        {
            'text': "asdfasdf",
            'phone_number': "8660970120",
            'country_code": "91",
            'sms_type':"transactional/promotional"
        }
    :return:
    """
    try:
        input_json = request
        # initializing invalid input types to promotional sms
        if 'sms_type' not in input_json or input_json['sms_type'] not in ["transactional", "promotional"]:
            input_json['sms_type'] = "promotional"
        if input_json['sms_type'] == "promotional":
            output_json = send_sms_promotional(input_json)
            return output_json
        output_json = send_sms_transactional(input_json)
        return output_json
    except Exception as ex:
        output_json = dict(zip(["Status", "Message", "Payload"],
                               ["Failure", f"Unable to send SMS. Exception encountered: {ex}", None]))
        return output_json