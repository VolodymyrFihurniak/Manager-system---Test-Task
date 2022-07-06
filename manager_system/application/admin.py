from django.contrib import admin

# Register your models here.
from .models import Worker, Category, Location, Appointment, Customer, Schedule

class WorkerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'phone', 'email', 'hours', 'address', 'description', 'image', 'rating', 'reviews', 'category')
    list_display_links = ('id', 'name')
    list_filter = ('category', 'address', 'hours', 'phone')
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

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'worker', 'customer', 'date', 'time', 'status')
    list_display_links = ('id', 'worker')
    list_filter = ('worker', 'customer', 'date', 'time', 'status')
    search_fields = ('worker', 'customer', 'date', 'time', 'status')
    list_per_page = 25
    ordering = ['id']

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'phone', 'email', 'address', 'city', 'state', 'zipcode', 'created_at', 'updated_at')
    list_display_links = ('id', 'name')
    list_filter = ('name', 'surname', 'phone', 'email', 'address', 'created_at')
    search_fields = ('name', 'surname', 'phone', 'email', 'address', 'created_at')
    list_per_page = 25
    ordering = ['id']

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'day', 'start_time', 'end_time')
    list_display_links = ('id', 'day')
    list_filter = ('day', 'start_time', 'end_time')
    search_fields = ('day', 'start_time', 'end_time')
    list_per_page = 25
    ordering = ['id']

admin.site.register(Worker, WorkerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Schedule, ScheduleAdmin)


