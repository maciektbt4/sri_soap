from django.urls import re_path, path
from django.contrib import admin
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoView
from .views import hello_world_service, app, HelloWorldService, PersonService


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^hello_world/', hello_world_service),
    re_path(r'^say_hello/', DjangoView.as_view(
        services=[HelloWorldService], tns='spyne.examples.django',
        in_protocol=Soap11(validator='lxml'), out_protocol=Soap11())),
    re_path(r'^get_person/', DjangoView.as_view(
        services=[PersonService], tns='spyne.examples.django',
        in_protocol=Soap11(validator='lxml'), out_protocol=Soap11())),
    re_path(r'^get_all_persons/', DjangoView.as_view(
        services=[PersonService], tns='spyne.examples.django',
        in_protocol=Soap11(validator='lxml'), out_protocol=Soap11())),
    re_path(r'^create_person/', DjangoView.as_view(
        services=[PersonService], tns='spyne.examples.django',
        in_protocol=Soap11(validator='lxml'), out_protocol=Soap11())),
    re_path(r'^delete_person/', DjangoView.as_view(
        services=[PersonService], tns='spyne.examples.django',
        in_protocol=Soap11(validator='lxml'), out_protocol=Soap11())),
    re_path(r'^update_person/', DjangoView.as_view(
        services=[PersonService], tns='spyne.examples.django',
        in_protocol=Soap11(validator='lxml'), out_protocol=Soap11())),
    re_path(r'^api/', DjangoView.as_view(application=app)),
]