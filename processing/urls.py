from django.urls import path
from .views import DataProcessingView, SafeguardReportListView, SafeguardReportUpdateView

urlpatterns = [
    path('data-processing/', DataProcessingView.as_view(), name='data-processing'),
    path('safeguard-reports/', SafeguardReportListView.as_view(), name='safeguard-reports'),
    path('safeguard-reports/<int:pk>/', SafeguardReportUpdateView.as_view(), name='safeguard-report-update'),
]

