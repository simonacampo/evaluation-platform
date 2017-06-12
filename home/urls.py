from django.conf import settings
from django.conf.urls import include, url

from home.views import HomePageView

urlpatterns = [

    url(r"^$", HomePageView.as_view(), name="home"),
]