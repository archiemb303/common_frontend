from collections import defaultdict
def get_activation_status_message(activation_status):
    """ Function to get activation status and message for different activation status values  """
    options = defaultdict(lambda: dict(zip(['Status', 'Message'],
                                           ["Failure", "Something went wrong during Registration process."])),
                          {1: dict(zip(['Status', 'Message'],
                                   ["Success", "Welcome back! Please check your inbox  and verify your "
                                               "email address"])),
                           2: dict(zip(['Status', 'Message'], ["Failure",
                                                               "User already exists for the given email address. If it's you then please login or reset your password to login."])),
                           3: dict(zip(['Status', 'Message'], ["Failure",
                                                               "Welcome back! Your account seems to be inactive. In order to activate your account please login or reset your password."])),
                           4: dict(zip(['Status', 'Message'], ["Failure",
                                                               "Given email id is blocked. Please use another one to  emaild to registation."])),
                           5: dict(zip(['Status', 'Message'], ["Failure",
                                                               "Something went wrong. We are fixing it. In the meanwhile you may try registering with another email address."])),
                           6: dict(zip(['Status', 'Message'], [
                               "Your account has been  deactivited.Please try to login in your account."])),
                           7: dict(zip(['Status', 'Message'], ["Failure",
                                                               "You have already registered with this email_id & not filled mandatory fields in your profile information. Please login and make updations to your Profile."]))})
    get_status_message = options[activation_status]
    return get_status_message

# def get_invite_flag(activation_status):
#     options = defaultdict(lambda: dict(zip(['Status', 'Message'],
#                                            ["Failure", "Something went wrong during Registration process."])),
#                           {0: dict(zip(['Status', 'Message'], ["Failure",
#                                                                "User already exists for the given email address. If it's you then please login or reset your password to login."])),
#                            1: dict(zip(['Status', 'Message'], ["Failure",
#                                                                "Welcome back! Your account seems to be inactive. In order to activate your account please login or reset your password."]))})
#
#
#
#     get_status_message = options[activation_status]
#     return get_status_message

