from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from consumers import views

urlpatterns = format_suffix_patterns([
    url(r'^consumer/$', views.ConsumerDetail.as_view()),
    url(r'^consumer/email/$', views.ConsumerEmail.as_view()),
    url(r'^consumer/email/validate/$', views.ConsumerEmailValidate.as_view()),
    url(r'^consumer/phone/$', views.ConsumerPhone.as_view()),
    url(r'^consumer/phone/validate/$', views.ConsumerPhoneValidate.as_view()),
    url(r'^consumer/notify/$', views.ConsumerNotify.as_view()),
])
