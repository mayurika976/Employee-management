from django.shortcuts import render
from django.shortcuts import render, get_list_or_404, redirect
from django.db import models
from django import forms
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Employee, SalaryHistory

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'  

class SalaryHistoryForm(forms.ModelForm):
    class Meta:
        model = SalaryHistory
        fields = '__all__'  

    class EmployeeListView(ListView):
        model = Employee
        template_name = 'employees/employee_list.html'

class EmployeeCreateView(CreateView):
    model = Employee
    fields = ['name', 'department', 'base_salary']
    template_name = 'employees/employee_form.html'
    success_url = reverse_lazy('employee_list')

class EmployeeUpdateView(UpdateView):
    model = Employee
    fields = ['name', 'department', 'base_salary']
    template_name = 'employees/employee_form.html'
    success_url = reverse_lazy('employee_list')

class EmployeeDeleteView(DeleteView):
    model = Employee
    template_name = 'employees/employee_confirm_delete.html'
    success_url = reverse_lazy('employee_list')

# Employee 
def create_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()  
    return render(request, 'create_employee.html', {'form': form})

#Salary History
def create_salary_history(request, employee_id):
    employee = get_list_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        form = SalaryHistoryForm(request.POST)
        if form.is_valid():
            salary_history = form.save(commit=False)
            salary_history.employee = employee  
            salary_history.save()
            return redirect('employee_list')
    else:
        form = SalaryHistoryForm()  
    return render(request, 'create_salary_history.html', {'form': form, 'employee': employee})

#List Employees
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employee_list.html', {'employees': employees})

#List Salary History
def salary_history_list(request, employee_id):
    employee = get_list_or_404(Employee, id=employee_id)
    salary_history = SalaryHistory.objects.filter(employee=employee)
    return render(request, 'salary_history_list.html', {'salary_history': salary_history, 'employee': employee})

from django.db import models

class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    hire_date = models.DateField()
    job_title = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    department = models.CharField(max_length=100)
         
def __str__(self):
    return f"{self.first_name} {self.last_name} - {self.job_title}"
    
class SalaryHistory(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='salary_history')
    date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    @property
    def net_salary(self):
        return self.salary + self.bonus - self.deductions
    
    def __str__(self):
        return f"{self.employee} - {self.date} - {self.net_salary}"

