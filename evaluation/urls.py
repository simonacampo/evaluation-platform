from django.conf import settings
from django.conf.urls import include, url

from evaluation import views

from uuid import uuid4

urlpatterns = [

    url(r"^(?P<platform_id>[0-9a-f-]+)/$", views.evaluation_wizard_view_wrapper, name="evaluation"),
    url(r"^(?P<platform_id>[0-9a-f-]+)/thanks/(?P<evaluation_code>[0-9a-zA-Z]+)/(?P<evaluation_id>[0-9]+)/$", views.evaluation_finished, name="finished")
]