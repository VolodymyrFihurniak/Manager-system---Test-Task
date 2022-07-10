from functools import partial
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Category, Worker, Appointment, \
    Location, Customer, Schedule, Period, WorkerTime
from .serializers import WorkerSerializer, CategorySerializer, \
    AppointmentSerializer, LocationSerializer, CustomerSerializer, \
    ScheduleSerializer, PeriodSerializer, WorkerTimeSerializer
from .forms import RecordForm, EditActiveForm


# Create your views here.

class HomeView(ListView):
    model = Worker
    template_name = 'application/main_list.html'
    context_object_name = 'workers'
    paginate_by = 10
    ordering = ['id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home page'
        context['categories'] = Category.objects.all()
        context['form'] = RecordForm()
        return context


class CategoryView(ListView):
    model = Worker
    template_name = 'application/main_list.html'
    context_object_name = 'workers'
    paginate_by = 10
    ordering = ['id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Category - {Category.objects.get(id=self.kwargs["category_id"]).name}'
        context['categories'] = Category.objects.all()
        context['form'] = RecordForm()
        return context

    def get_queryset(self):
        return Worker.objects.filter(category_id=self.kwargs['category_id'])


class DateView(ListView):
    model = Worker
    template_name = 'application/main_list.html'
    context_object_name = 'workers'
    paginate_by = 10
    ordering = ['id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Date'
        context['categories'] = Category.objects.all()
        context['form'] = RecordForm()
        return context

    def post(self, request, *args, **kwargs):
        return redirect(f'/date/{request.POST.get("date")}')

    def get_queryset(self):
        return Worker.objects.filter(Q(date__period__start_period=self.kwargs['date_str']) |
                                     Q(date__period__end_period=self.kwargs['date_str']))


class ActiveRecordView(ListView):
    model = Appointment
    template_name = 'application/active_record.html'
    context_object_name = 'appointments'
    paginate_by = 10
    ordering = ['id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Active record'
        context['workers'] = Worker.objects.all()
        return context


class ActiveRecordWorkerView(ListView):
    model = Appointment
    template_name = 'application/active_record.html'
    context_object_name = 'appointments'
    paginate_by = 10
    ordering = ['id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Active record'
        context['workers'] = Worker.objects.all()
        return context

    def get_queryset(self):
        return Appointment.objects.filter(worker_id=self.kwargs['worker_id'])


class ActiveRecordWorkerEdit(ListView):
    model = Appointment
    template_name = 'application/edit_appointment.html'
    context_object_name = 'appointments'
    paginate_by = 10
    ordering = ['id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Active record'
        print(self.kwargs['appointment_id'])
        context['form'] = EditActiveForm({'worker': Appointment.objects.get(id=self.kwargs['appointment_id']).worker,
                                          'customer': Appointment.objects.get(id=self.kwargs['appointment_id']).customer,
                                          'date': Appointment.objects.get(id=self.kwargs['appointment_id']).date,
                                          'time': Appointment.objects.get(id=self.kwargs['appointment_id']).time,
                                          'status': Appointment.objects.get(id=self.kwargs['appointment_id']).status})
        return context

    def get_queryset(self):
        return Appointment.objects.filter(id=self.kwargs['appointment_id'])

    def post(self, request, *args, **kwargs):
        form = EditActiveForm(request.POST)
        if form.is_valid():
            appointment = Appointment.objects.get(
                id=self.kwargs['appointment_id'])
            appointment.date = form.cleaned_data['date']
            appointment.time = form.cleaned_data['time']
            appointment.status = form.cleaned_data['status']
            appointment.save()
            return redirect('active_record')
        return render(request, self.template_name, {'form': form})


class ActiveRecordWorkerDelete(ListView):
    model = Appointment
    template_name = 'application/active_record.html'
    context_object_name = 'appointments'
    paginate_by = 10
    ordering = ['id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Active record'
        return context

    def get_queryset(self):
        return Appointment.objects.filter(id=self.kwargs['appointment_id'])

    def post(self, request, *args, **kwargs):
        appointment = Appointment.objects.get(id=self.kwargs['appointment_id'])
        appointment.delete()
        return redirect('active_record')


def record(request):
    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid():
            worker = Worker.objects.get(id=request.POST.get('worker'))
            if not Schedule.objects.filter(Q(period__start_period=form.cleaned_data['date']) |
                                           Q(period__end_period=form.cleaned_data['date'])):
                return render(request, 'application/record_form.html', {'form': form,
                                                                        'worker': worker,
                                                                        'error': 'This day is busy'})

            if not Schedule.objects.filter(Q(period__worker_time__start_time=form.cleaned_data['time']) |
                                           Q(period__worker_time__end_time=form.cleaned_data['time']) |
                                           Q(period__worker_time__additional_hours_start_time=form.cleaned_data['time']) |
                                           Q(period__worker_time__additional_hours_end_time=form.cleaned_data['time'])):
                return render(request, 'application/record_form.html', {'form': form,
                                                                        'worker': worker,
                                                                        'error': 'This time is busy'})

            if Appointment.objects.filter(Q(date=form.cleaned_data['date']) |
                                          Q(time=form.cleaned_data['time'])):
                return render(request, 'application/record_form.html', {'form': form,
                                                                        'worker': worker,
                                                                        'error': 'This data or time is busy'})

            customer = Customer(
                name=form.cleaned_data['name'], surname=form.cleaned_data['surname'],
                phone=form.cleaned_data['phone'], email=form.cleaned_data['email'],
                address=form.cleaned_data['address'], city=form.cleaned_data['city'],
                state=form.cleaned_data['state'], zipcode=form.cleaned_data['zipcode'])
            customer.save()
            appointment = Appointment(
                worker=worker, customer=customer, date=form.cleaned_data['date'], time=form.cleaned_data['time'], status=True)
            appointment.save()
            return redirect('active_record')
        else:
            worker = Worker.objects.get(id=request.POST.get('worker'))
            worker = {'id': worker.id, 'name': worker.name,
                      'surname': worker.surname, 'category': worker.category.name}
    else:
        form = RecordForm()

    return render(request, 'application/record_form.html', {'title': 'Record',
                                                            'worker': worker,
                                                            'form': form})


class ApiView(APIView):
    def get(self, request):
        return Response({'status': 'ok'})


class ApiWorkersView(APIView):
    def get(self, request):
        workers = Worker.objects.all()
        serializer = WorkerSerializer(workers, many=True)
        return Response(serializer.data)


class ApiWorkersCategoryView(APIView):
    def get(self, request, category_id):
        workers = Worker.objects.filter(category_id=category_id)
        serializer = WorkerSerializer(workers, many=True)
        return Response(serializer.data)


class ApiWorkerView(APIView):
    def get(self, request, pk):
        worker = Worker.objects.get(id=pk)
        serializer = WorkerSerializer(worker)
        return Response(serializer.data)

    def post(self, request, pk):
        worker = Worker.objects.get(id=pk)
        serializer = WorkerSerializer(worker, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        worker = Worker.objects.get(id=pk)
        serializer = WorkerSerializer(worker, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        worker = Worker.objects.get(id=pk)
        serializer = WorkerSerializer(worker, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        worker = Worker.objects.get(id=pk)
        worker.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ApiWorkerCreateView(APIView):
    def post(self, request):
        serializer = WorkerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiCategorysView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class ApiCategoryView(APIView):
    def get(self, request, pk):
        category = Category.objects.get(id=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def post(self, request, pk):
        category = Category.objects.get(id=pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        category = Category.objects.get(id=pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        category = Category.objects.get(id=pk)
        serializer = CategorySerializer(
            category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = Category.objects.get(id=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ApiCategoryCreateView(APIView):
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiAppointmentsView(APIView):
    def get(self, request):
        appointments = Appointment.objects.all()
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiAppointmentView(APIView):
    def get(self, request, pk):
        appointment = Appointment.objects.get(id=pk)
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)

    def post(self, request, pk):
        appointment = Appointment.objects.get(id=pk)
        serializer = AppointmentSerializer(appointment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        appointment = Appointment.objects.get(id=pk)
        serializer = AppointmentSerializer(appointment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        appointment = Appointment.objects.get(id=pk)
        serializer = AppointmentSerializer(
            appointment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        appointment = Appointment.objects.get(id=pk)
        appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ApiAppointmentCreateView(APIView):
    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiLocationsView(APIView):
    def get(self, request):
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiLocationView(APIView):
    def get(self, request, pk):
        location = Location.objects.get(id=pk)
        serializer = LocationSerializer(location)
        return Response(serializer.data)

    def post(self, request, pk):
        location = Location.objects.get(id=pk)
        serializer = LocationSerializer(location, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        location = Location.objects.get(id=pk)
        serializer = LocationSerializer(location, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        location = Location.objects.get(id=pk)
        serializer = LocationSerializer(
            location, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        location = Location.objects.get(id=pk)
        location.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ApiLocationCreateView(APIView):
    def post(self, request):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiSchedulesView(APIView):
    def get(self, request):
        schedules = Schedule.objects.all()
        serializer = ScheduleSerializer(schedules, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ScheduleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiSchedulePeriodView(APIView):
    def get(self, request, pk):
        period = Period.objects.get(id=pk)
        serializer = PeriodSerializer(period)
        return Response(serializer.data)

    def post(self, request, pk):
        period = Period.objects.get(id=pk)
        serializer = PeriodSerializer(period, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        period = Period.objects.get(id=pk)
        serializer = PeriodSerializer(period, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        period = Period.objects.get(id=pk)
        serializer = PeriodSerializer(
            period, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        period = Period.objects.get(id=pk)
        period.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ApiSchedulePeriodWorkerTimeView(APIView):
    def get(self, request, pk, worker_pk):
        period = Period.objects.get(id=pk)
        worker_time = period.worker_time.get(id=worker_pk)
        serializer = WorkerTimeSerializer(worker_time)
        return Response(serializer.data)

    def post(self, request, pk, worker_pk):
        period = Period.objects.get(id=pk)
        worker_time = period.worker_time.get(id=worker_pk)
        serializer = WorkerTimeSerializer(worker_time, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, worker_pk):
        period = Period.objects.get(id=pk)
        worker_time = period.worker_time.get(id=worker_pk)
        serializer = WorkerTimeSerializer(worker_time, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, worker_pk):
        period = Period.objects.get(id=pk)
        worker_time = period.worker_time.get(id=worker_pk)
        serializer = WorkerTimeSerializer(
            worker_time, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, worker_pk):
        period = Period.objects.get(id=pk)
        worker_time = period.worker_time.get(id=worker_pk)
        worker_time.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ApiSchedulesDateView(APIView):
    def get(self, request, date):
        schedule = Schedule.objects.filter(Q(period__start_period=date) |
                                           Q(period__end_period=date))
        serializer = ScheduleSerializer(schedule, many=True)
        return Response(serializer.data)


class ApiCustomersView(APIView):
    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiCustomerView(APIView):
    def get(self, request, pk):
        customer = Customer.objects.get(id=pk)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def post(self, request, pk):
        customer = Customer.objects.get(id=pk)
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        customer = Customer.objects.get(id=pk)
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        customer = Customer.objects.get(id=pk)
        serializer = CustomerSerializer(
            customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        customer = Customer.objects.get(id=pk)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ApiCustomerCreateView(APIView):
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
