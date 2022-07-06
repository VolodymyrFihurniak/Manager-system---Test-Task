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
    hours = models.ForeignKey(
        'Schedule', on_delete=models.CASCADE, related_name='hours', null=True)
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
    day = models.DateField(max_length=100)
    start_time = models.TimeField(max_length=100)
    end_time = models.TimeField(max_length=100)

    def __str__(self):
        return self.day.strftime("%Y-%m-%d") + ", " + self.start_time.strftime("%H:%M") + " - " + self.end_time.strftime("%H:%M")

    def get_absolute_url(self):
        return reverse("date", kwargs={"hours_id": self.pk})

    class Meta:
        db_table = "schedule"
        verbose_name = "Schedule"
        verbose_name_plural = "Schedules"


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
