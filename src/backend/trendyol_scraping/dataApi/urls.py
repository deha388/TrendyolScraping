from django.conf.urls import url
from dataApi import views

urlpatterns = [
    url(r'^data$',views.add_data),
]