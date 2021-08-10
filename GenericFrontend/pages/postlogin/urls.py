from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.generic import RedirectView

from pages.prelogin.modules.commonmodules.preloginhome.views_preloginhome import PreLoginHomeAPI
from pages.postlogin.modules.commonmodules.redirections.views_redirections import RedirectionsAPI
from pages.postlogin.modules.appspecificmodules.postloginhome.views_postloginhome import PostLoginHomeAPI
from pages.postlogin.modules.commonmodules.profile.views_profile import PostLoginProfileAPI
from pages.postlogin.modules.commonmodules.logout.views_logout import PostLoginLogoutAPI
from pages.postlogin.modules.commonmodules.api.logout_confirm.views_logout_confirm import PostLoginLogoutConfirmAPI

urlpatterns = [
    url(r'^$', PostLoginHomeAPI.as_view()),
    url(r'^home/', PostLoginHomeAPI.as_view(), name='home'),
    url(r'^redirect/', RedirectionsAPI.as_view(), name='user/redirect'),
    url(r'^profile/', PostLoginProfileAPI.as_view(), name='profile'),
    url(r'^logout/', PostLoginLogoutAPI.as_view(), name='logout'),
    url(r'^logout_confirm/', PostLoginLogoutConfirmAPI.as_view(), name='user/logout_confirm'),
]