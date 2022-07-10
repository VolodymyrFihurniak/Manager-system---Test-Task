from django.db import models
from django.urls import reverse
# Create your models here.


class Location(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Locations"


class Worker(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    date = models.ManyToManyField('Schedule', blank=True)
    price = models.CharField(max_length=100)
    address = models.ForeignKey(
        'Location', on_delete=models.CASCADE, related_name='address', null=True)
    description = models.CharField(max_length=100)
    image = models.ImageField(
        upload_to='images/%Y/%m/%d', blank=True, null=True)
    rating = models.CharField(max_length=100)
    reviews = models.CharField(max_length=100)
    category = models.ForeignKey('Category', on_delete=models.CASCADE,
                                 related_name='category', null=True)

    def __str__(self):
        return self.name + " " + self.surname

    def get_absolute_url(self):
        return reverse('active_record_view', kwargs={'worker_id': self.pk})

    class Meta:
        db_table = "Worker"
        verbose_name = "Wpecialist"
        verbose_name_plural = "Worker"
        ordering = ['id']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category", kwargs={"category_id": self.pk})

    class Meta:
        db_table = "category"
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Schedule(models.Model):
    period = models.ForeignKey(
        'Period', on_delete=models.CASCADE, related_name='period', null=True)

    def __str__(self):
        return self.period.start_period.strftime("%Y-%m-%d") + \
            " - " + self.period.end_period.strftime("%Y-%m-%d")


    class Meta:
        db_table = "schedule"
        verbose_name = "Schedule"
        verbose_name_plural = "Schedules"


class Period(models.Model):
    start_period = models.DateField(auto_now=False, auto_now_add=False)
    end_period = models.DateField(auto_now=False, auto_now_add=False)
    worker_time = models.ManyToManyField(
        'WorkerTime', related_name='worker_time', blank=True)

    class Meta:
        db_table = "period"
        verbose_name = "Period"
        verbose_name_plural = "Periods"
        ordering = ['id']

    def __str__(self):
        return self.start_period.strftime("%Y-%m-%d") + " - " + self.end_period.strftime("%Y-%m-%d")


class WorkerTime(models.Model):
    day_str = models.CharField(max_length=100, null=True, blank=True)
    day_num = models.DateField(
        auto_now=False, auto_now_add=False, null=True, blank=True)
    start_time = models.TimeField(auto_now=False, auto_now_add=False)
    end_time = models.TimeField(auto_now=False, auto_now_add=False)
    additional_hours_start_time = models.TimeField(
        auto_now=False, auto_now_add=False, null=True, blank=True)
    additional_hours_end_time = models.TimeField(
        auto_now=False, auto_now_add=False, null=True, blank=True)

    class Meta:
        db_table = "worker_time"
        verbose_name = "WorkerTime"
        verbose_name_plural = "WorkerTimes"

    def __str__(self):
        return self.day_str + " - " + self.start_time.strftime("%H:%M") + \
            " - " + self.end_time.strftime("%H:%M") if self.day_str else \
            self.start_time.strftime("%H:%M") + " - " + \
            self.end_time.strftime("%H:%M")


class Appointment(models.Model):
    worker = models.ForeignKey('Worker', on_delete=models.CASCADE,
                               related_name='appointment', null=True)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE,
                                 related_name='appointment', null=True)
    date = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.worker.name + " " + self.worker.surname

    def get_edit_url(self):
        return reverse("active_record_edit", kwargs={"appointment_id": self.pk})

    def get_delete_url(self):
        return reverse("active_record_delete", kwargs={"appointment_id": self.pk})

    class Meta:
        db_table = "appointment"
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"
        ordering = ['id']


class Customer(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + " " + self.surname

    class Meta:
        db_table = "customer"
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
