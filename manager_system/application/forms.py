from django import forms


class RecordForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Enter your name',
               'required': 'required'}))

    surname = forms.CharField(label='Surname', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Enter your surname',
               'required': 'required',
               'data-error': 'Surname is required',
               'data-minlength': '2',
               'data-maxlength': '100',
               'data-error': 'Surname must be between 2 and 100 characters',
               'data-minlength-error': 'Surname must be between 2 and 100 characters'}))

    phone = forms.CharField(label='Phone', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Phone',
               'required': 'required',
               'data-error': 'Phone is required',
               'pattern': '[0-9]{10}',
               'data-pattern-error': 'Phone must be 10 digits',
               'data-error-msg': 'Phone is required'}))

    email = forms.EmailField(label='Email', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Email',
               'required': 'required',
               'data-error': 'Email is required',
               'data-error-msg': 'Email is required'}))

    address = forms.CharField(label='Address', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Address',
               'required': 'required',
               'data-error': 'Address is required',
               'data-error-msg': 'Address is required'}))

    city = forms.CharField(label='City', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'City',
               'required': 'required',
               'data-error': 'City is required',
               'data-error-msg': 'City is required'}))

    state = forms.CharField(label='State', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'State',
               'required': 'required',
               'data-error': 'State is required',
               'data-error-msg': 'State is required'}))

    zipcode = forms.CharField(label='Zipcode', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Zipcode',
               'required': 'required',
               'data-error': 'Zipcode is required',
               'data-error-msg': 'Zipcode is required'}))

    date = forms.DateField(label='Date', widget=forms.DateInput(
        attrs={'class': 'form-control',
               'type': 'date',
               'placeholder': 'Date',
               'required': 'required',
               'data-error': 'Date is required',
               'data-error-msg': 'Date is required'}))

    time = forms.TimeField(label='Time', widget=forms.TimeInput(
        attrs={'class': 'form-control',
               'type': 'time',
               'placeholder': 'Time',
               'required': 'required',
               'data-error': 'Time is required',
               'data-error-msg': 'Time is required'}))


class EditActiveForm(forms.Form):
    worker = forms.CharField(label='Worker', widget=forms.TextInput(
        attrs={'class': 'form-control',
               'required': 'required',
               'data-error': 'Worker is required',
               'data-error-msg': 'Worker is required',
               'readonly': 'readonly'}))

    customer = forms.CharField(label='Customer', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Customer',
               'required': 'required',
               'data-error': 'Customer is required',
               'data-error-msg': 'Customer is required',
               'readonly': 'readonly'}))

    date = forms.DateField(label='Date', widget=forms.DateInput(
        attrs={'class': 'form-control',
               'type': 'date',
               'placeholder': 'Date',
               'required': 'required',
               'data-error': 'Date is required',
               'data-error-msg': 'Date is required'}))

    time = forms.TimeField(label='Time', widget=forms.TimeInput(
        attrs={'class': 'form-control',
               'type': 'time',
               'placeholder': 'Time',
               'required': 'required',
               'data-error': 'Time is required',
               'data-error-msg': 'Time is required'}))

    status = forms.BooleanField(label='Status', required=False, widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input',
               'placeholder': 'Status',
               'type': 'checkbox'}))
