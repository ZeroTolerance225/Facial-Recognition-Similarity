from django import forms
from .models import MaintenanceRequest, Tenant

class MaintenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        exclude = ['tenant', 'request_date', 'status']  # Exclude tenant, request_date, and status
        # Add any other configurations as needed


class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['name', 'apartment_number', 'phone', 'email', 'check_in_date', 'check_out_date']
        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'type': 'date'}),
        }
