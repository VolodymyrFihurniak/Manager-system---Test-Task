from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('api/', views.ApiView.as_view(), name='api'),
    path('api/workers/', views.ApiWorkersView.as_view(), name='api_view_workers'),
    path('api/workers/filter/category/<int:category_id>',
         views.ApiWorkersCategoryView.as_view(), name='api_view_filter_category_workers'),
    path('api/worker/<int:pk>/', views.ApiWorkerView.as_view(),
         name='api_view_worker'),
    path('api/worker/create/', views.ApiWorkerCreateView.as_view(),
         name='api_create_worker'),
    path('api/categorys/', views.ApiCategorysView.as_view(),
         name='api_view_categorys'),
    path('api/category/<int:pk>/', views.ApiCategoryView.as_view(),
         name='api_view_category'),
    path('api/category/create/', views.ApiCategoryCreateView.as_view(),
         name='api_create_category'),
    path('api/appointments/', views.ApiAppointmentsView.as_view(),
         name='api_view_appointments'),
    path('api/appointment/<int:pk>/', views.ApiAppointmentView.as_view(),
         name='api_view_appointment'),
    path('api/appointment/create/', views.ApiAppointmentCreateView.as_view(),
         name='api_create_appointment'),
    path('api/locations/', views.ApiLocationsView.as_view(),
         name='api_view_locations'),
    path('api/location/<int:pk>/', views.ApiLocationView.as_view(),
         name='api_view_location'),
    path('api/location/create/', views.ApiLocationCreateView.as_view(),
         name='api_create_location'),
    path('api/schedules/', views.ApiSchedulesView.as_view(),
         name='api_view_schedules'),
    path('api/schedule/period/<int:pk>/',
         views.ApiSchedulePeriodView.as_view(), name='api_view_schedule_period'),
    path('api/schedule/period/<int:pk>/worker_time/<int:worker_pk>',
         views.ApiSchedulePeriodWorkerTimeView.as_view(),
         name='api_view_schedule_period_worker_time'),
     path('api/schedule/filter/date/<str:date>',
            views.ApiSchedulesDateView.as_view(), name='api_view_filter_date_workers'),
    path('api/customers/', views.ApiCustomersView.as_view(),
         name='api_view_customers'),

    path('api/customer/<int:pk>/', views.ApiCustomerView.as_view(),
            name='api_view_customer'),
    path('api/customer/create/', views.ApiCustomerCreateView.as_view(),
            name='api_create_customer'),

    path('category/<int:category_id>',
         views.CategoryView.as_view(), name='category'),
    path('date/', views.DateView.as_view(), name='date'),
    path('date/<str:date_str>', views.DateView.as_view(), name='date_view'),
    path('record/', views.record, name='record'),
    path('active_record/', views.ActiveRecordView.as_view(), name='active_record'),
    path('active_record/worker/<int:worker_id>',
         views.ActiveRecordWorkerView.as_view(), name='active_record_view'),
    path('active_record/edit_appointment/<int:appointment_id>',
         views.ActiveRecordWorkerEdit.as_view(), name='active_record_edit'),
    path('active_record/delete_appointment/<int:appointment_id>',
         views.ActiveRecordWorkerDelete.as_view(), name='active_record_delete'),
]
