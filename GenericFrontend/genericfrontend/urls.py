"""genericfrontend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.generic import RedirectView
from common.registration.api.signup_initiation.views_signup_initiation import trigger_error
from common.login.api.userlogin.views_userlogin import UserLoginAPI
from common.login.api.social_login_authentication.views_social_login_authentication import SocialLoginAuthenticationAPI
from common.logout.api.userlogout.views_userlogout import UserLogoutAPI
from common.registration.api.signup_mobile_initiation.views_signup_mobile_initiation import SignUpInitiationMobileAPI
from common.registration.api.signup_mobileotp_verification.views_signup_mobileotp_verification import SignUpMobileOtpVerifyAPI
from common.registration.api.signup_mobile_completion.views_signup_mobile_completion import SignUpCompletionMobileAPI
from common.registration.api.signup_emailotp_initiation.views_signup_emailotp_initiation import  SignUpInitiationEmailOtpAPI
from common.registration.api.signup_emailotp_completion.views_signup_emailotp_completion import SignUpCompletionEmailOtpAPI
from common.registration.api.signup_emailotp_verification.views_signup_emailotp_verification import SignUpEmailOtpVerificationAPI

# ------------------------------------------ REVISED APIs ---------------------------------
# ------------------------- Revised website maintenance module ----------------------------
from common.website_management.api.get_website_availability.views_get_website_availability import GetWebsiteAvailabilityAPI


from common.location.api.getallcountriesdetails.views_getallcountriesdetails import GetAllCountriesAPI  # genericfrontend: Moved from existing to revised
from common.location.api.getallcitiesdetailsbystate.views_getallcitiesdetailsbystate import GetAllCitiesByStateAPI  # genericfrontend: Moved from existing to revised
from common.location.api.getallstatesdetailsbycountry.views_getallstatesdetailsbycountry import GetAllStatesByCountryAPI  # genericfrontend: Moved from existing to revised


# ------------------------------------------ support centre modules --------------
from common.supportcentre.api.post_login_get_ticket_types.views_post_login_get_ticket_types import PostLoginGetTicketTypesAPI
from common.supportcentre.api.post_login_get_questions_by_ticket_types.views_post_login_get_questions_by_ticket_types import PostLoginGetQuestionsByTicketTypesAPI
from common.supportcentre.api.pre_login_raise_ticket.views_pre_login_raise_ticket import PreLoginRaiseTicketAPI
from common.supportcentre.api.post_login_raise_ticket.views_post_login_raise_ticket import PostLoginRaiseTicketAPI
from common.supportcentre.api.post_login_fetch_my_tickets.views_post_login_fetch_my_tickets import PostLoginFetchMyTicketsAPI
from common.supportcentre.api.post_login_get_ticket_replies.views_post_login_get_ticket_replies import PostLoginGetTicketRepliesAPI
from common.supportcentre.api.post_login_reply_to_ticket.views_post_login_reply_to_ticket import PostLoginReplyToTicketAPI
from common.supportcentre.api.post_login_fetch_all_tickets.views_post_login_fetch_all_tickets import PostLoginFetchAllTicketsAPI
from common.supportcentre.api.post_login_update_ticket_status.views_post_login_update_ticket_status import PostLoginUpdateTicketStatusAPI
from common.supportcentre.api.post_login_filter_all_tickets.views_post_login_filter_all_tickets import PostLoginFilterAllTicketsAPI
from common.supportcentre.api.post_login_filter_my_tickets.views_post_login_filter_my_tickets import PostLoginFilterMyTicketsAPI

from common.location.api.get_user_geos.views_get_user_geos import GetUserGeosAPI

# -----------------------------------------Revised new Notification Module---------------------------------------#
from common.notifications_new.api.create_notification.views_create_notification import CreateNotificationAPI
from common.notifications_new.api.populate_my_notifications.views_populate_my_notifications import \
    PopulateMyNotificationsAPI
from common.notifications_new.api.fetch_my_notifications.views_fetch_my_notifications import FetchMyNotificationsAPI
from common.notifications_new.api.update_notification_status.views_update_notification_status import \
    UpdateNotificationStatusAPI

# -----------------------------------------Revised Master Table Population Module-------------------------------------#
from common.utilities.populate_all_master_tables.populate_all_master_tables import PopulateAllMasterTablesAPI


# -----------------------------------------Testing Sentry---------------------------------------#
def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [

    ############################################# FINALIZED URLS LISTING ##############################################

    # ------------------------- core module ----------------------------
    path('admin/', admin.site.urls),
    url(r'^debug', trigger_error),

    # ------------------------- sentry integration module ----------------------------
    path('sentry-debug/', trigger_error),

    # ------------------------- website maintenance module ----------------------------
    url(r'^get_website_availability/$', GetWebsiteAvailabilityAPI.as_view()),

    # ------------------------- geo module ----------------------------
    url(r'^get_all_countries_details/$', GetAllCountriesAPI.as_view()),
    url(r'^get_all_cities_by_state/$', GetAllCitiesByStateAPI.as_view()),
    url(r'^get_all_states_by_country/$', GetAllStatesByCountryAPI.as_view()),
    url(r'^get_user_geo/$', GetUserGeosAPI.as_view()),

    # ------------------------- registration module ----------------------------
    url(r'^login/$', UserLoginAPI.as_view()),
    url(r'^logout/$', UserLogoutAPI.as_view()),
    url(r'signup_mobile_initiate/$', SignUpInitiationMobileAPI.as_view()),
    url(r'signup_mobileotp_verify/$', SignUpMobileOtpVerifyAPI.as_view()),
    url(r'signup_mobile_complete/$', SignUpCompletionMobileAPI.as_view()),
    url(r'signup_email_otp_initiate/$', SignUpInitiationEmailOtpAPI.as_view()),
    url(r'signup_emailotp_verify/$', SignUpEmailOtpVerificationAPI.as_view()),
    url(r'signup_emailotp_complete/$', SignUpCompletionEmailOtpAPI.as_view()),
    url(r'social_log_auth/$', SocialLoginAuthenticationAPI.as_view()),

    # ------------------------- support center module ----------------------------
    url(r'^fetch_post_login_ticket_types_and_questions/$', PostLoginGetTicketTypesAPI.as_view()),
    url(r'^fetch_post_login_questions_by_ticket_type_id/$', PostLoginGetQuestionsByTicketTypesAPI.as_view()),
    url(r'^pre_login_raise_ticket/$', PreLoginRaiseTicketAPI.as_view()),
    url(r'^post_login_raise_ticket/$', PostLoginRaiseTicketAPI.as_view()),
    url(r'^post_login_fetch_my_tickets/$', PostLoginFetchMyTicketsAPI.as_view()),
    url(r'^post_login_fetch_ticket_details/$', PostLoginGetTicketRepliesAPI.as_view()),
    url(r'^post_login_reply_to_ticket/$', PostLoginReplyToTicketAPI.as_view()),
    url(r'^post_login_fetch_all_tickets/$', PostLoginFetchAllTicketsAPI.as_view()),
    url(r'^post_login_update_ticket_status/$', PostLoginUpdateTicketStatusAPI.as_view()),
    url(r'^post_login_filter_my_tickets/$', PostLoginFilterMyTicketsAPI.as_view()),
    url(r'^post_login_filter_all_tickets/$', PostLoginFilterAllTicketsAPI.as_view()),

    # ---------------------------------Revised Master Table Population Module--------------------------------#
    url(r'^populate_master_tables/$', PopulateAllMasterTablesAPI.as_view()),

    # ------------------------- notification module ----------------------------
    url(r'^create_notification/$', CreateNotificationAPI.as_view()),
    url(r'^populate_my_notifications/$', PopulateMyNotificationsAPI.as_view()),
    url(r'^fetch_my_notifications/$', FetchMyNotificationsAPI.as_view()),
    url(r'^update_notification_status/$', UpdateNotificationStatusAPI.as_view()),
 ]


