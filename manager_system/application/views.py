from django.shortcuts import redirect, render
from django.views.generic import ListView
from .models import Category, Worker, Appointment, Customer, Schedule
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
        context['hours'] = Schedule.objects.all()
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
        context['hours'] = Schedule.objects.all()
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
        context['hours'] = Schedule.objects.all()
        context['form'] = RecordForm()
        return context

    def get_queryset(self):
        return Worker.objects.filter(hours_id=self.kwargs['hours_id'])


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
            if not Schedule.objects.filter(day=form.cleaned_data['date']):
                return render(request, 'application/record_form.html', {'form': form,
                                                                        'worker': worker,
                                                                        'error': 'This day is busy'})

            if not Schedule.objects.filter(start_time__lte=form.cleaned_data['time'],
                                           end_time__gte=form.cleaned_data['time']):
                return render(request, 'application/record_form.html', {'form': form,
                                                                        'worker': worker,
                                                                        'error': 'This time is busy'})


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
