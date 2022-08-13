from django.urls import path

from .views import ProcessHookView


urlpatterns = [
    path("", ProcessHookView.as_view(), name="hook"),
]
