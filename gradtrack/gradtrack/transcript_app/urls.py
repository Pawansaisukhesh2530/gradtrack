from django.urls import path
from . import views
from .views import home, transcript_view, transcript_pdf, all_events_view

urlpatterns = [
    path('', views.home, name='home'),
    path('transcript/', views.transcript_view, name='transcript'),
    path('transcript/pdf/<str:roll_no>/', views.transcript_pdf, name='transcript_pdf'),
    path('all-events/<str:roll_no>/', views.all_events_view, name='all_events'),
]