from django.contrib import admin

from django.contrib import admin

from .models import Employee, SalaryHistory
admin.site.register(Employee)
admin.site.register(SalaryHistory)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'position', 'email', 'base_salary', 'bonus', 'deduction', 'get_calculated_salary')

    def get_calculated_salary(self, obj):
        return obj.calculate_salary()  
    get_calculated_salary.short_description = 'Calculated Salary'  

admin.site.register(Employee, EmployeeAdmin)



