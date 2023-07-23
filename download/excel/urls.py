
from django.urls import path
from . import views 

urlpatterns = [
    path('', views.DownloadView.as_view(),name='home'),
]
