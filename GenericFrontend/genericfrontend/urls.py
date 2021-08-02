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


# ------------------------------------------ REVISED APIs ---------------------------------
from pages.prelogin.modules.commonmodules.preloginhome.views_preloginhome import PreLoginHomeAPI
from pages.postlogin.modules.appspecificmodules.postloginhome.views_postloginhome import PostLoginHomeAPI
from pages.postlogin.modules.commonmodules.profile.views_profile import PostLoginProfileAPI

# -----------------------------------------Testing Sentry---------------------------------------#
def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [

    # ------------------------- core module ----------------------------
    path('admin/', admin.site.urls),
    url(r'^debug', trigger_error),

    # ------------------------- sentry integration module ----------------------------
    path('sentry-debug/', trigger_error),

    # ------------------------- frontend urls redirection ----------------------------
    url(r'^user/', include('pages.postlogin.urls')),
    url(r'^prelogin/', include('pages.prelogin.urls')),
    url(r'^[a-zA-Z0-9_]*\/$', RedirectView.as_view(url='/prelogin/')),
    url(r'^$', RedirectView.as_view(url='/prelogin/')),

]


