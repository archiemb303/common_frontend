from genericfrontend.shared_settings import SENDGRID_API_KEY
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger("genericfrontend_1.0")


# def senttestemail(request):
#     response_params = {}
#     subject = "mail test"
#     from_email = "genericfrontend@gmail.com"
#     to_list = "genericfrontendgenericfrontend1@gmail.com"
#     html_message = "Hi..folks"
#     response_params = sendmail(request,
#                                subject=subject, html_content=html_message, from_email=from_email, to_emails=to_list)
#     return response_params


def sendmail(request, **kwargs):
    output_params = {}
    message = Mail(
        from_email=kwargs["from_email"],
        to_emails=kwargs['to_emails'],
        subject=kwargs['subject'],
        html_content=kwargs['html_content'],
    )
    # Bcc1 = kwargs['bcc_email1']
    # Bcc2 = kwargs['bcc_email2']
    # message.add_bcc(Bcc1)
    # message.add_bcc(Bcc2)
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        output_params["Statuscode"] = response.status_code
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return output_params
    except Exception as ex:
        print(ex.body)  # print (e.read())
        logger.error("Error occured while sending email", exc_info=1)


# senttestemail(1)
