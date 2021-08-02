from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.generic import RedirectView

from pages.prelogin.modules.commonmodules.preloginhome.views_preloginhome import PreLoginHomeAPI
from pages.postlogin.modules.appspecificmodules.postloginhome.views_postloginhome import PostLoginHomeAPI
from pages.postlogin.modules.commonmodules.profile.views_profile import PostLoginProfileAPI


urlpatterns = [
    url(r'^$', PostLoginHomeAPI.as_view()),
    url(r'^home/', PostLoginHomeAPI.as_view()),
    url(r'^profile/', PostLoginProfileAPI.as_view()),
]