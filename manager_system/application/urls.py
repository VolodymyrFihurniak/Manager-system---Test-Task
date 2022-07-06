from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('category/<int:category_id>',
         views.CategoryView.as_view(), name='category'),
    path('date/<int:hours_id>', views.DateView.as_view(), name='date'),
    path('record/', views.record, name='record'),
    path('active_record/', views.ActiveRecordView.as_view(), name='active_record'),
    path('active_record/worker/<int:worker_id>',
         views.ActiveRecordWorkerView.as_view(), name='active_record_view'),
    path('active_record/edit_appointment/<int:appointment_id>',
         views.ActiveRecordWorkerEdit.as_view(), name='active_record_edit'),
    path('active_record/delete_appointment/<int:appointment_id>',
         views.ActiveRecordWorkerDelete.as_view(), name='active_record_delete'),
]
