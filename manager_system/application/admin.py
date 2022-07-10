from django.contrib import admin

# Register your models here.
from .models import Worker, Category, Location, Appointment, Customer, Schedule, Period, WorkerTime


class WorkerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'phone', 'email', 'price',
                    'address', 'description', 'image', 'rating', 'reviews', 'category')
    list_display_links = ('id', 'name')
    list_filter = ('category', 'address', 'phone')
    filter_horizontal = ('date',)
    search_fields = ('name',)
    list_per_page = 25
    ordering = ['id']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    list_filter = ('name',)
    search_fields = ('name',)
    list_per_page = 25
    ordering = ['id']


class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    list_filter = ('name',)
    search_fields = ('name',)
    list_per_page = 25
    ordering = ['id']

class PeriodAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_period', 'end_period')
    list_display_links = ('id', 'start_period', 'end_period')
    list_filter = ('start_period',)
    filter_horizontal = ('worker_time',)
    search_fields = ('start_period',)
    list_per_page = 25
    ordering = ['id']


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'worker', 'customer', 'date', 'time', 'status')
    list_display_links = ('id', 'worker')
    list_filter = ('worker', 'customer', 'date', 'time', 'status')
    search_fields = ('worker', 'customer', 'date', 'time', 'status')
    list_per_page = 25
    ordering = ['id']


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'phone', 'email', 'address',
                    'city', 'state', 'zipcode', 'created_at', 'updated_at')
    list_display_links = ('id', 'name')
    list_filter = ('name', 'surname', 'phone',
                   'email', 'address', 'created_at')
    search_fields = ('name', 'surname', 'phone',
                     'email', 'address', 'created_at')
    list_per_page = 25
    ordering = ['id']


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'period')
    list_display_links = ('id', 'period')
    list_per_page = 25
    ordering = ['id']


class WorkerTimeAdmin(admin.ModelAdmin):
    list_display = ('id', 'day_str', 'day_num', 'start_time', 'end_time', 'additional_hours_start_time', 'additional_hours_end_time')
    list_display_links = ('id', 'day_str', 'day_num', 'start_time', 'end_time', 'additional_hours_start_time', 'additional_hours_end_time')
    list_per_page = 25
    ordering = ['id']


admin.site.register(Worker, WorkerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Period, PeriodAdmin)
admin.site.register(WorkerTime, WorkerTimeAdmin)
