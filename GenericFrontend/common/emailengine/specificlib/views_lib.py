from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.views import Response
from django.views.generic import TemplateView
from django.core.mail import send_mail
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from django.template import loader
from django.template.loader import get_template
from django.http import HttpResponse
from .send_email import sendmail


class UserRegistrationEmailVerification(APIView):
    @classmethod
    def user_registration_email_verification(self, request, **kwargs):
        subject = kwargs['firstName'] + \
            ": Please verify your email address to proceed"
        from_email = str("support@genericfrontend.com")
        to_list = [kwargs['email_id']]
        # template_url = 'genericfrontendEmailEngine/email_templates/support_center_confirmation.html'

        html_message = loader.render_to_string(
            'user_registration_email_verification.html',
            {
                'user_name': kwargs['firstName'] + " " + kwargs['lastName'],
                'first_name': kwargs['firstName'],
                'last_name': kwargs['lastName'],
                'email_id': kwargs['email_id'],
                'activation_key': kwargs['activation_key']
                # 'mobile_otp': kwargs['mobile_otp']


            }
        )
        # send_mail(subject, html_message, from_email, to_list,
        #           fail_silently=True, html_message=html_message)
        sendmail(request, subject=subject, html_content=html_message, from_email=from_email, to_emails=to_list)
        return HttpResponse('mail_sent_successfully')

class UserRegistrationEmailOtpVerification(APIView):
    @classmethod
    def user_registration_email_otp_verification(self, request, **kwargs):
        from_email = str("support@genericfrontend.com")
        to_list = [kwargs['email_id']]
        subject = f"Login to genericfrontend through OTP."
        # template_url = 'genericfrontendEmailEngine/email_templates/support_center_confirmation.html'

        html_message = loader.render_to_string(
            'user_registration_email_verification_otp.html',
            {
                # 'user_name': kwargs['firstName'] + " " + kwargs['lastName'],
                # 'first_name': kwargs['firstName'],
                # 'last_name': kwargs['lastName'],
                'email_id': kwargs['email_id'],
                'otp': kwargs['otp']
                # 'activation_key': kwargs['activation_key']
                # 'mobile_otp': kwargs['mobile_otp']
            }
        )
        # send_mail(subject, html_message, from_email, to_list,
        #           fail_silently=True, html_message=html_message)
        sendmail(request, subject=subject, html_content=html_message, from_email=from_email, to_emails=to_list)
        return HttpResponse('mail_sent_successfully')

class UserRegistrationEmailVerificationViaInvite(APIView):
    @classmethod
    def user_registration_email_verification_via_invite(self, request, **kwargs):

        subject = kwargs['requester_fname'] + " " + kwargs['requester_lname'] + \
            " " + "has invited you to be their friend in genericfrontend platform"
        from_email = str("support@genericfrontend.com")
        to_list = [kwargs['email_id']]
        # template_url = 'genericfrontendEmailEngine/email_templates/support_center_confirmation.html'

        html_message = loader.render_to_string(
            'user_registration_email_verification_via_invite.html',
            {
                'user_name': kwargs['firstName'] + " " + kwargs['lastName'],
                'first_name': kwargs['firstName'],
                'last_name': kwargs['lastName'],
                'requester_name': kwargs['requester_fname'] + " "+kwargs['requester_lname'],
                'email_id': kwargs['email_id'],
                'activation_key': kwargs['activation_key'],
                # 'mobile_otp': kwargs['mobile_otp'],
                'invite_flag': kwargs['invite_flag']

            }
        )
        # send_mail(subject, html_message, from_email, to_list,
        #           fail_silently=True, html_message=html_message)
        sendmail(request, subject=subject, html_content=html_message, from_email=from_email, to_emails=to_list)

        return HttpResponse('mail_sent_successfully')


class UserRegistrationEmailVerificationViaInvitePartner(APIView):
    @classmethod
    def user_registration_email_verification_via_invite_partner(self, request, **kwargs):

        subject = kwargs['requester_fname'] + " " + kwargs['requester_lname'] + \
            " " + "has invited you to be their partner in genericfrontend platform."
        from_email = str("support@genericfrontend.com")
        to_list = [kwargs['email_id']]
        # template_url = 'genericfrontendEmailEngine/email_templates/support_center_confirmation.html'

        html_message = loader.render_to_string(
            'user_registration_email_verification_via_invite.html',
            {
                'user_name': kwargs['firstName'] + " " + kwargs['lastName'],
                'first_name': kwargs['firstName'],
                'last_name': kwargs['lastName'],
                'requester_name': kwargs['requester_fname'] + " "+kwargs['requester_lname'],
                'email_id': kwargs['email_id'],
                'activation_key': kwargs['activation_key'],
                # 'mobile_otp': kwargs['mobile_otp'],
                'invite_flag': kwargs['invite_flag']
            }
        )
        # send_mail(subject, html_message, from_email, to_list,
        #           fail_silently=True, html_message=html_message)
        sendmail(request, subject=subject, html_content=html_message, from_email=from_email, to_emails=to_list)

        return HttpResponse('mail_sent_successfully')


