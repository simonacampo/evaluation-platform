from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
    url(r"^admin/", include(admin.site.urls)),

    url(r'^evaluation/', include("evaluation.urls", namespace="evaluation")),
    url(r"^", include("home.urls", namespace="home")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
