from django.shortcuts import render
from django.core.mail import send_mail
from django.template import Context
from django.template.loader import render_to_string, get_template


def user_registration_email_verification(request, **kwargs):
    result = request  # FirstName, LastName, EmailId
    # return result
    subject = kwargs['firstName'] + ": Please verify your email address to proceed"
    from_email = str("support@genericfrontend.com")
    to_list = [kwargs['email_id']]
    # template_url = 'genericfrontendEmailEngine/email_templates/support_center_confirmation.html'

    # return(kwargs)
    html_message = loader.render_to_string(
        'user_registration_email_verification.html',
        {
            'user_name': kwargs['firstName'] + " " + kwargs['lastName'],
            'first_name': kwargs['firstName'],
            'last_name': kwargs['lastName'],
            'email_id': kwargs['email_id'],
            'activation_key': kwargs['activation_key'],
            'mobile_otp': kwargs['mobile_otp']

        }
    )
    send_mail(subject, html_message, from_email, to_list, fail_silently=True, html_message=html_message)

    return HttpResponse('mail_sent_successfully')


def forgot_password_email(request, **kwargs):
    print("came here email engine view 59")
    result = request  # FirstName, LastName, EmailId
    # return result
    subject = kwargs['firstName'] + ": One more step to reset your password"
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
            'forgot_pwd_key': kwargs['forgot_pwd_key'],
            'fpotp': kwargs['fp_mobile_otp']
        }
    )
    send_mail(subject, html_message, from_email, to_list, fail_silently=True, html_message=html_message)
    print("email sent")
    print(kwargs)
    return HttpResponse('mail_sent_successfully')