def invitation_email(request, **kwargs):
    # subject = kwargs['firstName'] + \
    #           ": Please verify your email address to proceed"

    subject = "Invitation: Please verify your email address to proceed"
    from_email = str("support@genericfrontend.com")
    to_list = [kwargs['email_id']]
    # template_url = 'genericfrontendEmailEngine/email_templates/support_center_confirmation.html'
    html_message = loader.render_to_string(
        'invitation_friend_request.html',
        {
            'user_name': kwargs['firstName'] + " " + kwargs['lastName'],
            'first_name': kwargs['firstName'],
            'last_name': kwargs['lastName'],
            'email_id': kwargs['email_id']
        }
    )
    # send_mail(subject, html_message, from_email, to_list,
    #           fail_silently=True, html_message=html_message)
    sendmail(request, subject=subject, html_content=html_message, from_email=from_email, to_emails=to_list)
    return HttpResponse('mail_sent_successfully')
# funct1(self, request, params)
#
# def funct1(self, request, format='json'):
#     print request
#
#
#  def func( *args,**kwargs)
#       func(5,6,7,'first_name'='raj', 'last_name'='singhania')
#       func(10,100,3,4,5, 'state'karnataka')
# funct1(self, request, 0,4,2,6,'abc')
# def funct1(self, request, *args):
#     print args[0]
#     print args[4]

# funct1(self, request, a=0,b=4,c=2,d=6,e='abc')
# def funct1(self, request, *kwargs):
#     print kwargs['c']


class ForgotPasswordEmail(APIView):
    @classmethod
    def forgot_password_email(self, request, **kwargs):

        subject = kwargs['firstName'] + \
            ": One more step to reset your password"
        from_email = str("support@genericfrontend.com")
        to_list = [kwargs['email_id']]
        # template_url = 'genericfrontendEmailEngine/email_templates/support_center_confirmation.html'
        html_message = loader.render_to_string(
            'forgot_password_email.html',
            {
                'user_name': kwargs['firstName'] + " " + kwargs['lastName'],
                'first_name': kwargs['firstName'],
                'last_name': kwargs['lastName'],
                'email_id': kwargs['email_id'],
                'forgot_pwd_key': kwargs['forgot_pwd_key']
                # 'fpotp': kwargs['fp_mobile_otp']
            }
        )
        send_mail(subject, html_message, from_email, to_list,
                  fail_silently=True, html_message=html_message)

        return HttpResponse('mail_sent_successfully')


class SendPasswordEmail(APIView):
    @classmethod
    def send_password_email(self, request, **kwargs):

        subject = kwargs['firstName'] + \
            ": Please reset  your password using  the   given  password as   cuurent    password "
        from_email = str("support@genericfrontend.com")
        to_list = [kwargs['email_id']]
        # template_url = 'genericfrontendEmailEngine/email_templates/support_center_confirmation.html'
        html_message = loader.render_to_string(
            'send_password_email.html',
            {
                'user_name': kwargs['firstName'] + " " + kwargs['lastName'],
                'first_name': kwargs['firstName'],
                'last_name': kwargs['lastName'],
                'email_id': kwargs['email_id'],
                'password_key': kwargs['password'],

            }
        )
        send_mail(subject, html_message, from_email, to_list,
                  fail_silently=True, html_message=html_message)

        return HttpResponse('mail_sent_successfully')


class UserNotifiedEmailForFriendAndPartner(APIView):
    @classmethod
    def user_notified_email_for_friend_and_partner_function(self, request, **kwargs):
        subject = kwargs['firstName'] + " " + \
            kwargs['lastName'] + " " + kwargs['message']
        from_email = str("support@genericfrontend.com")
        to_list = [kwargs['notified_email_id']]
        # template_url = 'genericfrontendEmailEngine/email_templates/support_center_confirmation.html'
        html_message = loader.render_to_string(
            'send_request_email.html',
            {

                'user_name': kwargs['notified_first_Name'] + " "+kwargs['notified_last_Name'],
                'first_name': kwargs['firstName'],
                'last_name': kwargs['lastName'],
                'requester_name': kwargs['firstName'] + " "+kwargs['lastName'],
                'email_id': kwargs['notified_email_id'],
                'notified_email_flag': kwargs['notified_email_flag'],


            }
        )

        send_mail(subject, html_message, from_email, to_list,
                  fail_silently=True, html_message=html_message)

        return HttpResponse('mail_sent_successfully')



class SendInvoiceEmail(APIView):
    @classmethod
    def send_invoice_email(self, request, **kwargs):
        from_email = str("support@genericfrontend.com")
        to_list = [kwargs['invoice_params']['customer_email']]
        subject = f"Invoice genericfrontend"
        # template_url = 'genericfrontendEmailEngine/email_templates/support_center_confirmation.html'

        html_message = loader.render_to_string(
            'send_invoice_email.html',
            {
                'invoice_info': kwargs['invoice_params']
            }
        )
        # send_mail(subject, html_message, from_email, to_list,
        #           fail_silently=True, html_message=html_message)
        sendmail(request, subject=subject, html_content=html_message, from_email=from_email, to_emails=to_list)
        return HttpResponse('mail_sent_successfully')
