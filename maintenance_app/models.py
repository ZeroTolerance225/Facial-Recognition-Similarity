from django.db import models

class Tenant(models.Model):
    name = models.CharField(max_length=100)
    apartment_number = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    check_in_date = models.DateField()
    check_out_date = models.DateField(null=True, blank=True)

class MaintenanceRequest(models.Model):
    request_id = models.AutoField(primary_key=True)  # Auto-generating unique request ID
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    problem_area = models.CharField(max_length=100)
    description = models.TextField()
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='pending')  # Default status set to 'pending'
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)  # Requires Pillow library

class StaffMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
