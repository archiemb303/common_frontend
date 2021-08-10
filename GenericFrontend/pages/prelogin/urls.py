from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.generic import RedirectView

from pages.prelogin.modules.commonmodules.preloginhome.views_preloginhome import PreLoginHomeAPI
from pages.postlogin.modules.appspecificmodules.postloginhome.views_postloginhome import PostLoginHomeAPI
from pages.postlogin.modules.commonmodules.profile.views_profile import PostLoginProfileAPI
from pages.prelogin.modules.commonmodules.api.generate_email_login_otp.views_generate_email_login_otp import GenerateEmailLoginOTPAPI
from pages.prelogin.modules.commonmodules.api.verify_email_login_otp.views_verify_email_login_otp import VerifyEmailLoginOTPAPI


urlpatterns = [
    # url(r'^home/', PreLoginHomeAPI.as_view()),
    url(r'^$', PreLoginHomeAPI.as_view()),
    url(r'^generate_email_login_otp/$', GenerateEmailLoginOTPAPI.as_view(), name='generate_email_login_otp'),
    url(r'^verify_email_login_otp/$', VerifyEmailLoginOTPAPI.as_view(), name='verify_email_login_otp'),

]